"""
Module thuật toán xác định trạng thái buồn ngủ
Kết hợp các chỉ số EAR và MAR để đưa ra cảnh báo buồn ngủ
"""

from ear_calculator import EARCalculator
from mar_calculator import MARCalculator


class DrowsinessDetector:
    """
    Class phát hiện trạng thái buồn ngủ dựa trên EAR và MAR
    """
    
    # Ngưỡng số frame mắt nhắm liên tục để cảnh báo buồn ngủ
    EYE_CLOSED_FRAMES_THRESHOLD = 90  # ~3 giây ở 30 FPS - mắt nhắm thực sự lâu
    
    # Ngưỡng số frame ngáp để cảnh báo
    YAWN_FRAMES_THRESHOLD = 30  # ~1 giây ở 30 FPS - ngáp thực sự
    
    # Ngưỡng số lần ngáp để cảnh báo nghiêm trọng
    YAWN_COUNT_THRESHOLD = 4  # Phải ngáp 4 lần mới cảnh báo
    
    # Điểm buồn ngủ tích lũy
    DROWSINESS_SCORE_THRESHOLD = 200  # Tăng ngưỡng để ít nhạy hơn
    
    def __init__(self):
        """Khởi tạo Drowsiness Detector"""
        self.eye_closed_frames = 0
        self.yawn_frames = 0
        self.drowsiness_score = 0
        self.total_yawns = 0
        self.alert_active = False
        self.pause_scoring_frames = -90  # Số frame còn lại cần tạm dừng tính điểm
    
    def reset(self):
        """Reset tất cả các biến đếm"""
        self.eye_closed_frames = 0
        self.yawn_frames = 0
        self.drowsiness_score = 0
        self.total_yawns = 0
        self.alert_active = False
        # đặt thời gian tạm dừng, cứ 30 frame là 1 giây
        self.pause_scoring_frames = 90
    
    def update(self, ear_value, mar_value):
        """
        Cập nhật trạng thái buồn ngủ dựa trên EAR và MAR
        
        Args:
            ear_value: Giá trị Eye Aspect Ratio
            mar_value: Giá trị Mouth Aspect Ratio
        
        Returns:
            dict: Dictionary chứa thông tin trạng thái
                {
                    'drowsy': bool - Có đang buồn ngủ không,
                    'alert_level': str - Mức độ cảnh báo ('SAFE', 'WARNING', 'DANGER'),
                    'reason': str - Lý do cảnh báo,
                    'ear': float - Giá trị EAR,
                    'mar': float - Giá trị MAR,
                    'eye_closed_frames': int - Số frame mắt nhắm,
                    'total_yawns': int - Tổng số lần ngáp
                }
        """
        # Kiểm tra nếu đang trong thời gian tạm dừng tính điểm
        if self.pause_scoring_frames > 0:
            self.pause_scoring_frames -= 1
            # Vẫn cập nhật giá trị nhưng không tính điểm
            return {
                'drowsy': False,
                'alert_level': 'SAFE',
                'reason': f'Tinh tao ({self.pause_scoring_frames // 30 + 1}s)',
                'ear': ear_value,
                'mar': mar_value,
                'eye_closed_frames': 0,
                'yawn_frames': 0,
                'total_yawns': self.total_yawns,
                'drowsiness_score': 0,
                'alert_active': False
            }
        
        # Kiểm tra mắt nhắm
        eyes_closed = EARCalculator.is_eyes_closed(ear_value)
        
        if eyes_closed:
            self.eye_closed_frames += 1
            self.drowsiness_score += 0.5  # Mỗi frame mắt nhắm +0.5 điểm (chậm hơn)
        else:
            self.eye_closed_frames = 0
            # Giảm dần điểm buồn ngủ khi mắt mở (chậm hơn)
            self.drowsiness_score = max(0, self.drowsiness_score - 0.3)
        
        # Kiểm tra ngáp
        is_yawning = MARCalculator.is_yawning(mar_value)
        
        if is_yawning:
            self.yawn_frames += 1
            if self.yawn_frames >= self.YAWN_FRAMES_THRESHOLD:
                # Đếm một lần ngáp khi đủ số frame
                if self.yawn_frames == self.YAWN_FRAMES_THRESHOLD:
                    self.total_yawns += 1
                    self.drowsiness_score += 3  # Mỗi lần ngáp +3 điểm (ít hơn)
        else:
            self.yawn_frames = 0
        
        # Xác định mức độ cảnh báo
        alert_level = 'SAFE'
        reason = 'Tinh tao'
        drowsy = False
        
        if self.eye_closed_frames >= self.EYE_CLOSED_FRAMES_THRESHOLD:
            # Cảnh báo mắt nhắm quá lâu
            alert_level = 'DANGER'
            reason = 'Mắt nhắm quá lâu!'
            drowsy = True
            self.alert_active = True
        elif self.total_yawns >= self.YAWN_COUNT_THRESHOLD:
            # Cảnh báo ngáp nhiều lần - MỨC NGHIÊM TRỌNG
            alert_level = 'DANGER'
            reason = f'Đã ngáp {self.total_yawns} lần - Buồn ngủ!'
            drowsy = True
            self.alert_active = True
        elif self.drowsiness_score >= self.DROWSINESS_SCORE_THRESHOLD:
            # Cảnh báo điểm buồn ngủ cao
            alert_level = 'DANGER'
            reason = 'Dấu hiệu buồn ngủ mạnh!'
            drowsy = True
            self.alert_active = True
        elif self.drowsiness_score >= self.DROWSINESS_SCORE_THRESHOLD * 0.5:
            # Cảnh báo nhẹ
            alert_level = 'WARNING'
            reason = 'Có dấu hiệu mệt mỏi'
            drowsy = False
        else:
            self.alert_active = False
        
        return {
            'drowsy': drowsy,
            'alert_level': alert_level,
            'reason': reason,
            'ear': ear_value,
            'mar': mar_value,
            'eye_closed_frames': self.eye_closed_frames,
            'yawn_frames': self.yawn_frames,
            'total_yawns': self.total_yawns,
            'drowsiness_score': self.drowsiness_score,
            'alert_active': self.alert_active
        }
    
    def get_status_text(self, status):
        """
        Tạo text hiển thị trạng thái chi tiết
        
        Args:
            status: Dictionary trạng thái từ hàm update()
        
        Returns:
            str: Text hiển thị trạng thái
        """
        if status['alert_level'] == 'DANGER':
            return f" CẢNH BÁO: {status['reason']}"
        elif status['alert_level'] == 'WARNING':
            return f" CHÚ Ý: {status['reason']}"
        else:
            return f" {status['reason']}"
    
    def get_status_color(self, status):
        """
        Lấy màu sắc cho trạng thái
        
        Args:
            status: Dictionary trạng thái từ hàm update()
        
        Returns:
            tuple: (R, G, B, A) màu sắc
        """
        if status['alert_level'] == 'DANGER':
            return (1, 0, 0, 1)  # Đỏ
        elif status['alert_level'] == 'WARNING':
            return (1, 0.65, 0, 1)  # Cam
        else:
            return (0, 1, 0, 1)  # Xanh lá
