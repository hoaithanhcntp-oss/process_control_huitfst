import streamlit as st
import numpy as np
import pandas as pd

def show_chart(fig):
    """Hiển thị biểu đồ Plotly tương thích mọi phiên bản Streamlit không sinh cảnh báo"""
    try:
        st.plotly_chart(fig, width="stretch")
    except (TypeError, ValueError):
        st.plotly_chart(fig, use_container_width=True)

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
