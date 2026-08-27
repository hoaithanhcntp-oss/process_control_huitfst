import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy import signal
from utils.control_utils import pade_approx

def render():
    st.header("1. Khảo Sát Các Khâu Động Học Điển Hình")
    
    with st.expander("📖 **Nguyên lý lý thuyết & Sơ đồ khối (Lý thuyết cơ bản)**", expanded=True):
        col_exp1, col_exp2 = st.columns([1.2, 1])
        with col_exp1:
            st.markdown("""
            **1. Khâu quán tính bậc 1 có trễ (FOPDT - First Order Plus Dead Time):**
            * Mô tả hầu hết các quá trình truyền nhiệt, mức dịch, bồn khuấy:
            $$G(s) = \\frac{K}{\\tau s + 1} e^{-\\theta s}$$
            * **Ý nghĩa thông số:**
              * $K$ (*Khuếch đại tĩnh*): Độ thay đổi đầu ra khi đầu vào thay đổi 1 đơn vị xác lập.
              * $\\tau$ (*Hằng số thời gian*): Thời gian để đáp ứng đạt **63.2%** giá trị xác lập cuối cùng. Sau $3\\tau$ đạt 95%, sau $4\\tau - 5\\tau$ coi như xác lập hoàn toàn.
              * $\\theta$ (*Thời gian trễ/Dead time*): Khoảng thời gian vật lý dòng chảy/tín hiệu di chuyển trước khi hệ thống bắt đầu có phản ứng.

            **2. Khâu dao động bậc 2 chuẩn (Standard Second-Order System):**
            $$G(s) = \\frac{\\omega_n^2}{s^2 + 2\\zeta\\omega_n s + \\omega_n^2}$$
            * $\\omega_n$: Tần số góc dao động riêng tự nhiên (*Natural Frequency*).
            * $\\zeta$: Hệ số tắt dần (*Damping Ratio*), quyết định dạng đáp ứng động học.
            """)
        with col_exp2:
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #dee2e6; text-align: center;">
                <h5 style="margin-top:0; color:#333;">Sơ Đồ Khối Khâu Động Học</h5>
                <svg width="100%" height="180" viewBox="0 0 420 180" xmlns="http://www.w3.org/2000/svg">
                    <rect x="120" y="20" width="180" height="55" rx="6" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
                    <text x="210" y="52" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#0d47a1" text-anchor="middle">K / (τs + 1) · e^(-θs)</text>
                    <line x1="30" y1="47" x2="115" y2="47" stroke="#333" stroke-width="2" marker-end="url(#arr1)"/>
                    <text x="70" y="38" font-family="Arial" font-size="12" fill="#333" text-anchor="middle">u(t)</text>
                    <line x1="305" y1="47" x2="390" y2="47" stroke="#333" stroke-width="2" marker-end="url(#arr1)"/>
                    <text x="350" y="38" font-family="Arial" font-size="12" fill="#333" text-anchor="middle">y(t)</text>
                    
                    <rect x="120" y="100" width="180" height="55" rx="6" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
                    <text x="210" y="132" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#e65100" text-anchor="middle">ωn² / (s² + 2ζωns + ωn²)</text>
                    <line x1="30" y1="127" x2="115" y2="127" stroke="#333" stroke-width="2" marker-end="url(#arr1)"/>
                    <text x="70" y="118" font-family="Arial" font-size="12" fill="#333" text-anchor="middle">u(t)</text>
                    <line x1="305" y1="127" x2="390" y2="127" stroke="#333" stroke-width="2" marker-end="url(#arr1)"/>
                    <text x="350" y="118" font-family="Arial" font-size="12" fill="#333" text-anchor="middle">y(t)</text>
                    
                    <defs>
                        <marker id="arr1" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                            <path d="M 0 1 L 10 5 L 0 9 z" fill="#333"/>
                        </marker>
                    </defs>
                </svg>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Cài đặt thông số")
        model_type = st.radio("Chọn loại khâu động học:", ["Khâu bậc 1 có trễ (FOPDT)", "Khâu bậc 2 chuẩn"])
        if model_type == "Khâu bậc 1 có trễ (FOPDT)":
            k_fopdt = st.slider("Hệ số khuếch đại K:", 0.1, 5.0, 1.5, 0.1)
            tau_fopdt = st.slider("Hằng số thời gian τ (s):", 0.5, 10.0, 3.0, 0.5)
            theta_delay = st.slider("Thời gian trễ θ (s):", 0.0, 5.0, 1.0, 0.2)
            
            num_p, den_p = pade_approx(theta_delay, order=2)
            num_t1 = np.polymul([k_fopdt], num_p)
            den_t1 = np.polymul([tau_fopdt, 1.0], den_p)
            st.latex(r"G(s) = \frac{" + str(k_fopdt) + r"}{" + str(tau_fopdt) + r"s + 1} e^{-" + str(theta_delay) + r"s}")
        else:
            wn = st.slider("Tần số dao động tự nhiên ωn (rad/s):", 0.5, 10.0, 2.5, 0.1)
            zeta = st.slider("Hệ số tắt dần ζ (damping ratio):", 0.0, 2.0, 0.4, 0.05)
            num_t1 = [wn**2]
            den_t1 = [1.0, 2.0 * zeta * wn, wn**2]
            st.latex(r"G(s) = \frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2} = \frac{" + f"{wn**2:.2f}" + r"}{s^2 + " + f"{2*zeta*wn:.2f}" + r"s + " + f"{wn**2:.2f}" + r"}")
            
            if zeta == 0:
                st.warning("⚠️ **ζ = 0 (Không suy giảm):** Nghiệm thuần ảo $s = \\pm j\\omega_n$, dao động điều hòa vĩnh cửu không tắt.")
            elif 0 < zeta < 1:
                st.info("ℹ️ **0 < ζ < 1 (Thiếu suy giảm):** Nghiệm phức liên hợp có phần thực âm, dao động tắt dần có độ vọt lố.")
            elif zeta == 1:
                st.success("✅ **ζ = 1 (Suy giảm tới hạn):** Nghiệm kép thực âm $s = -\\omega_n$, hệ đạt giá trị xác lập nhanh nhất mà không vọt lố.")
            else:
                st.info("ℹ️ **ζ > 1 (Quá suy giảm):** 2 nghiệm thực âm phân biệt, đáp ứng chậm chạp và không có vọt lố.")

    with col2:
        sys_t1 = signal.TransferFunction(num_t1, den_t1)
        t_span = np.linspace(0, 20, 500)
        t_out, y_step = signal.step(sys_t1, T=t_span)
        
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=t_out, y=y_step, mode='lines', name='Đáp ứng bước nhảy y(t)', line=dict(color='#1f77b4', width=2.5)))
        fig1.add_trace(go.Scatter(x=t_out, y=np.ones_like(t_out), mode='lines', name='Tín hiệu đặt r(t)=1', line=dict(color='red', dash='dash')))
        fig1.update_layout(title="Đồ thị Đáp ứng Bước nhảy (Step Response)", xaxis_title="Thời gian (s)", yaxis_title="Biên độ đầu ra")
        st.plotly_chart(fig1, use_container_width=True)
