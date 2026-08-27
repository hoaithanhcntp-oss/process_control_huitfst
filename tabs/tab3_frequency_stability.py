import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import signal
import pandas as pd
from utils.control_utils import compute_routh_table

def render():
    st.header("3. Khảo Sát Tính Ổn Định & Đặc Tính Miền Tần Số")
    
    with st.expander("📖 **Nguyên lý tính ổn định & Đặc tính tần số (Routh-Hurwitz & Bode)**", expanded=True):
        col_s1, col_s2 = st.columns([1.2, 1])
        with col_s1:
            st.markdown("""
            **1. Tiêu chuẩn đại số Routh-Hurwitz:**
            * Cho phương trình đặc trưng: $a_n s^n + a_{n-1} s^{n-1} + \\dots + a_1 s + a_0 = 0$.
            * **Điều kiện cần:** Tất cả hệ số $a_i$ phải cùng dấu và khác 0.
            * **Điều kiện đủ:** Tất cả các phần tử ở cột 1 của bảng Routh đều mang giá trị dương.
            * **Định lý:** *Số lần đổi dấu các phần tử ở cột 1 bằng đúng số nghiệm có phần thực dương (nằm bên phải trục ảo).*

            **2. Độ dự trữ ổn định trên biểu đồ Bode:**
            * **Tần số cắt biên ($\\omega_{gc}$):** Tần số tại đó $|G(j\\omega)| = 1$ ($0\\text{ dB}$).
              * **Độ dự trữ pha ($PM$ - Phase Margin):** $PM = 180^\\circ + \\angle G(j\\omega_{gc})$. Hệ ổn định khi $PM > 0$ (khuyến nghị $PM \\ge 45^\\circ - 60^\\circ$).
            * **Tần số cắt pha ($\\omega_{pc}$):** Tần số tại đó $\\angle G(j\\omega) = -180^\\circ$.
              * **Độ dự trữ biên ($GM$ - Gain Margin):** $GM = -20\\log_{10}|G(j\\omega_{pc})|\\text{ dB}$. Hệ ổn định khi $GM > 0\\text{ dB}$ (khuyến nghị $GM \\ge 6\\text{ dB}$).
            """)
        with col_s2:
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 10px; border-radius: 8px; border: 1px solid #dee2e6; text-align: center;">
                <h5 style="margin-top:0; color:#333;">Vùng Ổn Định Mặt Phẳng Phức s</h5>
                <svg width="100%" height="190" viewBox="0 0 340 190" xmlns="http://www.w3.org/2000/svg">
                    <rect x="20" y="20" width="140" height="150" fill="#e8f5e9" opacity="0.8"/>
                    <rect x="160" y="20" width="160" height="150" fill="#ffebee" opacity="0.8"/>
                    
                    <line x1="20" y1="95" x2="320" y2="95" stroke="#333" stroke-width="2"/>
                    <line x1="160" y1="20" x2="160" y2="170" stroke="#333" stroke-width="2"/>
                    <text x="310" y="115" font-family="Arial" font-size="12" fill="#333">σ (Re)</text>
                    <text x="165" y="32" font-family="Arial" font-size="12" fill="#333">jω (Im)</text>
                    
                    <text x="85" y="80" font-family="Arial" font-size="12" font-weight="bold" fill="#2e7d32" text-anchor="middle">VÙNG ỔN ĐỊNH</text>
                    <text x="85" y="100" font-family="Arial" font-size="10" fill="#2e7d32" text-anchor="middle">(Nửa trái: Re(s) < 0)</text>
                    
                    <text x="240" y="80" font-family="Arial" font-size="12" font-weight="bold" fill="#c62828" text-anchor="middle">MẤT ỔN ĐỊNH</text>
                    <text x="240" y="100" font-family="Arial" font-size="10" fill="#c62828" text-anchor="middle">(Nửa phải: Re(s) > 0)</text>
                    
                    <text x="95" y="55" font-family="Arial" font-size="16" font-weight="bold" fill="#1b5e20">✕</text>
                    <text x="95" y="145" font-family="Arial" font-size="16" font-weight="bold" fill="#1b5e20">✕</text>
                </svg>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    raw_den = st.text_input("Nhập các hệ số mẫu số (cách nhau bởi dấu phẩy):", "1, 3, 3, 2")
    raw_num = st.text_input("Nhập các hệ số tử số:", "2")
    
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
                st.success("✅ **Hệ thống ỔN ĐỊNH**: Cột 1 không đổi dấu (tất cả các nghiệm có phần thực âm).")
            else:
                st.error(f"❌ **Hệ thống KHÔNG ỔN ĐỊNH**: Có **{sc_count}** lần đổi dấu ở cột 1 (tương ứng {sc_count} nghiệm bên phải trục ảo).")
                
            st.subheader("📍 Mặt phẳng Cực - Zero (Pole-Zero Map)")
            poles = sys_t3.poles
            zeros = sys_t3.zeros
            fig_pz = go.Figure()
            fig_pz.add_vline(x=0, line_dash="dash", line_color="black")
            fig_pz.add_hline(y=0, line_dash="dash", line_color="black")
            fig_pz.add_trace(go.Scatter(x=np.real(poles), y=np.imag(poles), mode='markers', name='Cực (Poles)', marker=dict(symbol='x', size=12, color='crimson', line=dict(width=2))))
            if len(zeros) > 0:
                fig_pz.add_trace(go.Scatter(x=np.real(zeros), y=np.imag(zeros), mode='markers', name='Zeros', marker=dict(symbol='circle-open', size=12, color='blue', line=dict(width=2))))
            fig_pz.update_layout(xaxis_title="Trục thực (Re)", yaxis_title="Trục ảo (Im)", height=350)
            st.plotly_chart(fig_pz, use_container_width=True)

        with tab3_col2:
            st.subheader("📉 Biểu đồ Bode")
            w, mag, phase = signal.bode(sys_t3)
            fig_bode = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, subplot_titles=("Biên độ (dB)", "Góc pha (deg)"))
            fig_bode.add_trace(go.Scatter(x=w, y=mag, line=dict(color="blue")), row=1, col=1)
            fig_bode.add_trace(go.Scatter(x=w, y=phase, line=dict(color="orange")), row=2, col=1)
            fig_bode.update_xaxes(type="log", row=2, col=1, title_text="Tần số ω (rad/s)")
            fig_bode.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_bode, use_container_width=True)
    except Exception as e:
        st.error(f"Lỗi nhập dữ liệu đa thức: {e}")
