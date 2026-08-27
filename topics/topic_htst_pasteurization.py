import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def render():
    st.subheader("2. Thanh trùng sữa HTST dạng tấm (Plate Heat Exchanger)")
    
    with st.expander("📖 Sơ đồ Công nghệ & Đơn vị Thanh trùng (PU)", expanded=True):
        st.markdown("""
        ```
        Sữa nguyên liệu          ┌──────────────┐   Sữa nóng   ┌──────────────┐       Cảm biến TT [°C]
        (T_in: 4-10 °C) ───────> │  PHE Gia nhiệt│ ──────────> │ Ống lưu nhiệt│ ──────> ┌─────────────┐
                                 └──────┬───────┘   (Trễ θ: s) └──────────────┘         │ Van FDV 3 ngả│──> Sữa đạt chuẩn
                                        ▲                                               └──────┬──────┘
                                  Hơi cấp (Van MV: %)                                          │ (T < 72°C)
                                                                                               ▼ Hồi lưu
        ```
        * **Đơn vị thanh trùng (Pasteurization Units - PU):** $PU = \\int_{0}^{t} 10^{\\frac{T(t) - 60}{z}} \\frac{dt}{60}$ (với $z = 10^\\circ\\text{C}$, $1\\text{ PU} = 1\\text{ phút ở } 60^\\circ\\text{C}$).
        * **Van chuyển hướng dòng (Flow Diversion Valve - FDV):** Nếu nhiệt độ đầu ra $T(t) < 72^\\circ\\text{C}$, van tự động chuyển về bồn hồi lưu (Divert) để ngăn chặn sữa chưa tiệt khuẩn lọt ra thành phẩm.
        """)

    col_f1, col_f2 = st.columns([1, 2])
    with col_f1:
        sp_milk = st.slider("Nhiệt độ đặt SP [°C]:", 65.0, 85.0, 75.0, 0.5)
        tin_milk = st.slider("Nhiệt độ sữa đầu vào T_in [°C]:", 4.0, 20.0, 8.0, 1.0)
        hold_delay = st.slider("Thời gian trễ ống lưu nhiệt θ [s]:", 1.0, 15.0, 6.0, 0.5)
        kp_htst = st.slider("Kp [-]:", 0.0, 10.0, 3.0, 0.2, key="kp_h")
        ki_htst = st.slider("Ki [s⁻¹]:", 0.0, 2.0, 0.25, 0.02, key="ki_h")
        kd_htst = st.slider("Kd [s]:", 0.0, 5.0, 0.6, 0.05, key="kd_h")
        
    with col_f2:
        dt_htst = 0.1
        t_htst = np.arange(0, 120.0, dt_htst)
        n_h = len(t_htst)
        buf_h = [tin_milk] * max(1, int(hold_delay/dt_htst))
        pv_milk = np.zeros(n_h)
        pu_val = np.zeros(n_h)
        pv_milk[0] = tin_milk
        int_m, prev_em, curr_tm = 0.0, 0.0, tin_milk
        
        for i in range(1, n_h):
            meas_tm = buf_h.pop(0)
            e_m = sp_milk - meas_tm
            int_m += e_m * dt_htst
            der_m = (e_m - prev_em) / dt_htst
            prev_em = e_m
            u_steam = np.clip(kp_htst * e_m + ki_htst * int_m + kd_htst * der_m, 0.0, 100.0)
            dt_temp = ((0.85 * u_steam + tin_milk) - curr_tm) / 7.0
            curr_tm += dt_temp * dt_htst
            pv_milk[i] = curr_tm
            buf_h.append(curr_tm)
            rate_pu = 10.0 ** ((meas_tm - 60.0) / 10.0) if meas_tm >= 60.0 else 0.0
            pu_val[i] = pu_val[i-1] + (rate_pu * dt_htst / 60.0)
            
        fig_htst = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Nhiệt độ Sữa [°C] & Ngưỡng An toàn FDV (72°C)", "Đơn vị Thanh trùng Tích lũy (PU) [PU]"))
        fig_htst.add_trace(go.Scatter(x=t_htst, y=pv_milk, name="Nhiệt độ sữa PV [°C]", line=dict(color="blue", width=2)), row=1, col=1)
        fig_htst.add_trace(go.Scatter(x=t_htst, y=np.ones_like(t_htst)*sp_milk, name="Nhiệt độ đặt SP [°C]", line=dict(color="green", dash="dash")), row=1, col=1)
        fig_htst.add_trace(go.Scatter(x=t_htst, y=np.ones_like(t_htst)*72.0, name="Ngưỡng an toàn FDV 72°C [°C]", line=dict(color="red", dash="dot")), row=1, col=1)
        
        fig_htst.add_trace(go.Scatter(x=t_htst, y=pu_val, name="Đơn vị thanh trùng tích lũy [PU]", line=dict(color="green", width=2)), row=2, col=1)
        fig_htst.update_xaxes(title_text="Thời gian t [s]", row=2, col=1)
        fig_htst.update_yaxes(title_text="Nhiệt độ [°C]", row=1, col=1)
        fig_htst.update_yaxes(title_text="Đơn vị PU [PU]", row=2, col=1)
        fig_htst.update_layout(height=480, hovermode="x unified")
        st.plotly_chart(fig_htst, use_container_width=True)
