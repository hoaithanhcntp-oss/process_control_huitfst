import streamlit as st
import numpy as np
import plotly.graph_objects as go

def render():
    st.subheader("4. Bồn đệm mức nước quả / Dịch chiết (Buffer Tank Level)")
    
    with st.expander("📖 Phương trình Cân bằng Vật chất & Định luật Xả đáy", expanded=True):
        st.markdown("""
        * **Phương trình vi phân cân bằng khối lượng:** $A \\frac{dh(t)}{dt} = q_{in}(t) - q_{out}(t)$
          * $h(t)$ [m]: Mức chất lỏng trong bồn.
          * $A$ [m²]: Diện tích mặt cắt ngang đáy bồn.
          * $q_{in}(t)$ [m³/s]: Lưu lượng cấp từ bơm (biến thao tác $MV$).
          * $q_{out}(t) = C_v \\sqrt{h(t)}$ [m³/s]: Dòng xả đáy tự do theo định luật Torricelli.
        """)

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
    fig_b.add_trace(go.Scatter(x=t_b, y=lvl, name="Mức dịch thực tế h(t) [m]", line=dict(color="#1f77b4", width=2.5)))
    fig_b.add_trace(go.Scatter(x=t_b, y=np.ones_like(t_b)*sp_l, name="Mức đặt SP [m]", line=dict(color="red", dash="dash")))
    fig_b.update_layout(
        title="Đáp ứng Mức Chất lỏng trong Bồn đệm theo Thời gian",
        xaxis_title="Thời gian t [s]",
        yaxis_title="Mức chất lỏng h [m]",
        height=400,
        hovermode="x unified"
    )
    st.plotly_chart(fig_b, use_container_width=True)
