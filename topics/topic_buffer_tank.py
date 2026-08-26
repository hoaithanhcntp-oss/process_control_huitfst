import streamlit as st
import numpy as np
import plotly.graph_objects as go

def render():
    st.subheader("4. Bồn đệm mức nước quả / Dịch chiết")
    t_b = np.arange(0, 100.0, 0.1)
    n_b = len(t_b)
    lvl = np.zeros(n_b)
    lvl[0] = 0.5
    sp_l = 2.5
    int_l, prev_el, curr_l = 0.0, 0.0, 0.5
    
    for i in range(1, n_b):
        el = sp_l - curr_l
        int_l += el * 0.1
        der_l = (el - prev_el) / 0.1
        prev_el = el
        q_in = np.clip(1.5 * el + 0.2 * int_l + 0.4 * der_l, 0.0, 0.3)
        q_out = 0.08 * np.sqrt(max(0.0, curr_l))
        curr_l += ((q_in - q_out) / 2.0) * 0.1
        lvl[i] = max(0.0, curr_l)
        
    fig_b = go.Figure()
    fig_b.add_trace(go.Scatter(x=t_b, y=lvl, name="Mức dịch h(t)", line=dict(color="#1f77b4", width=2.5)))
    fig_b.add_trace(go.Scatter(x=t_b, y=np.ones_like(t_b)*sp_l, name="Mức đặt SP", line=dict(color="red", dash="dash")))
    fig_b.update_layout(xaxis_title="Thời gian (s)", yaxis_title="Mức chất lỏng (m)", height=400)
    st.plotly_chart(fig_b, use_container_width=True)
