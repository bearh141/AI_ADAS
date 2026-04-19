def run_prediction(model_info, frame):
    model = model_info["model"]

    return model.predict(
        source=frame,
        conf=model_info["conf"],
        iou=model_info["iou"],
        imgsz=model_info.get("imgsz", 640),
        max_det=model_info.get("max_det", 100),
        agnostic_nms=model_info.get("agnostic_nms", False),
        half=model_info.get("half", False),
        verbose=False
    )[0]