from app.services.model_loader import get_model
from app.utils.convert_classname import get_vietnamese_name
from app.utils.run_predict import run_prediction
from app.middleware.roi_filter import apply_roi, remap_detections

def object_prediction(frame):
    try:
        model_info = get_model("object")

        # Giới hạn vùng nhận diện: vùng trung tâm phía trước
        roi_frame, roi_meta = apply_roi(frame, "object")

        results = run_prediction(model_info, roi_frame)
        
        detections = []

        for box in results.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])

            label = get_vietnamese_name(cls_id, model_type='object')

            detections.append({
                "bbox": [int(x1), int(y1), int(x2), int(y2)],
                "label": label,
                "confidence": round(conf, 2)
            })

        # Map tọa độ bbox về frame gốc
        return remap_detections(detections, roi_meta, "object")

    except Exception as e:
        print(f"Error in object_prediction: {e}")
        return []