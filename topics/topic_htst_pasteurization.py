import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def render():
    st.subheader("2. Thanh trùng sữa HTST dạng tấm (Plate Heat Exchanger)")
    
    with st.expander("📖 **Nguyên lý công nghệ thanh trùng HTST & Van an toàn FDV**", expanded=True):
        c_ht1, c_ht2 = st.columns([1.2, 1])
        with c_ht1:
            st.markdown("""
            * **Công nghệ HTST (High Temperature Short Time):** Sữa được gia nhiệt nhanh đến $72^\circ\text{C} - 75^\circ\text{C}$ và duy trì trong tối thiểu **15 giây** ở ống lưu nhiệt (Holding Tube) để vô hoạt vi sinh vật gây bệnh mà vẫn bảo toàn dinh dưỡng.
            * **Van chuyển hướng dòng (FDV - Flow Diversion Valve):**
              * Nếu nhiệt độ đầu ra ống giữ nhiệt $\ge 72^\circ\text{C}$: Van mở hướng **Forward Flow** (đưa sữa đi làm nguội và đóng gói).
              * Nếu $T < 72^\circ\text{C}$: Van tự động chuyển sang chế độ **Divert Flow** (hồi lưu sữa về bồn đệm nguyên liệu để tái xử lý).
            * **Đơn vị thanh trùng (PU - Pasteurization Units):**
              $$PU = \int_{0}^{t} 10^{\frac{T(t) - 60}{z}} dt \quad (\text{với } z = 10^\circ\text{C})$$
            """)
        with c_ht2:
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 10px; border-radius: 8px; border: 1px solid #dee2e6; text-align: center;">
                <h5 style="margin-top:0; color:#333;">Sơ Đồ P&ID Hệ Thống HTST</h5>
                <svg width="100%" height="180" viewBox="0 0 380 180" xmlns="http://www.w3.org/2000/svg">
                    <!-- Feed tank -->
                    <rect x="15" y="70" width="45" height="60" rx="4" fill="#e0f7fa" stroke="#00838f" stroke-width="2"/>
                    <text x="37" y="105" font-family="Arial" font-size="9" font-weight="bold" fill="#006064" text-anchor="middle">Bồn Đệm</text>
                    
                    <!-- PHE Heat Exchanger -->
                    <rect x="105" y="55" width="80" height="90" rx="4" fill="#fff9c4" stroke="#fbc02d" stroke-width="2"/>
                    <text x="145" y="105" font-family="Arial" font-size="11" font-weight="bold" fill="#f57f17" text-anchor="middle">PHE (Gia nhiệt)</text>
                    
                    <!-- Steam Valve -->
                    <line x1="145" y1="15" x2="145" y2="55" stroke="#d32f2f" stroke-width="2" marker-end="url(#arr_ht)"/>
                    <text x="175" y="32" font-family="Arial" font-size="10" fill="#d32f2f">Hơi nóng</text>
                    
                    <!-- Holding Tube -->
                    <path d="M 185 85 L 250 85 L 250 115 L 290 115" fill="none" stroke="#0288d1" stroke-width="3"/>
                    <text x="240" y="75" font-family="Arial" font-size="10" fill="#0277bd">Ống giữ nhiệt (θ)</text>
                    
                    <!-- TT Sensor -->
                    <circle cx="290" cy="115" r="10" fill="#e1f5fe" stroke="#0288d1" stroke-width="1.5"/>
                    <text x="290" y="119" font-family="Arial" font-size="9" font-weight="bold" fill="#01579b" text-anchor="middle">TT</text>
                    
                    <!-- FDV Valve -->
                    <polygon points="325,105 345,115 325,125" fill="#ab47bc" stroke="#6a1b9a" stroke-width="1.5"/>
                    <polygon points="365,105 345,115 365,125" fill="#ab47bc" stroke="#6a1b9a" stroke-width="1.5"/>
                    <text x="345" y="98" font-family="Arial" font-size="10" font-weight="bold" fill="#6a1b9a" text-anchor="middle">FDV</text>
                    
                    <!-- Divert line back -->
                    <path d="M 345 125 L 345 160 L 37 160 L 37 130" fill="none" stroke="#c2185b" stroke-width="1.5" stroke-dasharray="3" marker-end="url(#arr_ht)"/>
                    <text x="180" y="155" font-family="Arial" font-size="9" fill="#c2185b" text-anchor="middle">Đường hồi lưu (T < 72°C)</text>
                    
                    <defs>
                        <marker id="arr_ht" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                            <path d="M 0 1 L 10 5 L 0 9 z" fill="#333"/>
                        </marker>
                    </defs>
                </svg>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    col_f1, col_f2 = st.columns([1, 2])
    with col_f1:
        sp_milk = st.slider("Nhiệt độ đặt SP (°C):", 65.0, 85.0, 75.0, 0.5)
        tin_milk = st.slider("Nhiệt độ sữa vào (°C):", 4.0, 20.0, 8.0, 1.0)
        hold_delay = st.slider("Trễ ống lưu nhiệt (s):", 1.0, 15.0, 6.0, 0.5)
        kp_htst = st.slider("Kp:", 0.0, 10.0, 3.0, 0.2, key="kp_h")
        ki_htst = st.slider("Ki:", 0.0, 2.0, 0.25, 0.02, key="ki_h")
        kd_htst = st.slider("Kd:", 0.0, 5.0, 0.6, 0.05, key="kd_h")
        
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
            
        fig_htst = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Nhiệt độ Sữa & Ngưỡng Van Đảo Dòng FDV (72°C)", "Đơn vị Thanh trùng Tích lũy (PU)"))
        fig_htst.add_trace(go.Scatter(x=t_htst, y=pv_milk, name="Nhiệt độ sữa (°C)", line=dict(color="blue", width=2)), row=1, col=1)
        fig_htst.add_trace(go.Scatter(x=t_htst, y=np.ones_like(t_htst)*sp_milk, name="SP", line=dict(color="green", dash="dash")), row=1, col=1)
        fig_htst.add_trace(go.Scatter(x=t_htst, y=np.ones_like(t_htst)*72.0, name="Ngưỡng FDV (72°C)", line=dict(color="red", dash="dot")), row=1, col=1)
        fig_htst.add_trace(go.Scatter(x=t_htst, y=pu_val, name="PU tích lũy", line=dict(color="green", width=2)), row=2, col=1)
        fig_htst.update_layout(height=480, hovermode="x unified")
        st.plotly_chart(fig_htst, use_container_width=True)
