from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
import base64
import io
from PIL import Image

from models.vision import ImageAnalysisRequest, ImageAnalysisResponse
from services.vision_service import VisionService
from utils.image_utils import validate_image, resize_image

router = APIRouter()
vision_service = VisionService()

@router.post("/analyze", response_model=ImageAnalysisResponse)
async def analyze_image(request: ImageAnalysisRequest):
    """Analyze image with AI"""
    try:
        # Validate base64 image
        image_data = base64.b64decode(request.image)
        
        # Process image based on analysis type
        if request.analysis_type == "object_detection":
            result = await vision_service.detect_objects(image_data)
        elif request.analysis_type == "classification":
            result = await vision_service.classify_image(image_data)
        elif request.analysis_type == "segmentation":
            result = await vision_service.segment_image(image_data)
        else:
            raise HTTPException(status_code=400, detail="Invalid analysis type")
        
        return ImageAnalysisResponse(
            results=result,
            confidence=result.get("confidence", 0.0),
            analysis_type=request.analysis_type
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload-analyze")
async def upload_and_analyze(
    file: UploadFile = File(...),
    analysis_type: str = "object_detection"
):
    """Upload and analyze image file"""
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read and process image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to base64 for processing
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # Create request
        request = ImageAnalysisRequest(
            image=img_str,
            analysis_type=analysis_type
        )
        
        # Process using existing endpoint logic
        return await analyze_image(request)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
