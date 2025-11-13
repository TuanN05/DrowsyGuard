"""
Module tính toán Eye Aspect Ratio (EAR) để phát hiện mắt nhắm
"""

from scipy.spatial import distance


class EARCalculator:
    """
    Class tính toán Eye Aspect Ratio (EAR)
    EAR được sử dụng để xác định trạng thái mở/nhắm mắt
    """
    
    # Ngưỡng EAR để xác định mắt nhắm
    # EAR < EYE_CLOSED_THRESHOLD = Mắt nhắm
    # EAR >= EYE_CLOSED_THRESHOLD = Mắt mở
    EYE_CLOSED_THRESHOLD = 0.25
    
    @staticmethod
    def calculate_ear(eye_landmarks):
        """
        Tính Eye Aspect Ratio (EAR) cho một mắt
        
        Công thức EAR:
        EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)
        
        Trong đó:
        - p1, p4: Điểm đầu và cuối mắt (góc ngoài và góc trong)
        - p2, p3, p5, p6: Các điểm trên và dưới mắt
        
        Args:
            eye_landmarks: List các tọa độ (x, y) của 6 điểm landmark mắt
                            Thứ tự: [góc_ngoài, trên1, trên2, góc_trong, dưới1, dưới2]
        
        Returns:
            float: Giá trị EAR (thường trong khoảng 0.15 - 0.35)
        """
        # Tính khoảng cách dọc (vertical)
        A = distance.euclidean(eye_landmarks[1], eye_landmarks[5])  # trên1 - dưới2
        B = distance.euclidean(eye_landmarks[2], eye_landmarks[4])  # trên2 - dưới1
        
        # Tính khoảng cách ngang (horizontal)
        C = distance.euclidean(eye_landmarks[0], eye_landmarks[3])  # góc_ngoài - góc_trong
        
        # Công thức EAR
        ear = (A + B) / (2.0 * C)
        return ear
    
    @staticmethod
    def calculate_avg_ear(left_eye_landmarks, right_eye_landmarks):
        """
        Tính EAR trung bình của cả hai mắt
        
        Args:
            left_eye_landmarks: List tọa độ 6 điểm landmark mắt trái
            right_eye_landmarks: List tọa độ 6 điểm landmark mắt phải
        
        Returns:
            float: EAR trung bình
        """
        left_ear = EARCalculator.calculate_ear(left_eye_landmarks)
        right_ear = EARCalculator.calculate_ear(right_eye_landmarks)
        avg_ear = (left_ear + right_ear) / 2.0
        return avg_ear
    
    @staticmethod
    def is_eyes_closed(ear_value):
        """
        Kiểm tra xem mắt có đang nhắm hay không
        
        Args:
            ear_value: Giá trị EAR
        
        Returns:
            bool: True nếu mắt đang nhắm, False nếu mắt đang mở
        """
        return ear_value < EARCalculator.EYE_CLOSED_THRESHOLD
    
    @staticmethod
    def get_eye_state(ear_value):
        """
        Lấy trạng thái mắt dưới dạng chuỗi
        
        Args:
            ear_value: Giá trị EAR
        
        Returns:
            str: "CLOSED" hoặc "OPEN"
        """
        return "CLOSED" if EARCalculator.is_eyes_closed(ear_value) else "OPEN"
