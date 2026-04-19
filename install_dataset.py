import os
from roboflow import Roboflow
import dotenv
import shutil

dotenv.load_dotenv()

rf = Roboflow(api_key=os.getenv("ROBOFLOWKEY"))
project = rf.workspace(os.getenv("ROBOWORKSPACE")).project(os.getenv("ROBOPROJECT"))
version = project.version(os.getenv("ROVOVERSION"))
dataset = version.download(os.getenv("DATASETFORMAT"))

old_name = dataset.location
new_name = os.path.join(os.getcwd(), "datasets")  # đường dẫn tuyệt đối, tránh lỗi

# Nếu thư mục 'datasets' đã tồn tại -> xóa hoặc ghi đè
if os.path.exists(new_name):
    print("⚠️ Thư mục 'datasets' đã tồn tại, đang ghi đè...")
    shutil.rmtree(new_name)

# Dùng shutil.move thay vì os.rename (an toàn hơn trên Windows)
shutil.move(old_name, new_name)

print(f"✅ Đã đổi tên và di chuyển thư mục thành: {new_name}")
