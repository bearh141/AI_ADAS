import os
import torch
from ultralytics import YOLO
from app.config.settings import settings
from threading import Lock

_loaded_once = False
_lock = Lock()
loaded_models = {}

def load_models():
    """Load models 1 lần duy nhất."""
    global loaded_models, _loaded_once
    with _lock:
        if _loaded_once:
            return loaded_models
        print("🔹 Loading models...")
        torch.backends.cudnn.benchmark = True
        for name, info in settings.MODELS.items():
            model_path = info.get("path")
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model '{name}' not found at: {model_path}")

            print(f"  → Loading '{name}' model from: {model_path}")
            
            if torch.cuda.is_available():
                model = YOLO(model_path).to("cuda")
                print(f"    • Model '{name}' loaded on GPU.")
            else:
                model = YOLO(model_path)
                print(f"    • Model '{name}' loaded on CPU.")


            loaded_models[name] = {
                "model": model,
                "conf": info.get("conf", 0.5),
                "iou": info.get("iou", 0.45)
            }

        _loaded_once = True
        print("✅ All models loaded successfully!\n")
        print(f"🔹 load model '{name}'")
        return loaded_models

def get_model(name: str):
    """Trả về model đã load (lazy load nếu chưa có)."""
    if not loaded_models:
        load_models()
    model = loaded_models.get(name)
    if not model:
        raise ValueError(f"Model '{name}' not loaded.")
    return model
