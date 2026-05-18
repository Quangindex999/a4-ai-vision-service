from datetime import datetime

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    camera_id: str = Field(..., description="Camera ID")
    image_url: str = Field(..., description="Image URL")
    timestamp: datetime = Field(..., description="Capture timestamp")


class AnalyzeResponse(BaseModel):
    detected: bool
    object: str
    confidence: float = Field(ge=0.0, le=1.0)
    risk_level: str
