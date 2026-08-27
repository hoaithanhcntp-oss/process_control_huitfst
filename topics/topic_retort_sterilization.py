import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def render():
    st.subheader("3. Nồi tiệt trùng đồ hộp Retort (Sterilization Retort)")
    
    with st.expander("📖 **Nguyên lý nhiệt tiệt trùng đồ hộp & Tính toán giá trị F0**", expanded=True):
        c_rt1, c_rt2 = st.columns([1.2, 1])
        with c_rt1:
            st.markdown("""
            * **Quá trình truyền nhiệt vào tâm đồ hộp:** Nhiệt từ hơi trong buồng nồi hấp truyền qua vỏ hộp kim loại rồi đi vào tâm hình học (Cold Point) theo cơ chế dẫn nhiệt/đối lưu. Quá trình này có quán tính nhiệt lớn (hệ bậc 2 nối tiếp $\\tau_1, \\tau_2$).
            * **Giá trị tiệt trùng công nghiệp ($F_0$ Value):**
              $$F_0 = \\int_{0}^{t} 10^{\\frac{T_{core}(t) - 121.1}{z}} dt \\quad (\\text{chuẩn } z = 10^\\circ\\text{C})$$
            * **Tiêu chuẩn an toàn:** Đối với đồ hộp ít chua ($pH > 4.5$), $F_0$ bắt buộc phải đạt tối thiểu từ **$3.0 - 6.0\\text{ phút}$** để tiêu diệt $12D$ bào tử *Clostridium botulinum*.
            """)
        with c_rt2:
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 10px; border-radius: 8px; border: 1px solid #dee2e6; text-align: center;">
                <h5 style="margin-top:0; color:#333;">Mô Hình Truyền Nhiệt Nồi Hấp Retort</h5>
                <svg width="100%" height="180" viewBox="0 0 340 180" xmlns="http://www.w3.org/2000/svg">
                    <!-- Retort Autoclave shell -->
                    <rect x="25" y="25" width="290" height="135" rx="20" fill="#eceff1" stroke="#455a64" stroke-width="2.5"/>
                    <text x="170" y="45" font-family="Arial" font-size="11" font-weight="bold" fill="#37474f" text-anchor="middle">Buồng Tiệt Trùng Retort (121.1°C)</text>
                    
                    <!-- Can inside -->
                    <rect x="130" y="65" width="80" height="75" rx="6" fill="#ffe082" stroke="#ff8f00" stroke-width="2"/>
                    <text x="170" y="95" font-family="Arial" font-size="10" font-weight="bold" fill="#e65100" text-anchor="middle">Đồ Hộp</text>
                    
                    <!-- Thermocouple probe -->
                    <circle cx="170" cy="115" r="5" fill="#d32f2f"/>
                    <text x="170" y="130" font-family="Arial" font-size="8" font-weight="bold" fill="#d32f2f" text-anchor="middle">Tâm hộp</text>
                    
                    <!-- Steam entry -->
                    <line x1="70" y1="5" x2="70" y2="25" stroke="#d32f2f" stroke-width="3" marker-end="url(#arr_rt)"/>
                    <text x="70" y="18" font-family="Arial" font-size="9" fill="#d32f2f" text-anchor="middle">Hơi Steam</text>
                    
                    <defs>
                        <marker id="arr_rt" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                            <path d="M 0 1 L 10 5 L 0 9 z" fill="#d32f2f"/>
                        </marker>
                    </defs>
                </svg>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    t_ret = np.arange(0, 300.0, 0.2)
    n_r = len(t_ret)
    t_vessel = np.zeros(n_r)
    t_can = np.zeros(n_r)
    t_vessel[0], t_can[0] = 30.0, 30.0
    f0_val = np.zeros(n_r)
    curr_v, curr_c, int_r, prev_er = 30.0, 30.0, 0.0, 0.0
    
    for i in range(1, n_r):
        er = 121.1 - curr_v
        int_r += er * 0.2
        der_r = (er - prev_er) / 0.2
        prev_er = er
        u_r = np.clip(3.5 * er + 0.15 * int_r + 1.0 * der_r, 0.0, 100.0)
        curr_v += (((0.95 * u_r + 30.0) - curr_v) / 18.0) * 0.2
        curr_c += ((curr_v - curr_c) / 40.0) * 0.2
        t_vessel[i] = curr_v
        t_can[i] = curr_c
        l_rate = 10.0 ** ((curr_c - 121.1) / 10.0) if curr_c >= 100.0 else 0.0
        f0_val[i] = f0_val[i-1] + (l_rate * 0.2 / 60.0)
        
    fig_r = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Nhiệt độ Nồi và Tâm Đồ hộp (°C)", "Giá trị Tiệt trùng F0 (phút)"))
    fig_r.add_trace(go.Scatter(x=t_ret, y=t_vessel, name="Nhiệt độ buồng hấp", line=dict(color="orange")), row=1, col=1)
    fig_r.add_trace(go.Scatter(x=t_ret, y=t_can, name="Nhiệt độ tâm hộp", line=dict(color="crimson", width=2.5)), row=1, col=1)
    fig_r.add_trace(go.Scatter(x=t_ret, y=np.ones_like(t_ret)*121.1, name="Chuẩn 121.1°C", line=dict(color="black", dash="dash")), row=1, col=1)
    fig_r.add_trace(go.Scatter(x=t_ret, y=f0_val, name="F0 (min)", line=dict(color="purple", width=2)), row=2, col=1)
    fig_r.add_trace(go.Scatter(x=t_ret, y=np.ones_like(t_ret)*3.0, name="F0 tối thiểu (3.0 min)", line=dict(color="red", dash="dot")), row=2, col=1)
    fig_r.update_layout(height=480, hovermode="x unified")
    st.plotly_chart(fig_r, use_container_width=True)
