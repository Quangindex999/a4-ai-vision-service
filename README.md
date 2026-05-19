# B4 - AI Vision Service

> **Smart Campus System** | Dịch vụ phân tích hình ảnh và nhận diện bất thường theo thời gian thực.

---

## 1. Tổng quan (Overview)

AI Vision Service là một microservice trong hệ thống Smart Campus, chịu trách nhiệm **nhận frame ảnh từ nhóm Camera Stream (B2)**, xử lý bằng logic AI mock hoặc mô hình AI thật, và trả về kết quả phát hiện đối tượng kèm mức độ tin cậy. Ở giai đoạn thiết kế hiện tại, service cũng đã được định hướng sẵn để tích hợp với **Core Business (B6)** và **Analytics (B5)** trong các bước phát triển tiếp theo.

```text
[B2 - Camera Stream] ──POST /api/v1/vision/analyze──► [B4 - AI Vision]
                                  │
                                  ├──► [B6 - Core Business]
                                  └──► [B5 - Analytics]
```

**Công nghệ sử dụng:**

- **Runtime:** Python 3.11
- **Framework:** FastAPI
- **Validation:** Pydantic v2
- **Containerization:** Docker + Docker Compose
- **Testing:** Postman / Newman

---

## 2. Vai trò trong hệ thống

AI Vision Service đóng vai trò trung tâm trong chuỗi xử lý hình ảnh:

- Nhận ảnh/frame từ `Camera Stream (B2)`
- Chạy mô hình AI hoặc mô phỏng kết quả AI
- Trả về kết quả phát hiện và độ tin cậy
- Cung cấp nền tảng để gửi dữ liệu sang `Core Business (B6)` và `Analytics (B5)`

---

## 3. Nhiệm vụ chính

Service cần đáp ứng các nhiệm vụ sau:

- Nhận ảnh từ Camera Stream
- Kiểm tra và hợp lệ hóa dữ liệu đầu vào
- Chạy mô hình AI hoặc mô phỏng kết quả AI
- Trả về kết quả phát hiện
- Cho biết mức độ tin cậy của kết quả
- Chuẩn bị luồng tích hợp cho Analytics và Core Business

---

## 4. Dữ liệu đầu vào và đầu ra

### 4.1. Dữ liệu đầu vào gợi ý

```json
{
  "camera_id": "cam-gate-01",
  "image_url": "http://example.com/frame.jpg",
  "timestamp": "2026-05-02T09:10:00"
}
```

### 4.2. Đầu ra mong đợi

```json
{
  "detected": true,
  "object": "person",
  "confidence": 0.91,
  "risk_level": "medium"
}
```

### 4.3. Ý nghĩa các trường

| Field        | Type                          | Mô tả                        |
| ------------ | ----------------------------- | ---------------------------- |
| `detected`   | boolean                       | Có phát hiện đối tượng hay không |
| `object`     | string                        | Tên đối tượng nhận diện      |
| `confidence` | float [0.0–1.0]               | Độ tin cậy của kết quả       |
| `risk_level` | enum: `low`, `medium`, `high` | Mức độ rủi ro                |

---

## 5. Luồng xử lý (Workflow)

### 5.1. Luồng hiện tại

1. `B2 - Camera Stream` gửi request chứa `camera_id`, `image_url`, `timestamp`.
2. `B4 - AI Vision` nhận request tại `POST /api/v1/vision/analyze`.
3. Hệ thống validate dữ liệu bằng Pydantic.
4. Service chạy logic AI mock hoặc mô hình AI thật nếu được tích hợp.
5. Service trả về kết quả phát hiện gồm `detected`, `object`, `confidence`, `risk_level`.

### 5.2. Luồng mở rộng trong kiến trúc

Sau khi xử lý ảnh, service có thể:

- gửi dữ liệu sự kiện sang `B5 - Analytics` để phục vụ thống kê
- gửi kết quả phát hiện sang `B6 - Core Business` để hỗ trợ ra quyết định nghiệp vụ

> Lưu ý: Ở phiên bản hiện tại, dự án tập trung hoàn thiện luồng làm việc với `B2`. Các kết nối sang `B5` và `B6` đã được thiết kế trong kiến trúc và sẽ được triển khai ở giai đoạn tiếp theo.

---

## 6. Cấu trúc Service (Service Boundary)

```text
src/
├── main.py              # Khởi tạo FastAPI app, cấu hình CORS, / và /health, include_router
├── routes/
│   └── api.py           # Endpoint POST /api/v1/vision/analyze
├── services/
│   └── vision_service.py# Logic xử lý AI mock + nền tảng tích hợp tương lai
├── models/
│   └── schemas.py       # Pydantic schemas: AnalyzeRequest, AnalyzeResponse
└── utils/
    ├── image_utils.py   # Hàm tiện ích xử lý ảnh
    └── logger.py        # Hàm tiện ích logging
```

**Nguyên tắc thiết kế:**

- `models/` chứa schema Pydantic
- `services/` chứa logic xử lý
- `routes/` chỉ nhận request và gọi service
- `main.py` chỉ khởi tạo app và đăng ký router

---

## 7. API Contract (Endpoints)

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

**Error Responses:**

| Code  | Mô tả                                                         |
| ----- | ------------------------------------------------------------- |
| `422` | Thiếu hoặc sai định dạng field bắt buộc (Pydantic validation) |
| `500` | Lỗi server khi xử lý AI model                                 |

---

## 8. Trạng thái triển khai hiện tại

### Đã hoàn thành

- API nhận ảnh từ `B2`
- Schema request/response bằng Pydantic
- Logic mock AI
- FastAPI application structure
- Docker / Docker Compose
- Swagger UI / OpenAPI

### Đang được thiết kế

- Luồng gửi kết quả sang `B6 - Core Business`
- Luồng đẩy dữ liệu thống kê sang `B5 - Analytics`
- Mô hình AI thật thay thế mock AI

### Định hướng mở rộng

- Tích hợp YOLOv8 / YOLOv11 / Ultralytics
- Tích hợp OpenCV cho tiền xử lý ảnh
- Cơ chế tách luồng xử lý sự kiện cho Analytics và Core Business

---

## 9. Mô tả mock AI

Do giới hạn tài nguyên hoặc mục tiêu tập trung vào kiến trúc service, phiên bản hiện tại sử dụng **mock AI** để mô phỏng kết quả phát hiện.

**Lý do sử dụng mock AI:**

- Giữ cho demo ổn định
- Không phụ thuộc vào cấu hình máy
- Hoàn thiện API contract trước
- Dễ thay thế bằng model thật trong tương lai

**Thiết kế của service đảm bảo:**

- Khi chuyển sang AI thật, API đầu ra vẫn giữ nguyên cấu trúc
- Phần xử lý AI có thể thay đổi mà không ảnh hưởng đến client

---

## 10. Yêu cầu hệ thống (Requirements)

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) đã cài đặt và đang chạy
- Hoặc Python 3.11+ để chạy trực tiếp

---

## 11. Hướng dẫn chạy (Quick Start)

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

## 12. Kiểm thử (Testing)

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

## 13. Tích hợp đa Service (Integration)

Service này giao tiếp với:

| Nhóm                   | Vai trò                             | Trạng thái / Kết nối                                      |
| ---------------------- | ----------------------------------- | --------------------------------------------------------- |
| **B2 - Camera Stream** | Gửi frame ảnh đến AI Vision         | Đã triển khai qua `POST /api/v1/vision/analyze`           |
| **B5 - Analytics**     | Nhận dữ liệu thống kê phát hiện     | Đã thiết kế trong kiến trúc, triển khai ở giai đoạn sau   |
| **B6 - Core Business** | Nhận kết quả phân tích để ra quyết định | Đã thiết kế trong kiến trúc, triển khai ở giai đoạn sau |

### Luồng tích hợp đề xuất

- `B2` gửi ảnh/frame đến `B4`
- `B4` xử lý và trả kết quả phát hiện
- `B4` chuẩn bị dữ liệu sự kiện để gửi sang `B5`
- `B4` chuẩn bị kết quả nghiệp vụ để gửi sang `B6`

---

## 14. Thông tin nhóm (Team)

### Phân chia nhiệm vụ

| Nhiệm vụ | Mô tả |
| -------- | ----- |
| Nhiệm vụ 1 | Thiết kế và xây dựng API cho service AI Vision |
| Nhiệm vụ 2 | Xử lý dữ liệu đầu vào, validation và mock AI logic |
| Nhiệm vụ 3 | Docker hóa service, cấu hình môi trường và chạy local |
| Nhiệm vụ 4 | Kiểm thử API, viết tài liệu và chuẩn bị tích hợp mở rộng |

### Thành viên nhóm

| Thành viên | MSSV | Vai trò |
| ---------- | ---- | ------ |
| [Tên thành viên 1] | [MSSV] | [Phân công sau] |
| [Tên thành viên 2] | [MSSV] | [Phân công sau] |
| [Tên thành viên 3] | [MSSV] | [Phân công sau] |
| [Tên thành viên 4] | [MSSV] | [Phân công sau] |

**Môn học:** [Tên môn học]  
**Giảng viên:** [Tên giảng viên]  
**Học kỳ:** HK2 2025–2026
