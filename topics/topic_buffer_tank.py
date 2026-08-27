import streamlit as st
import numpy as np
import plotly.graph_objects as go

def render():
    st.subheader("4. Bồn đệm mức nước quả / Dịch chiết")
    
    # ---------------------------------------------------------
    # PHẦN 1: MÔ PHỎNG & ĐỒ THỊ TƯƠNG TÁC (ĐẶT Ở TRÊN)
    # ---------------------------------------------------------
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
    fig_b.update_layout(xaxis_title="Thời gian t (s)", yaxis_title="Mức chất lỏng h (m)", height=400, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_b, use_container_width=True)

    # ---------------------------------------------------------
    # PHẦN 2: LÝ THUYẾT & NGUYÊN LÝ (ĐƯA XUỐNG DƯỚI CÙNG)
    # ---------------------------------------------------------
    st.divider()
    with st.expander("📖 Nguyên Lý Cân Bằng Vật Chất & Điều Khiển Mức Bồn Đệm", expanded=True):
        col_tk1, col_tk2 = st.columns(2)
        with col_tk1:
            st.markdown("### 🔹 Sơ đồ P&ID bồn chứa chất lỏng")
            st.graphviz_chart('''
            digraph BufferTank {
                rankdir=TD;
                node [shape=box, style="filled,rounded", fillcolor="#e1f5fe", fontname="Helvetica"];
                Qin [label="Lưu lượng cấp vào q_in(t)\n(Bơm điều khiển)"];
                Tank [label="Bồn đệm tiết diện A\nMức chất lỏng h(t)"];
                Qout [label="Lưu lượng xả đáy q_out(t)\nq_out = Cv * sqrt(h)"];
                
                Qin -> Tank -> Qout;
            }
            ''')
        with col_tk2:
            st.markdown("### 🔹 Phương trình vi phân & Tuyến tính hóa")
            st.latex(r"A \frac{dh(t)}{dt} = q_{in}(t) - q_{out}(t)")
            st.latex(r"q_{out}(t) = C_v \sqrt{h(t)}")
            st.markdown("""
            * **Tính phi tuyến:** Dòng xả qua van đáy tỷ lệ với căn bậc hai của mức dịch $\\sqrt{h}$.
            * **Hàm truyền xấp xỉ bậc 1:** Tuyến tính hóa quanh điểm làm việc $h_0$ cho ta:
            """)
            st.latex(r"G(s) = \frac{H(s)}{Q_{in}(s)} = \frac{R}{ARs + 1} \quad \left(R = \frac{2\sqrt{h_0}}{C_v}\right)")
