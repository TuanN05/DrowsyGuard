"""
Module nhận diện khuôn mặt sử dụng Mediapipe Face Mesh
"""

import mediapipe as mp
import cv2


class FaceDetector:
    """
    Class nhận diện khuôn mặt và trích xuất các landmark
    """
    
    # Chỉ số landmarks của các phần trên khuôn mặt
    LEFT_EYE_INDICES = [362, 385, 387, 263, 373, 380]
    RIGHT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
    
    # Landmarks miệng cho MAR (8 điểm chính):
    # [0] góc trong trái (78), [1] góc trong phải (308)
    # [2] trên giữa (13), [3] dưới giữa (14) 
    # [4] trên trái phụ (81), [5] dưới trái phụ (178)
    # [6] trên phải phụ (311), [7] dưới phải phụ (402)
    MOUTH_INDICES = [78, 308, 13, 14, 81, 178, 311, 402]
    
    def __init__(self, max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        """
        Khởi tạo Face Detector
        
        Args:
            max_num_faces: Số lượng khuôn mặt tối đa cần phát hiện
            min_detection_confidence: Ngưỡng tin cậy tối thiểu để phát hiện
            min_tracking_confidence: Ngưỡng tin cậy tối thiểu để tracking
        """
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=max_num_faces,
            refine_landmarks=True,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
    
    def detect_face(self, frame):
        """
        Phát hiện khuôn mặt trong frame
        
        Args:
            frame: Frame ảnh BGR từ camera
            
        Returns:
            tuple: (face_detected, landmarks_dict) 
                    face_detected: True nếu phát hiện khuôn mặt
                    landmarks_dict: Dictionary chứa tọa độ các điểm landmark
        """
        # Chuyển BGR sang RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Phát hiện khuôn mặt
        results = self.face_mesh.process(rgb_frame)
        
        if not results.multi_face_landmarks:
            return False, None
        
        # Lấy landmarks của khuôn mặt đầu tiên
        face_landmarks = results.multi_face_landmarks[0]
        
        # Chuyển đổi landmarks sang tọa độ pixel
        h, w, _ = frame.shape
        landmarks = []
        for lm in face_landmarks.landmark:
            x, y = int(lm.x * w), int(lm.y * h)
            landmarks.append((x, y))
        
        # Trích xuất landmarks cho các vùng quan trọng
        landmarks_dict = {
            'left_eye': [landmarks[i] for i in self.LEFT_EYE_INDICES],
            'right_eye': [landmarks[i] for i in self.RIGHT_EYE_INDICES],
            'mouth': [landmarks[i] for i in self.MOUTH_INDICES],
            'all': landmarks
        }
        
        return True, landmarks_dict
    
    def draw_landmarks(self, frame, landmarks_dict, draw_eyes=True, draw_mouth=True):
        """
        Vẽ các landmark lên frame
        
        Args:
            frame: Frame ảnh
            landmarks_dict: Dictionary chứa tọa độ landmarks
            draw_eyes: Vẽ viền mắt
            draw_mouth: Vẽ viền miệng
            
        Returns:
            frame: Frame đã vẽ landmarks
        """
        if landmarks_dict is None:
            return frame
        
        import numpy as np
        
        if draw_eyes:
            # Vẽ viền mắt trái
            cv2.polylines(frame, [np.array(landmarks_dict['left_eye'])], 
                            True, (0, 255, 0), 1)
            # Vẽ viền mắt phải
            cv2.polylines(frame, [np.array(landmarks_dict['right_eye'])], 
                            True, (0, 255, 0), 1)
        
        if draw_mouth:
            # Vẽ viền miệng
            cv2.polylines(frame, [np.array(landmarks_dict['mouth'])], 
                            True, (255, 0, 0), 1)
        
        return frame
    
    def release(self):
        """Giải phóng tài nguyên"""
        self.face_mesh.close()
