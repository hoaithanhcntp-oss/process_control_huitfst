import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import signal
import pandas as pd
from utils.control_utils import compute_routh_table

def render():
    st.header("3. Khảo Sát Tính Ổn Định & Đặc Tính Miền Tần Số")
    raw_den = st.text_input("Nhập các hệ số mẫu số (cách nhau bởi dấu phẩy):", "1, 3, 3, 2")
    raw_num = st.text_input("Nhập các hệ số tử số:", "2")
    
    try:
        den_poly = [float(x.strip()) for x in raw_den.split(",")]
        num_poly = [float(x.strip()) for x in raw_num.split(",")]
        sys_t3 = signal.TransferFunction(num_poly, den_poly)
        
        tab3_col1, tab3_col2 = st.columns(2)
        with tab3_col1:
            st.subheader("📌 Tiêu chuẩn Routh-Hurwitz")
            routh_tbl, is_stab, sc_count = compute_routh_table(den_poly)
            row_labels = [f"s^{len(den_poly)-1-i}" for i in range(len(den_poly))]
            df_routh = pd.DataFrame(routh_tbl, index=row_labels)
            st.dataframe(df_routh.style.format("{:.3f}"))
            
            if is_stab:
                st.success("✅ **Hệ thống ỔN ĐỊNH**: Cột 1 không đổi dấu.")
            else:
                st.error(f"❌ **Hệ thống KHÔNG ỔN ĐỊNH**: Có **{sc_count}** lần đổi dấu ở cột 1.")
                
            st.subheader("📍 Mặt phẳng Cực - Zero (Pole-Zero Map)")
            poles = sys_t3.poles
            zeros = sys_t3.zeros
            fig_pz = go.Figure()
            fig_pz.add_vline(x=0, line_dash="dash", line_color="black")
            fig_pz.add_hline(y=0, line_dash="dash", line_color="black")
            fig_pz.add_trace(go.Scatter(x=np.real(poles), y=np.imag(poles), mode='markers', name='Cực (Poles)', marker=dict(symbol='x', size=12, color='crimson', line=dict(width=2))))
            if len(zeros) > 0:
                fig_pz.add_trace(go.Scatter(x=np.real(zeros), y=np.imag(zeros), mode='markers', name='Zeros', marker=dict(symbol='circle-open', size=12, color='blue', line=dict(width=2))))
            fig_pz.update_layout(xaxis_title="Trục thực (Re)", yaxis_title="Trục ảo (Im)", height=350)
            st.plotly_chart(fig_pz, use_container_width=True)

        with tab3_col2:
            st.subheader("📉 Biểu đồ Bode")
            w, mag, phase = signal.bode(sys_t3)
            fig_bode = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, subplot_titles=("Biên độ (dB)", "Góc pha (deg)"))
            fig_bode.add_trace(go.Scatter(x=w, y=mag, line=dict(color="blue")), row=1, col=1)
            fig_bode.add_trace(go.Scatter(x=w, y=phase, line=dict(color="orange")), row=2, col=1)
            fig_bode.update_xaxes(type="log", row=2, col=1, title_text="Tần số ω (rad/s)")
            fig_bode.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_bode, use_container_width=True)
    except Exception as e:
        st.error(f"Lỗi nhập dữ liệu đa thức: {e}")
