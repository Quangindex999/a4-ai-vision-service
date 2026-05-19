from fastapi import APIRouter, BackgroundTasks
from src.models.schemas import AnalyzeRequest, AnalyzeResponse
from src.services.vision_service import process_image, notify_other_services

# Prefix đã bao trọn gói, ở dưới chỉ cần ghi "/analyze"
router = APIRouter(prefix="/api/v1/vision", tags=["vision"])

@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_frame(request: AnalyzeRequest, background_tasks: BackgroundTasks):
    """
    Nhận frame ảnh từ B2, phân tích, trả kết quả và chạy ngầm gửi data cho B5, B6.
    """
    # 1. Gọi Service lõi để xử lý ảnh
    result = process_image(request.image_url)
    
    # 2. Giao việc cho thư ký FastAPI chạy ngầm
    background_tasks.add_task(
        notify_other_services,
        result_data=result,
        camera_id=request.camera_id,
        timestamp=request.timestamp.isoformat()
    )
    
    # 3. Trả kết quả ngay lập tức cho B2
    return AnalyzeResponse(**result)