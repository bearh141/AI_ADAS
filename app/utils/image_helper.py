import numpy as np
import cv2

def read_image(file_storage):
    img_bytes = np.frombuffer(file_storage.read(), np.uint8)
    frame = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
    return frame
