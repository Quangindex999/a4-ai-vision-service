🟢 TRƯỚC KHI BẮT ĐẦU
Mở VS Code, mở Terminal (Ctrl + `) và đảm bảo bạn đang đứng đúng ở thư mục dự án a4-ai-vision-service.

🛠️ CÁCH 1: CHẠY MÔI TRƯỜNG ẢO (Khuyên dùng khi ngồi code/sửa lỗi)
Cách này giúp máy tính nhẹ, các thư viện không bị xung đột.

Kích hoạt phòng ảo:

PowerShell
.\venv\Scripts\activate
(Thành công khi thấy chữ (venv) màu xanh hiện ra ở đầu dòng).

Bật Server:

PowerShell
uvicorn src.main:app --reload
Tắt Server (khi không dùng nữa):
Bấm tổ hợp phím Ctrl + C ngay tại Terminal đó.

Thoát khỏi phòng ảo:

PowerShell
deactivate
⚡ CÁCH 2: CHẠY TRỰC TIẾP (Chạy nhanh, không cần venv)
Cách này dùng lệnh py huyền thoại lúc máy bạn bị lỗi môi trường.

Bật Server:

PowerShell
py -m uvicorn src.main:app --reload
Tắt Server:
Bấm tổ hợp phím Ctrl + C.

🐳 CÁCH 3: CHẠY BẰNG DOCKER (Dùng khi Test kết nối Ngrok hoặc Demo nộp bài)
Cách này xịn nhất, nó tự động set up mọi thứ y hệt một máy chủ thực tế.
(⚠️ Lưu ý: Phải chắc chắn bạn ĐÃ TẮT server ở Cách 1 hoặc Cách 2 để cổng 8000 không bị chiếm).

Khởi động "Thùng" (Số tự động):

PowerShell
docker-compose up -d
PowerShell
Gộp lệnh build và run trong 1 câu lệnh
docker-compose up -d --build
Lệnh loại bỏ container cũ:
docker-compose up -d --build --remove-orphans
Kiểm tra sức khỏe:

PowerShell
docker ps
(Đợi khoảng 30s và gõ lại lệnh này cho đến khi thấy chữ (healthy)).

Tắt và dọn dẹp "Thùng" (Khi làm xong việc):

PowerShell
docker-compose down
📡 BƯỚC MỞ RỘNG: MỞ ĐƯỜNG HẦM NGROK (Áp dụng sau khi đã chạy 1 trong 3 cách trên)
Khi server đã báo running on http://127.0.0.1:8000, bạn làm tiếp các bước sau để mở cửa ra Internet:

Mở một Terminal MỚI (Bấm dấu + trong bảng Terminal của VS Code, để nguyên cái Terminal đang chạy server).

Khởi động Ngrok:

PowerShell
.\ngrok http 8000
Lấy Link: Copy cái link ở dòng Forwarding (ví dụ: https://xyz...ngrok-free.dev).

Mở Radar theo dõi: Mở trình duyệt web, gõ http://127.0.0.1:4040 để ngồi canh dữ liệu đổ về.
