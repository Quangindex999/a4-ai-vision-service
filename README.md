# A4 - AI Vision Service

> **Smart Campus System** | Dịch vụ phân tích hình ảnh và nhận diện bất thường theo thời gian thực.

---

## 1. Tổng quan (Overview)

AI Vision Service là một microservice trong hệ thống Smart Campus, chịu trách nhiệm **nhận frame ảnh từ nhóm Camera Stream (A2)**, phân tích bằng mô hình AI/Computer Vision, và trả về kết quả nhận diện đối tượng kèm mức độ rủi ro cho nhóm Core Business (A6).

```
[A2 - Camera Stream] ──POST /api/v1/vision/analyze──► [A4 - AI Vision] ──► [A6 - Core Business]
```

**Công nghệ sử dụng:**

- **Runtime:** Python 3.11
- **Framework:** FastAPI + Uvicorn
- **Validation:** Pydantic v2
- **Containerization:** Docker + Docker Compose
- **Testing:** Postman / Newman

---

## 2. Kiến trúc Service (Service Boundary)

```
src/
├── main.py          # Khởi tạo FastAPI app, đăng ký routes
├── routes/          # Định nghĩa các endpoint
│   └── vision.py
├── services/        # Logic xử lý AI (mock → real model)
│   └── vision_service.py
├── models/          # Pydantic schemas (Request / Response)
│   └── schemas.py
└── utils/           # Hàm tiện ích (logger, xử lý ảnh)
    └── helpers.py
```

**Nguyên tắc thiết kế:** Logic AI được tách hoàn toàn vào `services/` theo pattern Strategy — việc swap từ mock sang model thật (OpenCV, YOLO) chỉ cần sửa 1 file duy nhất mà không ảnh hưởng đến route hay response schema.

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
  "label": "person",
  "confidence": 0.95,
  "risk_level": "medium"
}
```

| Field        | Type                          | Mô tả                        |
| ------------ | ----------------------------- | ---------------------------- |
| `detected`   | boolean                       | Có phát hiện đối tượng không |
| `label`      | string                        | Tên đối tượng nhận diện      |
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
- Không cần cài Python hay bất kỳ thư viện nào thêm trên máy local

---

## 5. Hướng dẫn chạy (Quick Start)

### Chạy bằng Docker Compose (Khuyến nghị)

```bash
# Bước 1: Clone repo
git clone <repo-url>
cd a4-ai-vision-service

# Bước 2: Tạo file môi trường
cp .env.example .env

# Bước 3: Build và khởi chạy
docker-compose up -d

# Bước 4: Kiểm tra service đang healthy (chờ ~35 giây)
docker ps

# Bước 5: Truy cập Swagger UI
# http://localhost:8000/docs
```

### Chạy trực tiếp (Development)

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```

---

## 6. Biến môi trường (Environment Variables)

Sao chép `.env.example` thành `.env` và chỉnh sửa theo môi trường:

| Biến                      | Mặc định                    | Mô tả                       |
| ------------------------- | --------------------------- | --------------------------- |
| `PORT`                    | `8000`                      | Cổng chạy service           |
| `ENVIRONMENT`             | `development`               | Môi trường chạy             |
| `AI_CONFIDENCE_THRESHOLD` | `0.6`                       | Ngưỡng confidence tối thiểu |
| `CORE_BUSINESS_URL`       | `http://core-business:8000` | URL của nhóm A6             |

> ⚠️ Không commit file `.env` thật lên Git. File `.env` đã được thêm vào `.gitignore`.

---

## 7. Kiểm thử (Testing)

Bộ test được viết bằng Postman, bao gồm **5 test case** tự động:

| #   | Tên                 | Loại       | Mô tả                                                                 |
| --- | ------------------- | ---------- | --------------------------------------------------------------------- |
| 1   | Health Check        | Happy Path | Kiểm tra service sống và trả đúng schema                              |
| 2   | Analyze Valid Data  | Happy Path | Kiểm tra response đủ field, confidence trong [0,1], risk_level hợp lệ |
| 3   | Missing `image_url` | Negative   | Expect 422 + `detail` array                                           |
| 4   | Missing `camera_id` | Negative   | Expect 422 + `detail` array                                           |
| 5   | Missing `timestamp` | Negative   | Expect 422 + `detail` array                                           |

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

## 8. Tích hợp đa Service (Integration)

Service này giao tiếp với:

| Nhóm                   | Vai trò                             | Endpoint                         |
| ---------------------- | ----------------------------------- | -------------------------------- |
| **A2 - Camera Stream** | Gửi frame ảnh đến AI Vision         | `POST /api/v1/vision/analyze`    |
| **A6 - Core Business** | Nhận kết quả phân tích từ AI Vision | `CORE_BUSINESS_URL` trong `.env` |

### Demo tích hợp với Ngrok

```bash
# Sau khi service đang chạy:
ngrok http 8000

# Gửi Public URL cho nhóm A2
# Theo dõi request real-time tại: http://127.0.0.1:4040
```

---

## 9. Reliability Checklist

- [x] **Happy Path:** `/health` và `/api/v1/vision/analyze` hoạt động đúng, trả về đầy đủ các trường `detected`, `label`, `risk_level` (thuộc tập hợp hợp lệ) và `confidence` (0.0–1.0)
- [x] **Negative Path:** Pydantic chặn và trả `422 Unprocessable Entity` kèm `detail` array khi thiếu bất kỳ field bắt buộc nào (`image_url`, `camera_id`, `timestamp`)
- [x] **Data Integrity:** Validate chặt chẽ ở tầng model trước khi vào logic xử lý
- [x] **Isolate Environment:** Không hard-code URL, dùng biến `{{base_url}}` qua Postman Environment và `.env` file
- [x] **Container Health:** Docker tự động kiểm tra sức khỏe service qua `healthcheck` mỗi 30 giây
- [x] **Security:** Container chạy bằng non-root user (`appuser`), không expose secrets lên Git

---

## 10. Thông tin nhóm (Team)

| Thành viên         | MSSV   | Vai trò                 |
| ------------------ | ------ | ----------------------- |
| [Tên thành viên 1] | [MSSV] | Backend / API Design    |
| [Tên thành viên 2] | [MSSV] | DevOps / Docker         |
| [Tên thành viên 3] | [MSSV] | Testing / Documentation |
| [Tên thành viên 3] | [MSSV] | Testing / Documentation |

**Môn học:** [Tên môn học]
**Giảng viên:** [Tên giảng viên]
**Học kỳ:** HK2 2025–2026
