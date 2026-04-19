import os
from ultralytics import YOLO

def run_lane_detection(image_folder_name='images', conf_threshold=0.25):
    """
    Hàm thực hiện test model nhận diện làn đường.
    
    Args:
        image_folder_name (str): Tên folder chứa ảnh nằm trong thư mục 'test'. Mặc định là 'images'.
        conf_threshold (float): Ngưỡng tin cậy (confidence) để vẽ box.
        
    Returns:
        str: Đường dẫn đến folder chứa kết quả.
    """
    
    # --- 1. THIẾT LẬP ĐƯỜNG DẪN ---
    # Lấy đường dẫn hiện tại của file này (đang nằm trong folder 'test')
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Đường dẫn model: từ 'test' ra ngoài cha '..', vào 'models/lane/best.pt'
    model_path = os.path.join(current_dir, '..', 'models', 'lane', 'best.pt')
    
    # Đường dẫn ảnh input: 'test/{image_folder_name}'
    source_images = os.path.join(current_dir, image_folder_name)
    
    # Đường dẫn output: 'test/results'
    output_dir = os.path.join(current_dir, 'results')

    # --- 2. KIỂM TRA ---
    if not os.path.exists(model_path):
        print(f"❌ [Lỗi] Không tìm thấy model tại: {model_path}")
        return None
    
    if not os.path.exists(source_images):
        print(f"❌ [Lỗi] Không tìm thấy folder ảnh tại: {source_images}")
        print(f"👉 Vui lòng tạo folder '{image_folder_name}' trong thư mục 'test' và thêm ảnh vào.")
        return None

    # --- 3. LOAD MODEL & PREDICT ---
    print(f"🔄 Đang load model: {os.path.basename(model_path)}...")
    try:
        model = YOLO(model_path)
        
        print(f"📷 Đang xử lý ảnh trong: {source_images}...")
        results = model.predict(
            source=source_images,
            save=True,
            conf=conf_threshold,
            project=output_dir,
            name='lane_prediction',
            exist_ok=True
        )
        
        result_path = os.path.join(output_dir, 'lane_prediction')
        print(f"✅ Xong! Kết quả lưu tại: {result_path}")
        return result_path

    except Exception as e:
        print(f"❌ Lỗi Runtime: {e}")
        return None