# app/routes/drowsy_router.py
from flask import Blueprint, request, jsonify
import time
import base64
import numpy as np
import cv2
import uuid # Thêm thư viện để tạo Session ID tạm thời

# Giả sử DrowsinessDetectorService đã được import đúng
from app.services.drowsy_service import DrowsinessDetectorService as DrowsyDetector

drowsy_bp = Blueprint("drowsy", __name__)

# Tạo 1 instance dùng chung (chỉ chứa logic xử lý, KHÔNG chứa trạng thái session)
detector = DrowsyDetector()

# Dictionary tạm thời để lưu trạng thái session: {session_id: frame_count}
# TRONG THỰC TẾ, CẦN DÙNG REDIS HOẶC DATABASE ĐỂ LƯU TRỮ TRẠNG THÁI NÀY
session_states = {} 


def _bytes_to_cv2_image(b: bytes):
    """Decode ảnh từ bytes -> cv2 BGR image."""
    arr = np.frombuffer(b, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return img


def _base64_to_cv2_image(data: str):
    """
    Nhận:
      - "data:image/jpeg;base64,...."
      - hoặc chuỗi base64 thuần
    -> trả về cv2 image hoặc None nếu lỗi
    """
    if not data:
        return None

    # Nếu là data URL thì cắt prefix "data:...;base64,"
    if "," in data:
        data = data.split(",", 1)[1]

    try:
        img_bytes = base64.b64decode(data)
    except Exception:
        return None

    return _bytes_to_cv2_image(img_bytes)


@drowsy_bp.route("/predict", methods=["POST"])
def drowsy_predict():
    """
    Input: Cần thêm 'session_id' để theo dõi frame_count liên tục.
    {
      "image_base64": "...",
      "session_id": "user-abc-123" 
    }

    Output JSON:
        {
          "is_drowsy": bool,
          "message": str,
          "angle": float, 
          "frame_count": int,
          "latency_ms": int
        }
    """
    t0 = time.time()
    img = None
    session_id = None
    
    # --- Xử lý Input & Session ID ---
    body = {}
    if request.is_json:
        body = request.get_json(silent=True) or {}
        session_id = body.get("session_id")
        b64_str = body.get("image_base64") or body.get("image")
        if b64_str:
            img = _base64_to_cv2_image(b64_str)

    # --- Fallback: multipart file (chỉ nên dùng cho test/setup, vì không có session_id) ---
    if img is None:
        file = request.files.get("image")
        if file:
            img_bytes = file.read()
            img = _bytes_to_cv2_image(img_bytes)
        
        # Nếu không có session_id từ JSON, tạo session ID tạm thời cho file upload
        if not session_id:
             session_id = "temp_" + str(uuid.uuid4())
             
    if img is None:
        return jsonify({"error": "Missing or invalid image (image_base64 or file 'image')"}), 400

    if not session_id:
         return jsonify({"error": "Missing 'session_id' in request body."}), 400
    
    # Lấy frame_count hiện tại từ session
    current_frame_count = session_states.get(session_id, 0)


    try:
        # GỌI HÀM XỬ LÝ CHÍNH ĐÃ SỬA: process_frame(image, current_frame_count)
        # Hứng đủ 4 giá trị trả về
        _img_out, message, angle, new_frame_count = detector.process_frame(img, current_frame_count)

        # CẬP NHẬT TRẠNG THÁI MỚI VÀO SESSION
        session_states[session_id] = new_frame_count

        # Quy ước is_drowsy: khác "AWAKE" và "FOCUS..." là cảnh báo
        is_drowsy = message not in ("AWAKE", "FOCUS - KHONG NHAN DIEN DUOC KHUON MAT")

        resp = {
            "is_drowsy": bool(is_drowsy),
            "message": message,
            "angle": round(angle, 2), # Thêm angle
            "frame_count": int(new_frame_count),
            "session_id": session_id,
            "latency_ms": int((time.time() - t0) * 1000),
        }
        return jsonify(resp), 200

    except Exception as e:
        # Nếu có lỗi, reset frame_count của session để tránh lỗi liên tục
        session_states[session_id] = 0
        return jsonify({"error": f"Internal processing error: {str(e)}", "session_id": session_id}), 500