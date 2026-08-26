import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import signal
import pandas as pd

# ==============================================================================
# CẤU HÌNH TRANG
# ==============================================================================
st.set_page_config(
    page_title="Process Control & Automation Suite",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎛️ Process Control & Automation Simulation Suite")
st.caption("Bộ mô phỏng Lý thuyết Điều khiển Tự động & Điều khiển Quá trình trong Công nghệ Thực phẩm")

# ==============================================================================
# CÁC HÀM TOÁN HỌC & ĐIỀU KHIỂN BỔ TRỢ
# ==============================================================================
def pade_approx(theta, order=2):
    """Xấp xỉ khâu trễ e^(-theta*s) theo Padé bậc 1 hoặc bậc 2"""
    if theta <= 1e-4:
        return [1.0], [1.0]
    if order == 1:
        return [-theta / 2.0, 1.0], [theta / 2.0, 1.0]
    elif order == 2:
        return [theta**2 / 12.0, -theta / 2.0, 1.0], [theta**2 / 12.0, theta / 2.0, 1.0]

def calc_step_metrics(t, y, y_final=None):
    """Tính các chỉ tiêu chất lượng quá độ"""
    if y_final is None:
        y_final = y[-1]
    y_max = np.max(y)
    peak_time = t[np.argmax(y)]
    overshoot = max(0.0, (y_max - y_final) / abs(y_final) * 100.0) if abs(y_final) > 1e-5 else 0.0
    
    tol = 0.02 * abs(y_final) if abs(y_final) > 1e-5 else 0.02
    settled_idx = np.where(np.abs(y - y_final) > tol)[0]
    ts = t[settled_idx[-1]] if len(settled_idx) > 0 and settled_idx[-1] < len(t) - 1 else t[-1]
    
    idx10 = np.where(y >= 0.1 * y_final)[0]
    idx90 = np.where(y >= 0.9 * y_final)[0]
    tr = t[idx90[0]] - t[idx10[0]] if len(idx10) > 0 and len(idx90) > 0 else 0.0
    ess = abs(1.0 - y_final)
    return {"OS": overshoot, "Tp": peak_time, "Ts": ts, "Tr": tr, "Ess": ess, "Yfinal": y_final}

def compute_routh_table(coeffs):
    """Tính bảng tiêu chuẩn đại số Routh-Hurwitz"""
    coeffs = [float(c) for c in coeffs]
    n = len(coeffs)
    if n == 0:
        return [], True, 0
    rows = n
    cols = (n + 1) // 2
    table = np.zeros((rows, cols))
    
    for i, c in enumerate(coeffs):
        table[i % 2, i // 2] = c
        
    for r in range(2, rows):
        for c in range(cols - 1):
            a = table[r-1, 0]
            if abs(a) < 1e-9:
                a = 1e-5
            b = table[r-2, 0]
            c1 = table[r-2, c+1]
            c2 = table[r-1, c+1]
            table[r, c] = (a * c1 - b * c2) / a
            
    first_col = table[:, 0]
    sign_changes = 0
    prev_s = np.sign(first_col[0])
    for val in first_col[1:]:
        s = np.sign(val)
        if s != 0 and s != prev_s:
            sign_changes += 1
            prev_s = s
    is_stable = (sign_changes == 0) and all(c > 0 for c in coeffs)
    return table, is_stable, sign_changes

# ==============================================================================
# DANH SÁCH 5 TAB CHỨC NĂNG
# ==============================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1. Khâu Động Học Cơ Bản",
    "2. Đáp Ứng Thời Gian & Chỉ Tiêu",
    "3. Tính Ổn Định & Miền Tần Số",
    "4. Bộ Điều Khiển PID & Chỉnh Định",
    "5. Chuyên Đề Process Control (Thực Phẩm)"
])

# ------------------------------------------------------------------------------
# TAB 1: KHÂU ĐỘNG HỌC CƠ BẢN
# ------------------------------------------------------------------------------
with tab1:
    st.header("1. Khảo Sát Các Khâu Động Học Điển Hình")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        model_type = st.radio("Chọn loại khâu động học:", ["Khâu bậc 1 có trễ (FOPDT)", "Khâu bậc 2 chuẩn"])
        if model_type == "Khâu bậc 1 có trễ (FOPDT)":
            k_fopdt = st.slider("Hệ số khuếch đại K:", 0.1, 5.0, 1.5, 0.1)
            tau_fopdt = st.slider("Hằng số thời gian τ (s):", 0.5, 10.0, 3.0, 0.5)
            theta_delay = st.slider("Thời gian trễ θ (s):", 0.0, 5.0, 1.0, 0.2)
            
            num_p, den_p = pade_approx(theta_delay, order=2)
            num_t1 = np.polymul([k_fopdt], num_p)
            den_t1 = np.polymul([tau_fopdt, 1.0], den_p)
            st.latex(r"G(s) = \frac{" + str(k_fopdt) + r"}{" + str(tau_fopdt) + r"s + 1} e^{-" + str(theta_delay) + r"s}")
        else:
            wn = st.slider("Tần số dao động tự nhiên ωn (rad/s):", 0.5, 10.0, 2.5, 0.1)
            zeta = st.slider("Hệ số tắt dần ζ (damping ratio):", 0.0, 2.0, 0.4, 0.05)
            num_t1 = [wn**2]
            den_t1 = [1.0, 2.0 * zeta * wn, wn**2]
            st.latex(r"G(s) = \frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2} = \frac{" + f"{wn**2:.2f}" + r"}{s^2 + " + f"{2*zeta*wn:.2f}" + r"s + " + f"{wn**2:.2f}" + r"}")
            
            if zeta == 0:
                st.warning("ζ = 0: Không suy giảm (Undamped) - Dao động vĩnh cửu.")
            elif 0 < zeta < 1:
                st.info("0 < ζ < 1: Thiếu suy giảm (Underdamped) - Dao động tắt dần có vọt lố.")
            elif zeta == 1:
                st.success("ζ = 1: Suy giảm tới hạn (Critically Damped) - Xác lập nhanh nhất, không vọt lố.")
            else:
                st.info("ζ > 1: Quá suy giảm (Overdamped) - Đáp ứng chậm, không vọt lố.")

    with col2:
        sys_t1 = signal.TransferFunction(num_t1, den_t1)
        t_span = np.linspace(0, 20, 500)
        t_out, y_step = signal.step(sys_t1, T=t_span)
        
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=t_out, y=y_step, mode='lines', name='Đáp ứng bước nhảy y(t)', line=dict(color='#1f77b4', width=2.5)))
        fig1.add_trace(go.Scatter(x=t_out, y=np.ones_like(t_out), mode='lines', name='Tín hiệu đặt r(t)=1', line=dict(color='red', dash='dash')))
        fig1.update_layout(title="Đồ thị Đáp ứng Bước nhảy (Step Response)", xaxis_title="Thời gian (s)", yaxis_title="Biên độ đầu ra")
        st.plotly_chart(fig1, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 2: ĐÁP ỨNG THỜI GIAN & CHỈ TIÊU CHẤT LƯỢNG
# ------------------------------------------------------------------------------
with tab2:
    st.header("2. Khảo Sát Đáp Ứng Thời Gian & Chỉ Tiêu Quá Độ")
    c_in1, c_in2 = st.columns([1, 2])
    
    with c_in1:
        st.subheader("Cấu hình Hàm truyền")
        wn_t2 = st.slider("Tần số riêng ωn:", 0.5, 8.0, 3.0, 0.5, key="wn2")
        zeta_t2 = st.slider("Hệ số tắt ζ:", 0.05, 1.5, 0.35, 0.05, key="zeta2")
        sig_type = st.selectbox("Tín hiệu kích thích đầu vào:", ["Bước nhảy (Step)", "Xung kích (Impulse)", "Hàm dốc (Ramp)"])
        
        num_t2 = [wn_t2**2]
        den_t2 = [1.0, 2.0 * zeta_t2 * wn_t2, wn_t2**2]
        sys_t2 = signal.TransferFunction(num_t2, den_t2)

    with c_in2:
        t_arr = np.linspace(0, 15, 600)
        fig_t2 = go.Figure()
        
        if sig_type == "Bước nhảy (Step)":
            t_s, y_s = signal.step(sys_t2, T=t_arr)
            m = calc_step_metrics(t_s, y_s, y_final=1.0)
            
            fig_t2.add_trace(go.Scatter(x=t_s, y=y_s, name="y(t)", line=dict(color="#1f77b4", width=2.5)))
            fig_t2.add_trace(go.Scatter(x=t_s, y=np.ones_like(t_s), name="r(t)", line=dict(color="red", dash="dash")))
            fig_t2.add_trace(go.Scatter(x=t_s, y=np.ones_like(t_s)*1.02, name="+2%", line=dict(color="gray", dash="dot")))
            fig_t2.add_trace(go.Scatter(x=t_s, y=np.ones_like(t_s)*0.98, name="-2%", line=dict(color="gray", dash="dot")))
            st.plotly_chart(fig_t2, use_container_width=True)
            
            mc1, mc2, mc3, mc4 = st.columns(4)
            mc1.metric("Độ vọt lố (%OS)", f"{m['OS']:.2f} %")
            mc2.metric("Thời gian đỉnh (Tp)", f"{m['Tp']:.2f} s")
            mc3.metric("Thời gian xác lập (Ts 2%)", f"{m['Ts']:.2f} s")
            mc4.metric("Thời gian lên (Tr)", f"{m['Tr']:.2f} s")
            
        elif sig_type == "Xung kích (Impulse)":
            t_i, y_i = signal.impulse(sys_t2, T=t_arr)
            fig_t2.add_trace(go.Scatter(x=t_i, y=y_i, name="Đáp ứng xung h(t)", line=dict(color="#2ca02c", width=2.5)))
            fig_t2.update_layout(title="Đáp ứng Xung Kích (Impulse Response)", xaxis_title="Thời gian (s)", yaxis_title="Biên độ")
            st.plotly_chart(fig_t2, use_container_width=True)
        else:
            u_ramp = t_arr
            t_r, y_r, _ = signal.lsim(sys_t2, U=u_ramp, T=t_arr)
            fig_t2.add_trace(go.Scatter(x=t_r, y=y_r, name="y(t)", line=dict(color="#1f77b4", width=2.5)))
            fig_t2.add_trace(go.Scatter(x=t_r, y=u_ramp, name="Tín hiệu dốc r(t)=t", line=dict(color="red", dash="dash")))
            fig_t2.update_layout(title="Đáp ứng Hàm Dốc (Ramp Response)", xaxis_title="Thời gian (s)", yaxis_title="Biên độ")
            st.plotly_chart(fig_t2, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 3: TÍNH ỔN ĐỊNH & MIỀN TẦN SỐ
# ------------------------------------------------------------------------------
with tab3:
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

# ------------------------------------------------------------------------------
# TAB 4: BỘ ĐIỀU KHIỂN PID & CHỈNH ĐỊNH
# ------------------------------------------------------------------------------
with tab4:
    st.header("4. Thiết Kế & Chỉnh Định Bộ Điều Khiển PID")
    col_pid_ctrl, col_pid_plot = st.columns([1, 2])
    
    with col_pid_ctrl:
        st.subheader("Đối tượng điều khiển FOPDT")
        kp_p = st.number_input("K (Khuếch đại đối tượng):", value=1.0, step=0.1)
        tau_p = st.number_input("τ (Hằng số thời gian s):", value=4.0, step=0.5)
        theta_p = st.number_input("θ (Thời gian trễ s):", value=1.5, step=0.2)
        
        st.divider()
        st.subheader("Chỉnh định tự động (Auto-Tuning)")
        tune_method = st.selectbox("Chọn công thức tính mẫu:", ["Thử sai thủ công", "Ziegler-Nichols 1 (S-curve)", "Cohen-Coon"])
        
        if tune_method == "Ziegler-Nichols 1 (S-curve)":
            kp_calc = 1.2 * (tau_p / (kp_p * max(0.1, theta_p)))
            ti_calc = 2.0 * theta_p
            td_calc = 0.5 * theta_p
            ki_calc = kp_calc / ti_calc
            kd_calc = kp_calc * td_calc
            st.success(f"Thông số Z-N: Kp={kp_calc:.2f}, Ki={ki_calc:.2f}, Kd={kd_calc:.2f}")
        elif tune_method == "Cohen-Coon":
            r = theta_p / tau_p
            kp_calc = (1.0 / (kp_p * r)) * (4.0/3.0 + r / 4.0)
            ti_calc = theta_p * (32.0 + 6.0 * r) / (13.0 + 8.0 * r)
            td_calc = theta_p * 4.0 / (11.0 + 2.0 * r)
            ki_calc = kp_calc / ti_calc
            kd_calc = kp_calc * td_calc
            st.success(f"Thông số Cohen-Coon: Kp={kp_calc:.2f}, Ki={ki_calc:.2f}, Kd={kd_calc:.2f}")
        else:
            kp_calc, ki_calc, kd_calc = 2.5, 0.3, 0.8
            
        kp_val = st.slider("Hệ số Kp:", 0.0, 20.0, float(kp_calc), 0.1)
        ki_val = st.slider("Hệ số Ki:", 0.0, 5.0, float(ki_calc), 0.05)
        kd_val = st.slider("Hệ số Kd:", 0.0, 10.0, float(kd_calc), 0.1)

    with col_pid_plot:
        dt_sim = 0.05
        t_pid = np.arange(0, 30.0, dt_sim)
        n_pid = len(t_pid)
        d_steps = max(1, int(theta_p / dt_sim))
        buff = [0.0] * d_steps
        
        y_open = np.zeros(n_pid)
        y_closed = np.zeros(n_pid)
        u_ctrl = np.zeros(n_pid)
        int_e, prev_e, curr_y_cl, curr_y_op = 0.0, 0.0, 0.0, 0.0
        
        for i in range(1, n_pid):
            u_in_op = 1.0 if t_pid[i] >= 1.0 else 0.0
            dy_op = (kp_p * u_in_op - curr_y_op) / tau_p
            curr_y_op += dy_op * dt_sim
            y_open[i] = curr_y_op
            
            y_meas = buff.pop(0)
            err = 1.0 - y_meas
            int_e += err * dt_sim
            der_e = (err - prev_e) / dt_sim
            prev_e = err
            
            u = np.clip(kp_val * err + ki_val * int_e + kd_val * der_e, 0.0, 100.0)
            u_ctrl[i] = u
            
            dy_cl = (kp_p * u - curr_y_cl) / tau_p
            curr_y_cl += dy_cl * dt_sim
            y_closed[i] = curr_y_cl
            buff.append(curr_y_cl)

        fig_pid = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("So sánh Đáp ứng Đầu ra y(t)", "Tín hiệu Điều khiển u(t)"), vertical_spacing=0.1)
        fig_pid.add_trace(go.Scatter(x=t_pid, y=y_closed, name="Vòng kín PID (Closed Loop)", line=dict(color="#1f77b4", width=2.5)), row=1, col=1)
        fig_pid.add_trace(go.Scatter(x=t_pid, y=y_open, name="Vòng hở (Open Loop)", line=dict(color="orange", dash="dash")), row=1, col=1)
        fig_pid.add_trace(go.Scatter(x=t_pid, y=np.ones_like(t_pid), name="Tín hiệu đặt SP=1", line=dict(color="red", dash="dot")), row=1, col=1)
        fig_pid.add_trace(go.Scatter(x=t_pid, y=u_ctrl, name="Tín hiệu Van u(t)", line=dict(color="green")), row=2, col=1)
        fig_pid.update_layout(height=500, hovermode="x unified")
        st.plotly_chart(fig_pid, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 5: CHUYÊN ĐỀ PROCESS CONTROL & CÔNG NGHỆ THỰC PHẨM
# ------------------------------------------------------------------------------
with tab5:
    st.header("5. Chuyên Đề Process Control & Ứng Dụng Công Nghệ Thực Phẩm")
    app_choice = st.selectbox("Chọn mô hình quá trình:", [
        "1. Điều khiển Phản hồi + Truyền thẳng (Feedback + Feedforward)",
        "2. Thanh trùng sữa HTST dạng tấm (Plate Heat Exchanger - PU & FDV)",
        "3. Nồi tiệt trùng đồ hộp Retort (Sterilization Retort - F0 Value)",
        "4. Bồn đệm mức nước quả / Dịch chiết"
    ])
    
    if "Feedback + Feedforward" in app_choice:
        col_pc1, col_pc2 = st.columns([1, 2])
        with col_pc1:
            st.subheader("Cấu hình Vòng điều khiển P&ID")
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
            fig_pc.update_layout(height=500, hovermode="x unified")
            st.plotly_chart(fig_pc, use_container_width=True)

    elif "Thanh trùng sữa" in app_choice:
        col_f1, col_f2 = st.columns([1, 2])
        with col_f1:
            st.subheader("Cài đặt HTST")
            sp_milk = st.slider("Nhiệt độ đặt SP (°C):", 65.0, 85.0, 75.0, 0.5)
            tin_milk = st.slider("Nhiệt độ sữa vào (°C):", 4.0, 20.0, 8.0, 1.0)
            hold_delay = st.slider("Trễ ống lưu nhiệt (s):", 1.0, 15.0, 6.0, 0.5)
            kp_htst = st.slider("Kp:", 0.0, 10.0, 3.0, 0.2, key="kp_h")
            ki_htst = st.slider("Ki:", 0.0, 2.0, 0.25, 0.02, key="ki_h")
            kd_htst = st.slider("Kd:", 0.0, 5.0, 0.6, 0.05, key="kd_h")
            
        with col_f2:
            dt_htst = 0.1
            t_htst = np.arange(0, 120.0, dt_htst)
            n_h = len(t_htst)
            buf_h = [tin_milk] * max(1, int(hold_delay/dt_htst))
            pv_milk = np.zeros(n_h)
            pu_val = np.zeros(n_h)
            pv_milk[0] = tin_milk
            int_m, prev_em, curr_tm = 0.0, 0.0, tin_milk
            
            for i in range(1, n_h):
                meas_tm = buf_h.pop(0)
                e_m = sp_milk - meas_tm
                int_m += e_m * dt_htst
                der_m = (e_m - prev_em) / dt_htst
                prev_em = e_m
                u_steam = np.clip(kp_htst * e_m + ki_htst * int_m + kd_htst * der_m, 0.0, 100.0)
                dt_temp = ((0.85 * u_steam + tin_milk) - curr_tm) / 7.0
                curr_tm += dt_temp * dt_htst
                pv_milk[i] = curr_tm
                buf_h.append(curr_tm)
                rate_pu = 10.0 ** ((meas_tm - 60.0) / 10.0) if meas_tm >= 60.0 else 0.0
                pu_val[i] = pu_val[i-1] + (rate_pu * dt_htst / 60.0)
                
            fig_htst = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Nhiệt độ Sữa & Ngưỡng Van Đảo Dòng FDV (72°C)", "Đơn vị Thanh trùng Tích lũy (PU)"))
            fig_htst.add_trace(go.Scatter(x=t_htst, y=pv_milk, name="Nhiệt độ sữa (°C)", line=dict(color="blue", width=2)), row=1, col=1)
            fig_htst.add_trace(go.Scatter(x=t_htst, y=np.ones_like(t_htst)*sp_milk, name="SP", line=dict(color="green", dash="dash")), row=1, col=1)
            fig_htst.add_trace(go.Scatter(x=t_htst, y=np.ones_like(t_htst)*72.0, name="Ngưỡng FDV (72°C)", line=dict(color="red", dash="dot")), row=1, col=1)
            fig_htst.add_trace(go.Scatter(x=t_htst, y=pu_val, name="PU tích lũy", line=dict(color="green", width=2)), row=2, col=1)
            fig_htst.update_layout(height=480, hovermode="x unified")
            st.plotly_chart(fig_htst, use_container_width=True)

    elif "Nồi tiệt trùng" in app_choice:
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

    else:
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

