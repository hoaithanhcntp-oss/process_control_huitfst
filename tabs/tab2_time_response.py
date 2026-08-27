import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy import signal
from utils.control_utils import calc_step_metrics

def render():
    st.header("2. Khảo Sát Đáp Ứng Thời Gian & Chỉ Tiêu Quá Độ")
    
    with st.expander("📖 **Nguyên Lý & Định Nghĩa Các Chỉ Tiêu Chất Lượng Miền Thời Gian**", expanded=False):
        st.markdown(r"""
        * **1. Độ vọt lố (Percentage Overshoot - $\%OS$):**
          $$\%OS = \frac{y_{max} - y(\infty)}{y(\infty)} \times 100\% = e^{-\frac{\zeta\pi}{\sqrt{1-\zeta^2}}} \times 100\%$$
        * **2. Thời gian đạt đỉnh (Peak Time - $t_p$):** Thời điểm đầu ra đạt giá trị cực đại đầu tiên:
          $$t_p = \frac{\pi}{\omega_d} = \frac{\pi}{\omega_n \sqrt{1 - \zeta^2}}$$
        * **3. Thời gian tăng trưởng (Rise Time - $t_r$):** Thời gian để đáp ứng tăng từ $10\%$ đến $90\%$ giá trị xác lập (xấp xỉ $t_r \approx \frac{1.8}{\omega_n}$).
        * **4. Thời gian xác lập (Settling Time - $t_s$):** Thời gian để đáp ứng đi vào và duy trì trong dải dung sai $\pm 2\%$ quanh giá trị xác lập ($t_s \approx \frac{4}{\zeta\omega_n}$) hoặc tiêu chuẩn $5\%$ ($t_s \approx \frac{3}{\zeta\omega_n}$).
        * **5. Sai số xác lập (Steady-State Error - $e_{ss}$):** $e_{ss} = \lim_{t \to \infty} [r(t) - y(t)]$.
        """)

    c_in1, c_in2 = st.columns([1, 2])
    
    with c_in1:
        st.subheader("Cấu hình Hàm truyền")
        wn_t2 = st.slider("Tần số riêng ωn:", 0.5, 8.0, 3.0, 0.5, key="wn2")
        zeta_t2 = st.slider("Hệ số tắt ζ:", 0.05, 1.5, 0.35, 0.05, key="zeta2")
        sig_type = st.selectbox("Tín hiệu kích thích đầu vào:", ["Bước nhảy (Step)", "Xung kích (Impulse)", "Hàm dốc (Ramp)"])
        
        num_t2 = [wn_t2**2]
        den_t2 = [1.0, 2.0 * zeta_t2 * wn_t2, wn_t2**2]
        sys_t2 = signal.TransferFunction(num_t2, den_t2)

    with c_in2:
        t_arr = np.linspace(0, 15, 600)
        fig_t2 = go.Figure()
        
        if sig_type == "Bước nhảy (Step)":
            t_s, y_s = signal.step(sys_t2, T=t_arr)
            m = calc_step_metrics(t_s, y_s, y_final=1.0)
            
            fig_t2.add_trace(go.Scatter(x=t_s, y=y_s, name="y(t)", line=dict(color="#1f77b4", width=2.5)))
            fig_t2.add_trace(go.Scatter(x=t_s, y=np.ones_like(t_s), name="r(t)=1", line=dict(color="red", dash="dash")))
            # Vùng ±2%
            fig_t2.add_trace(go.Scatter(x=t_s, y=np.ones_like(t_s)*1.02, name="+2% Dung sai", line=dict(color="gray", dash="dot")))
            fig_t2.add_trace(go.Scatter(x=t_s, y=np.ones_like(t_s)*0.98, name="-2% Dung sai", line=dict(color="gray", dash="dot")))
            fig_t2.update_layout(title="Đáp ứng Bước nhảy với Vùng Dung sai Xác lập ±2%", xaxis_title="Thời gian (s)", yaxis_title="Biên độ", hovermode="x unified")
            st.plotly_chart(fig_t2, use_container_width=True)
            
            mc1, mc2, mc3, mc4 = st.columns(4)
            mc1.metric("Độ vọt lố (%OS)", f"{m['OS']:.2f} %")
            mc2.metric("Thời gian đỉnh (Tp)", f"{m['Tp']:.2f} s")
            mc3.metric("Thời gian xác lập (Ts 2%)", f"{m['Ts']:.2f} s")
            mc4.metric("Thời gian lên (Tr)", f"{m['Tr']:.2f} s")
            
        elif sig_type == "Xung kích (Impulse)":
            t_i, y_i = signal.impulse(sys_t2, T=t_arr)
            fig_t2.add_trace(go.Scatter(x=t_i, y=y_i, name="Đáp ứng xung h(t)", line=dict(color="#2ca02c", width=2.5)))
            fig_t2.update_layout(title="Đáp ứng Xung Kích (Impulse Response)", xaxis_title="Thời gian (s)", yaxis_title="Biên độ", hovermode="x unified")
            st.plotly_chart(fig_t2, use_container_width=True)
        else:
            u_ramp = t_arr
            t_r, y_r, _ = signal.lsim(sys_t2, U=u_ramp, T=t_arr)
            fig_t2.add_trace(go.Scatter(x=t_r, y=y_r, name="y(t)", line=dict(color="#1f77b4", width=2.5)))
            fig_t2.add_trace(go.Scatter(x=t_r, y=u_ramp, name="Tín hiệu dốc r(t)=t", line=dict(color="red", dash="dash")))
            fig_t2.update_layout(title="Đáp ứng Hàm Dốc (Ramp Response)", xaxis_title="Thời gian (s)", yaxis_title="Biên độ", hovermode="x unified")
            st.plotly_chart(fig_t2, use_container_width=True)
