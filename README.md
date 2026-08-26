\# 🎛️ Process Control \& Automation Simulation Suite

Phần mềm mô phỏng tương tác phục vụ giảng dạy và nghiên cứu \*\*Lý thuyết Điều khiển Tự động \& Điều khiển Quá trình (Process Control)\*\* trong công nghiệp và Công nghệ Thực phẩm.



\## 📌 Các Module chức năng chính



\### 1. Cơ sở Lý thuyết Điều khiển (Basic Control Theory)

\- \*\*Mô hình động học:\*\* Hệ bậc 1, bậc 2 chuẩn (ζ, ωn), khâu trễ vận chuyển (Padé Approximation).

\- \*\*Phân tích miền thời gian:\*\* Đánh giá phản ứng Step/Impulse/Ramp, trích xuất tự động %OS, tp, ts, tr, ess.

\- \*\*Phân tích ổn định \& Miền tần số:\*\* Tiêu chuẩn Routh-Hurwitz, biểu đồ Bode, Nyquist, Pole-Zero map.



\### 2. Chuyên đề Điều khiển Quá trình (Process Control Engineering)

\- \*\*Thuật ngữ \& Biến quá trình chuẩn P\&ID:\*\*

&#x20; - SP (Set Point): Giá trị đặt.

&#x20; - PV (Process Variable) / CV (Controlled Variable): Biến quá trình cần duy trì.

&#x20; - MV (Manipulated Variable): Biến thao tác (tín hiệu điều khiển van hơi/bơm 0-100%).

&#x20; - DV (Disturbance Variable): Nhiễu tải đầu vào (lưu lượng, nhiệt độ môi trường).

\- \*\*Cấu trúc điều khiển nâng cao:\*\*

&#x20; - \*\*Feedback + Feedforward Control:\*\* Kết hợp phản hồi PID và bù nhiễu truyền thẳng.

&#x20; - \*\*Cascade Control (Điều khiển Tầng):\*\* Vòng ngoài (Nhiệt độ) -> Vòng trong (Lưu lượng/Áp suất hơi).

&#x20; - \*\*Đặc tính Van điều khiển:\*\* Tuyến tính (Linear), Tỷ lệ phần trăm bằng nhau (Equal Percentage), chống bão hòa tích phân.



\### 3. Ứng dụng thực tế trong Công nghệ Thực phẩm

\- \*\*Thanh trùng HTST (Plate Heat Exchanger):\*\* Tính toán tích phân Đơn vị thanh trùng (PU), điều khiển van chuyển hướng dòng (FDV) bảo vệ an toàn vi sinh (72°C).

\- \*\*Tiệt trùng Retort (Đồ hộp):\*\* Tính toán giá trị tiệt trùng F0 (121.1°C, z=10°C) đảm bảo an toàn vi sinh (C. botulinum).

\- \*\*Bồn đệm mức dịch (Buffer Tank):\*\* Cân bằng vật chất phi tuyến theo định luật Torricelli.



\---



\## 🚀 Cài đặt \& Khởi chạy



```bash

pip install -r requirements.txt

streamlit run app.py

```





