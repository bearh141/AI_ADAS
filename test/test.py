import cv2
import os
import glob
import sys
import traceback

# --- 1. SETUP ĐƯỜNG DẪN & IMPORT ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Import hàm test Lane (cùng thư mục test/)
try:
    from test_lane_detection import run_lane_detection
except ImportError:
    print(" Cảnh báo: Không tìm thấy file 'test_lane_detection.py' cùng thư mục.")

# Import class DrowsyDetector (từ app/services/)
try:
    from app.services.drowsy_service import DrowsinessDetectorService
except ImportError as e:
    print(f" Lỗi Import: Không thể tìm thấy class DrowsinessDetectorService.")
    print(f"Chi tiết lỗi: {e}")
    # Không exit ngay để vẫn có thể chạy test lane nếu muốn
    DrowsinessDetectorService = None 


# --- 2. HÀM TEST DROWSINESS ---
def run_drowsiness_test():
    print("\n" + "="*40)
    print("  BẮT ĐẦU TEST: DROWSINESS DETECTION")
    print("="*40)

    if DrowsinessDetectorService is None:
        print(" Bỏ qua test Drowsiness do lỗi import library.")
        return

    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(base_dir, "images")
    output_dir = os.path.join(base_dir, "results", "drowsy_results") # Gom riêng vào folder con cho gọn

    os.makedirs(output_dir, exist_ok=True)

    # Lấy ảnh
    image_paths = glob.glob(os.path.join(input_dir, "*.jpg")) + glob.glob(os.path.join(input_dir, "*.png"))

    if not image_paths:
        print(f" Không tìm thấy ảnh nào trong: {input_dir}")
        return

    print(f" Tìm thấy {len(image_paths)} ảnh. Đang xử lý...")

    try:
        detector = DrowsinessDetectorService()
    except Exception as e:
        print(f" Lỗi khởi tạo detector: {e}")
        return

    for img_path in image_paths:
        filename = os.path.basename(img_path)
        image = cv2.imread(img_path)

        if image is None:
            continue
        
        try:
            # Chạy phân tích
            annotated_image, message, angle, _= detector.process_frame(image, current_frame_count=0)
            ratio = "N/A (See Image)"
            
            print(f" {filename}: {message} | Angle: {angle:.2f}")

            # Lưu ảnh
            output_path = os.path.join(output_dir, f"res_{filename}")
            cv2.imwrite(output_path, annotated_image)

        except Exception as e:
            print(f" Lỗi file {filename}: {e}")

    print(f"✅ Hoàn thành test Drowsiness. Kết quả tại: {output_dir}")


# --- 3. MAIN EXECUTION (MENU LỰA CHỌN) ---
if __name__ == "__main__":
    print("\n" + "="*40)
    print(" CHỌN CHỨC NĂNG MUỐN TEST:")
    print("1. Test Cảnh báo buồn ngủ (Drowsiness)")
    print("2. Test Nhận diện làn đường (Lane Detection)")
    print("3. Chạy cả hai (All)")
    print("="*40)
    
    choice = input("👉 Nhập số (1, 2 hoặc 3): ").strip()

    if choice == '1':
        run_drowsiness_test()
        
    elif choice == '2':
        # Gọi hàm test Lane
        try:
            # Lưu ý: Import function này ở đầu file rồi nhé
            if 'run_lane_detection' in globals():
                run_lane_detection()
            else:
                from test_lane_detection import run_lane_detection
                run_lane_detection()
        except Exception as e:
            print(f"Lỗi khi chạy Lane detection: {e}")

    elif choice == '3':
        run_drowsiness_test()
        print("\n" + "-"*30 + "\n")
        try:
            if 'run_lane_detection' in globals():
                run_lane_detection()
            else:
                from test_lane_detection import run_lane_detection
                run_lane_detection()
        except Exception as e:
            print(f"Lỗi khi chạy Lane detection: {e}")
            
    else:
        print("Lựa chọn không hợp lệ. Vui lòng chạy lại và nhập 1, 2 hoặc 3.")

    print("\n === KẾT THÚC ===")