# 🧠 AI_ADAS Server

---

## ⚙️ Chức năng chính
- Phát hiện làn đường
- Nhận dạng biển báo giao thông  
- Phát hiện buồn ngủ 
- Phát hiện vật thể
- Cấu hình thông qua `config.yaml`

---

## 🧩 Cấu trúc thư mục dự án
```
├── 📂 app/
│   ├── 📄 __init__.py
│   ├── 📂 config/
│   │   ├── 📄 __init__.py
│   │   └── 📄 settings.py
│   ├── 📄 main.py
│   ├── 📂 routes/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 drowsy_router.py
│   │   ├── 📄 lane_router.py
│   │   ├── 📄 object_router.py
│   │   └── 📄 sign_router.py
│   ├── 📂 services/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 drowsy_service.py
│   │   ├── 📄 lane_service.py
│   │   ├── 📄 model_loader.py
│   │   ├── 📄 object_service.py
│   │   └── 📄 sign_service.py
│   └── 📂 utils/
│       └── 📄 image_helper.py
├── 📄 config.yaml
├── 📄 generate_changelog.py
├── 📄 generate_readme.py
├── 📄 install_dataset.py
├── 📂 models/
│   ├── 📂 lane/
│   ├── 📂 object/
│   └── 📂 sign/
├── 📄 README.md
├── 📄 requirements.txt
├── 📄 run.py
├── 📂 test/
│   ├── 📄 test.py
│   ├── 📄 test_lane_detection.py
│   ├── 📄 test_object_model.py
│   ├── 📄 test_sign_detection.py
│   └── 📄 test_sign_router.py
```

---

## 📘 Hướng dẫn cài đặt và sử dụng

### 1. Tạo môi trường ảo
Tạo môi trường ảo trong thư mục gốc của dự án:
```bash
cd AI_ADAS
py -3.11 -m venv venv-ai-adas
```

### 2. Kích hoạt môi trường ảo
Kích hoạt môi trường ảo bằng một trong hai lệnh sau:

**Lệnh 1:**
```bash
venv-ai-adas/Scripts/activate
```

**Lệnh 2 (Nếu lệnh 1 không hoạt động):**
```bash
source venv-ai-adas/Scripts/activate
```

### 3. Cài đặt thư viện cần thiết
Cài đặt toàn bộ thư viện từ tệp `requirements.txt`:
```bash
pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu130
```

### 4. Cài thêm thư viện mới (nếu cần)
```bash
pip install <tên_thư_viện>
pip freeze > requirements.txt
```

### 5. Chạy server AI
```bash
python run.py
```

Server chạy tại:
```
http://localhost:8500
```

---

## 🧠 Các mô hình AI khả dụng
- **sign** → `models/sign/best.pt`
- **object** → `models/object/best.pt`
- **lane** → `models/lane/best.pt`


---

## 🕒 Generated
2025-12-12 21:31:02

---

> File này được tạo tự động bởi `generate_readme.py`. Đừng chỉnh sửa thủ công!
