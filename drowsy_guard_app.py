"""
DrowsyGuard - Ứng dụng phát hiện buồn ngủ khi lái xe
Yêu cầu: Python 3.8+, Kivy, OpenCV, Mediapipe
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.audio import SoundLoader
import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial import distance

class DrowsyGuardLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # Khởi tạo biến
        self.capture = None
        self.is_monitoring = False
        self.eye_closed_frames = 0
        self.ALARM_THRESHOLD = 20  # Số frame mắt nhắm liên tục để cảnh báo
        
        # Khởi tạo Mediapipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Chỉ số landmarks của mắt trong Mediapipe
        self.LEFT_EYE = [362, 385, 387, 263, 373, 380]
        self.RIGHT_EYE = [33, 160, 158, 133, 153, 144]
        
        # Tải âm thanh cảnh báo (tạo beep sound đơn giản)
        self.setup_alarm()
        
        # === GIAO DIỆN ===
        
        # Tiêu đề
        title = Label(
            text='DrowsyGuard',
            font_size='32sp',
            bold=True,
            size_hint=(1, 0.1),
            color=(0.2, 0.6, 1, 1)
        )
        self.add_widget(title)
        
        # Màn hình camera
        self.img_widget = Image(size_hint=(1, 0.6))
        self.add_widget(self.img_widget)
        
        # Nhãn trạng thái
        self.status_label = Label(
            text='Trạng thái: Chưa bắt đầu',
            font_size='20sp',
            size_hint=(1, 0.1),
            color=(1, 1, 1, 1)
        )
        self.add_widget(self.status_label)
        
        # Nút điều khiển
        btn_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        
        self.start_btn = Button(
            text='Bắt đầu giám sát',
            background_color=(0.2, 0.8, 0.2, 1),
            font_size='18sp',
            bold=True
        )
        self.start_btn.bind(on_press=self.start_monitoring)
        
        self.stop_btn = Button(
            text='Dừng',
            background_color=(0.8, 0.2, 0.2, 1),
            font_size='18sp',
            bold=True,
            disabled=True
        )
        self.stop_btn.bind(on_press=self.stop_monitoring)
        
        btn_layout.add_widget(self.start_btn)
        btn_layout.add_widget(self.stop_btn)
        self.add_widget(btn_layout)
        
        # Hướng dẫn
        guide = Label(
            text='Đặt điện thoại sao cho khuôn mặt bạn hiện rõ trước camera',
            font_size='14sp',
            size_hint=(1, 0.1),
            color=(0.7, 0.7, 0.7, 1)
        )
        self.add_widget(guide)
    
    def setup_alarm(self):
        """Tạo âm thanh cảnh báo"""
        # Trong thực tế, bạn nên có file âm thanh .wav hoặc .mp3
        # Ví dụ: self.alarm_sound = SoundLoader.load('alarm.wav')
        self.alarm_sound = None  # Placeholder
    
    def start_monitoring(self, instance):
        """Bắt đầu giám sát"""
        self.capture = cv2.VideoCapture(0)  # Camera trước (0)
        self.is_monitoring = True
        self.start_btn.disabled = True
        self.stop_btn.disabled = False
        self.status_label.text = 'Trạng thái: Đang phân tích...'
        self.status_label.color = (1, 1, 0, 1)
        
        # Cập nhật frame mỗi 0.033s (~30 FPS)
        Clock.schedule_interval(self.update, 1.0 / 30.0)
    
    def stop_monitoring(self, instance):
        """Dừng giám sát"""
        self.is_monitoring = False
        Clock.unschedule(self.update)
        if self.capture:
            self.capture.release()
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        self.status_label.text = 'Trạng thái: Đã dừng'
        self.status_label.color = (1, 1, 1, 1)
        self.eye_closed_frames = 0
    
    def calculate_ear(self, eye_landmarks):
        """
        Tính Eye Aspect Ratio (EAR)
        EAR < 0.25 = Mắt nhắm
        EAR > 0.25 = Mắt mở
        """
        # Tính khoảng cách dọc
        A = distance.euclidean(eye_landmarks[1], eye_landmarks[5])
        B = distance.euclidean(eye_landmarks[2], eye_landmarks[4])
        
        # Tính khoảng cách ngang
        C = distance.euclidean(eye_landmarks[0], eye_landmarks[3])
        
        # Công thức EAR
        ear = (A + B) / (2.0 * C)
        return ear
    
    def update(self, dt):
        """Cập nhật frame từ camera và phân tích"""
        if not self.is_monitoring:
            return
        
        ret, frame = self.capture.read()
        if not ret:
            return
        
        # Lật ảnh để hiển thị như gương
        frame = cv2.flip(frame, 1)
        
        # Chuyển BGR sang RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Phát hiện khuôn mặt
        results = self.face_mesh.process(rgb_frame)
        
        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]
            
            # Lấy tọa độ landmarks
            h, w, _ = frame.shape
            landmarks = []
            for lm in face_landmarks.landmark:
                x, y = int(lm.x * w), int(lm.y * h)
                landmarks.append((x, y))
            
            # Lấy tọa độ mắt trái và phải
            left_eye_coords = [landmarks[i] for i in self.LEFT_EYE]
            right_eye_coords = [landmarks[i] for i in self.RIGHT_EYE]
            
            # Tính EAR cho cả hai mắt
            left_ear = self.calculate_ear(left_eye_coords)
            right_ear = self.calculate_ear(right_eye_coords)
            avg_ear = (left_ear + right_ear) / 2.0
            
            # Vẽ contour mắt
            cv2.polylines(frame, [np.array(left_eye_coords)], True, (0, 255, 0), 1)
            cv2.polylines(frame, [np.array(right_eye_coords)], True, (0, 255, 0), 1)
            
            # Kiểm tra trạng thái mắt
            if avg_ear < 0.25:  # Mắt nhắm
                self.eye_closed_frames += 1
                cv2.putText(frame, "Canh bao: Mat nham!", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                if self.eye_closed_frames >= self.ALARM_THRESHOLD:
                    # CẢNH BÁO BUỒN NGỦ!
                    self.status_label.text = '⚠️ CẢNH BÁO: BUỒN NGỦ!'
                    self.status_label.color = (1, 0, 0, 1)
                    cv2.putText(frame, ">>> BUON NGU! <<<", (10, 70),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    
                    # Phát âm thanh (nếu có)
                    if self.alarm_sound:
                        self.alarm_sound.play()
            else:  # Mắt mở
                self.eye_closed_frames = 0
                self.status_label.text = '✅ Trạng thái: Tỉnh táo'
                self.status_label.color = (0, 1, 0, 1)
                cv2.putText(frame, "Tinh tao", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Hiển thị EAR
            cv2.putText(frame, f"EAR: {avg_ear:.2f}", (w - 150, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        else:
            # Không phát hiện khuôn mặt
            self.status_label.text = '⚠️ Không phát hiện khuôn mặt'
            self.status_label.color = (1, 1, 0, 1)
            cv2.putText(frame, "Khong phat hien khuon mat", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # Chuyển frame sang texture để hiển thị
        buf = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.img_widget.texture = texture


class DrowsyGuardApp(App):
    def build(self):
        return DrowsyGuardLayout()
    
    def on_stop(self):
        # Giải phóng camera khi đóng app
        layout = self.root
        if layout.capture:
            layout.capture.release()


if __name__ == '__main__':
    DrowsyGuardApp().run()
