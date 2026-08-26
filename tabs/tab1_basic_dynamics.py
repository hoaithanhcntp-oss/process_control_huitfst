import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy import signal
from utils.control_utils import pade_approx

def render():
    st.header("1. Khảo Sát Các Khâu Động Học Điển Hình")
    col1, col2 = st.columns([1, 2])
    
    with col1:
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
                st.warning("ζ = 0: Không suy giảm (Undamped) - Dao động vĩnh cửu.")
            elif 0 < zeta < 1:
                st.info("0 < ζ < 1: Thiếu suy giảm (Underdamped) - Dao động tắt dần có vọt lố.")
            elif zeta == 1:
                st.success("ζ = 1: Suy giảm tới hạn (Critically Damped) - Xác lập nhanh nhất, không vọt lố.")
            else:
                st.info("ζ > 1: Quá suy giảm (Overdamped) - Đáp ứng chậm, không vọt lố.")

    with col2:
        sys_t1 = signal.TransferFunction(num_t1, den_t1)
        t_span = np.linspace(0, 20, 500)
        t_out, y_step = signal.step(sys_t1, T=t_span)
        
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=t_out, y=y_step, mode='lines', name='Đáp ứng bước nhảy y(t)', line=dict(color='#1f77b4', width=2.5)))
        fig1.add_trace(go.Scatter(x=t_out, y=np.ones_like(t_out), mode='lines', name='Tín hiệu đặt r(t)=1', line=dict(color='red', dash='dash')))
        fig1.update_layout(title="Đồ thị Đáp ứng Bước nhảy (Step Response)", xaxis_title="Thời gian (s)", yaxis_title="Biên độ đầu ra")
        st.plotly_chart(fig1, use_container_width=True)
