"""
ROI (Region of Interest) Middleware
Giới hạn vùng nhận diện cho từng module AI:
  - lane  : vùng dưới-giữa frame (làn đường đang đi)
  - sign  : vùng trên-giữa frame (biển báo phía trước, bỏ 2 bên)
  - object: vùng trung tâm phía trước

Tỉ lệ ROI được đọc từ config.yaml (mục roi:), fallback về giá trị mặc định nếu không có.
"""

import cv2
import numpy as np
from typing import Literal

ModuleType = Literal["lane", "sign", "object"]

_DEFAULT_ROI = {
    "lane":   (0.15, 0.50, 0.85, 1.00),
    "sign":   (0.20, 0.00, 0.80, 0.60),
    "object": (0.10, 0.30, 0.90, 0.90),
}


def _load_roi_presets() -> dict:
    """Đọc ROI presets từ config.yaml, fallback về _DEFAULT_ROI."""
    try:
        import yaml
        with open("config.yaml", "r") as f:
            cfg = yaml.safe_load(f)
        roi_cfg = cfg.get("roi", {})
        presets = {}
        for module, default in _DEFAULT_ROI.items():
            raw = roi_cfg.get(module)
            presets[module] = tuple(raw) if raw and len(raw) == 4 else default
        return presets
    except Exception:
        return dict(_DEFAULT_ROI)


_ROI_PRESETS: dict = _load_roi_presets()


def _get_roi_config(module: ModuleType, frame_h: int, frame_w: int) -> dict:
    rx1, ry1, rx2, ry2 = _ROI_PRESETS[module]
    return {
        "x1": int(rx1 * frame_w),
        "y1": int(ry1 * frame_h),
        "x2": int(rx2 * frame_w),
        "y2": int(ry2 * frame_h),
    }


def crop_roi(frame: np.ndarray, module: ModuleType) -> tuple[np.ndarray, dict]:
    h, w = frame.shape[:2]
    roi = _get_roi_config(module, h, w)
    cropped = frame[roi["y1"]:roi["y2"], roi["x1"]:roi["x2"]]
    return cropped, {"offset_x": roi["x1"], "offset_y": roi["y1"]}


def remap_detections(detections: list[dict], roi_meta: dict, module: ModuleType) -> list[dict]:
    ox, oy = roi_meta["offset_x"], roi_meta["offset_y"]

    remapped = []
    for det in detections:
        det = det.copy()

        if "box" in det:
            x1, y1, x2, y2 = det["box"]
            det["box"] = [x1 + ox, y1 + oy, x2 + ox, y2 + oy]

        elif "bbox" in det:
            x1, y1, x2, y2 = det["bbox"]
            det["bbox"] = [x1 + ox, y1 + oy, x2 + ox, y2 + oy]

        remapped.append(det)

    return remapped


def apply_roi(frame: np.ndarray, module: ModuleType) -> tuple[np.ndarray, dict]:
    return crop_roi(frame, module)


def draw_roi_debug(frame: np.ndarray, module: ModuleType) -> np.ndarray:
    COLOR = {"lane": (0, 255, 0), "sign": (255, 165, 0), "object": (0, 165, 255)}
    h, w = frame.shape[:2]
    roi = _get_roi_config(module, h, w)
    vis = frame.copy()
    cv2.rectangle(vis, (roi["x1"], roi["y1"]), (roi["x2"], roi["y2"]),
                  COLOR.get(module, (255, 255, 255)), 2)
    cv2.putText(vis, f"ROI:{module}", (roi["x1"] + 4, roi["y1"] + 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR.get(module, (255, 255, 255)), 2)
    return vis
