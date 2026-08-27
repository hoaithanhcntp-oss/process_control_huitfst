import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def render():
    st.subheader("1. Điều khiển Phản hồi + Truyền thẳng (Feedback + Feedforward)")
    
    # ---------------------------------------------------------
    # PHẦN 1: MÔ PHỎNG & ĐỒ THỊ TƯƠNG TÁC (ĐẶT Ở TRÊN)
    # ---------------------------------------------------------
    col_pc1, col_pc2 = st.columns([1, 2])
    with col_pc1:
        st.markdown("**Cấu hình Vòng điều khiển P&ID**")
        sp_val = st.slider("Giá trị đặt SP (°C):", 50.0, 90.0, 75.0, 1.0)
        dist_mag = st.slider("Nhiễu tải DV (°C):", -15.0, 15.0, -8.0, 1.0)
        dist_step_time = st.slider("Thời điểm xảy ra nhiễu (s):", 10, 80, 40)
        enable_ff = st.checkbox("Kích hoạt Bù truyền thẳng (Feedforward)", value=True)
        kp_fb = st.slider("Kp (Phản hồi):", 0.1, 10.0, 2.5, 0.1)
        ki_fb = st.slider("Ki (Phản hồi):", 0.0, 2.0, 0.3, 0.05)
        k_ff = st.slider("Hệ số K_ff:", 0.0, 2.0, 1.0, 0.1) if enable_ff else 0.0
        
    with col_pc2:
        dt = 0.1
        t_pc = np.arange(0, 120.0, dt)
        n_pc = len(t_pc)
        pv_fb_only = np.zeros(n_pc)
        pv_fb_ff = np.zeros(n_pc)
        mv_fb_only = np.zeros(n_pc)
        mv_fb_ff = np.zeros(n_pc)
        
        for mode, pv_arr, mv_arr in [("FB_ONLY", pv_fb_only, mv_fb_only), ("FB_FF", pv_fb_ff, mv_fb_ff)]:
            curr_pv, int_err = 25.0, 0.0
            for i in range(1, n_pc):
                t = t_pc[i]
                dv = dist_mag if t >= dist_step_time else 0.0
                err = sp_val - curr_pv
                int_err += err * dt
                u_fb = kp_fb * err + ki_fb * int_err
                u_ff = (-k_ff * dv) if (mode == "FB_FF" and enable_ff) else 0.0
                u_total = np.clip(u_fb + u_ff, 0.0, 100.0)
                mv_arr[i] = u_total
                dpv = (0.75 * u_total + dv + 25.0 - curr_pv) / 8.0
                curr_pv += dpv * dt
                pv_arr[i] = curr_pv
        
        fig_pc = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Biến quá trình PV (°C)", "Tín hiệu điều khiển Van MV (%)"), vertical_spacing=0.1)
        fig_pc.add_trace(go.Scatter(x=t_pc, y=pv_fb_only, name="Chỉ dùng Feedback (PID)", line=dict(color="orange", dash="dash")), row=1, col=1)
        fig_pc.add_trace(go.Scatter(x=t_pc, y=pv_fb_ff, name="Kết hợp Feedback + Feedforward", line=dict(color="#1f77b4", width=2.5)), row=1, col=1)
        fig_pc.add_trace(go.Scatter(x=t_pc, y=np.ones_like(t_pc)*sp_val, name="Giá trị đặt SP", line=dict(color="green", dash="dot")), row=1, col=1)
        fig_pc.add_trace(go.Scatter(x=t_pc, y=mv_fb_only, name="MV (Chỉ Feedback)", line=dict(color="orange", dash="dash")), row=2, col=1)
        fig_pc.add_trace(go.Scatter(x=t_pc, y=mv_fb_ff, name="MV (Feedback + Feedforward)", line=dict(color="#1f77b4")), row=2, col=1)
        fig_pc.update_layout(height=450, hovermode="x unified", margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_pc, use_container_width=True)

    # ---------------------------------------------------------
    # PHẦN 2: LÝ THUYẾT & NGUYÊN LÝ (ĐƯA XUỐNG DƯỚI CÙNG)
    # ---------------------------------------------------------
    st.divider()
    with st.expander("📖 Nguyên Lý Điều Khiển Phản Hồi Kết Hợp Bù Truyền Thẳng", expanded=True):
        col_ff1, col_ff2 = st.columns(2)
        with col_ff1:
            st.markdown("### 🔹 Sơ đồ khối cấu trúc Feedforward + Feedback")
            st.graphviz_chart('''
            digraph FF_Control {
                rankdir=LR;
                node [shape=box, style="filled,rounded", fillcolor="#fff3e0", fontname="Helvetica"];
                D [shape=plaintext, label="Nhiễu tải D(s)"];
                R [shape=plaintext, label="SP r(s)"];
                Sum1 [shape=circle, label="+ / -"];
                Sum2 [shape=circle, label="+"];
                FB [label="Bộ phản hồi\nGfb(s)"];
                FF [label="Bộ truyền thẳng\nGff(s) = -Gd/Gp"];
                Plant [label="Đối tượng\nGp(s)"];
                DistPlant [label="Hàm truyền nhiễu\nGd(s)"];
                SumOut [shape=circle, label="+"];
                Y [shape=plaintext, label="PV y(s)"];
                
                D -> FF;
                D -> DistPlant;
                R -> Sum1;
                Sum1 -> FB;
                FB -> Sum2;
                FF -> Sum2;
                Sum2 -> Plant;
                Plant -> SumOut;
                DistPlant -> SumOut;
                SumOut -> Y;
                Y -> Sum1 [label="hồi tiếp"];
            }
            ''')
            
        with col_ff2:
            st.markdown("### 🔹 Công thức toán học & Cơ chế bù nhiễu")
            st.latex(r"Y(s) = G_p(s) U(s) + G_d(s) D(s)")
            st.latex(r"U(s) = G_{fb}(s) E(s) + G_{ff}(s) D(s)")
            st.latex(r"G_{ff}(s) = -\frac{G_d(s)}{G_p(s)}")
            st.markdown("""
            * **Hạn chế của Feedback:** Chỉ hành động sau khi biến quá trình $PV$ đã bị lệch khỏi $SP$.
            * **Ưu điểm của Feedforward:** Đo lường biến nhiễu $DV$ (ví dụ: nhiệt độ nguyên liệu lạnh đột ngột) và điều chỉnh van hơi tức thì trước khi nhiệt độ bồn bị giảm.
            """)
