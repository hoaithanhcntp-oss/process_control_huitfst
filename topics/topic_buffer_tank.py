import streamlit as st
import numpy as np
import plotly.graph_objects as go

def render():
    st.subheader("4. Bồn đệm mức nước quả / Dịch chiết")
    
    with st.expander("📖 **Nguyên lý cân bằng vật chất & Điều khiển mức dịch bồn chứa**", expanded=True):
        c_bt1, c_bt2 = st.columns([1.2, 1])
        with c_bt1:
            st.markdown("""
            * **Phương trình vi phân cân bằng thể tích:**
              $$A \\frac{dh(t)}{dt} = q_{in}(t) - q_{out}(t)$$
            * **Dòng tháo tự do phi tuyến (Định luật Torricelli):** $q_{out}(t) = C_v \\sqrt{h(t)}$.
            * **Tuyến tính hóa quanh điểm làm việc $(h_0, q_0)$:**
              $$G(s) = \\frac{H(s)}{Q_{in}(s)} = \\frac{R}{ARs + 1} \\quad \\text{với } R = \\frac{2\\sqrt{h_0}}{C_v}$$
            """)
        with c_bt2:
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 10px; border-radius: 8px; border: 1px solid #dee2e6; text-align: center;">
                <h5 style="margin-top:0; color:#333;">Sơ Đồ P&ID Bồn Đệm Mức</h5>
                <svg width="100%" height="170" viewBox="0 0 320 170" xmlns="http://www.w3.org/2000/svg">
                    <rect x="80" y="40" width="120" height="90" rx="4" fill="#e1f5fe" stroke="#0288d1" stroke-width="2"/>
                    <rect x="82" y="75" width="116" height="53" fill="#81d4fa" opacity="0.6"/>
                    <text x="140" y="105" font-family="Arial" font-size="10" font-weight="bold" fill="#01579b" text-anchor="middle">Mức dịch h(t)</text>
                    
                    <!-- Inflow pump -->
                    <line x1="20" y1="25" x2="140" y2="25" stroke="#0288d1" stroke-width="2"/>
                    <line x1="140" y1="25" x2="140" y2="40" stroke="#0288d1" stroke-width="2" marker-end="url(#arr_bt)"/>
                    <text x="50" y="18" font-family="Arial" font-size="10" fill="#0288d1">Dòng vào q_in</text>
                    
                    <!-- Outflow valve -->
                    <line x1="200" y1="115" x2="280" y2="115" stroke="#0288d1" stroke-width="2" marker-end="url(#arr_bt)"/>
                    <text x="250" y="105" font-family="Arial" font-size="10" fill="#0288d1">q_out</text>
                    
                    <defs>
                        <marker id="arr_bt" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                            <path d="M 0 1 L 10 5 L 0 9 z" fill="#0288d1"/>
                        </marker>
                    </defs>
                </svg>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

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
