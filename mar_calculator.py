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
        Tính Mouth Aspect Ratio (MAR) - Chuẩn Mediapipe Face Mesh
        
        Công thức MAR:
        MAR = (||top-bottom|| + ||top_left-bottom_left|| + ||top_right-bottom_right||) / (3 * ||left-right||)
        
        Landmarks Mediapipe (thứ tự thực tế):
        - [0] góc trong trái (78), [1] góc trong phải (308)
        - [2] trên giữa (13), [3] dưới giữa (14) 
        - [4] trên trái phụ (81), [5] dưới trái phụ (178)
        - [6] trên phải phụ (311), [7] dưới phải phụ (402)
        
        Args:
            mouth_landmarks: List các tọa độ (x, y) của 8 điểm landmark miệng
                            Thứ tự: [góc_trong_trái(78), góc_trong_phải(308), trên_giữa(13), dưới_giữa(14), 
                                    trên_trái_phụ(81), dưới_trái_phụ(178), trên_phải_phụ(311), dưới_phải_phụ(402)]
        
        Returns:
            float: Giá trị MAR (thường 0.2-0.8, ngáp khi > 0.6)
        """
        # Đảm bảo có đủ điểm landmarks
        if len(mouth_landmarks) < 8:
            return 0.0
        
        # Lấy các điểm landmarks (thứ tự: [78, 308, 13, 14, 81, 178, 311, 402])
        left_corner = mouth_landmarks[0]      # 78 (Góc trong trái miệng)
        right_corner = mouth_landmarks[1]     # 308 (Góc trong phải miệng)
        
        top_mid = mouth_landmarks[2]          # 13 (Đỉnh môi trên giữa)
        bottom_mid = mouth_landmarks[3]       # 14 (Đáy môi dưới giữa)
        
        top_left = mouth_landmarks[4]         # 81 (Điểm phụ trên trái)
        bottom_left = mouth_landmarks[5]      # 178 (Điểm phụ dưới trái - đối xứng với 81)
        
        top_right = mouth_landmarks[6]        # 311 (Điểm phụ trên phải)
        bottom_right = mouth_landmarks[7]     # 402 (Điểm phụ dưới phải - đối xứng với 311)
        
        # Tính khoảng cách dọc (vertical) - độ mở miệng
        A = distance.euclidean(top_mid, bottom_mid)          # Giữa miệng
        B = distance.euclidean(top_left, bottom_left)        # Bên trái
        C = distance.euclidean(top_right, bottom_right)      # Bên phải
        
        # Tính khoảng cách ngang (horizontal) - độ rộng miệng
        D = distance.euclidean(left_corner, right_corner)    # Góc trái đến góc phải
        
        # Tránh chia cho 0
        if D < 0.01:
            return 0.0
        
        # Công thức MAR chuẩn
        mar = (A + B + C) / (3.0 * D)
        return mar
    
    @staticmethod
    def is_yawning(mar_value):
        """
        Kiểm tra xem có đang ngáp hay không
            mar_value: Giá trị MAR
        
            bool: True nếu đang ngáp, False nếu không ngáp
        """
        return mar_value > MARCalculator.YAWN_THRESHOLD
    
    @staticmethod
    def get_mouth_state(mar_value):
        """
        Lấy trạng thái miệng dưới dạng chuỗi
        
            mar_value: Giá trị MAR
        
            str: "YAWNING" hoặc "NORMAL"
        """
        return "YAWNING" if MARCalculator.is_yawning(mar_value) else "NORMAL"
