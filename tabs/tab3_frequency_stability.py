import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import signal
import pandas as pd
from utils.control_utils import compute_routh_table

def render():
    st.header("3. Khảo Sát Tính Ổn Định & Đặc Tính Miền Tần Số")
    
    with st.expander("📖 Nguyên lý Tiêu chuẩn Routh-Hurwitz & Biểu đồ Bode", expanded=True):
        st.markdown("""
        * **Mặt phẳng phức $s = \\sigma + j\\omega$:** 
          * Nửa trái mặt phẳng phức ($\text{Re}(s) < 0$): Hệ thống **Ổn định**.
          * Nửa phải mặt phẳng phức ($\text{Re}(s) > 0$): Hệ thống **Mất ổn định**.
        * **Tiêu chuẩn Routh-Hurwitz:** Số nghiệm nằm bên phải trục ảo bằng số lần đổi dấu ở cột 1 của bảng Routh.
        * **Đặc tính tần số (Bode Plot):**
          * Biểu đồ Biên độ: $L(\\omega) = 20\\log_{10}|G(j\\omega)|$ [dB]. Tần số cắt biên $\\omega_{gc}$ [rad/s] tại $0\\text{ dB}$.
          * Biểu đồ Pha: $\\phi(\\omega) = \\angle G(j\\omega)$ [deg]. Tần số cắt pha $\\omega_{pc}$ [rad/s] tại $-180^\\circ$.
          * Độ dự trữ pha $PM = 180^\\circ + \\phi(\\omega_{gc})$ [deg].
        """)

    raw_den = st.text_input("Nhập các hệ số đa thức mẫu số a_n, a_{n-1}, ..., a_0:", "1, 3, 3, 2")
    raw_num = st.text_input("Nhập các hệ số đa thức tử số:", "2")
    
    try:
        den_poly = [float(x.strip()) for x in raw_den.split(",")]
        num_poly = [float(x.strip()) for x in raw_num.split(",")]
        sys_t3 = signal.TransferFunction(num_poly, den_poly)
        
        tab3_col1, tab3_col2 = st.columns(2)
        with tab3_col1:
            st.subheader("📌 Tiêu chuẩn Routh-Hurwitz")
            routh_tbl, is_stab, sc_count = compute_routh_table(den_poly)
            row_labels = [f"s^{len(den_poly)-1-i}" for i in range(len(den_poly))]
            df_routh = pd.DataFrame(routh_tbl, index=row_labels)
            st.dataframe(df_routh.style.format("{:.3f}"))
            
            if is_stab:
                st.success("✅ **Hệ thống ỔN ĐỊNH**: Cột 1 không đổi dấu (tất cả nghiệm có phần thực âm).")
            else:
                st.error(f"❌ **Hệ thống KHÔNG ỔN ĐỊNH**: Có **{sc_count}** lần đổi dấu ở cột 1.")
                
            st.subheader("📍 Mặt phẳng Cực - Zero (Pole-Zero Map)")
            poles = sys_t3.poles
            zeros = sys_t3.zeros
            fig_pz = go.Figure()
            fig_pz.add_vline(x=0, line_dash="dash", line_color="black")
            fig_pz.add_hline(y=0, line_dash="dash", line_color="black")
            fig_pz.add_trace(go.Scatter(x=np.real(poles), y=np.imag(poles), mode='markers', name='Cực (Poles)', marker=dict(symbol='x', size=12, color='crimson', line=dict(width=2))))
            if len(zeros) > 0:
                fig_pz.add_trace(go.Scatter(x=np.real(zeros), y=np.imag(zeros), mode='markers', name='Zeros', marker=dict(symbol='circle-open', size=12, color='blue', line=dict(width=2))))
            fig_pz.update_layout(
                xaxis_title="Trục thực σ [s⁻¹]",
                yaxis_title="Trục ảo jω [rad/s]",
                height=350,
                hovermode="closest"
            )
            st.plotly_chart(fig_pz, use_container_width=True)

        with tab3_col2:
            st.subheader("📉 Biểu đồ Bode")
            w, mag, phase = signal.bode(sys_t3)
            fig_bode = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, subplot_titles=("Biên độ L(ω) [dB]", "Góc pha φ(ω) [deg]"))
            fig_bode.add_trace(go.Scatter(x=w, y=mag, line=dict(color="blue"), name="Biên độ [dB]"), row=1, col=1)
            fig_bode.add_trace(go.Scatter(x=w, y=phase, line=dict(color="orange"), name="Góc pha [deg]"), row=2, col=1)
            fig_bode.add_trace(go.Scatter(x=w, y=np.zeros_like(w), line=dict(color="gray", dash="dot"), name="0 dB"), row=1, col=1)
            fig_bode.add_trace(go.Scatter(x=w, y=np.ones_like(w)*(-180.0), line=dict(color="red", dash="dot"), name="-180 deg"), row=2, col=1)
            
            fig_bode.update_xaxes(type="log", row=2, col=1, title_text="Tần số góc ω [rad/s]")
            fig_bode.update_yaxes(title_text="Biên độ [dB]", row=1, col=1)
            fig_bode.update_yaxes(title_text="Góc pha [deg]", row=2, col=1)
            fig_bode.update_layout(height=420, showlegend=False, hovermode="x unified")
            st.plotly_chart(fig_bode, use_container_width=True)
    except Exception as e:
        st.error(f"Lỗi nhập dữ liệu đa thức: {e}")
