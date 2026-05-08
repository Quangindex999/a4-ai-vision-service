# Sử dụng image Python bản nhẹ
FROM python:3.11-slim

# Biến môi trường quan trọng cho Python trong Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Thiết lập thư mục làm việc bên trong container
WORKDIR /app

# Copy file requirements vào trước để tận dụng cache của Docker
COPY requirements.txt .

# Cài đặt các thư viện cần thiết
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt

# Tạo user không phải root để chạy app (best practice bảo mật)
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# Copy toàn bộ mã nguồn vào container
COPY src/ /app/src/

# Mở cổng 8000 để giao tiếp ra bên ngoài
EXPOSE 8000

# Lệnh khởi chạy server, đọc PORT từ biến môi trường (mặc định 8000)
CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}"]