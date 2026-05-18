from fastapi import APIRouter, BackgroundTasks

from src.models.schemas import AnalyzeRequest, AnalyzeResponse
from src.services.vision_service import analyze_image

router = APIRouter(prefix="/api/v1/vision", tags=["vision"])


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest, background_tasks: BackgroundTasks) -> AnalyzeResponse:
    return analyze_image(payload, background_tasks)
