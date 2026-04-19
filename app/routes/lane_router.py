from flask import Blueprint, request, jsonify
from app.services.lane_service import lane_prediction
import base64, cv2
import numpy as np

lane_bp = Blueprint("lane", __name__)

@lane_bp.route("/predict", methods=["POST"])
def lane_predict():
    try:
        data = request.get_json()
        if not data or "image_base64" not in data:
            return jsonify({"data": []})

        base64_url = data["image_base64"]

        # Decode ảnh từ base64
        try:
            # Tách bỏ prefix nếu có
            if "," in base64_url:
                base64_url = base64_url.split(",")[1]

            img_bytes = base64.b64decode(base64_url)
            np_arr = np.frombuffer(img_bytes, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        except Exception as e:
            print("Decode base64 lane failed:", e)
            return jsonify({"data": []})

        if frame is None:
            print("Không tạo được ảnh lane từ base64")
            return jsonify({"data": []})

        # YOLO detect lane
        detections = lane_prediction(frame)
        print(f"Phát hiện {len(detections)} làn đường")

        return jsonify(detections)

    except Exception as e:
        print("Lane Error:", e)
        return jsonify([])