import streamlit as st
from topics import (
    topic_feedforward,
    topic_htst_pasteurization,
    topic_retort_sterilization,
    topic_buffer_tank,
)

def render():
    st.header("5. Chuyên Đề Process Control & Ứng Dụng Công Nghệ Thực Phẩm")
    app_choice = st.selectbox("Chọn mô hình quá trình:", [
        "1. Điều khiển Phản hồi + Truyền thẳng (Feedback + Feedforward)",
        "2. Thanh trùng sữa HTST dạng tấm (Plate Heat Exchanger - PU & FDV)",
        "3. Nồi tiệt trùng đồ hộp Retort (Sterilization Retort - F0 Value)",
        "4. Bồn đệm mức nước quả / Dịch chiết"
    ])
    
    if "Feedback + Feedforward" in app_choice:
        topic_feedforward.render()
    elif "Thanh trùng sữa" in app_choice:
        topic_htst_pasteurization.render()
    elif "Nồi tiệt trùng" in app_choice:
        topic_retort_sterilization.render()
    else:
        topic_buffer_tank.render()
