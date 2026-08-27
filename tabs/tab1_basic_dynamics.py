import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy import signal
from utils.control_utils import pade_approx

def render():
    st.header("1. Khảo Sát Các Khâu Động Học Điển Hình")
    
    with st.expander("📖 **Nguyên Lý Các Khâu Động Học Cơ Bản & Mô Hình Toán Học**", expanded=False):
        st.markdown(r"""
        * **1. Khâu Quán Tính Bậc Nhất Có Trễ (FOPDT):**
          $$G(s) = \frac{K}{\tau s + 1} e^{-\theta s}$$
          * $K$ (Hệ số khuếch đại tĩnh): Độ nhạy đầu ra khi đầu vào thay đổi 1 đơn vị ($y(\infty) = K \cdot u_0$).
          * $\tau$ (Hằng số thời gian): Thời gian để đáp ứng đạt $63.2\%$ giá trị xác lập. Sau $3\tau$ đạt $95\%$, sau $4\tau$ đạt $98\%$.
          * $\theta$ (Thời gian trễ / Dead time): Khoảng thời gian tín hiệu trôi trong đường ống trước khi cảm biến ghi nhận được.
        * **2. Khâu Dao Động Bậc Hai Chuẩn (Second-Order System):**
          $$G(s) = \frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}$$
          * $\omega_n$ (Tần số dao động tự nhiên): Tốc độ đáp ứng cơ bản của hệ thống.
          * $\zeta$ (Hệ số tắt dần - Damping Ratio): Quyết định đặc tính dao động:
            * $\zeta = 0$: Không suy giảm (Undamped) - Dao động điều hòa liên tục.
            * $0 < \zeta < 1$: Dưới suy giảm (Underdamped) - Dao động tắt dần có vọt lố ($\%OS$).
            * $\zeta = 1$: Suy giảm tới hạn (Critically Damped) - Đáp ứng nhanh nhất mà không bị vọt lố.
            * $\zeta > 1$: Quá suy giảm (Overdamped) - Không dao động, đáp ứng chậm.
        """)

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
                st.warning("⚠️ **ζ = 0: Không suy giảm (Undamped)** - Cực nằm trên trục ảo, dao động vĩnh cửu.")
            elif 0 < zeta < 1:
                st.info(f"ℹ️ **0 < ζ < 1: Dưới suy giảm (Underdamped)** - Cực phức liên hợp. Vọt lố lý thuyết: {100*np.exp(-zeta*np.pi/np.sqrt(1-zeta**2)):.1f}%.")
            elif zeta == 1:
                st.success("✅ **ζ = 1: Suy giảm tới hạn (Critically Damped)** - Xác lập nhanh nhất, không vọt lố.")
            else:
                st.info("ℹ️ **ζ > 1: Quá suy giảm (Overdamped)** - Hai cực thực âm phân biệt, đáp ứng chậm.")

    with col2:
        sys_t1 = signal.TransferFunction(num_t1, den_t1)
        t_span = np.linspace(0, 20, 500)
        t_out, y_step = signal.step(sys_t1, T=t_span)
        
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=t_out, y=y_step, mode='lines', name='Đáp ứng bước nhảy y(t)', line=dict(color='#1f77b4', width=2.5)))
        fig1.add_trace(go.Scatter(x=t_out, y=np.ones_like(t_out) * (k_fopdt if model_type == "Khâu bậc 1 có trễ (FOPDT)" else 1.0), mode='lines', name='Giá trị xác lập lý thuyết', line=dict(color='red', dash='dash')))
        fig1.update_layout(title="Đồ thị Đáp ứng Bước nhảy (Step Response)", xaxis_title="Thời gian (giây)", yaxis_title="Biên độ đầu ra y(t)", hovermode="x unified")
        st.plotly_chart(fig1, use_container_width=True)
