import base64
import io
from PIL import Image, ImageOps
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

def validate_image(image_data: bytes, max_size_mb: int = 10) -> bool:
    """Validate image data"""
    try:
        # Check file size
        if len(image_data) > max_size_mb * 1024 * 1024:
            raise ValueError(f"Image size exceeds {max_size_mb}MB limit")
        
        # Try to open image
        image = Image.open(io.BytesIO(image_data))
        image.verify()  # Verify image integrity
        
        return True
        
    except Exception as e:
        logger.error(f"Image validation failed: {str(e)}")
        raise ValueError(f"Invalid image: {str(e)}")

def resize_image(image_data: bytes, max_width: int = 1024, max_height: int = 1024) -> bytes:
    """Resize image if it exceeds maximum dimensions"""
    try:
        image = Image.open(io.BytesIO(image_data))
        
        # Check if resize is needed
        if image.width <= max_width and image.height <= max_height:
            return image_data
        
        # Calculate new dimensions maintaining aspect ratio
        ratio = min(max_width / image.width, max_height / image.height)
        new_width = int(image.width * ratio)
        new_height = int(image.height * ratio)
        
        # Resize image
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert back to bytes
        buffered = io.BytesIO()
        resized_image.save(buffered, format=image.format or 'PNG')
        return buffered.getvalue()
        
    except Exception as e:
        logger.error(f"Image resize failed: {str(e)}")
        raise ValueError(f"Failed to resize image: {str(e)}")

def base64_to_image(base64_string: str) -> Image.Image:
    """Convert base64 string to PIL Image"""
    try:
        # Remove data URL prefix if present
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        
        image_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_data))
        return image
        
    except Exception as e:
        logger.error(f"Base64 to image conversion failed: {str(e)}")
        raise ValueError(f"Invalid base64 image: {str(e)}")

def image_to_base64(image: Image.Image, format: str = 'PNG') -> str:
    """Convert PIL Image to base64 string"""
    try:
        buffered = io.BytesIO()
        image.save(buffered, format=format)
        image_str = base64.b64encode(buffered.getvalue()).decode()
        return image_str
        
    except Exception as e:
        logger.error(f"Image to base64 conversion failed: {str(e)}")
        raise ValueError(f"Failed to convert image to base64: {str(e)}")

def get_image_info(image_data: bytes) -> dict:
    """Get image information"""
    try:
        image = Image.open(io.BytesIO(image_data))
        
        return {
            "width": image.width,
            "height": image.height,
            "format": image.format,
            "mode": image.mode,
            "size_bytes": len(image_data)
        }
        
    except Exception as e:
        logger.error(f"Failed to get image info: {str(e)}")
        raise ValueError(f"Invalid image: {str(e)}")

def auto_orient_image(image_data: bytes) -> bytes:
    """Auto-orient image based on EXIF data"""
    try:
        image = Image.open(io.BytesIO(image_data))
        
        # Auto-orient based on EXIF
        oriented_image = ImageOps.exif_transpose(image)
        
        # Convert back to bytes
        buffered = io.BytesIO()
        oriented_image.save(buffered, format=image.format or 'PNG')
        return buffered.getvalue()
        
    except Exception as e:
        logger.error(f"Image orientation failed: {str(e)}")
        # Return original if orientation fails
        return image_data
