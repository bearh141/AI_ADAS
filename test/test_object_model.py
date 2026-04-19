import sys
import os

current_file_path = os.path.abspath(__file__)
# Lấy thư mục cha của file này (thư mục 'test')
test_dir = os.path.dirname(current_file_path)
project_root = os.path.dirname(test_dir)

if project_root not in sys.path:
    sys.path.insert(0, project_root)

import cv2
from app.config.settings import settings
from app.services.model_loader import get_model

INPUT_DIR = os.path.join(project_root, 'test\\images\\objects') 
RESULT_DIR = os.path.join(project_root, 'test\\results\\object_model')

def get_next_run_folder(base_dir, run_name="object_run"):
    """Tạo folder run#n tăng dần"""
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    i = 1
    while True:
        run_folder = os.path.join(base_dir, f"{run_name}#{i}")
        if not os.path.exists(run_folder):
            os.makedirs(run_folder)
            return run_folder
        i += 1

def main():
    # 1. Xác định tên model cần dùng
    if not hasattr(settings, 'MODELS') or not settings.MODELS:
        print("Config không có settings.MODELS hoặc dictionary rỗng.")
        return
    
    # Lấy key đầu tiên trong file config
    model_name = list(settings.MODELS.keys())[1]
    
    try:
        print(f"Bắt đầu test với model key: {model_name}")
        # Gọi hàm get_model từ service của bạn
        model_info = get_model(model_name)
        model = model_info["model"]
        conf_thres = model_info["conf"]
        
    except Exception as e:
        print(f"Lỗi khởi tạo model: {e}")
        return

    # 2. Kiểm tra input
    if not os.path.exists(INPUT_DIR):
        print(f"Không tìm thấy folder input: {INPUT_DIR}")
        return
    
    valid_exts = ('.jpg', '.jpeg', '.png', '.bmp')
    image_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(valid_exts)]
    
    if not image_files:
        print("Không có file ảnh nào để test.")
        return

    # 3. Tạo folder output
    save_dir = get_next_run_folder(RESULT_DIR)
    print(f"Kết quả sẽ được lưu tại: {save_dir}")

    # 4. Xử lý từng ảnh
    for img_name in image_files:
        img_path = os.path.join(INPUT_DIR, img_name)
        
        # Predict
        results = model.predict(source=img_path, conf=conf_thres, save=False, verbose=False)
        result = results[0]
        
        # --- A. Lưu ảnh (Image) ---
        annotated_frame = result.plot()
        cv2.imwrite(os.path.join(save_dir, img_name), annotated_frame)
        
        # --- B. Lưu file thông số (TXT) ---
        txt_filename = os.path.splitext(img_name)[0] + ".txt"
        with open(os.path.join(save_dir, txt_filename), "w", encoding="utf-8") as f:
            # Header
            f.write(f"Image: {img_name}\n")
            f.write(f"Model: {model_name} | Conf Thres: {conf_thres}\n")
            f.write(f"{'ID':<5} {'Class Name':<20} {'Conf':<10} {'BBox [x1, y1, x2, y2]'}\n")
            f.write("-" * 70 + "\n")
            
            if len(result.boxes) == 0:
                f.write("No objects detected.\n")
            else:
                for box in result.boxes:
                    cls_id = int(box.cls[0])
                    cls_name = model.names[cls_id]
                    conf = float(box.conf[0])
                    xyxy = [int(x) for x in box.xyxy[0].tolist()]
                    
                    f.write(f"{cls_id:<5} {cls_name:<20} {conf:.4f}     {xyxy}\n")
        
        print(f"Processed: {img_name}")

    print(f"\nTest hoàn tất! Kiểm tra folder: {save_dir}")

if __name__ == "__main__":
    main()