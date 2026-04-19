import mediapipe as mp
from scipy.spatial import distance as dis
import cv2
import math
import numpy as np

# --- Class Dịch vụ Chính (Duy trì cấu trúc an toàn cho luồng) ---

class DrowsinessDetectorService:
    # ... (Phần __init__ giữ nguyên)
    def __init__(self) -> None:
        self.face_mesh = mp.solutions.face_mesh
        self.draw_utils = mp.solutions.drawing_utils
        
        # Cấu hình MediaPipe (giữ nguyên)
        self.STATIC_IMAGE = False
        self.MAX_NO_FACES = 2
        self.DETECTION_CONFIDENCE = 0.6
        self.TRACKING_CONFIDENCE = 0.5
        self.COLOR_RED = (0, 0, 255)
        self.COLOR_BLUE = (255, 0, 0)
        self.COLOR_GREEN = (0, 255, 0)
        
        # Danh sách các điểm mốc (Giữ nguyên)
        self.RIGHT_EYE_TOP_BOTTOM = [159, 145] # Vertical points for right eye
        self.RIGHT_EYE_LEFT_RIGHT = [133, 33]  # Horizontal points for right eye
        self.LEFT_EYE_TOP_BOTTOM = [386, 374]  # Vertical points for left eye
        self.LEFT_EYE_LEFT_RIGHT = [263, 362]  # Horizontal points for left eye
        self.FACE = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400,
                     377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]

        self.face_model = self.face_mesh.FaceMesh(static_image_mode=self.STATIC_IMAGE,
                                                 max_num_faces=self.MAX_NO_FACES,
                                                 min_detection_confidence=self.DETECTION_CONFIDENCE,
                                                 min_tracking_confidence=self.TRACKING_CONFIDENCE)
        
        # Ngưỡng EAR: Theo bài PyImageSearch, ngưỡng này thường là 0.25 (hoặc 0.3)
        self.EYE_AR_THRESH = 0.25 
        
        # Ngưỡng frame liên tục: Bài PyImageSearch thường dùng 15-20 frames
        self.EYE_AR_CONSEC_FRAMES = 18 

    def euclidean_distance(self, image, top, bottom):
        """Tính khoảng cách Euclidean giữa hai điểm mốc."""
        height, width = image.shape[0:2]
        point1 = int(top.x * width), int(top.y * height)
        point2 = int(bottom.x * width), int(bottom.y * height)
        distance = dis.euclidean(point1, point2)
        return distance

    def get_eye_aspect_ratio(self, image, outputs, top_bottom, left_right):
        """Tính Eye Aspect Ratio (EAR) theo công thức chuẩn."""
        landmark = outputs.multi_face_landmarks[0]
        
        # Khoảng cách dọc (Vertical) (Tử số)
        top = landmark.landmark[top_bottom[0]]
        bottom = landmark.landmark[top_bottom[1]]
        vertical_dis = self.euclidean_distance(image, top, bottom)
        
        # Khoảng cách ngang (Horizontal) (Mẫu số)
        left = landmark.landmark[left_right[0]]
        right = landmark.landmark[left_right[1]]
        horizontal_dis = self.euclidean_distance(image, left, right)
        
        # EAR = Vertical / Horizontal
        # Thay vì (Left_Right / Top_Bottom) như code gốc, ta dùng (Top_Bottom / Left_Right)
        ear = vertical_dis / (horizontal_dis + 0.0001)
        return ear # Trả về EAR (không phải ratio)

    # ... (Các hàm draw_landmarks, draw_eye_line_and_calculate_angle giữ nguyên)

    def draw_landmarks(self, image, outputs, land_mark, color):
        """Vẽ các điểm mốc lên ảnh."""
        height, width = image.shape[:2]
        for face_index in land_mark:
            point = outputs.multi_face_landmarks[0].landmark[face_index]
            point_scale = (int(point.x * width), int(point.y * height))
            cv2.circle(image, point_scale, 2, color, 1)

    def draw_eye_line_and_calculate_angle(self, image, outputs):
        """Vẽ đường thẳng nối hai mắt và tính góc quay đầu."""
        height, width = image.shape[:2]
        landmark = outputs.multi_face_landmarks[0]
        
        right_eye_left_point = landmark.landmark[self.RIGHT_EYE_LEFT_RIGHT[1]]
        left_eye_right_point = landmark.landmark[self.LEFT_EYE_LEFT_RIGHT[0]]
        
        point1 = (int(right_eye_left_point.x * width), int(right_eye_left_point.y * height))
        point2 = (int(left_eye_right_point.x * width), int(left_eye_right_point.y * height))
        
        cv2.line(image, point1, point2, self.COLOR_BLUE, 2)
        
        dx = point2[0] - point1[0]
        dy = point2[1] - point1[1]
        
        angle_h = math.degrees(math.atan2(dy, dx))
        angle = 180 - abs(angle_h) if angle_h > 0 else abs(angle_h) 
        
        cv2.putText(image, f'Angle: {round(angle, 2)}', (point1[0], point1[1] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, self.COLOR_BLUE, 1, cv2.LINE_AA)
        
        return image, angle

    def process_frame(self, image: np.ndarray, current_frame_count: int = 0):
        """
        Phương thức chính để xử lý khung hình theo thuật toán EAR.
        
        Args:
            image (numpy.ndarray): Khung hình đầu vào (BGR).
            current_frame_count (int): Số frame liên tiếp hiện tại mắt đang đóng.

        Returns:
            tuple: (image, message, angle, new_frame_count)
        """
        angle = 0.0 
        new_frame_count = current_frame_count
        message = 'AWAKE'
        
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        outputs = self.face_model.process(image_rgb)
        
        if outputs.multi_face_landmarks:
            # 1. Vẽ các điểm mốc (Giữ nguyên)
            self.draw_landmarks(image, outputs, self.FACE, self.COLOR_GREEN)
            # ... (vẽ các điểm mắt khác)

            # 2. Tính EAR
            ear_left = self.get_eye_aspect_ratio(image, outputs, self.LEFT_EYE_TOP_BOTTOM, self.LEFT_EYE_LEFT_RIGHT)
            ear_right = self.get_eye_aspect_ratio(image, outputs, self.RIGHT_EYE_TOP_BOTTOM, self.RIGHT_EYE_LEFT_RIGHT)
            avg_ear = round((ear_left + ear_right) / 2.0, 2)

            # 3. Tính góc quay đầu
            image, angle = self.draw_eye_line_and_calculate_angle(image, outputs)

            # 4. Logic phát hiện ngủ gật theo EAR
            if avg_ear < self.EYE_AR_THRESH: # Nếu EAR thấp hơn ngưỡng (mắt đóng)
                new_frame_count += 1  # Tăng bộ đếm frame
                message = 'Drowsy detected...' # Tạm thời
            else:
                new_frame_count = 0
                message = 'AWAKE'
            
            # Cảnh báo dựa trên số frame liên tục
            print("new_frame_count", new_frame_count)
            print("EYE_AR_CONSEC_FRAMES", self.EYE_AR_CONSEC_FRAMES)
            if new_frame_count >= self.EYE_AR_CONSEC_FRAMES:

                # Phân loại theo góc quay đầu
                if angle > 165: 
                    message = 'CANH BAO TAI XE DANG NGU GUC SANG PHAI'
                elif angle < 15: 
                    message = 'CANH BAO TAI XE DANG NGU GUC SANG TRAI'
                else: 
                    message = 'CANH BAO TAI XE DANG NGU GAT'
                
        else:
            message = 'FOCUS - KHONG NHAN DIEN DUOC KHUON MAT'
            new_frame_count = 0
            angle = 0.0

        # Vẽ trạng thái lên ảnh
        cv2.putText(image, f'STATE: {message} (EAR: {avg_ear if "avg_ear" in locals() else 0})', 
                    (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 
                    (0, 255, 0) if message == 'AWAKE' else (0, 0, 255), 2, cv2.LINE_AA)
        
        frame_count = new_frame_count

        # Trả về 4 kết quả
        return image, message, angle, frame_count