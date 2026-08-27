import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy import signal
from utils.control_utils import calc_step_metrics

def render():
    st.header("2. Khảo Sát Đáp Ứng Thời Gian & Chỉ Tiêu Quá Độ")
    
    with st.expander("📖 **Định nghĩa các chỉ tiêu chất lượng quá độ (Step Response Performance Metrics)**", expanded=True):
        c_m1, c_m2 = st.columns([1.2, 1])
        with c_m1:
            st.markdown("""
            Khi đưa tín hiệu bước nhảy $r(t) = 1(t)$ vào hệ thống kín, chất lượng động học được đánh giá qua 5 chỉ tiêu:
            * **Độ vọt lố ($\\%OS$ - Percentage Overshoot):**
              $$\\%OS = \\frac{y_{max} - y(\\infty)}{y(\\infty)} \\times 100\\% = e^{-\\frac{\\zeta\\pi}{\\sqrt{1-\\zeta^2}}} \\times 100\\%$$
            * **Thời gian đạt đỉnh ($t_p$ - Peak Time):** Thời điểm đầu ra đạt giá trị cực đại đầu tiên: $t_p = \\frac{\\pi}{\\omega_n \\sqrt{1-\\zeta^2}}$.
            * **Thời gian tăng trưởng ($t_r$ - Rise Time):** Thời gian để $y(t)$ tăng từ $10\\%$ đến $90\\%$ giá trị xác lập.
            * **Thời gian xác lập ($t_s$ - Settling Time):** Thời gian để đáp ứng đi vào và nằm hẳn trong dải dung sai $\\pm 2\\%$ quanh giá trị xác lập: $t_s \\approx \\frac{4}{\\zeta \\omega_n}$ (hoặc $\\pm 5\\%: t_s \\approx \\frac{3}{\\zeta \\omega_n}$).
            * **Sai số xác lập ($e_{ss}$ - Steady-State Error):** $e_{ss} = \\lim_{t \\to \\infty} |r(t) - y(t)|$.
            """)
        with c_m2:
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 10px; border-radius: 8px; border: 1px solid #dee2e6; text-align: center;">
                <h5 style="margin-top:0; color:#333;">Biểu Đồ Định Nghĩa Chỉ Tiêu Quá Độ</h5>
                <svg width="100%" height="190" viewBox="0 0 380 190" xmlns="http://www.w3.org/2000/svg">
                    <line x1="40" y1="160" x2="360" y2="160" stroke="#333" stroke-width="2"/>
                    <line x1="40" y1="160" x2="40" y2="20" stroke="#333" stroke-width="2"/>
                    <text x="360" y="180" font-family="Arial" font-size="12" fill="#333">t</text>
                    <text x="20" y="30" font-family="Arial" font-size="12" fill="#333">y(t)</text>
                    
                    <line x1="40" y1="85" x2="350" y2="85" stroke="green" stroke-width="1.5" stroke-dasharray="4"/>
                    <text x="352" y="89" font-family="Arial" font-size="10" fill="green">y(∞)=1</text>
                    
                    <line x1="40" y1="79" x2="350" y2="79" stroke="#aaa" stroke-width="1" stroke-dasharray="2"/>
                    <line x1="40" y1="91" x2="350" y2="91" stroke="#aaa" stroke-width="1" stroke-dasharray="2"/>
                    <text x="315" y="73" font-family="Arial" font-size="9" fill="#777">±2% band</text>
                    
                    <path d="M 40 160 Q 70 155 90 85 T 130 45 T 180 95 T 230 83 T 280 85 L 350 85" fill="none" stroke="#1f77b4" stroke-width="2.5"/>
                    
                    <line x1="130" y1="45" x2="130" y2="85" stroke="red" stroke-width="1.5" stroke-dasharray="3"/>
                    <text x="135" y="60" font-family="Arial" font-size="11" font-weight="bold" fill="red">%OS</text>
                    
                    <line x1="130" y1="45" x2="130" y2="160" stroke="#888" stroke-width="1" stroke-dasharray="2"/>
                    <text x="125" y="175" font-family="Arial" font-size="11" fill="#444">tp</text>
                    
                    <line x1="245" y1="83" x2="245" y2="160" stroke="#888" stroke-width="1" stroke-dasharray="2"/>
                    <text x="240" y="175" font-family="Arial" font-size="11" fill="#444">ts (2%)</text>
                </svg>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

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
