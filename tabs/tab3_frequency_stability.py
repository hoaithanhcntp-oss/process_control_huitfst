import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import signal
import pandas as pd
from utils.control_utils import compute_routh_table

def poly_to_latex(coeffs, var="s"):
    """Chuyển danh sách hệ số đa thức thành chuỗi LaTeX toán học chuẩn."""
    coeffs = [float(c) for c in coeffs]
    if len(coeffs) == 0 or all(c == 0 for c in coeffs):
        return "0"
    
    # Bỏ số 0 ở đầu
    while len(coeffs) > 1 and coeffs[0] == 0:
        coeffs.pop(0)
    n = len(coeffs)
    
    terms = []
    for i, c in enumerate(coeffs):
        if c == 0:
            continue
        power = n - 1 - i
        abs_c = abs(c)
        sign = "-" if c < 0 else ("+" if (len(terms) > 0 and c > 0) else "")
        coeff_str = f"{int(abs_c)}" if abs_c.is_integer() else f"{abs_c:.3g}"
        
        if power == 0:
            term = f"{sign} {coeff_str}".strip()
        elif power == 1:
            term = f"{sign} {var}".strip() if abs_c == 1 else f"{sign} {coeff_str}{var}".strip()
        else:
            term = f"{sign} {var}^{{{power}}}".strip() if abs_c == 1 else f"{sign} {coeff_str}{var}^{{{power}}}".strip()
        terms.append(term)
        
    return " ".join(terms) if terms else "0"

def render():
    st.header("3. Khảo Sát Tính Ổn Định & Đặc Tính Miền Tần Số")
    
    # --------------------------------------------------------------------------
    # NGUYÊN LÝ & SƠ ĐỒ KHỐI
    # --------------------------------------------------------------------------
    with st.expander("📖 **Nguyên lý: Hàm truyền, Tính ổn định & Tiêu chuẩn Routh-Hurwitz**", expanded=False):
        st.markdown(r"""
        * **Hàm truyền đạt (Transfer Function):** Tỉ số giữa biến đổi Laplace của tín hiệu đầu ra $Y(s)$ và đầu vào $X(s)$ khi điều kiện đầu bằng 0:
          $$G(s) = \frac{Y(s)}{X(s)} = \frac{N(s)}{D(s)} = \frac{b_m s^m + b_{m-1} s^{m-1} + \dots + b_1 s + b_0}{a_n s^n + a_{n-1} s^{n-1} + \dots + a_1 s + a_0}$$
        * **Tính ổn định hệ thống tuyến tính (BIBO Stability):**
          * **Hệ ổn định:** Tất cả các cực (nghiệm của $D(s) = 0$) đều có phần thực âm ($\text{Re}(p_i) < 0$), nằm hoàn toàn ở **nửa trái mặt phẳng phức $s$**.
          * **Hệ không ổn định:** Có ít nhất một cực có phần thực dương ($\text{Re}(p_i) > 0$), nằm ở **nửa phải mặt phẳng phức**.
          * **Hệ ở biên giới ổn định:** Có cực thuần ảo đơn ($\text{Re}(p_i) = 0$).
        * **Tiêu chuẩn Routh-Hurwitz:** Số nghiệm nằm bên phải mặt phẳng phức bằng **số lần đổi dấu của các phần tử ở cột thứ nhất** trong bảng Routh.
        """)
    
    # --------------------------------------------------------------------------
    # NHẬP HỆ SỐ TỬ SỐ VÀ MẪU SỐ
    # --------------------------------------------------------------------------
    st.subheader("📝 Nhập Hệ Số Hàm Truyền")
    st.caption("Nhập các hệ số phân cách bởi dấu phẩy theo thứ tự số mũ giảm dần từ $s^n \\to s^0$. Ví dụ: `s^2 + 2s + 1` nhập là `1, 2, 1`.")
    
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        raw_num = st.text_input("Tử số N(s) - Các hệ số:", value="2, 1", help="Ví dụ: 2, 1 ứng với 2s + 1")
    with col_in2:
        raw_den = st.text_input("Mẫu số D(s) - Các hệ số (Đa thức đặc trưng):", value="1, 3, 3, 2", help="Ví dụ: 1, 3, 3, 2 ứng với s^3 + 3s^2 + 3s + 2")
    
    try:
        num_poly = [float(x.strip()) for x in raw_num.split(",") if x.strip()]
        den_poly = [float(x.strip()) for x in raw_den.split(",") if x.strip()]
        
        if len(num_poly) == 0 or len(den_poly) == 0:
            st.warning("Vui lòng nhập đầy đủ hệ số cho cả tử số và mẫu số.")
            return
            
        if all(c == 0 for c in den_poly):
            st.error("Mẫu số không thể bằng 0.")
            return
            
        # TẠO CHUỖI LATEX HÀM TRUYỀN TƯƠNG ỨNG VỚI CÁC HỆ SỐ VỪA NHẬP
        num_latex = poly_to_latex(num_poly)
        den_latex = poly_to_latex(den_poly)
        
        # HIỂN THỊ HÀM TRUYỀN TOÁN HỌC TRỰC QUAN
        st.markdown("#### 🎯 Hàm truyền tương ứng:")
        st.latex(r"G(s) = \frac{" + num_latex + r"}{" + den_latex + r"}")
        
        # Khởi tạo đối tượng hàm truyền
        sys_t3 = signal.TransferFunction(num_poly, den_poly)
        poles = sys_t3.poles
        zeros = sys_t3.zeros
        
        st.divider()
        
        # ----------------------------------------------------------------------
        # PHÂN TÍCH TÍNH ỔN ĐỊNH & ĐẶC TÍNH TẦN SỐ
        # ----------------------------------------------------------------------
        tab3_col1, tab3_col2 = st.columns(2)
        
        with tab3_col1:
            st.subheader("📌 Tiêu chuẩn Đại số Routh-Hurwitz")
            routh_tbl, is_stab, sc_count = compute_routh_table(den_poly)
            
            # Xây dựng nhãn dòng s^n, s^(n-1), ...
            deg = len(den_poly) - 1
            row_labels = [f"s^{deg - i}" if (deg - i) > 1 else ("s" if (deg - i) == 1 else "s^0") for i in range(len(den_poly))]
            df_routh = pd.DataFrame(routh_tbl, index=row_labels)
            
            st.dataframe(df_routh.style.format("{:.3f}"), use_container_width=True)
            
            if is_stab:
                st.success(f"✅ **Hệ thống ỔN ĐỊNH (Stable):** Cột 1 không đổi dấu. Toàn bộ {len(poles)} cực đều nằm ở nửa trái mặt phẳng phức.")
            else:
                st.error(f"❌ **Hệ thống KHÔNG ỔN ĐỊNH (Unstable):** Cột 1 đổi dấu **{sc_count}** lần (tương ứng hệ có {sc_count} cực nằm bên phải trục ảo).")
                
            st.subheader("📍 Mặt phẳng Cực - Zero (Pole-Zero Map)")
            fig_pz = go.Figure()
            
            # Vùng nửa trái mặt phẳng phức (Vùng ổn định - màu xanh nhạt)
            max_re = max([abs(np.real(p)) for p in poles] + ([abs(np.real(z)) for z in zeros] if len(zeros) else [1.0]) + [2.0]) * 1.5
            max_im = max([abs(np.imag(p)) for p in poles] + ([abs(np.imag(z)) for z in zeros] if len(zeros) else [1.0]) + [2.0]) * 1.5
            
            fig_pz.add_vrect(x0=-max_re*2, x1=0, fillcolor="rgba(46, 204, 113, 0.12)", layer="below", line_width=0)
            fig_pz.add_vrect(x0=0, x1=max_re*2, fillcolor="rgba(231, 76, 60, 0.12)", layer="below", line_width=0)
            
            # Trục tọa độ
            fig_pz.add_vline(x=0, line_dash="dash", line_color="black", annotation_text="Trục ảo jω", annotation_position="top left")
            fig_pz.add_hline(y=0, line_dash="dash", line_color="black", annotation_text="Trục thực σ", annotation_position="bottom right")
            
            # Điểm cực (Poles - X)
            fig_pz.add_trace(go.Scatter(
                x=np.real(poles), y=np.imag(poles),
                mode='markers+text', name='Cực (Poles)',
                text=[f" p{i+1}: {np.real(p):.2f}+{np.imag(p):.2f}j" if np.imag(p) != 0 else f" p{i+1}: {np.real(p):.2f}" for i, p in enumerate(poles)],
                textposition="top right",
                marker=dict(symbol='x', size=13, color='crimson', line=dict(width=2.5))
            ))
            
            # Điểm Zero (Zeros - O)
            if len(zeros) > 0:
                fig_pz.add_trace(go.Scatter(
                    x=np.real(zeros), y=np.imag(zeros),
                    mode='markers+text', name='Zeros',
                    text=[f" z{i+1}: {np.real(z):.2f}+{np.imag(z):.2f}j" if np.imag(z) != 0 else f" z{i+1}: {np.real(z):.2f}" for i, z in enumerate(zeros)],
                    textposition="top right",
                    marker=dict(symbol='circle-open', size=13, color='blue', line=dict(width=2.5))
                ))
                
            fig_pz.update_layout(
                xaxis=dict(title="Phần thực (Real Axis - σ)", range=[-max_re, max_re]),
                yaxis=dict(title="Phần ảo (Imag Axis - jω)", range=[-max_im, max_im]),
                height=380,
                margin=dict(l=20, r=20, t=30, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_pz, use_container_width=True)

        with tab3_col2:
            st.subheader("📉 Biểu đồ Tần số Bode (Bode Plot)")
            w, mag, phase = signal.bode(sys_t3)
            
            fig_bode = make_subplots(
                rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                subplot_titles=("Biên độ |G(jω)| (dB)", "Góc pha ∠G(jω) (độ)")
            )
            fig_bode.add_trace(go.Scatter(x=w, y=mag, name="Biên độ (dB)", line=dict(color="#1f77b4", width=2.5)), row=1, col=1)
            fig_bode.add_hline(y=0, line_dash="dot", line_color="gray", row=1, col=1)
            
            fig_bode.add_trace(go.Scatter(x=w, y=phase, name="Góc pha (deg)", line=dict(color="#ff7f0e", width=2.5)), row=2, col=1)
            fig_bode.add_hline(y=-180, line_dash="dot", line_color="red", row=2, col=1)
            
            fig_bode.update_xaxes(type="log", row=2, col=1, title_text="Tần số góc ω (rad/s)")
            fig_bode.update_layout(height=420, showlegend=False, margin=dict(l=20, r=20, t=30, b=20), hovermode="x unified")
            st.plotly_chart(fig_bode, use_container_width=True)
            
            # Tọa độ nghiệm chi tiết
            with st.expander("🔍 Chi tiết Tọa độ Cực (Poles) & Zeros"):
                pole_df = pd.DataFrame({
                    "Cực": [f"p_{i+1}" for i in range(len(poles))],
                    "Phần thực (Re)": [f"{np.real(p):.4f}" for p in poles],
                    "Phần ảo (Im)": [f"{np.imag(p):.4f}" for p in poles],
                    "Vị trí": ["Nửa trái (Ổn định)" if np.real(p) < -1e-6 else ("Nửa phải (Bất ổn)" if np.real(p) > 1e-6 else "Trục ảo") for p in poles]
                })
                st.table(pole_df)
                
    except ValueError:
        st.error("Dữ liệu nhập không hợp lệ. Vui lòng chỉ nhập các số thực phân tách bằng dấu phẩy (ví dụ: `1, 3, 3, 2`).")
    except Exception as e:
        st.error(f"Lỗi phân tích hàm truyền: {e}")
