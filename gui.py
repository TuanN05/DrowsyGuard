"""
Module giao diện người dùng sử dụng Kivy
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.audio import SoundLoader
import cv2

from camera_processor import CameraProcessor
from drowsiness_detector import DrowsinessDetector


class DrowsyGuardLayout(BoxLayout):
    """
    Layout chính của ứng dụng DrowsyGuard
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # Khởi tạo Camera Processor
        self.camera_processor = CameraProcessor(camera_index=0)
        self.is_monitoring = False
        self.is_paused = False  # Trạng thái tạm dừng khi có cảnh báo
        self.alert_popup = None  # Popup cảnh báo
        
        # Tải âm thanh cảnh báo
        self.setup_alarm()
        
        # Xây dựng giao diện
        self._build_ui()
    
    def _build_ui(self):
        """Xây dựng giao diện người dùng"""
        
        # === TIÊU ĐỀ ===
        title = Label(
            text='DrowsyGuard - Cảnh báo buồn ngủ',
            font_size='32sp',
            bold=True,
            size_hint=(1, 0.1),
            color=(0.2, 0.6, 1, 1)
        )
        self.add_widget(title)
        
        # === MÀN HÌNH CAMERA ===
        self.img_widget = Image(size_hint=(1, 0.6))
        self.add_widget(self.img_widget)
        
        # === THÔNG TIN TRẠNG THÁI ===
        info_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.15), spacing=5)
        
        # Nhãn trạng thái chính
        self.status_label = Label(
            text='Trạng thái: Chưa bắt đầu',
            font_size='20sp',
            size_hint=(1, 0.5),
            color=(1, 1, 1, 1),
            bold=True
        )
        info_layout.add_widget(self.status_label)
        
        # Nhãn thông tin chi tiết
        self.detail_label = Label(
            text='',
            font_size='14sp',
            size_hint=(1, 0.5),
            color=(0.8, 0.8, 0.8, 1)
        )
        info_layout.add_widget(self.detail_label)
        
        self.add_widget(info_layout)
        
        # === NÚT ĐIỀU KHIỂN ===
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
        
        # === HƯỚNG DẪN ===
        guide = Label(
            text='Đặt camera sao cho khuôn mặt bạn hiện rõ. Ứng dụng sẽ cảnh báo khi phát hiện dấu hiệu buồn ngủ.',
            font_size='14sp',
            size_hint=(1, 0.05),
            color=(0.7, 0.7, 0.7, 1)
        )
        self.add_widget(guide)
    
    def setup_alarm(self):
        """
        Tải âm thanh cảnh báo
        
        Note: Bạn cần có file âm thanh alarm.wav hoặc alarm.mp3 trong thư mục
        Nếu không có, có thể tạo file âm thanh hoặc để None
        """
        try:
            self.alarm_sound = SoundLoader.load('alarm.wav')
            if self.alarm_sound is None:
                # Thử tải file .mp3
                self.alarm_sound = SoundLoader.load('alarm.mp3')
        except:
            self.alarm_sound = None
            print("Không tìm thấy file âm thanh cảnh báo")
    
    def start_monitoring(self, instance):
        """Bắt đầu giám sát"""
        if self.camera_processor.start():
            self.is_monitoring = True
            self.start_btn.disabled = True
            self.stop_btn.disabled = False
            self.status_label.text = 'Trạng thái: Đang phân tích...'
            self.status_label.color = (1, 1, 0, 1)
            
            # Cập nhật frame mỗi 0.033s (~30 FPS)
            Clock.schedule_interval(self.update, 1.0 / 30.0)
        else:
            self.status_label.text = '❌ Lỗi: Không thể mở camera'
            self.status_label.color = (1, 0, 0, 1)
    
    def stop_monitoring(self, instance):
        """Dừng giám sát"""
        self.is_monitoring = False
        self.is_paused = False
        Clock.unschedule(self.update)
        self.camera_processor.stop()
        
        # Đóng popup nếu đang mở
        if self.alert_popup:
            self.alert_popup.dismiss()
            self.alert_popup = None
        
        # Dừng âm thanh
        if self.alarm_sound and self.alarm_sound.state == 'play':
            self.alarm_sound.stop()
            self.alarm_sound.loop = False
        
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        self.status_label.text = 'Trạng thái: Đã dừng'
        self.status_label.color = (1, 1, 1, 1)
        self.detail_label.text = ''
    
    def update(self, dt):
        """
        Cập nhật frame từ camera và hiển thị
        
        Args:
            dt: Delta time từ Clock
        """
        if not self.is_monitoring or self.is_paused:
            return
        
        # Xử lý frame
        success, frame, status = self.camera_processor.process_frame()
        
        if not success or frame is None:
            return
        
        # Cập nhật thông tin trạng thái
        if status:
            self._update_status_display(status)
            
            # Kiểm tra nếu phát hiện buồn ngủ nghiêm trọng
            if status['drowsy'] and status['alert_active'] and not self.is_paused:
                self._show_drowsiness_alert(status)
                return
            
            # Phát âm thanh cảnh báo nếu cần
            if status['alert_active'] and self.alarm_sound:
                if self.alarm_sound.state != 'play':
                    self.alarm_sound.play()
        
        # Chuyển frame sang texture để hiển thị
        self._display_frame(frame)
    
    def _update_status_display(self, status):
        """
        Cập nhật hiển thị trạng thái
        
        Args:
            status: Dictionary trạng thái từ CameraProcessor
        """
        # Cập nhật text trạng thái
        status_text = DrowsinessDetector().get_status_text(status)
        self.status_label.text = f'Trạng thái: {status_text}'
        
        # Cập nhật màu sắc
        status_color = DrowsinessDetector().get_status_color(status)
        self.status_label.color = status_color
        
        # Cập nhật thông tin chi tiết
        if status['alert_level'] != 'NO_FACE':
            detail_text = (
                f"EAR: {status['ear']:.3f} | "
                f"MAR: {status['mar']:.3f} | "
                f"Ngáp: {status['total_yawns']} lần | "
                f"Điểm: {status['drowsiness_score']}"
            )
            self.detail_label.text = detail_text
        else:
            self.detail_label.text = 'Vui lòng đưa khuôn mặt vào khung hình'
    
    def _display_frame(self, frame):
        """
        Hiển thị frame lên Image widget
        
        Args:
            frame: Frame ảnh từ OpenCV (BGR format)
        """
        # Lật frame theo chiều dọc để hiển thị đúng trong Kivy
        buf = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]), 
            colorfmt='bgr'
        )
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.img_widget.texture = texture
    
    def _show_drowsiness_alert(self, status):
        """
        Hiển thị popup cảnh báo buồn ngủ và tạm dừng giám sát
        
        Args:
            status: Dictionary trạng thái từ CameraProcessor
        """
        # Tạm dừng giám sát
        self.is_paused = True
        
        # Dừng âm thanh nếu đang phát
        if self.alarm_sound and self.alarm_sound.state == 'play':
            self.alarm_sound.stop()
        
        # Tạo nội dung popup
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Icon cảnh báo
        warning_label = Label(
            text='⚠️',
            font_size='80sp',
            size_hint=(1, 0.3),
            color=(1, 0, 0, 1)
        )
        content.add_widget(warning_label)
        
        # Tiêu đề cảnh báo
        title_label = Label(
            text='CẢNH BÁO BUỒN NGỦ!',
            font_size='28sp',
            bold=True,
            size_hint=(1, 0.15),
            color=(1, 0, 0, 1)
        )
        content.add_widget(title_label)
        
        # Thông tin chi tiết
        reason_label = Label(
            text=status['reason'],
            font_size='20sp',
            size_hint=(1, 0.15),
            color=(1, 1, 1, 1)
        )
        content.add_widget(reason_label)
        
        # Thông báo hành động
        action_label = Label(
            text='Vui lòng nghỉ ngơi!\nBấm XÁC NHẬN để tiếp tục giám sát.',
            font_size='16sp',
            size_hint=(1, 0.2),
            color=(1, 1, 0, 1),
            halign='center'
        )
        content.add_widget(action_label)
        
        # Nút xác nhận
        confirm_btn = Button(
            text='XÁC NHẬN - Tôi đã tỉnh táo',
            font_size='18sp',
            bold=True,
            size_hint=(1, 0.2),
            background_color=(0.2, 0.8, 0.2, 1)
        )
        content.add_widget(confirm_btn)
        
        # Tạo popup
        self.alert_popup = Popup(
            title='',
            content=content,
            size_hint=(0.9, 0.7),
            auto_dismiss=False,
            separator_height=0
        )
        
        # Bind nút xác nhận
        confirm_btn.bind(on_press=self._on_confirm_alert)
        
        # Hiển thị popup
        self.alert_popup.open()
        
        # Phát âm thanh cảnh báo mạnh
        if self.alarm_sound:
            self.alarm_sound.loop = True
            self.alarm_sound.play()
    
    def _on_confirm_alert(self, instance):
        """
        Xử lý khi người dùng xác nhận đã tỉnh táo
        
        Args:
            instance: Button instance
        """
        # Đóng popup
        if self.alert_popup:
            self.alert_popup.dismiss()
            self.alert_popup = None
        
        # Dừng âm thanh
        if self.alarm_sound and self.alarm_sound.state == 'play':
            self.alarm_sound.stop()
            self.alarm_sound.loop = False
        
        # Reset bộ phát hiện buồn ngủ
        self.camera_processor.drowsiness_detector.reset()
        
        # Tiếp tục giám sát
        self.is_paused = False
        self.status_label.text = 'Trạng thái: Đã xác nhận - Tiếp tục giám sát'
        self.status_label.color = (0, 1, 0, 1)
    
    def on_stop(self):
        """Cleanup khi đóng ứng dụng"""
        # Đóng popup nếu đang mở
        if self.alert_popup:
            self.alert_popup.dismiss()
        
        # Dừng âm thanh
        if self.alarm_sound and self.alarm_sound.state == 'play':
            self.alarm_sound.stop()
        
        # Giải phóng camera
        self.camera_processor.release()


class DrowsyGuardApp(App):
    """
    Ứng dụng DrowsyGuard chính
    """
    
    def build(self):
        """Xây dựng và trả về layout chính"""
        return DrowsyGuardLayout()
    
    def on_stop(self):
        """Cleanup khi đóng ứng dụng"""
        if hasattr(self.root, 'on_stop'):
            self.root.on_stop()
