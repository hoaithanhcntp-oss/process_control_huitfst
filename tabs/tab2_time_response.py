import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy import signal
from utils.control_utils import calc_step_metrics

def render():
    st.header("2. Khảo Sát Đáp Ứng Thời Gian & Chỉ Tiêu Quá Độ")
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
            fig_t2.add_trace(go.Scatter(x=t_s, y=np.ones_like(t_s), name="r(t)", line=dict(color="red", dash="dash")))
            fig_t2.add_trace(go.Scatter(x=t_s, y=np.ones_like(t_s)*1.02, name="+2%", line=dict(color="gray", dash="dot")))
            fig_t2.add_trace(go.Scatter(x=t_s, y=np.ones_like(t_s)*0.98, name="-2%", line=dict(color="gray", dash="dot")))
            st.plotly_chart(fig_t2, use_container_width=True)
            
            mc1, mc2, mc3, mc4 = st.columns(4)
            mc1.metric("Độ vọt lố (%OS)", f"{m['OS']:.2f} %")
            mc2.metric("Thời gian đỉnh (Tp)", f"{m['Tp']:.2f} s")
            mc3.metric("Thời gian xác lập (Ts 2%)", f"{m['Ts']:.2f} s")
            mc4.metric("Thời gian lên (Tr)", f"{m['Tr']:.2f} s")
            
        elif sig_type == "Xung kích (Impulse)":
            t_i, y_i = signal.impulse(sys_t2, T=t_arr)
            fig_t2.add_trace(go.Scatter(x=t_i, y=y_i, name="Đáp ứng xung h(t)", line=dict(color="#2ca02c", width=2.5)))
            fig_t2.update_layout(title="Đáp ứng Xung Kích (Impulse Response)", xaxis_title="Thời gian (s)", yaxis_title="Biên độ")
            st.plotly_chart(fig_t2, use_container_width=True)
        else:
            u_ramp = t_arr
            t_r, y_r, _ = signal.lsim(sys_t2, U=u_ramp, T=t_arr)
            fig_t2.add_trace(go.Scatter(x=t_r, y=y_r, name="y(t)", line=dict(color="#1f77b4", width=2.5)))
            fig_t2.add_trace(go.Scatter(x=t_r, y=u_ramp, name="Tín hiệu dốc r(t)=t", line=dict(color="red", dash="dash")))
            fig_t2.update_layout(title="Đáp ứng Hàm Dốc (Ramp Response)", xaxis_title="Thời gian (s)", yaxis_title="Biên độ")
            st.plotly_chart(fig_t2, use_container_width=True)
