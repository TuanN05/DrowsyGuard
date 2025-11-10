"""
Module giao diện người dùng sử dụng Kivy
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider   # <- thêm
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
        self.is_paused = False
        self.alert_popup = None

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

        self.status_label = Label(
            text='Trạng thái: Chưa bắt đầu',
            font_size='20sp',
            size_hint=(1, 0.5),
            color=(1, 1, 1, 1),
            bold=True
        )
        info_layout.add_widget(self.status_label)

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

        # Nút Mặc định
        self.default_btn = Button(
            text='Mặc định',
            background_color=(0.2, 0.4, 0.9, 1),
            font_size='18sp',
            bold=True
        )
        self.default_btn.bind(on_press=self.reset_defaults)

        # Nút Tùy chỉnh độ nhạy
        self.sensitivity_btn = Button(
            text='Tùy chỉnh độ nhạy',
            background_color=(0.9, 0.6, 0.2, 1),
            font_size='18sp',
            bold=True
        )
        self.sensitivity_btn.bind(on_press=self.open_sensitivity_popup)

        # Thêm nút vào layout (đúng thứ tự)
        btn_layout.add_widget(self.start_btn)
        btn_layout.add_widget(self.stop_btn)
        btn_layout.add_widget(self.default_btn)
        btn_layout.add_widget(self.sensitivity_btn)

        # Đưa layout nút lên giao diện
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
        """Tải âm thanh cảnh báo"""
        try:
            self.alarm_sound = SoundLoader.load('alarm.wav')
            if self.alarm_sound is None:
                self.alarm_sound = SoundLoader.load('alarm.mp3')
        except Exception:
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

        if self.alert_popup:
            self.alert_popup.dismiss()
            self.alert_popup = None

        if self.alarm_sound and self.alarm_sound.state == 'play':
            self.alarm_sound.stop()
            self.alarm_sound.loop = False

        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        self.status_label.text = 'Trạng thái: Đã dừng'
        self.status_label.color = (1, 1, 1, 1)
        self.detail_label.text = ''

    def update(self, dt):
        """Cập nhật frame từ camera"""
        if not self.is_monitoring or self.is_paused:
            return

        success, frame, status = self.camera_processor.process_frame()
        if not success or frame is None:
            return

        if status:
            self._update_status_display(status)
            if status['drowsy'] and status['alert_active'] and not self.is_paused:
                self._show_drowsiness_alert(status)
                return

            if status['alert_active'] and self.alarm_sound:
                if self.alarm_sound.state != 'play':
                    self.alarm_sound.play()

        self._display_frame(frame)

    def _update_status_display(self, status):
        """Cập nhật hiển thị trạng thái"""
        status_text = DrowsinessDetector().get_status_text(status)
        self.status_label.text = f'Trạng thái: {status_text}'
        self.status_label.color = DrowsinessDetector().get_status_color(status)

        if status['alert_level'] != 'NO_FACE':
            text = (
                f"EAR: {status['ear']:.3f} | "
                f"MAR: {status['mar']:.3f} | "
                f"Ngáp: {status['total_yawns']} lần | "
                f"Điểm: {status['drowsiness_score']}"
            )
        else:
            text = 'Vui lòng đưa khuôn mặt vào khung hình'

        # Luôn hiển thị ngưỡng hiện tại để bạn kiểm tra nhanh
        ear_thr = getattr(self.camera_processor.drowsiness_detector, 'EAR_THRESHOLD', 0.25)
        mar_thr = getattr(self.camera_processor.drowsiness_detector, 'MAR_THRESHOLD', 0.6)
        text += f"\n(Độ nhạy hiện tại: EAR={ear_thr:.2f}, MAR={mar_thr:.2f})"

        self.detail_label.text = text

    def _display_frame(self, frame):
        """Hiển thị frame lên Image widget"""
        buf = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.img_widget.texture = texture

    def _show_drowsiness_alert(self, status):
        """Hiển thị popup cảnh báo buồn ngủ"""
        self.is_paused = True

        if self.alarm_sound and self.alarm_sound.state == 'play':
            self.alarm_sound.stop()

        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        warning_label = Label(text='⚠️', font_size='80sp', color=(1, 0, 0, 1))
        title_label = Label(text='CẢNH BÁO BUỒN NGỦ!', font_size='28sp', bold=True, color=(1, 0, 0, 1))
        reason_label = Label(text=status['reason'], font_size='20sp', color=(1, 1, 1, 1))
        action_label = Label(
            text='Vui lòng nghỉ ngơi!\nBấm XÁC NHẬN để tiếp tục giám sát.',
            font_size='16sp',
            color=(1, 1, 0, 1),
            halign='center'
        )
        confirm_btn = Button(
            text='XÁC NHẬN - Tôi đã tỉnh táo',
            font_size='18sp',
            bold=True,
            background_color=(0.2, 0.8, 0.2, 1)
        )

        content.add_widget(warning_label)
        content.add_widget(title_label)
        content.add_widget(reason_label)
        content.add_widget(action_label)
        content.add_widget(confirm_btn)

        self.alert_popup = Popup(
            title='',
            content=content,
            size_hint=(0.9, 0.7),
            auto_dismiss=False,
            separator_height=0
        )
        confirm_btn.bind(on_press=self._on_confirm_alert)
        self.alert_popup.open()

        if self.alarm_sound:
            self.alarm_sound.loop = True
            self.alarm_sound.play()

    def _on_confirm_alert(self, instance):
        """Xử lý khi người dùng xác nhận đã tỉnh táo"""
        if self.alert_popup:
            self.alert_popup.dismiss()
            self.alert_popup = None

        if self.alarm_sound and self.alarm_sound.state == 'play':
            self.alarm_sound.stop()
            self.alarm_sound.loop = False

        self.camera_processor.drowsiness_detector.reset()
        self.is_paused = False
        self.status_label.text = 'Trạng thái: Đã xác nhận - Tiếp tục giám sát'
        self.status_label.color = (0, 1, 0, 1)

    def reset_defaults(self, instance):
        """Đặt lại ngưỡng EAR/MAR về giá trị mặc định"""
        try:
            self.camera_processor.drowsiness_detector.EAR_THRESHOLD = 0.25
            self.camera_processor.drowsiness_detector.MAR_THRESHOLD = 0.6
            self.status_label.text = "Đã đặt lại EAR=0.25, MAR=0.6 về mặc định"
            self.status_label.color = (0.4, 0.8, 1, 1)
            self.detail_label.text = ""
            print("✅ Reset EAR=0.25, MAR=0.6 thành công.")
        except Exception as e:
            print("❌ Lỗi khi đặt lại mặc định:", e)
            self.status_label.text = "❌ Lỗi khi đặt lại mặc định"
            self.status_label.color = (1, 0, 0, 1)

    def open_sensitivity_popup(self, instance):
        """
        Mở popup cho phép người dùng tùy chỉnh độ nhạy (EAR, MAR)
        """
        # Lấy giá trị hiện tại
        current_ear = getattr(self.camera_processor.drowsiness_detector, 'EAR_THRESHOLD', 0.25)
        current_mar = getattr(self.camera_processor.drowsiness_detector, 'MAR_THRESHOLD', 0.6)

        layout = BoxLayout(orientation='vertical', spacing=12, padding=20)

        # --- Slider EAR ---
        ear_label = Label(text=f"Ngưỡng EAR hiện tại: {current_ear:.2f}", font_size='16sp')
        ear_slider = Slider(min=0.15, max=0.35, value=current_ear, step=0.01)
        ear_slider.bind(value=lambda s, v: ear_label.setter('text')(ear_label, f"Ngưỡng EAR hiện tại: {v:.2f}"))

        # --- Slider MAR ---
        mar_label = Label(text=f"Ngưỡng MAR hiện tại: {current_mar:.2f}", font_size='16sp')
        mar_slider = Slider(min=0.4, max=0.8, value=current_mar, step=0.01)
        mar_slider.bind(value=lambda s, v: mar_label.setter('text')(mar_label, f"Ngưỡng MAR hiện tại: {v:.2f}"))

        # --- Nút Lưu ---
        save_btn = Button(
            text='Lưu cài đặt',
            background_color=(0.2, 0.8, 0.2, 1),
            size_hint=(1, 0.3),
            bold=True
        )

        # Tạo popup trước, để hàm con có thể gọi popup.dismiss()
        popup = Popup(
            title='⚙️ Tùy chỉnh độ nhạy phát hiện',
            content=layout,
            size_hint=(0.9, 0.7),
            auto_dismiss=True
        )

        def save_thresholds(instance_btn):
            new_ear = ear_slider.value
            new_mar = mar_slider.value
            self.camera_processor.drowsiness_detector.EAR_THRESHOLD = new_ear
            self.camera_processor.drowsiness_detector.MAR_THRESHOLD = new_mar
            self.status_label.text = f"✅ EAR={new_ear:.2f}, MAR={new_mar:.2f} đã được cập nhật"
            self.status_label.color = (0.3, 1, 0.7, 1)
            print(f"[INFO] Ngưỡng mới áp dụng: EAR={new_ear:.2f}, MAR={new_mar:.2f}")
            popup.dismiss()

        save_btn.bind(on_press=save_thresholds)

        # Ghép layout
        layout.add_widget(ear_label)
        layout.add_widget(ear_slider)
        layout.add_widget(mar_label)
        layout.add_widget(mar_slider)
        layout.add_widget(save_btn)

        popup.open()

    def on_stop(self):
        """Cleanup khi đóng ứng dụng"""
        if self.alert_popup:
            self.alert_popup.dismiss()
        if self.alarm_sound and self.alarm_sound.state == 'play':
            self.alarm_sound.stop()
        self.camera_processor.release()


class DrowsyGuardApp(App):
    """Ứng dụng DrowsyGuard chính"""

    def build(self):
        return DrowsyGuardLayout()

    def on_stop(self):
        if hasattr(self.root, 'on_stop'):
            self.root.on_stop()
