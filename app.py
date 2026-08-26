import streamlit as st

# Cấu hình giao diện Streamlit
st.set_page_config(
    page_title="Process Control & Automation Suite",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎛️ Process Control & Automation Simulation Suite")
st.caption("Bộ mô phỏng Lý thuyết Điều khiển Tự động & Điều khiển Quá trình trong Công nghệ Thực phẩm")

# Import các tab module
from tabs import (
    tab1_basic_dynamics,
    tab2_time_response,
    tab3_frequency_stability,
    tab4_pid_tuning,
    tab5_process_control,
)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1. Khâu Động Học Cơ Bản",
    "2. Đáp Ứng Thời Gian & Chỉ Tiêu",
    "3. Tính Ổn Định & Miền Tần Số",
    "4. Bộ Điều Khiển PID & Chỉnh Định",
    "5. Chuyên Đề Process Control (Thực Phẩm)"
])

with tab1:
    tab1_basic_dynamics.render()

with tab2:
    tab2_time_response.render()

with tab3:
    tab3_frequency_stability.render()

with tab4:
    tab4_pid_tuning.render()

with tab5:
    tab5_process_control.render()
