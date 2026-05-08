from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from enum import Enum

class AnalysisType(str, Enum):
    OBJECT_DETECTION = "object_detection"
    CLASSIFICATION = "classification"
    SEGMENTATION = "segmentation"

class BoundingBox(BaseModel):
    x: float
    y: float
    width: float
    height: float
    confidence: float
    label: str

class ClassificationResult(BaseModel):
    label: str
    confidence: float
    class_id: Optional[int] = None

class SegmentationResult(BaseModel):
    mask: List[List[int]]  # 2D array representing segmentation mask
    confidence: float
    label: str

class ImageAnalysisRequest(BaseModel):
    image: str = Field(..., description="Base64 encoded image")
    analysis_type: AnalysisType = Field(..., description="Type of analysis to perform")
    options: Optional[Dict[str, Any]] = Field(default={}, description="Additional options")

class ImageAnalysisResponse(BaseModel):
    results: Dict[str, Any]
    confidence: float
    analysis_type: str
    processing_time: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str
