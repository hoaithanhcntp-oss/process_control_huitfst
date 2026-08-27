import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import signal
import pandas as pd
from utils.control_utils import compute_routh_table, poly_to_latex

def render():
    st.header("3. Khảo Sát Tính Ổn Định & Đặc Tính Miền Tần Số")
    
    # Khung giải thích nguyên lý & sơ đồ
    with st.expander("📖 **Nguyên Lý Tính Ổn Định & Biểu Đồ Tần Số (Bode / Nyquist)**", expanded=False):
        st.markdown(r"""
        * **Tiêu chuẩn Ổn định Routh-Hurwitz:** Phương trình đặc trưng $D(s) = a_n s^n + a_{n-1} s^{n-1} + \dots + a_0 = 0$. Hệ thống ổn định khi và chỉ khi tất cả các hệ số ở cột 1 của bảng Routh đều cùng dấu dương. Số lần đổi dấu ở cột 1 bằng đúng số nghiệm nằm ở nửa phải mặt phẳng phức $\text{Re}(s) > 0$.
        * **Mặt phẳng Cực - Zero (Pole-Zero Map):** Tất cả các cực (Poles) phải nằm hoàn toàn bên trái trục ảo ($\text{Re}(s) < 0$) thì hệ thống mới ổn định tiệm cận.
        * **Biểu đồ Bode:** Thể hiện độ lợi $|G(j\omega)|$ theo thang dB ($20\log_{10}|G|$) và góc pha $\angle G(j\omega)$ theo độ (deg).
        * **Độ dự trữ biên độ ($GM$) & Độ dự trữ pha ($PM$):**
          * Tần số cắt pha $\omega_{pc}$: $\angle G(j\omega_{pc}) = -180^\circ \implies GM = -20\log_{10}|G(j\omega_{pc})|\text{ (dB)}$.
          * Tần số cắt biên $\omega_{gc}$: $|G(j\omega_{gc})| = 1\text{ (0 dB)} \implies PM = 180^\circ + \angle G(j\omega_{gc})\text{ (deg)}$.
        """)

    st.subheader("Nhập Thông Số Hàm Truyền")
    
    col_input1, col_input2 = st.columns([1, 1])
    
    with col_input1:
        raw_num = st.text_input("1. Nhập hệ số TỬ SỐ N(s) (cách nhau bởi dấu phẩy):", "2")
        raw_den = st.text_input("2. Nhập hệ số MẪU SỐ D(s) (cách nhau bởi dấu phẩy):", "1, 3, 3, 2")
    
    try:
        num_poly = [float(x.strip()) for x in raw_num.split(",") if x.strip()]
        den_poly = [float(x.strip()) for x in raw_den.split(",") if x.strip()]
        
        # Tạo công thức LaTeX tương ứng
        latex_num = poly_to_latex(num_poly)
        latex_den = poly_to_latex(den_poly)
        
        with col_input2:
            st.markdown("**Hàm truyền tương ứng $G(s)$:**")
            st.latex(r"G(s) = \frac{N(s)}{D(s)} = \frac{" + latex_num + r"}{" + latex_den + r"}")
            st.caption(f"Bậc của hệ thống: $n = {len(den_poly)-1}$")
            
        sys_t3 = signal.TransferFunction(num_poly, den_poly)
        
        st.divider()
        tab3_col1, tab3_col2 = st.columns(2)
        
        with tab3_col1:
            st.subheader("📌 Bảng Tiêu Chuẩn Routh-Hurwitz")
            routh_tbl, is_stab, sc_count = compute_routh_table(den_poly)
            row_labels = [f"s^{len(den_poly)-1-i}" for i in range(len(den_poly))]
            df_routh = pd.DataFrame(routh_tbl, index=row_labels)
            st.dataframe(df_routh.style.format("{:.3f}"), use_container_width=True)
            
            if is_stab:
                st.success("✅ **Hệ thống ỔN ĐỊNH**: Toàn bộ hệ số cột 1 cùng dấu dương (tất cả cực đều nằm ở nửa trái mặt phẳng $s$).")
            else:
                st.error(f"❌ **Hệ thống KHÔNG ỔN ĐỊNH**: Có **{sc_count}** lần đổi dấu ở cột 1 (tương ứng với {sc_count} cực nằm ở nửa phải mặt phẳng $s$).")
                
            st.subheader("📍 Mặt Phẳng Cực - Zero (Pole-Zero Map)")
            poles = sys_t3.poles
            zeros = sys_t3.zeros
            
            fig_pz = go.Figure()
            fig_pz.add_vline(x=0, line_dash="dash", line_color="black", annotation_text="Trục ảo jω", annotation_position="top left")
            fig_pz.add_hline(y=0, line_dash="dash", line_color="black", annotation_text="Trục thực σ", annotation_position="bottom right")
            
            # Vùng ổn định (nửa trái mặt phẳng s)
            fig_pz.add_vrect(x0=-100, x1=0, fillcolor="rgba(0, 255, 0, 0.05)", layer="below", line_width=0, annotation_text="Vùng Ổn Định", annotation_position="bottom left")
            fig_pz.add_vrect(x0=0, x1=100, fillcolor="rgba(255, 0, 0, 0.05)", layer="below", line_width=0, annotation_text="Vùng Mất Ổn Định", annotation_position="bottom right")
            
            fig_pz.add_trace(go.Scatter(
                x=np.real(poles), y=np.imag(poles),
                mode='markers', name='Cực (Poles)',
                marker=dict(symbol='x', size=14, color='crimson', line=dict(width=2.5))
            ))
            if len(zeros) > 0:
                fig_pz.add_trace(go.Scatter(
                    x=np.real(zeros), y=np.imag(zeros),
                    mode='markers', name='Zeros',
                    marker=dict(symbol='circle-open', size=14, color='blue', line=dict(width=2.5))
                ))
            
            # Set axis limits around poles/zeros
            all_real = np.real(list(poles) + list(zeros)) if len(zeros) > 0 else np.real(poles)
            all_imag = np.imag(list(poles) + list(zeros)) if len(zeros) > 0 else np.imag(poles)
            max_r = max(2.0, np.max(np.abs(all_real)) * 1.5 if len(all_real) > 0 else 2.0)
            max_i = max(2.0, np.max(np.abs(all_imag)) * 1.5 if len(all_imag) > 0 else 2.0)
            
            fig_pz.update_xaxes(range=[-max_r, max_r], title_text="Trục Thực (Real Axis - σ)")
            fig_pz.update_yaxes(range=[-max_i, max_i], title_text="Trục Ảo (Imag Axis - jω)")
            fig_pz.update_layout(height=400, margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig_pz, use_container_width=True)

        with tab3_col2:
            st.subheader("📉 Biểu Đồ Tần Số Bode (Bode Plot)")
            w, mag, phase = signal.bode(sys_t3)
            
            fig_bode = make_subplots(
                rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                subplot_titles=("Biên độ: 20 log10 |G(jω)| (dB)", "Góc pha: ∠G(jω) (deg)")
            )
            fig_bode.add_trace(go.Scatter(x=w, y=mag, name="Magnitude (dB)", line=dict(color="#1f77b4", width=2.5)), row=1, col=1)
            fig_bode.add_hline(y=0, line_dash="dash", line_color="gray", row=1, col=1)
            
            fig_bode.add_trace(go.Scatter(x=w, y=phase, name="Phase (deg)", line=dict(color="#ff7f0e", width=2.5)), row=2, col=1)
            fig_bode.add_hline(y=-180, line_dash="dash", line_color="red", row=2, col=1)
            
            fig_bode.update_xaxes(type="log", row=2, col=1, title_text="Tần số góc ω (rad/s)")
            fig_bode.update_layout(height=480, showlegend=False, margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig_bode, use_container_width=True)
            
    except Exception as e:
        st.error(f"Lỗi cú pháp nhập đa thức: {e}. Vui lòng nhập các số thực cách nhau bằng dấu phẩy (Ví dụ: 1, 2, 4).")
