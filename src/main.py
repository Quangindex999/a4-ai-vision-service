from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from fastapi.responses import HTMLResponse

# Khởi tạo app
app = FastAPI(
    title="AI Vision Service",
    description="Smart Campus - AI Vision API",
    version="1.0.0"
)

# --- MODELS ---

class AnalyzeRequest(BaseModel):
    camera_id: str
    image_url: str
    timestamp: datetime

class AnalyzeResponse(BaseModel):
    detected: bool
    label: Optional[str] = None           # ✅ ĐỔI TÊN: "object" → "label" (object là built-in Python)
    confidence: float = Field(            # ✅ THÊM: ràng buộc range hợp lệ bằng Field
        default=0.0, ge=0.0, le=1.0
    )
    risk_level: str = "low"

# --- ROUTES ---

@app.get("/health")
def health_check():
    """Endpoint để Docker/Compose kiểm tra xem service có đang sống không"""
    return {
        "status": "ok",
        "service": "ai-vision",
        "timestamp": datetime.now().isoformat()   # ✅ SỬA: .isoformat() để JSON-serializable
    }

@app.post("/api/v1/vision/analyze", response_model=AnalyzeResponse)
def analyze_frame(request: AnalyzeRequest):
    """
    Nhận frame ảnh từ nhóm Camera Stream (A2).
    Tại đây chúng ta sẽ giả lập (mock) logic gọi AI trước.
    """
    try:
        # TODO: Cắm logic gọi OpenCV, YOLO hoặc AI Agent ở đây sau
        # Hiện tại mock data để trả về ngay lập tức

        mock_detected = True

        if mock_detected:
            return AnalyzeResponse(
                detected=True,
                label="person",            # ✅ ĐỔI TÊN: khớp với field mới
                confidence=0.95,
                risk_level="medium"
            )
        else:
            return AnalyzeResponse(detected=False)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>AI Vision Service</title>
            <style>
                body { font-family: sans-serif; text-align: center; padding-top: 50px; background-color: #f4f4f9; }
                .container { border: 1px solid #ddd; display: inline-block; padding: 20px; background: white; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
                h1 { color: #2c3e50; }
                a { color: #3498db; text-decoration: none; font-weight: bold; }
                .status { color: #27ae60; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Sẵn sàng tích hợp với nhóm A2</h1>
                <h1>👁️ AI Vision Service API</h1>
                <p>Trạng thái hệ thống: <span class="status">Đang hoạt động</span></p>
                <p>Vui lòng truy cập <a href="/docs">Tài liệu API (/docs)</a> để bắt đầu.</p>
            </div>
        </body>
    </html>
    """