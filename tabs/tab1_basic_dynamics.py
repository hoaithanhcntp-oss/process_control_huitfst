import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy import signal
from utils.control_utils import pade_approx

def render():
    st.header("1. Khảo Sát Các Khâu Động Học Điển Hình")
    
    # Khối nguyên lý & Sơ đồ minh họa
    with st.expander("📖 Nguyên lý & Sơ đồ khối (Block Diagram)", expanded=True):
        col_sch, col_txt = st.columns([1, 1])
        with col_sch:
            st.markdown("""
            ```
            Tín hiệu vào u(t)        ┌────────────────────────────┐       Đáp ứng ra y(t)
            ───────────────────────> │  Hàm truyền đối tượng G(s) │ ───────────────────────>
            (Đơn vị: V, %, mA)       └────────────────────────────┘       (Đơn vị: °C, m, m³/s)
            ```
            """)
        with col_txt:
            st.markdown("""
            * **Khâu bậc 1 có trễ (FOPDT):** $G(s) = \\frac{K}{\\tau s + 1} e^{-\\theta s}$
              * $K$ [đơn vị ra / đơn vị vào]: Hệ số khuếch đại tĩnh.
              * $\\tau$ [s]: Hằng số thời gian quán tính (thời gian để $y(t)$ đạt 63.2% giá trị xác lập).
              * $\\theta$ [s]: Thời gian trễ vận chuyển (Dead time).
            * **Khâu bậc 2 chuẩn:** $G(s) = \\frac{\\omega_n^2}{s^2 + 2\\zeta\\omega_n s + \\omega_n^2}$
              * $\\omega_n$ [rad/s]: Tần số dao động tự nhiên riêng.
              * $\\zeta$ [không thứ nguyên]: Hệ số tắt dần (Damping ratio).
            """)

    col1, col2 = st.columns([1, 2])
    
    with col1:
        model_type = st.radio("Chọn loại khâu động học:", ["Khâu bậc 1 có trễ (FOPDT)", "Khâu bậc 2 chuẩn"])
        if model_type == "Khâu bậc 1 có trễ (FOPDT)":
            k_fopdt = st.slider("Hệ số khuếch đại K [đơn vị ra/vào]:", 0.1, 5.0, 1.5, 0.1)
            tau_fopdt = st.slider("Hằng số thời gian τ [s]:", 0.5, 10.0, 3.0, 0.5)
            theta_delay = st.slider("Thời gian trễ θ [s]:", 0.0, 5.0, 1.0, 0.2)
            
            num_p, den_p = pade_approx(theta_delay, order=2)
            num_t1 = np.polymul([k_fopdt], num_p)
            den_t1 = np.polymul([tau_fopdt, 1.0], den_p)
            st.latex(r"G(s) = \frac{" + str(k_fopdt) + r"}{" + str(tau_fopdt) + r"s + 1} e^{-" + str(theta_delay) + r"s}")
        else:
            wn = st.slider("Tần số riêng ωn [rad/s]:", 0.5, 10.0, 2.5, 0.1)
            zeta = st.slider("Hệ số tắt dần ζ [-]:", 0.0, 2.0, 0.4, 0.05)
            num_t1 = [wn**2]
            den_t1 = [1.0, 2.0 * zeta * wn, wn**2]
            st.latex(r"G(s) = \frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2} = \frac{" + f"{wn**2:.2f}" + r"}{s^2 + " + f"{2*zeta*wn:.2f}" + r"s + " + f"{wn**2:.2f}" + r"}")
            
            if zeta == 0:
                st.warning("ζ = 0: Không suy giảm (Undamped) - Cực nằm trên trục ảo, dao động vĩnh cửu.")
            elif 0 < zeta < 1:
                st.info(f"0 < ζ < 1: Thiếu suy giảm (Underdamped) - Dao động tắt dần, độ vọt lố lý thuyết = {100*np.exp(-zeta*np.pi/np.sqrt(1-zeta**2)):.1f}%.")
            elif zeta == 1:
                st.success("ζ = 1: Suy giảm tới hạn (Critically Damped) - Xác lập nhanh nhất mà không vọt lố.")
            else:
                st.info("ζ > 1: Quá suy giảm (Overdamped) - Hai cực thực âm phân biệt, đáp ứng chậm.")

    with col2:
        sys_t1 = signal.TransferFunction(num_t1, den_t1)
        t_span = np.linspace(0, 20, 500)
        t_out, y_step = signal.step(sys_t1, T=t_span)
        
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=t_out, y=y_step, mode='lines', name='Đáp ứng y(t) [đơn vị đầu ra]', line=dict(color='#1f77b4', width=2.5)))
        fig1.add_trace(go.Scatter(x=t_out, y=np.ones_like(t_out) * (k_fopdt if model_type == "Khâu bậc 1 có trễ (FOPDT)" else 1.0), mode='lines', name='Giá trị xác lập y_ss [đơn vị đầu ra]', line=dict(color='red', dash='dash')))
        fig1.update_layout(
            title="Đồ thị Đáp ứng Bước nhảy (Step Response)",
            xaxis_title="Thời gian t [s]",
            yaxis_title="Biên độ đầu ra y(t) [đơn vị]",
            hovermode="x unified"
        )
        st.plotly_chart(fig1, use_container_width=True)
