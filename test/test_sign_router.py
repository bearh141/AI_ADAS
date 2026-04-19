import os
import cv2
import requests
import json
from datetime import datetime

# =============================
# 1️⃣ Cấu hình
# =============================
API_URL = "http://127.0.0.1:8500/sign/predict"   # endpoint của Flask
input_path = "test/images"
base_save_dir = "test/results"

os.makedirs(base_save_dir, exist_ok=True)

# =============================
# 2️⃣ Tạo thư mục cho mỗi lần chạy
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
# 3️⃣ Lấy danh sách ảnh đầu vào
# =============================
valid_ext = [".jpg", ".jpeg", ".png", ".bmp"]
if os.path.isdir(input_path):
    image_files = [
        os.path.join(input_path, f)
        for f in os.listdir(input_path)
        if os.path.splitext(f)[1].lower() in valid_ext
    ]
else:
    image_files = [input_path] if os.path.splitext(input_path)[1].lower() in valid_ext else []

if not image_files:
    raise FileNotFoundError("❌ Không tìm thấy ảnh hợp lệ trong thư mục test/images")

print(f"🖼️ Số ảnh cần test: {len(image_files)}")

# =============================
# 4️⃣ Gửi request và lưu kết quả
# =============================
for idx, image_path in enumerate(image_files, start=1):
    img_name = os.path.splitext(os.path.basename(image_path))[0]
    result_json_path = os.path.join(save_dir, f"{img_name}_result.json")

    # Gửi ảnh đến API
    with open(image_path, "rb") as f:
        files = {"image": (os.path.basename(image_path), f, "image/jpeg")}
        response = requests.post(API_URL, files=files)

    if response.status_code != 200:
        print(f"❌ [{idx}] Lỗi khi gửi {img_name}: {response.status_code}")
        continue

    result = response.json()
    detections = result.get("data", [])

    # Ghi kết quả JSON
    with open(result_json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    # Vẽ bbox lên ảnh gốc
    frame = cv2.imread(image_path)
    for det in detections:
        box = [int(x) for x in det["box"]]
        cls_name = det["class_name"]
        conf = det["confidence"]
        cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
        cv2.putText(frame, f"{cls_name} {conf:.2f}", (box[0], box[1] - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    result_img_path = os.path.join(save_dir, f"{img_name}_result.jpg")
    cv2.imwrite(result_img_path, frame)

    print(f"✅ [{idx}/{len(image_files)}] Đã xử lý: {img_name} ({len(detections)} biển báo)")

# =============================
# 5️⃣ Tổng kết
# =============================
summary_path = os.path.join(save_dir, "summary.txt")
with open(summary_path, "w", encoding="utf-8") as f:
    f.write(f"📦 Run ID: #{run_id}\n")
    f.write(f"🕒 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"📸 Tổng số ảnh test: {len(image_files)}\n\n")
    f.write("Xem kết quả chi tiết trong các file *_result.json / *_result.jpg\n")

print(f"\n🎯 Toàn bộ kết quả của lần chạy #{run_id} nằm trong: {save_dir}")
