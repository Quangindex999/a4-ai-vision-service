import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# TODO: Đặt link API của nhóm B5, B6 vào đây khi họ làm xong
B5_ANALYTICS_URL = "http://b5-analytics-service/api/stats"
B6_CORE_BUSINESS_URL = "http://b6-core-business-service/api/alert"

def process_image(image_url: str) -> dict:
    """
    Hàm lõi: Chạy AI phân tích ảnh.
    Hiện tại đang Mock data, sau này sẽ cắm YOLO/OpenCV vào đây.
    """
    return {
        "detected": True,
        "object": "person",
        "confidence": 0.95,
        "risk_level": "medium"
    }

def notify_other_services(result_data: dict, camera_id: str, timestamp: str):
    """
    Hàm chạy ngầm: Bắn dữ liệu sang B5 và B6.
    """
    payload = {
        "camera_id": camera_id,
        "timestamp": timestamp,
        "analysis_result": result_data
    }
    
    # --- 1. GỬI CHO B5 (ANALYTICS) ---
    try:
        logger.info(f"🔄 [BACKGROUND] Đang gửi dữ liệu thống kê cho B5...")
        # import requests
        # requests.post(B5_ANALYTICS_URL, json=payload, timeout=5)
        logger.info(f"✅ [BACKGROUND] Giả lập gửi B5 thành công!")
    except Exception as e:
        logger.error(f"❌ [BACKGROUND] Lỗi gửi B5: {e}")

    # --- 2. GỬI CHO B6 (CORE BUSINESS) ---
    if result_data.get("risk_level") in ["medium", "high"]:
        try:
            logger.info(f"⚠️ [BACKGROUND] Phát hiện rủi ro '{result_data['risk_level']}'. Đang bắn cảnh báo cho B6...")
            # import requests
            # requests.post(B6_CORE_BUSINESS_URL, json=payload, timeout=5)
            logger.info(f"✅ [BACKGROUND] Giả lập gửi cảnh báo B6 thành công!")
        except Exception as e:
            logger.error(f"❌ [BACKGROUND] Lỗi cảnh báo B6: {e}")