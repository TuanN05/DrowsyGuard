"""
Module tính toán Mouth Aspect Ratio (MAR) để phát hiện ngáp
"""

from scipy.spatial import distance


class MARCalculator:
    """
    Class tính toán Mouth Aspect Ratio (MAR)
    MAR được sử dụng để xác định trạng thái ngáp
    """
    
    # Ngưỡng MAR để xác định ngáp
    # MAR > YAWN_THRESHOLD = Đang ngáp
    # MAR <= YAWN_THRESHOLD = Không ngáp
    YAWN_THRESHOLD = 0.6
    
    @staticmethod
    def calculate_mar(mouth_landmarks):
        """
        Tính Mouth Aspect Ratio (MAR)
        
        Công thức MAR:
        MAR = (||p2-p8|| + ||p3-p7|| + ||p4-p6||) / (2 * ||p1-p5||)
        
        Trong đó:
        - p1, p5: Điểm góc trái và góc phải miệng
        - p2, p3, p4: Các điểm trên môi trên
        - p6, p7, p8: Các điểm dưới môi dưới
        
        Args:
            mouth_landmarks: List các tọa độ (x, y) của 8 điểm landmark miệng
                           Thứ tự: [góc_trái, trên1, trên2, trên3, dưới1, dưới2, dưới3, góc_phải]
        
        Returns:
            float: Giá trị MAR (thường trong khoảng 0.3 - 1.0)
        """
        # Đảm bảo có đủ điểm landmarks
        if len(mouth_landmarks) < 8:
            return 0.0
        
        # Tính khoảng cách dọc (vertical) - độ mở miệng
        A = distance.euclidean(mouth_landmarks[1], mouth_landmarks[7])  # trên1 - dưới3
        B = distance.euclidean(mouth_landmarks[2], mouth_landmarks[6])  # trên2 - dưới2
        C = distance.euclidean(mouth_landmarks[3], mouth_landmarks[5])  # trên3 - dưới1
        
        # Tính khoảng cách ngang (horizontal) - độ rộng miệng
        D = distance.euclidean(mouth_landmarks[0], mouth_landmarks[4])  # góc_trái - góc_phải
        
        # Công thức MAR
        mar = (A + B + C) / (2.0 * D)
        return mar
    
    @staticmethod
    def is_yawning(mar_value):
        """
        Kiểm tra xem có đang ngáp hay không
        
        Args:
            mar_value: Giá trị MAR
        
        Returns:
            bool: True nếu đang ngáp, False nếu không ngáp
        """
        return mar_value > MARCalculator.YAWN_THRESHOLD
    
    @staticmethod
    def get_mouth_state(mar_value):
        """
        Lấy trạng thái miệng dưới dạng chuỗi
        
        Args:
            mar_value: Giá trị MAR
        
        Returns:
            str: "YAWNING" hoặc "NORMAL"
        """
        return "YAWNING" if MARCalculator.is_yawning(mar_value) else "NORMAL"
