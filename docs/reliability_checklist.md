# Reliability Checklist - AI Vision Service

- [x] **Happy Path:** Endpoint `/health` và `/api/v1/vision/analyze` hoạt động đúng, trả về đầy đủ các trường `detected`, `label`, `risk_level` (thuộc tập hợp hợp lệ) và `confidence` (0.0 - 1.0).
- [x] **Negative Path (Missing Fields):** Pydantic chặn đứng và trả về `422 Unprocessable Entity` kèm array `detail` giải thích rõ lỗi khi thiếu bất kỳ trường bắt buộc nào (`image_url`, `camera_id`, `timestamp`).
- [x] **Data Integrity:** Dữ liệu được validate chặt chẽ ở tầng model trước khi đưa vào xử lý logic.
- [x] **Isolate Environment:** Không hard-code URL, sử dụng biến `{{base_url}}` qua Postman Environment.
