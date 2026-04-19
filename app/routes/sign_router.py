from flask import Blueprint, request, jsonify
from app.services.sign_service import sign_prediction
import imghdr
import time

sign_bp = Blueprint("sign", __name__)

@sign_bp.route("/predict", methods=["POST"])
def sign_predict():
    start_time = time.time()
    try:
        data = request.get_json()
        if not data or "image_base64" not in data:
            return jsonify({"data": []})

        base64_url = data["image_base64"]

        # Decode ảnh từ base64
        try:
            import base64, cv2
            import numpy as np

            # Tách bỏ prefix "data:image/jpeg;base64," nếu có
            if "," in base64_url:
                base64_url = base64_url.split(",")[1]

            img_bytes = base64.b64decode(base64_url)
            np_arr = np.frombuffer(img_bytes, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        except Exception as e:
            print("Decode base64 failed:", e)
            return jsonify({"data": []})

        if frame is None:
            print("Không tạo được ảnh từ base64")
            return jsonify({"data": []})

        # YOLO detect
        detections = sign_prediction(frame)
        print(f"Phát hiện {len(detections)} biển báo")

        processing_time = time.time() - start_time
        return jsonify({"data": detections, "processing_time": processing_time})

    except Exception as e:
        print("Error:", e)
        return jsonify({"data": []})