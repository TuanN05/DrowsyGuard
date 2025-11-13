"""
Module xử lý video từ camera
Kết hợp tất cả các module để phân tích trạng thái buồn ngủ
"""

import cv2
import numpy as np
from face_detector import FaceDetector
from ear_calculator import EARCalculator
from mar_calculator import MARCalculator
from drowsiness_detector import DrowsinessDetector


class CameraProcessor:
    """
    Class xử lý video từ camera và phân tích trạng thái buồn ngủ
    """
    
    def __init__(self, camera_index=0):
        """
        Khởi tạo Camera Processor
        
        Args:
            camera_index: Index của camera (thường 0 cho camera trước)
        """
        self.camera_index = camera_index
        self.capture = None
        self.is_running = False
        
        # Khởi tạo các module
        self.face_detector = FaceDetector()
        self.drowsiness_detector = DrowsinessDetector()
        
        # Trạng thái hiện tại
        self.current_status = None
    
    def start(self):
        """
        Bắt đầu xử lý camera
        
        Returns:
            bool: True nếu khởi động thành công, False nếu thất bại
        """
        try:
            self.capture = cv2.VideoCapture(self.camera_index)
            if not self.capture.isOpened():
                return False
            
            self.is_running = True
            self.drowsiness_detector.reset()
            return True
        except Exception as e:
            print(f"Lỗi khi khởi động camera: {e}")
            return False
    
    def stop(self):
        """Dừng xử lý camera"""
        self.is_running = False
        if self.capture:
            self.capture.release()
            self.capture = None
        self.drowsiness_detector.reset()
    
    def process_frame(self):
        """
        Xử lý một frame từ camera
        
        Returns:
            tuple: (success, frame, status)
                success: True nếu xử lý thành công
                frame: Frame đã được xử lý và vẽ thông tin
                status: Dictionary chứa thông tin trạng thái (từ DrowsinessDetector)
        """
        if not self.is_running or self.capture is None:
            return False, None, None
        
        # Đọc frame từ camera
        ret, frame = self.capture.read()
        if not ret:
            return False, None, None
        
        # Lật ảnh để hiển thị như gương
        frame = cv2.flip(frame, 1)
        
        # Phát hiện khuôn mặt
        face_detected, landmarks = self.face_detector.detect_face(frame)
        
        if face_detected and landmarks:
            # Tính EAR (Eye Aspect Ratio)
            ear_value = EARCalculator.calculate_avg_ear(
                landmarks['left_eye'],
                landmarks['right_eye']
            )
            
            # Tính MAR (Mouth Aspect Ratio)
            mar_value = MARCalculator.calculate_mar(landmarks['mouth'])
            
            # Cập nhật trạng thái buồn ngủ
            status = self.drowsiness_detector.update(ear_value, mar_value)
            self.current_status = status
            
            # Vẽ landmarks lên frame
            self.face_detector.draw_landmarks(frame, landmarks, 
                                            draw_eyes=True, draw_mouth=True)
            
            # Vẽ thông tin lên frame
            self._draw_info_on_frame(frame, status)
            
            return True, frame, status
        else:
            # Không phát hiện khuôn mặt
            self._draw_no_face_warning(frame)
            status = {
                'drowsy': False,
                'alert_level': 'NO_FACE',
                'reason': 'Không phát hiện khuôn mặt',
                'ear': 0,
                'mar': 0,
                'eye_closed_frames': 0,
                'yawn_frames': 0,
                'total_yawns': 0,
                'drowsiness_score': 0,
                'alert_active': False
            }
            return True, frame, status
    
    def _draw_info_on_frame(self, frame, status):
        """
        Vẽ thông tin trạng thái lên frame
        
        Args:
            frame: Frame ảnh
            status: Dictionary trạng thái từ DrowsinessDetector
        """
        h, w, _ = frame.shape
        
        # Màu sắc theo mức độ cảnh báo
        if status['alert_level'] == 'DANGER':
            color = (0, 0, 255)  # Đỏ
            text = f"CANH BAO: {status['reason']}"
        elif status['alert_level'] == 'WARNING':
            color = (0, 165, 255)  # Cam
            text = f"CHU Y: {status['reason']}"
        else:
            color = (0, 255, 0)  # Xanh lá
            text = status['reason']
        
        # Vẽ text trạng thái
        cv2.putText(frame, text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        # Vẽ thông tin EAR
        cv2.putText(frame, f"EAR: {status['ear']:.2f}", (w - 150, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Vẽ thông tin MAR
        cv2.putText(frame, f"MAR: {status['mar']:.2f}", (w - 150, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Vẽ số lần ngáp
        if status['total_yawns'] > 0:
            cv2.putText(frame, f"Ngap: {status['total_yawns']}", (w - 150, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        # Vẽ thanh điểm buồn ngủ
        score_percentage = min(100, (status['drowsiness_score'] / 
                                    DrowsinessDetector.DROWSINESS_SCORE_THRESHOLD) * 100)
        bar_width = int((w - 40) * score_percentage / 100)
        
        # Màu thanh theo mức độ
        if score_percentage >= 100:
            bar_color = (0, 0, 255)
        elif score_percentage >= 50:
            bar_color = (0, 165, 255)
        else:
            bar_color = (0, 255, 0)
        
        cv2.rectangle(frame, (20, h - 40), (20 + bar_width, h - 20), bar_color, -1)
        cv2.rectangle(frame, (20, h - 40), (w - 20, h - 20), (255, 255, 255), 2)
        cv2.putText(frame, f"Buon ngu: {int(score_percentage)}%", (25, h - 45),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Vẽ cảnh báo lớn nếu ở mức DANGER
        if status['alert_level'] == 'DANGER':
            cv2.putText(frame, ">>> BUON NGU! <<<", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    
    def _draw_no_face_warning(self, frame):
        """
        Vẽ cảnh báo không phát hiện khuôn mặt
        
        Args:
            frame: Frame ảnh
        """
        cv2.putText(frame, "Khong phat hien khuon mat", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    
    def get_current_status(self):
        """
        Lấy trạng thái hiện tại
        
        Returns:
            dict: Dictionary trạng thái hiện tại hoặc None
        """
        return self.current_status
    
    def release(self):
        """Giải phóng tài nguyên"""
        self.stop()
        self.face_detector.release()
