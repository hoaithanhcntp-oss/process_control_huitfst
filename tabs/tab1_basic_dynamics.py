import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy import signal
from utils.control_utils import pade_approx

def render():
    st.header("1. Khảo Sát Các Khâu Động Học Điển Hình")
    
    # ---------------------------------------------------------
    # PHẦN 1: MÔ PHỎNG & ĐỒ THỊ TƯƠNG TÁC (ĐẶT Ở TRÊN)
    # ---------------------------------------------------------
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Cài đặt thông số khâu động học")
        model_type = st.radio("Chọn loại khâu động học:", ["Khâu bậc 1 có trễ (FOPDT)", "Khâu bậc 2 chuẩn"])
        
        if model_type == "Khâu bậc 1 có trễ (FOPDT)":
            k_fopdt = st.slider("Hệ số khuếch đại K:", 0.1, 5.0, 1.5, 0.1)
            tau_fopdt = st.slider("Hằng số thời gian τ (s):", 0.5, 10.0, 3.0, 0.5)
            theta_delay = st.slider("Thời gian trễ θ (s):", 0.0, 5.0, 1.0, 0.2)
            
            num_p, den_p = pade_approx(theta_delay, order=2)
            num_t1 = np.polymul([k_fopdt], num_p)
            den_t1 = np.polymul([tau_fopdt, 1.0], den_p)
        else:
            wn = st.slider("Tần số dao động riêng ωn (rad/s):", 0.5, 10.0, 2.5, 0.1)
            zeta = st.slider("Hệ số tắt dần ζ (damping ratio):", 0.0, 2.0, 0.4, 0.05)
            num_t1 = [wn**2]
            den_t1 = [1.0, 2.0 * zeta * wn, wn**2]

    with col2:
        st.subheader("Đồ thị đáp ứng bước nhảy (Step Response)")
        sys_t1 = signal.TransferFunction(num_t1, den_t1)
        t_span = np.linspace(0, 20, 500)
        t_out, y_step = signal.step(sys_t1, T=t_span)
        
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=t_out, y=y_step, mode='lines', name='Đáp ứng y(t)', line=dict(color='#1f77b4', width=2.5)))
        fig1.add_trace(go.Scatter(x=t_out, y=np.ones_like(t_out), mode='lines', name='Tín hiệu đặt r(t)=1', line=dict(color='red', dash='dash')))
        fig1.update_layout(xaxis_title="Thời gian t (s)", yaxis_title="Biên độ đầu ra y(t)", height=400, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig1, use_container_width=True)

    # ---------------------------------------------------------
    # PHẦN 2: LÝ THUYẾT & NGUYÊN LÝ (ĐƯA XUỐNG DƯỚI CÙNG)
    # ---------------------------------------------------------
    st.divider()
    with st.expander("📖 Cơ Sở Lý Thuyết, Sơ Đồ Khối & Công Thức Toán Học", expanded=True):
        col_th1, col_th2 = st.columns(2)
        with col_th1:
            st.markdown("### 🔹 Sơ đồ khối hệ thống")
            if model_type == "Khâu bậc 1 có trễ (FOPDT)":
                st.graphviz_chart('''
                digraph FOPDT {
                    rankdir=LR;
                    node [shape=box, style="filled,rounded", fillcolor="#e1f5fe", fontname="Helvetica"];
                    edge [fontname="Helvetica"];
                    R [shape=plaintext, label="Đầu vào u(t)"];
                    G1 [label="Khâu quán tính\nK / (τs + 1)"];
                    G2 [label="Khâu trễ\ne^(-θs)"];
                    Y [shape=plaintext, label="Đầu ra y(t)"];
                    R -> G1 -> G2 -> Y;
                }
                ''')
                st.latex(r"G(s) = \frac{K}{\tau s + 1} e^{-\theta s}")
                st.markdown(f"""
                * **Hệ số khuếch đại ($K = {k_fopdt}$):** Giá trị xác lập cuối cùng khi đầu vào là bước nhảy đơn vị ($y_{{ss}} = K$).
                * **Hằng số thời gian ($\tau = {tau_fopdt}\\text{{s}}$):** Thời gian để đáp ứng đạt $63.2\%$ giá trị xác lập.
                * **Thời gian trễ ($\theta = {theta_delay}\\text{{s}}$):** Khoảng thời gian chết (dead time) trước khi đầu ra bắt đầu phản ứng.
                """)
            else:
                st.graphviz_chart('''
                digraph SecondOrder {
                    rankdir=LR;
                    node [shape=box, style="filled,rounded", fillcolor="#f3e5f5", fontname="Helvetica"];
                    R [shape=plaintext, label="Đầu vào r(t)"];
                    G [label="Hệ bậc 2 chuẩn\nωn² / (s² + 2ζωn s + ωn²)"];
                    Y [shape=plaintext, label="Đầu ra y(t)"];
                    R -> G -> Y;
                }
                ''')
                st.latex(r"G(s) = \frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}")
                st.markdown(f"""
                * **Tần số tự nhiên ($\omega_n = {wn}\\text{{ rad/s}}$):** Đặc trưng cho tốc độ dao động của hệ thống.
                * **Hệ số tắt dần ($\zeta = {zeta}$):** Quyết định tính chất dao động của hệ thống:
                """)
                if zeta == 0:
                    st.warning("⚠️ **ζ = 0 (Undamped):** Cặp cực thuần ảo $s = \\pm j\\omega_n$, dao động điều hòa không bao giờ tắt.")
                elif 0 < zeta < 1:
                    st.info(f"ℹ️ **0 < ζ < 1 (Underdamped):** Cặp cực phức liên hợp, dao động tắt dần với độ vọt lố $\%OS = {100*np.exp(-zeta*np.pi/np.sqrt(1-zeta**2)):.1f}\\%$.")
                elif zeta == 1:
                    st.success("✅ **ζ = 1 (Critically Damped):** Cực kép thực âm, hệ về xác lập nhanh nhất mà không bị vọt lố.")
                else:
                    st.info("ℹ️ **ζ > 1 (Overdamped):** Hai cực thực âm phân biệt, đáp ứng chậm chạp và không vọt lố.")
                    
        with col_th2:
            st.markdown("### 🔹 Ý nghĩa trong điều khiển & vật lý")
            st.markdown("""
            1. **Khâu bậc nhất có trễ (FOPDT):** Là mô hình kinh điển đại diện cho $>90\%$ các quá trình nhiệt, bồn mức, nồng độ trong công nghiệp thực phẩm và hóa chất.
            2. **Khâu bậc hai:** Mô tả chuyển động cơ học (khối lượng - lò xo - giảm chấn), chuyển động của van điều khiển khí nén hoặc động cơ điện.
            3. **Khâu trễ vận chuyển $e^{-\theta s}$:** Làm trễ góc pha trên biểu đồ tần số một lượng $-\theta \omega\\text{ (rad)}$, là nguyên nhân chính khiến hệ thống dễ bị mất ổn định khi tăng hệ số khuếch đại.
            """)
