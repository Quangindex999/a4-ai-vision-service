from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from src.routes.api import router as api_router

app = FastAPI(
    title="AI Vision Service",
    description="Smart Campus - AI Vision API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "ai-vision",
        "timestamp": datetime.now().isoformat(),
    }


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
