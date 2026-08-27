import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def render():
    st.subheader("1. Điều khiển Phản hồi + Truyền thẳng (Feedback + Feedforward)")
    
    with st.expander("📖 **Nguyên lý Điều khiển Truyền thẳng (Feedforward Control Principle)**", expanded=True):
        c_ff1, c_ff2 = st.columns([1.2, 1])
        with c_ff1:
            st.markdown("""
            * **Nhược điểm của Feedback thuần túy:** Phải chờ đến khi nhiễu $DV$ đã làm biến quá trình $PV$ lệch khỏi $SP$, sai số $e(t)$ xuất hiện thì bộ điều khiển mới bắt đầu can thiệp.
            * **Nguyên lý Feedforward:** Đo trực tiếp giá trị nhiễu tải $DV$ (ví dụ: nhiệt độ sữa nguyên liệu đầu vào hoặc lưu lượng dòng cấp) ngay khi nó vừa phát sinh, và tính toán trước lượng điều chỉnh van $\\Delta u_{ff}$ để **bù trừ và triệt tiêu ảnh hưởng của nhiễu trước khi nó làm thay đổi $PV$**.
            * **Hàm truyền bộ bù lý tưởng:**
              $$G_{ff}(s) = -\\frac{G_d(s)}{G_p(s)}$$
            * **Tín hiệu điều khiển tổng hợp:** $u(t) = u_{feedback}(t) + u_{feedforward}(t)$.
            """)
        with c_ff2:
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 10px; border-radius: 8px; border: 1px solid #dee2e6; text-align: center;">
                <h5 style="margin-top:0; color:#333;">Sơ Đồ Phản Hồi Kết Hợp Truyền Thẳng</h5>
                <svg width="100%" height="180" viewBox="0 0 380 180" xmlns="http://www.w3.org/2000/svg">
                    <line x1="20" y1="25" x2="110" y2="25" stroke="#e65100" stroke-width="2" marker-end="url(#arr_ff)"/>
                    <text x="25" y="18" font-family="Arial" font-size="11" font-weight="bold" fill="#e65100">Nhiễu DV d(t)</text>
                    
                    <!-- Feedforward Controller -->
                    <rect x="110" y="8" width="90" height="34" rx="4" fill="#fff3e0" stroke="#f57c00" stroke-width="1.5"/>
                    <text x="155" y="30" font-family="Arial" font-size="11" font-weight="bold" fill="#e65100" text-anchor="middle">Gff(s)</text>
                    
                    <!-- Summing junction for MV -->
                    <circle cx="250" cy="90" r="12" fill="#fff" stroke="#333" stroke-width="1.5"/>
                    <text x="250" y="94" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle">Σ</text>
                    
                    <line x1="200" y1="25" x2="250" y2="25" stroke="#e65100" stroke-width="2"/>
                    <line x1="250" y1="25" x2="250" y2="78" stroke="#e65100" stroke-width="2" marker-end="url(#arr_ff)"/>
                    <text x="255" y="45" font-family="Arial" font-size="10" fill="#e65100">uff(t)</text>
                    
                    <!-- Feedback loop -->
                    <line x1="20" y1="90" x2="65" y2="90" stroke="#333" stroke-width="1.5" marker-end="url(#arr_ff)"/>
                    <text x="25" y="82" font-family="Arial" font-size="10">SP</text>
                    
                    <circle cx="75" cy="90" r="10" fill="#fff" stroke="#333" stroke-width="1.5"/>
                    <text x="75" y="94" font-family="Arial" font-size="12" text-anchor="middle">Σ</text>
                    
                    <line x1="85" y1="90" x2="110" y2="90" stroke="#333" stroke-width="1.5" marker-end="url(#arr_ff)"/>
                    <rect x="110" y="73" width="90" height="34" rx="4" fill="#e3f2fd" stroke="#1976d2" stroke-width="1.5"/>
                    <text x="155" y="95" font-family="Arial" font-size="11" font-weight="bold" fill="#0d47a1" text-anchor="middle">PID FB</text>
                    
                    <line x1="200" y1="90" x2="238" y2="90" stroke="#333" stroke-width="1.5" marker-end="url(#arr_ff)"/>
                    <text x="215" y="82" font-family="Arial" font-size="10">ufb(t)</text>
                    
                    <!-- Plant -->
                    <line x1="262" y1="90" x2="290" y2="90" stroke="#333" stroke-width="1.5" marker-end="url(#arr_ff)"/>
                    <rect x="290" y="73" width="75" height="34" rx="4" fill="#e8f5e9" stroke="#388e3c" stroke-width="1.5"/>
                    <text x="327" y="95" font-family="Arial" font-size="11" font-weight="bold" fill="#1b5e20" text-anchor="middle">Gp(s)</text>
                    
                    <line x1="365" y1="90" x2="380" y2="90" stroke="#333" stroke-width="1.5"/>
                    
                    <!-- Feedback line -->
                    <line x1="375" y1="90" x2="375" y2="150" stroke="#333" stroke-width="1.5"/>
                    <line x1="375" y1="150" x2="75" y2="150" stroke="#333" stroke-width="1.5"/>
                    <line x1="75" y1="150" x2="75" y2="100" stroke="#333" stroke-width="1.5" marker-end="url(#arr_ff)"/>
                    
                    <defs>
                        <marker id="arr_ff" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                            <path d="M 0 1 L 10 5 L 0 9 z" fill="#333"/>
                        </marker>
                    </defs>
                </svg>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

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
        fig_pc.update_layout(height=480, hovermode="x unified")
        st.plotly_chart(fig_pc, use_container_width=True)
