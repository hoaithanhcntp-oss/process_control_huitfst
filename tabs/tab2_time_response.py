import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy import signal
from utils.control_utils import calc_step_metrics

def render():
    st.header("2. Khảo Sát Đáp Ứng Thời Gian & Chỉ Tiêu Quá Độ")
    
    # ---------------------------------------------------------
    # PHẦN 1: MÔ PHỎNG & ĐỒ THỊ TƯƠNG TÁC (ĐẶT Ở TRÊN)
    # ---------------------------------------------------------
    c_in1, c_in2 = st.columns([1, 2])
    
    with c_in1:
        st.subheader("Cấu hình hệ thống")
        wn_t2 = st.slider("Tần số riêng ωn (rad/s):", 0.5, 8.0, 3.0, 0.5, key="wn2")
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
            fig_t2.update_layout(title="Đáp ứng Bước Nhảy Đơn Vị", xaxis_title="Thời gian t (s)", yaxis_title="Biên độ y(t)", height=380, margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig_t2, use_container_width=True)
            
            mc1, mc2, mc3, mc4 = st.columns(4)
            mc1.metric("Độ vọt lố (%OS)", f"{m['OS']:.2f} %")
            mc2.metric("Thời gian đạt đỉnh (Tp)", f"{m['Tp']:.2f} s")
            mc3.metric("Thời gian xác lập (Ts 2%)", f"{m['Ts']:.2f} s")
            mc4.metric("Thời gian lên (Tr)", f"{m['Tr']:.2f} s")
            
        elif sig_type == "Xung kích (Impulse)":
            t_i, y_i = signal.impulse(sys_t2, T=t_arr)
            fig_t2.add_trace(go.Scatter(x=t_i, y=y_i, name="Đáp ứng xung h(t)", line=dict(color="#2ca02c", width=2.5)))
            fig_t2.update_layout(title="Đáp ứng Xung Kích (Impulse Response)", xaxis_title="Thời gian t (s)", yaxis_title="Biên độ h(t)", height=380, margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig_t2, use_container_width=True)
        else:
            u_ramp = t_arr
            t_r, y_r, _ = signal.lsim(sys_t2, U=u_ramp, T=t_arr)
            fig_t2.add_trace(go.Scatter(x=t_r, y=y_r, name="y(t)", line=dict(color="#1f77b4", width=2.5)))
            fig_t2.add_trace(go.Scatter(x=t_r, y=u_ramp, name="r(t)=t", line=dict(color="red", dash="dash")))
            fig_t2.update_layout(title="Đáp ứng Hàm Dốc (Ramp Response)", xaxis_title="Thời gian t (s)", yaxis_title="Biên độ", height=380, margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig_t2, use_container_width=True)

    # ---------------------------------------------------------
    # PHẦN 2: LÝ THUYẾT & NGUYÊN LÝ (ĐƯA XUỐNG DƯỚI CÙNG)
    # ---------------------------------------------------------
    st.divider()
    with st.expander("📖 Cơ Sở Lý Thuyết & Định Nghĩa Các Chỉ Tiêu Chất Lượng Quá Độ", expanded=True):
        st.markdown("### 🔹 Công thức giải tích các chỉ tiêu chất lượng (Hệ bậc 2 thiếu suy giảm $0 < \\zeta < 1$)")
        c_eq1, c_eq2 = st.columns(2)
        with c_eq1:
            st.latex(r"\%OS = e^{-\frac{\zeta\pi}{\sqrt{1-\zeta^2}}} \times 100\%")
            st.latex(r"t_p = \frac{\pi}{\omega_d} = \frac{\pi}{\omega_n \sqrt{1-\zeta^2}}")
        with c_eq2:
            st.latex(r"t_s (2\%) \approx \frac{4}{\zeta \omega_n}, \quad t_s (5\%) \approx \frac{3}{\zeta \omega_n}")
            st.latex(r"t_r \approx \frac{\pi - \arccos(\zeta)}{\omega_n \sqrt{1-\zeta^2}} \approx \frac{1.8}{\omega_n}")
        st.markdown("""
        * **Độ vọt lố (Percentage Overshoot - $\%OS$):** Phần trăm biên độ vượt quá giá trị xác lập lớn nhất. Chỉ phụ thuộc duy nhất vào $\zeta$.
        * **Thời gian đạt đỉnh ($t_p$):** Thời điểm đầu ra đạt giá trị cực đại đầu tiên.
        * **Thời gian xác lập ($t_s$):** Thời gian để đáp ứng đi vào và nằm luôn trong dải dung sai cho phép ($\pm 2\%$ hoặc $\pm 5\%$).
        * **Sai số xác lập ($e_{ss}$):** Độ chênh lệch giữa tín hiệu đặt $r(t)$ và tín hiệu ra $y(t)$ khi $t \to \infty$.
        """)
