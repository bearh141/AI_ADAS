from ultralytics import YOLO
import cv2
import os
from datetime import datetime

# =============================
# 1️⃣ Cấu hình đường dẫn
# =============================
model_path = "models/sign/best.pt"   # model đã train
input_path = "test/images"           # có thể là 1 ảnh hoặc thư mục
base_save_dir = "test/results"       # nơi lưu kết quả

os.makedirs(base_save_dir, exist_ok=True)

# =============================
# 2️⃣ Tạo thư mục mới cho mỗi lần chạy
# =============================
def create_new_run_folder(base_dir):
    existing = [d for d in os.listdir(base_dir) if d.startswith("run_#")]
    run_ids = []
    for d in existing:
        try:
            run_ids.append(int(d.replace("run_#", "")))
        except:
            pass
    next_id = max(run_ids) + 1 if run_ids else 1
    new_dir = os.path.join(base_dir, f"run_#{next_id}")
    os.makedirs(new_dir, exist_ok=True)
    return new_dir, next_id

save_dir, run_id = create_new_run_folder(base_save_dir)
print(f"🆕 Tạo thư mục lưu kết quả: {save_dir}")

# =============================
# 3️⃣ Load model và nhãn
# =============================
model = YOLO(model_path)
names = model.names

# =============================
# 4️⃣ Lấy danh sách ảnh đầu vào
# =============================
valid_ext = [".jpg", ".jpeg", ".png", ".bmp"]
if os.path.isdir(input_path):
    image_files = [os.path.join(input_path, f) for f in os.listdir(input_path) if os.path.splitext(f)[1].lower() in valid_ext]
else:
    image_files = [input_path] if os.path.splitext(input_path)[1].lower() in valid_ext else []

if not image_files:
    raise FileNotFoundError("❌ Không tìm thấy ảnh hợp lệ trong đường dẫn test.")

print(f"🖼️ Số ảnh cần test: {len(image_files)}")

# =============================
# 5️⃣ Chạy predict và lưu kết quả
# =============================
for idx, image_path in enumerate(image_files, start=1):
    results = model.predict(source=image_path, conf=0.45, iou=0.45,verbose=False)
    r = results[0]

    # Tên file gốc
    img_name = os.path.splitext(os.path.basename(image_path))[0]
    result_img_path = os.path.join(save_dir, f"{img_name}_result.jpg")
    result_txt_path = os.path.join(save_dir, f"{img_name}_result.txt")

    # Lưu ảnh kết quả
    im_array = r.plot()
    cv2.imwrite(result_img_path, im_array)

    # Chuẩn bị dữ liệu bounding box
    boxes_data = []
    for box in r.boxes:
        cls_id = int(box.cls[0])
        label = names.get(cls_id, f"class_{cls_id}")
        conf = float(box.conf[0])
        xyxy = [round(x, 1) for x in box.xyxy[0].tolist()]
        boxes_data.append((cls_id, label, conf, xyxy))

    # Căn lề động
    max_label_len = max(len(label) for _, label, _, _ in boxes_data) if boxes_data else 10

    # Ghi file TXT
    with open(result_txt_path, "w", encoding="utf-8") as f:
        f.write(f"📦 Run ID: #{run_id}\n")
        f.write(f"🕒 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"📸 Image: {os.path.basename(image_path)}\n\n")
        f.write(f"{'Class':<7} {'Label':<{max_label_len+3}} {'Conf':<8} {'BBox (x1,y1,x2,y2)'}\n")
        f.write("-" * (25 + max_label_len) + "\n")
        for cls_id, label, conf, xyxy in boxes_data:
            f.write(f"{cls_id:<7} {label:<{max_label_len+3}} {conf:<8.2f} {str(xyxy)}\n")

    print(f"✅ [{idx}/{len(image_files)}] Đã xử lý: {img_name}")

print(f"\n🎯 Toàn bộ kết quả của lần chạy #{run_id} nằm trong: {save_dir}")
