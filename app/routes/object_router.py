from flask import Blueprint, request, jsonify
import time
import base64
import cv2
import numpy as np

# Import hàm logic vừa tạo
from app.services.object_service import object_prediction 

object_bp = Blueprint('object', __name__)

@object_bp.route('/predict', methods=['POST'])
def predict():
    start_time = time.time()
    try:
        data = request.get_json()
        if not data or 'image_base64' not in data:
            return jsonify({"data": []}) # Trả về rỗng an toàn giống Sign

        image_base64 = data['image_base64']
        
        # Decode ảnh
        try:
            if "," in image_base64:
                image_base64 = image_base64.split(",")[1]
            
            image_bytes = base64.b64decode(image_base64)
            np_arr = np.frombuffer(image_bytes, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        except Exception as e:
            print("Decode Error:", e)
            return jsonify({"data": []})

        if frame is None:
            return jsonify({"data": []})

        # --- GỌI SERVICE ---
        detections = object_prediction(frame)
        
        # Trả về format chuẩn giống Sign: { data: [...], processing_time: ... }
        process_time = time.time() - start_time
        return jsonify({
            "data": detections,
            "processing_time": process_time
        })

    except Exception as e:
        print(f"Router Error: {e}")
        return jsonify({"data": []})