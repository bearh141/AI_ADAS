# app/utils/convert_classname.py
from typing import Union, Dict

# ==========================================
# 1. DỮ LIỆU (DATA DEFINITION)
# ==========================================

# --- DATASET 1: LANE (Làn đường) ---
LANE_CLASSES: Dict[int, str] = {
    0: "Vạch trắng: Đứt và Liền",
    1: "Vạch vàng: Đứt và Liền",
    2: "Vạch trắng đứt",
    3: "Vạch vàng đứt",
    4: "Vạch đôi liền trắng",
    5: "Vạch đôi liền vàng",
    6: "Hướng rẽ trái",
    7: "Hướng rẽ phải",
    8: "Vạch liền trắng",
    9: "Vạch liền vàng",
    10: "Hướng đi thẳng"
}

# --- DATASET 2: SIGN (Biển báo) ---
# Danh sách biển báo từ labels.txt
_SIGN_LIST = [
    "Bến xe buýt", "Các xe chỉ được rẽ phải", "Các xe chỉ được rẽ trái", "Cấm đi ngược chiều",
    "Cấm đỗ xe", "Cấm dừng xe và đỗ xe", "Cấm quay đầu xe", "Cấm rẽ phải", "Cấm xe ô tô",
    "Cấm xe tải", "Cấm xe tải trên 2.5 tấn", "Chiều cao an toàn", "Chỗ quay xe", "Đi chậm",
    "Đường giao nhau cung cấp", "Đường một chiều", "Giao nhau với đường không ưu tiên",
    "Giao nhau với đường không ưu tiên bên phải", "Giao nhau với đường không ưu tiên bên trái",
    "Giao nhau với đường sắt có rào chắn", "Giao nhau với đường ưu tiên", "Hạn chế chiều cao",
    "Người đi bộ cắt ngang", "Nhiều chỗ ngoặt liên tiếp bên phải", "Nhiều chỗ ngoặt liên tiếp bên trái",
    "Nơi giao nhau chạy theo vòng xuyến", "Tốc độ tối đa cho phép", "Trẻ em", "Vòng chướng ngại vật sang phải",
    "Vòng chướng ngại vật sang trái", "Chỗ ngoặt nguy hiểm vòng bên phải", "Chỗ ngoặt nguy hiểm vòng bên trái",
    "Cấm xe khách trên 16 chỗ", "Giới hạn tốc độ 40", "Giao nhau có tín hiệu đèn", "Hạn chế trọng tải xe",
    "Xe chỉ được đi thẳng và rẽ phải", "Cấm rẽ trái và rẽ phải", "Biển báo phụ biểu thị thời gian",
    "Biển báo phụ xe tải", "Đường đôi", "Biển báo phụ phạm vi tác dụng của biển", "Cẩn thận điện giật",
    "Biển báo gộp làn đường", "Biển báo phụ khoảng cách đến đối tượng báo hiệu",
    "Làn đường dành cho xe máy và xe đạp", "Biển báo phụ xe khách", "Hướng đi trên mỗi làn đường phải theo",
    "Cấm đi thẳng", "Chợ", "Cấm xe ô tô khách", "Nơi đường sắt giao vuông góc với đường bộ",
    "Nơi người đi bộ sang ngang", "Hết khu vực cấm xe ô tô tải", "Đường cấm", "Cấm ô tô rẽ phải",
    "Cấm ô tô rẽ trái", "Cấm mô tô", "Cấm ô tô và mô tô", "Cấm xe chở hàng nguy hiểm",
    "Cấm ô tô khách và ô tô tải", "Cấm ô tô, máy kéo kéo moóc và sơ mi rơ moóc", "Cấm máy kéo",
    "Cấm đi xe đạp", "Cấm xe đạp thồ", "Cấm xe gắn máy", "Cấm xe lam", "Cấm xe lôi máy",
    "Cấm xe 3 bánh loại không có động cơ", "Cấm người đi bộ", "Cấm xe người kéo, đẩy", "Cấm xe súc vật kéo",
    "Hạn chế trọng lượng xe", "Hạn chế trọng lượng trục xe", "Hạn chế chiều ngang",
    "Hạn chế chiều dài ô tô, máy kéo kéo moóc, sơ mi rơ moóc", "Cự ly tối thiểu giữa 2 xe", "Dừng lại",
    "Cấm ô tô quay đầu xe", "Cấm rẽ trái và quay đầu xe", "Cấm rẽ phải và quay đầu xe",
    "Cấm ô tô rẽ trái và quay đầu xe", "Cấm ô tô rẽ phải và quay đầu xe", "Cấm vượt",
    "Cấm ô tô tải vượt", "Cấm sử dụng còi", "Kiểm tra", "Cấm đỗ xe ngày lẻ", "Cấm đỗ xe ngày chẵn",
    "Nhường đường cho xe cơ giới đi ngược chiều qua đường hẹp", "Hết cấm vượt", "Hết hạn chế tốc độ tối đa",
    "Hết tất cả các lệnh cấm", "Cấm đi thẳng và rẽ trái", "Cấm đi thẳng và rẽ phải", "Cấm xe công nông",
    "Đường giao nhau", "Hạn chế chiều dài", "Cấm rẽ trái", "Chỗ ngoặt nguy hiểm liên tiếp",
    "Đường bị hẹp", "Đường bị hẹp bên trái", "Đường bị hẹp bên phải", "Đường hai chiều",
    "Giao nhau với đường sắt không có rào chắn", "Cầu hẹp", "Cầu tạm", "Cầu xoay cầu cất",
    "Đường ngầm", "Bến phà", "Cửa chui", "Đường không bằng phẳng", "Đường trơn", "Gia súc",
    "Gió ngang", "Nguy hiểm khác", "Giao nhau với đường 2 chiều", "Hết đường đôi", "Cầu vồng",
    "Đường cao tốc phía trước", "Đường cáp điện phía trước", "Đường hầm", "Thôn bản",
    "Đoạn đường hay xảy ra tai nạn", "Chướng ngại vật", "Hướng đi thẳng phải theo",
    "Hướng đi trái phải theo", "Hướng đi phải phải theo", "Các xe chỉ được đi thẳng và rẽ phải",
    "Các xe chỉ được đi thẳng và rẽ trái", "Các xe chỉ được rẽ trái và phải",
    "Hướng phải đi vòng sang phải", "Hướng phải đi vòng sang trái", "Đường dành cho người đi bộ",
    "Tốc độ tối thiểu", "Hạn chế tốc độ tối thiểu", "Tuyến đường cầu vượt cắt qua", "Ấn còi",
    "Được rẽ phải khi đèn đỏ", "Được đi thẳng khi đèn đỏ", "Đường dành cho xe thô sơ",
    "Đường người đi xe đạp cắt ngang", "Đường bị hẹp cả hai bên", "Đá lở", "Cấm ô tô mô tô 3 bánh",
    "Cấm xe khách và ô tô tải", "Cấm ô tô kéo moóc", "Đường dành cho xe ô tô",
    "Hết đường dành cho xe ô tô", "Hết tốc độ tối thiểu", "Được rẽ trái và quay đầu",
    "Biển số hiệu đường bộ", "Bắt đầu đường ưu tiên", "Hết đường ưu tiên", "Đường cụt",
    "Được ưu tiên qua đường hẹp", "Khu vực quay xe", "Cầu vượt qua đường cho người đi bộ",
    "Bệnh viện", "Khu vực cấm", "Hết khu vực cấm", "Khu vực cấm đỗ xe", "Hết khu vực cấm đỗ xe",
    "Khu vực dừng xe", "Hết khu vực dừng xe", "Khu vực hạn chế tốc độ", "Hết khu vực hạn chế tốc độ",
    "Cảnh sát giao thông", "Bến xe điện", "Có hầm chui", "Hết hầm chui", "Có người đi bộ",
    "Có cấm tải", "Nhà nghỉ lưu động", "Nơi nghỉ mát", "Đường cứu nạn", "Đường nhập làn xe",
    "Đường ưu tiên", "Đường hết ưu tiên", "Hướng đi xe hàng nguy hiểm", "Tắc nghẽn giao thông",
    "Sỏi đá bắn lên", "Nơi giao nhau với đường tàu điện", "Chỗ ngoặt bên trái", "Chỗ ngoặt bên phải",
    "Lề đường nguy hiểm", "Đường dành cho ô tô", "Đường ô tô và mô tô", "Hết đường dành cho ô tô",
    "Hết đường cho ô tô và mô tô", "Đường cụt bên phải", "Đường cụt bên trái", "Đường cụt phía trước",
    "Nơi đỗ xe", "Làn xe ô tô khách", "Đường có làn xe ô tô khách", "Rẽ ra đường có làn xe ô tô khách",
    "Chỉ hướng đường", "Lối đi đường vòng tránh", "Chỉ hướng phải đi cho từng loại xe",
    "Lối đi ở những chỗ cấm rẽ", "Bắt đầu khu đông dân cư", "Chỉ dẫn địa giới", "Hết khu đông dân cư",
    "Di tích lịch sử", "Cầu cho người đi bộ", "Khách sạn", "Cửa hàng ăn uống", "Điện thoại",
    "Nơi rửa xe", "Trạm cung cấp xăng dầu", "Trạm sửa chữa", "Trạm cấp cứu", "Đường cao tốc",
    "Hết đường cao tốc", "Tốc độ trên đường cao tốc", "Tên cầu", "Đoạn đường thi công",
    "Công trường phía trước", "Đường cho người tàn tật", "Phân biệt địa điểm", "Xe kéo moóc",
    "Cầu vượt liên thông", "Trạm kiểm tra tải trọng", "Nhập làn", "Biển hướng rẽ", "Nguy cơ lật xe",
    "Hết đường dành cho người đi bộ", "Hết đường dành cho xe thô sơ", "Cấm xe đạp và xe gắn máy",
    "Phân làn", "Đường dành cho xe máy", "Đường dành cho xe ô tô xe máy",
    "Xe chở hàng nguy hiểm chỉ được rẽ trái", "Xe chở hàng nguy hiểm chỉ được rẽ phải",
    "Xe chở hàng nguy hiểm chỉ được đi thẳng", "Có thể đi vòng sang trái hoặc phải",
    "Kết thúc đường hầm", "Cấm xe khách trên 30 chỗ", "Điểm dừng xe buýt", "Tuyến đường xuyên A17",
    "Làn đường cho ô tô và xe tải", "Làn đường cho ô tô và xe máy", "Làn đường cho xe máy và xe đạp",
    "Làn đường cho xe ô tô", "Làn đi thẳng rẽ phải", "Làn đi thẳng", "Làn rẽ trái", "Làn rẽ phải",
    "Bãi đỗ xe cách 400m", "Bãi đỗ xe cách đường thẳng 200m và bãi đỗ xe bên trái cách 100m",
    "Cấm xe mô tô và xe máy", "Đi chậm chú ý quan sát", "Đoạn đường thường xuyên giám sát tốc độ",
    "Bãi đỗ xe", "Cho phép đỗ xe ngoài giờ cao điểm", "Biển báo hiệu giao nhau với đường ưu tiên",
    "Quốc lộ 1", "Hiệu lực với xe tải 2.5 tấn", "Hiệu lực với xe khách", "Hiệu lực với xe tải",
    "Cấm xe tải 5 tấn", "Làn ô tô", "Làn ô tô xe máy", "Làn xe máy xe đạp", "Biển phụ xe gắn máy xe đạp",
    "Bãi đỗ xe", "Gộp làn", "Biển phụ thu phí đỗ xe", "Biển phụ trừ xe buýt",
    "Biển khu vực thời gian cấm xe khách", "Biển khu vực thời gian cấm xe tải",
    "Biển phụ quy định loại xe khách", "Biển đèn tín hiệu cho người đi bộ",
    "Biển phụ khu vực đoàn trả khách", "Hạn chế trọng tải 17 tấn", "Biển khu vực cấm đỗ xe",
    "Biển chỉ dẫn đường một chiều", "Biển phụ thời gian", "Biển phụ đỗ xe ngoài giờ cao điểm",
    "Biển phụ hướng tác dụng", "Biển chỉ dẫn hướng đi khoảng cách", "Biển phụ ô tô",
    "Biển chỉ dẫn dành cho người đi bộ sang ngang", "Biển cấm đỗ xe ngày chẵn"
]
SIGN_CLASSES: Dict[int, str] = dict(enumerate(_SIGN_LIST))

# --- DATASET 3: OBJECT/OBSTACLE (Vật cản) ---
# Dựa trên data.yaml: ['bicycle', 'bike', 'car', 'human', 'priorityvehicle']
_OBJECT_LIST = [
    "Xe đạp",           # 0: bicycle
    "Xe máy",           # 1: bike
    "Ô tô",             # 2: car
    "Người đi bộ",      # 3: human
    "Xe ưu tiên"        # 4: priorityvehicle
]
OBJECT_CLASSES: Dict[int, str] = dict(enumerate(_OBJECT_LIST))


# ==========================================
# 2. CẤU HÌNH MAPPING (CONFIGURATION)
# ==========================================

MODEL_REGISTRY = {
    'lane': LANE_CLASSES,
    'sign': SIGN_CLASSES,
    'object': OBJECT_CLASSES
}

# ==========================================
# 3. HÀM XỬ LÝ CHÍNH
# ==========================================

def get_vietnamese_name(class_id: Union[int, str], model_type: str = 'sign') -> str:
    """
    Chuyển đổi Class ID thành tên Tiếng Việt dựa trên loại model.
    
    Args:
        class_id (int/str): ID trả về từ model.
        model_type (str): 'lane' | 'sign' | 'object'.
        
    Returns:
        str: Tên tiếng Việt tương ứng.
    """
    # 1. Lấy bộ dữ liệu (dataset) tương ứng với model_type
    target_dataset = MODEL_REGISTRY.get(model_type)
    
    if target_dataset is None:
        valid_keys = ", ".join(MODEL_REGISTRY.keys())
        return f"Model '{model_type}' chưa hỗ trợ. (Hỗ trợ: {valid_keys})"

    # 2. Tra cứu ID trong dataset
    try:
        idx = int(class_id)
        return target_dataset.get(idx, f"Không xác định (ID: {idx})")
    except (ValueError, TypeError):
        return "Lỗi định dạng ID"