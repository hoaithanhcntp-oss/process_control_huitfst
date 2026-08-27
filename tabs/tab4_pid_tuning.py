import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def render():
    st.header("4. Thiết Kế & Chỉnh Định Bộ Điều Khiển PID")
    
    with st.expander("📖 Cấu trúc Bộ điều khiển PID & Bảng quy tắc Chỉnh định", expanded=True):
        col_b1, col_b2 = st.columns([1, 1])
        with col_b1:
            st.markdown("""
            ```
            Tín hiệu đặt R(s)       Sai số E(s)   ┌─────────────┐   Tín hiệu u(t)  ┌─────────────┐   Đầu ra Y(s)
            ───────────────>(+) ───>──────────> │   PID C(s)  │ ─────────────> │ Plant G(s)  │ ─────────┬─────>
                             ^ (-)              └─────────────┘   [Van: 0-100%]    └─────────────┘          │
                             │                                                                              │
                             └──────────────────────────────────────────────────────────────────────────────┘
            ```
            """)
        with col_b2:
            st.markdown("""
            * **Hàm truyền PID:** $C(s) = K_p + \\frac{K_i}{s} + K_d s = K_p \\left(1 + \\frac{1}{T_i s} + T_d s\\right)$
              * $K_p$ [-]: Khuếch đại tỷ lệ (tăng tốc độ đáp ứng, giảm sai số nhưng dễ gây vọt lố).
              * $K_i$ [$s^{-1}$]: Khâu tích phân (triệt tiêu hoàn toàn sai số xác lập $e_{ss} \\to 0$).
              * $K_d$ [s]: Khâu vi phân (giảm xóc, ghìm độ vọt lố).
            * **Quy tắc Ziegler-Nichols 1 (FOPDT):** $K_p = 1.2\\frac{\\tau}{K\\theta}$, $T_i = 2\\theta$ [s], $T_d = 0.5\\theta$ [s].
            """)

    col_pid_ctrl, col_pid_plot = st.columns([1, 2])
    
    with col_pid_ctrl:
        st.subheader("Đối tượng điều khiển FOPDT")
        kp_p = st.number_input("K (Khuếch đại đối tượng) [đơn vị/ %]:", value=1.0, step=0.1)
        tau_p = st.number_input("τ (Hằng số thời gian) [s]:", value=4.0, step=0.5)
        theta_p = st.number_input("θ (Thời gian trễ) [s]:", value=1.5, step=0.2)
        
        st.divider()
        st.subheader("Chỉnh định tự động (Auto-Tuning)")
        tune_method = st.selectbox("Chọn công thức tính mẫu:", ["Thử sai thủ công", "Ziegler-Nichols 1 (S-curve)", "Cohen-Coon"])
        
        if tune_method == "Ziegler-Nichols 1 (S-curve)":
            kp_calc = 1.2 * (tau_p / (kp_p * max(0.1, theta_p)))
            ti_calc = 2.0 * theta_p
            td_calc = 0.5 * theta_p
            ki_calc = kp_calc / ti_calc
            kd_calc = kp_calc * td_calc
            st.success(f"Thông số Z-N: Kp={kp_calc:.2f}, Ki={ki_calc:.2f} s⁻¹, Kd={kd_calc:.2f} s")
        elif tune_method == "Cohen-Coon":
            r = theta_p / tau_p
            kp_calc = (1.0 / (kp_p * r)) * (4.0/3.0 + r / 4.0)
            ti_calc = theta_p * (32.0 + 6.0 * r) / (13.0 + 8.0 * r)
            td_calc = theta_p * 4.0 / (11.0 + 2.0 * r)
            ki_calc = kp_calc / ti_calc
            kd_calc = kp_calc * td_calc
            st.success(f"Thông số Cohen-Coon: Kp={kp_calc:.2f}, Ki={ki_calc:.2f} s⁻¹, Kd={kd_calc:.2f} s")
        else:
            kp_calc, ki_calc, kd_calc = 2.5, 0.3, 0.8
            
        kp_val = st.slider("Hệ số Kp [-]:", 0.0, 20.0, float(kp_calc), 0.1)
        ki_val = st.slider("Hệ số Ki [s⁻¹]:", 0.0, 5.0, float(ki_calc), 0.05)
        kd_val = st.slider("Hệ số Kd [s]:", 0.0, 10.0, float(kd_calc), 0.1)

    with col_pid_plot:
        dt_sim = 0.05
        t_pid = np.arange(0, 30.0, dt_sim)
        n_pid = len(t_pid)
        d_steps = max(1, int(theta_p / dt_sim))
        buff = [0.0] * d_steps
        
        y_open = np.zeros(n_pid)
        y_closed = np.zeros(n_pid)
        u_ctrl = np.zeros(n_pid)
        int_e, prev_e, curr_y_cl, curr_y_op = 0.0, 0.0, 0.0, 0.0
        
        for i in range(1, n_pid):
            u_in_op = 1.0 if t_pid[i] >= 1.0 else 0.0
            dy_op = (kp_p * u_in_op - curr_y_op) / tau_p
            curr_y_op += dy_op * dt_sim
            y_open[i] = curr_y_op
            
            y_meas = buff.pop(0)
            err = 1.0 - y_meas
            int_e += err * dt_sim
            der_e = (err - prev_e) / dt_sim
            prev_e = err
            
            u = np.clip(kp_val * err + ki_val * int_e + kd_val * der_e, 0.0, 100.0)
            u_ctrl[i] = u
            
            dy_cl = (kp_p * u - curr_y_cl) / tau_p
            curr_y_cl += dy_cl * dt_sim
            y_closed[i] = curr_y_cl
            buff.append(curr_y_cl)

        fig_pid = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Đáp ứng Đầu ra y(t) [đơn vị]", "Tín hiệu Điều khiển Van u(t) [%]"), vertical_spacing=0.1)
        fig_pid.add_trace(go.Scatter(x=t_pid, y=y_closed, name="Vòng kín PID (Closed Loop) [đơn vị]", line=dict(color="#1f77b4", width=2.5)), row=1, col=1)
        fig_pid.add_trace(go.Scatter(x=t_pid, y=y_open, name="Vòng hở (Open Loop) [đơn vị]", line=dict(color="orange", dash="dash")), row=1, col=1)
        fig_pid.add_trace(go.Scatter(x=t_pid, y=np.ones_like(t_pid), name="Tín hiệu đặt SP=1.0 [đơn vị]", line=dict(color="red", dash="dot")), row=1, col=1)
        fig_pid.add_trace(go.Scatter(x=t_pid, y=u_ctrl, name="Tín hiệu Van u(t) [%]", line=dict(color="green")), row=2, col=1)
        
        fig_pid.update_xaxes(title_text="Thời gian t [s]", row=2, col=1)
        fig_pid.update_yaxes(title_text="Biên độ y(t) [đơn vị]", row=1, col=1)
        fig_pid.update_yaxes(title_text="Độ mở van [%]", row=2, col=1)
        fig_pid.update_layout(height=500, hovermode="x unified")
        st.plotly_chart(fig_pid, use_container_width=True)
