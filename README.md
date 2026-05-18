# B4 - AI Vision Service

> **Smart Campus System** | Dịch vụ phân tích hình ảnh và nhận diện bất thường theo thời gian thực.

---

## 1. Tổng quan (Overview)

AI Vision Service là một microservice trong hệ thống Smart Campus, chịu trách nhiệm **nhận frame ảnh từ nhóm Camera Stream (B2)**, phân tích bằng logic AI mock hiện tại, và trả về kết quả nhận diện đối tượng kèm mức độ rủi ro cho nhóm Core Business (B6).

```
[B2 - Camera Stream] ──POST /api/v1/vision/analyze──► [B4 - AI Vision] ──► [B6 - Core Business]
```

**Công nghệ sử dụng:**

- **Runtime:** Python 3.11
- **Framework:** FastAPI
- **Validation:** Pydantic v2
- **Containerization:** Docker + Docker Compose
- **Testing:** Postman / Newman

---

## 2. Cấu trúc Service (Service Boundary)

```
src/
├── main.py              # Khởi tạo FastAPI app, cấu hình CORS, / và /health, include_router
├── routes/
│   └── api.py           # Endpoint POST /api/v1/vision/analyze
├── services/
│   └── vision_service.py# Logic xử lý AI mock + BackgroundTasks placeholder
├── models/
│   └── schemas.py       # Pydantic schemas: AnalyzeRequest, AnalyzeResponse
└── utils/
    ├── image_utils.py   # Hàm tiện ích xử lý ảnh
    └── logger.py        # Hàm tiện ích logging
```

**Nguyên tắc thiết kế:** Tách rõ theo lớp:
- `models/` chứa schema Pydantic
- `services/` chứa logic xử lý
- `routes/` chỉ nhận request và gọi service
- `main.py` chỉ khởi tạo app và đăng ký router

---

## 3. API Contract (Endpoints)

Tài liệu API đầy đủ tự động sinh tại: `http://localhost:8000/docs` (Swagger UI)

### `GET /health`

Kiểm tra trạng thái service.

**Response `200 OK`:**

```json
{
  "status": "ok",
  "service": "ai-vision",
  "timestamp": "2026-05-06T09:00:00.000000"
}
```

---

### `GET /`

Trang HTML chào mừng và liên kết đến tài liệu API.

**Response `200 OK`:** HTML page với nội dung:
- “Sẵn sàng tích hợp với nhóm A2”
- “👁️ AI Vision Service API”
- trạng thái hệ thống đang hoạt động
- link tới `/docs`

---

### `POST /api/v1/vision/analyze`

Nhận frame ảnh từ Camera Stream, phân tích và trả về kết quả nhận diện.

**Request Body:**

```json
{
  "camera_id": "cam-gate-01",
  "image_url": "http://example.com/frame.jpg",
  "timestamp": "2026-05-02T09:10:00Z"
}
```

| Field       | Type     | Bắt buộc | Mô tả                       |
| ----------- | -------- | -------- | --------------------------- |
| `camera_id` | string   | ✅       | ID camera gửi frame         |
| `image_url` | string   | ✅       | URL ảnh/frame cần phân tích |
| `timestamp` | datetime | ✅       | Thời điểm chụp frame        |

**Response `200 OK`:**

```json
{
  "detected": true,
  "object": "person",
  "confidence": 0.95,
  "risk_level": "medium"
}
```

| Field        | Type                          | Mô tả                        |
| ------------ | ----------------------------- | ---------------------------- |
| `detected`   | boolean                       | Có phát hiện đối tượng không |
| `object`     | string                        | Tên đối tượng nhận diện      |
| `confidence` | float [0.0–1.0]               | Độ tin cậy của kết quả       |
| `risk_level` | enum: `low`, `medium`, `high` | Mức độ rủi ro                |

**Error Responses:**

| Code  | Mô tả                                                         |
| ----- | ------------------------------------------------------------- |
| `422` | Thiếu hoặc sai định dạng field bắt buộc (Pydantic validation) |
| `500` | Lỗi server khi xử lý AI model                                 |

---

## 4. Yêu cầu hệ thống (Requirements)

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) đã cài đặt và đang chạy
- Hoặc Python 3.11+ để chạy trực tiếp

---

## 5. Hướng dẫn chạy (Quick Start)

### Chạy bằng Docker Compose

```bash
# Bước 1: Clone repo
git clone <repo-url>
cd a4-ai-vision-service

# Bước 2: Tạo file môi trường
cp .env.example .env

# Bước 3: Build và khởi chạy
docker-compose up -d

# Bước 4: Truy cập Swagger UI
# http://localhost:8000/docs
```

### Chạy trực tiếp (Development)

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```

---

## 6. Kiểm thử (Testing)

Bộ test được viết bằng Postman.

### Chạy bằng Postman UI

1. Import `tests/postman_collection.json` vào Postman
2. Import `tests/environment_local.json` và chọn environment `AI Vision Local Env`
3. Bấm **Run Collection**

### Chạy bằng Newman (CLI)

```bash
npm install -g newman
newman run tests/postman_collection.json -e tests/environment_local.json -r cli,htmlextra
```

---

## 7. Tích hợp đa Service (Integration)

Service này giao tiếp với:

| Nhóm                   | Vai trò                             | Endpoint                      |
| ---------------------- | ----------------------------------- | ----------------------------- |
| **B2 - Camera Stream** | Gửi frame ảnh đến AI Vision         | `POST /api/v1/vision/analyze` |
| **B6 - Core Business** | Nhận kết quả phân tích từ AI Vision | BackgroundTasks placeholder   |
| **B5 - Analytics**     | Cung cấp dữ liệu thống kê được phát hiện | BackgroundTasks placeholder   |

---

## 8. Thông tin nhóm (Team)

| Thành viên         | MSSV   | Vai trò                 |
| ------------------ | ------ | ----------------------- |
| [Tên thành viên 1] | [MSSV] | Backend / API Design    |
| [Tên thành viên 2] | [MSSV] | DevOps / Docker         |
| [Tên thành viên 3] | [MSSV] | Testing / Documentation |
| [Tên thành viên 4] | [MSSV] | Testing / Documentation |

**Môn học:** [Tên môn học]
**Giảng viên:** [Tên giảng viên]
**Học kỳ:** HK2 2025–2026
