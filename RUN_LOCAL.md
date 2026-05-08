# Hướng dẫn chạy AI Vision Service cục bộ

Dự án này được đóng gói hoàn toàn bằng Docker. Bạn không cần cài đặt Python hay các thư viện AI phức tạp trên máy tính cá nhân.

## Yêu cầu hệ thống

- Docker Desktop đã được cài đặt và đang chạy.

## Các bước chạy

**Bước 0: Tạo file môi trường**
Copy file biến môi trường mẫu thành file thật (chỉ làm 1 lần):

```bash
cp .env.example .env
```

**Bước 1: Build Docker Image**
Mở terminal tại thư mục gốc của project và chạy lệnh:

```bash
docker build -t a4-ai-vision .
```

**Bước 2: Chạy Container**
Sau khi build xong, khởi chạy service bằng lệnh:

```bash
docker run --name ai-vision-container --env-file .env -p 8000:8000 -d a4-ai-vision
```

**Bước 3: Kiểm tra hoạt động**
Mở trình duyệt hoặc dùng Postman truy cập vào:

- Health check: `http://localhost:8000/health`
- Swagger UI (Tài liệu API tự động): `http://localhost:8000/docs`

**Bước 4: Xem log service**
Nếu cần kiểm tra log khi đang chạy:

```bash
docker logs -f ai-vision-container
```

**Bước 5: Dừng Service**
Khi không cần sử dụng nữa, gõ lệnh:

```bash
docker stop ai-vision-container
docker rm ai-vision-container
```
