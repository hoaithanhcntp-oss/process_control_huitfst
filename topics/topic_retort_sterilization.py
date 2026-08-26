import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def render():
    st.subheader("3. Nồi tiệt trùng đồ hộp Retort (Sterilization Retort)")
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
