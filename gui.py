"""
Module giao diện người dùng sử dụng Kivy - Phong cách cổ điển
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.graphics import Color, Line, Rectangle
from kivy.core.audio import SoundLoader
import cv2

from camera_processor import CameraProcessor
from drowsiness_detector import DrowsinessDetector


class GroupBox(BoxLayout):
    """Widget GroupBox kiểu cổ điển với viền và tiêu đề"""
    
    def __init__(self, title='', **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [10, 35, 10, 10]
        self.spacing = 5
        self.title_text = title
        
        with self.canvas.before:
            # Màu nền nhạt
            Color(0.15, 0.15, 0.18, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            
            # Viền
            Color(0.4, 0.4, 0.45, 1)
            self.border = Line(rectangle=(self.x, self.y, self.width, self.height), width=1.5)
        
        # Tiêu đề
        self.title_label = Label(
            text=f'  {title}  ',
            size_hint=(None, None),
            pos_hint={'top': 1, 'left': 1},
            font_size='15sp',
            bold=True,
            color=(0.7, 0.7, 0.75, 1)
        )
        self.title_label.bind(texture_size=self.title_label.setter('size'))
        
        self.bind(pos=self.update_graphics, size=self.update_graphics)
        
    def update_graphics(self, *args):
        """Cập nhật vị trí viền và nền"""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border.rectangle = (self.x, self.y, self.width, self.height)
        self.title_label.pos = (self.x + 15, self.y + self.height - 25)
        
    def add_widget(self, widget, *args, **kwargs):
        """Override để thêm tiêu đề trước"""
        if widget is self.title_label:
            return super(BoxLayout, self).add_widget(widget, *args, **kwargs)
        
        if len(self.children) == 0:
            super(BoxLayout, self).add_widget(self.title_label)
        
        super().add_widget(widget, *args, **kwargs)


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
        
        # THÊM: Biến lưu trữ calibration
        self.calibration_mode = False
        self.calibration_samples = {'ear': [], 'mar': []}
        self.calibration_frames = 0
        self.CALIBRATION_DURATION = 150  # 5 giây ở 30 FPS

        # Tải âm thanh cảnh báo
        self.setup_alarm()

        # Xây dựng giao diện
        self._build_ui()

    def _build_ui(self):
        """Xây dựng giao diện người dùng - Phong cách cổ điển"""
        
        # Màu nền tổng thể
        with self.canvas.before:
            Color(0.12, 0.12, 0.15, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

        # === TIÊU ĐỀ ===
        title_box = BoxLayout(orientation='vertical', size_hint=(1, 0.08), padding=[15, 8])
        
        title = Label(
            text='DrowsyGuard - Hệ thống cảnh báo buồn ngủ',
            font_size='26sp',
            bold=True,
            color=(0.85, 0.85, 0.9, 1),
            halign='center'
        )
        title.bind(size=title.setter('text_size'))
        title_box.add_widget(title)
        
        self.add_widget(title_box)

        # === LAYOUT CHÍNH: CAMERA BÊN TRÁI, ĐIỀU KHIỂN BÊN PHẢI ===
        main_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.85), spacing=10)
        
        # === PHẦN TRÁI: MÀN HÌNH CAMERA ===
        camera_group = GroupBox(title='Màn hình giám sát', size_hint=(0.65, 1))
        self.img_widget = Image()
        camera_group.add_widget(self.img_widget)
        main_layout.add_widget(camera_group)

        # === PHẦN PHẢI: TRẠNG THÁI VÀ ĐIỀU KHIỂN ===
        right_panel = BoxLayout(orientation='vertical', size_hint=(0.35, 1), spacing=10)
        
        # GROUPBOX: THÔNG TIN TRẠNG THÁI
        info_group = GroupBox(title='Thông tin trạng thái', size_hint=(1, 0.4))
        
        self.status_label = Label(
            text='Trạng thái: Chưa bắt đầu',
            font_size='16sp',
            size_hint=(1, 0.35),
            color=(0.9, 0.9, 0.95, 1),
            bold=True
        )
        info_group.add_widget(self.status_label)

        self.detail_label = Label(
            text='Nhấn "Bắt đầu" để khởi động hệ thống giám sát',
            font_size='12sp',
            size_hint=(1, 0.65),
            color=(0.7, 0.7, 0.75, 1)
        )
        info_group.add_widget(self.detail_label)
        
        right_panel.add_widget(info_group)

        # GROUPBOX: ĐIỀU KHIỂN
        control_group = GroupBox(title='Bảng điều khiển', size_hint=(1, 0.6))
        
        # Hàng 1: Bắt đầu | Dừng
        row1 = BoxLayout(size_hint=(1, 0.3), spacing=8)
        
        self.start_btn = Button(
            text='▶ Bắt đầu',
            background_color=(0.25, 0.6, 0.25, 1),
            background_normal='',
            font_size='16sp',
            bold=True
        )
        self.start_btn.bind(on_press=self.start_monitoring)
        
        self.stop_btn = Button(
            text='◼ Dừng',
            background_color=(0.7, 0.3, 0.3, 1),
            background_normal='',
            font_size='16sp',
            bold=True,
            disabled=True
        )
        self.stop_btn.bind(on_press=self.stop_monitoring)
        
        row1.add_widget(self.start_btn)
        row1.add_widget(self.stop_btn)
        control_group.add_widget(row1)

        # Separator
        sep1 = Label(text='', size_hint=(1, 0.08))
        control_group.add_widget(sep1)
        
        # Hàng 2: Mặc định | Tùy chỉnh
        row2 = BoxLayout(size_hint=(1, 0.28), spacing=8)
        
        self.default_btn = Button(
            text='Mặc định',
            background_color=(0.45, 0.45, 0.5, 1),
            background_normal='',
            font_size='15sp',
            bold=True
        )
        self.default_btn.bind(on_press=self.reset_defaults)
        
        self.sensitivity_btn = Button(
            text='Tùy chỉnh',
            background_color=(0.45, 0.45, 0.5, 1),
            background_normal='',
            font_size='15sp',
            bold=True
        )
        self.sensitivity_btn.bind(on_press=self.open_sensitivity_popup)
        
        row2.add_widget(self.default_btn)
        row2.add_widget(self.sensitivity_btn)
        control_group.add_widget(row2)
        
        # Hàng 3: Hiệu chỉnh (full width)
        row3 = BoxLayout(size_hint=(1, 0.28), spacing=8)
        
        self.calibrate_btn = Button(
            text='Hiệu chỉnh',
            background_color=(0.45, 0.45, 0.5, 1),
            background_normal='',
            font_size='15sp',
            bold=True
        )
        self.calibrate_btn.bind(on_press=self.start_calibration)
        
        row3.add_widget(self.calibrate_btn)
        control_group.add_widget(row3)
        
        right_panel.add_widget(control_group)
        
        main_layout.add_widget(right_panel)
        self.add_widget(main_layout)

        # === HƯỚNG DẪN ===
        guide_box = BoxLayout(size_hint=(1, 0.07), padding=[15, 5])
        guide = Label(
            text='💡 Lưu ý: Đặt camera sao cho khuôn mặt hiện rõ. Sử dụng "Hiệu chỉnh" để tối ưu độ chính xác.',
            font_size='11sp',
            color=(0.6, 0.65, 0.7, 1),
            italic=True,
            halign='center'
        )
        guide.bind(size=guide.setter('text_size'))
        guide_box.add_widget(guide)
        self.add_widget(guide_box)
    
    def _update_bg(self, *args):
        """Cập nhật màu nền"""
        self.bg.pos = self.pos
        self.bg.size = self.size

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
            # Disable 3 nút cài đặt trong lúc giám sát
            self.default_btn.disabled = True
            self.sensitivity_btn.disabled = True
            self.calibrate_btn.disabled = True
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
        # Enable lại 3 nút cài đặt
        self.default_btn.disabled = False
        self.sensitivity_btn.disabled = False
        self.calibrate_btn.disabled = False
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
                f"EAR: {status['ear']:.3f}  |  "
                f"MAR: {status['mar']:.3f}  |  "
                f"Ngáp: {status['total_yawns']} lần  |  "
                f"Điểm: {round(status['drowsiness_score'], 2)}\n"
            )
        else:
            text = 'Không phát hiện khuôn mặt - Vui lòng điều chỉnh vị trí\n'

        # Hiển thị ngưỡng hiện tại
        ear_thr = getattr(self.camera_processor.drowsiness_detector, 'EAR_THRESHOLD', 0.25)
        mar_thr = getattr(self.camera_processor.drowsiness_detector, 'MAR_THRESHOLD', 0.6)
        text += f"Ngưỡng cài đặt: EAR={ear_thr:.2f} | MAR={mar_thr:.2f}"

        self.detail_label.text = text

    def _display_frame(self, frame):
        """Hiển thị frame lên Image widget"""
        buf = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.img_widget.texture = texture

    def _show_drowsiness_alert(self, status):
        """Hiển thị popup cảnh báo buồn ngủ - Phong cách cổ điển"""
        self.is_paused = True

        if self.alarm_sound and self.alarm_sound.state == 'play':
            self.alarm_sound.stop()

        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Nền đỏ cảnh báo
        with content.canvas.before:
            Color(0.3, 0.05, 0.05, 1)
            content.bg = Rectangle(pos=content.pos, size=content.size)
        content.bind(pos=lambda *args: setattr(content.bg, 'pos', content.pos),
                    size=lambda *args: setattr(content.bg, 'size', content.size))
        
        warning_label = Label(
            text='⚠',
            font_size='80sp',
            color=(1, 0.9, 0, 1),
            size_hint=(1, 0.2)
        )
        
        title_label = Label(
            text='CẢNH BÁO BUỒN NGỦ!',
            font_size='28sp',
            bold=True,
            color=(1, 0.2, 0.2, 1),
            size_hint=(1, 0.15)
        )
        
        reason_label = Label(
            text=status['reason'],
            font_size='18sp',
            color=(1, 1, 0.9, 1),
            bold=True,
            size_hint=(1, 0.15)
        )
        
        action_label = Label(
            text='━━━━━━━━━━━━━━━━━━\nVui lòng nghỉ ngơi ngay!\n━━━━━━━━━━━━━━━━━━\nBấm XÁC NHẬN khi đã tỉnh táo',
            font_size='16sp',
            color=(1, 0.95, 0.7, 1),
            halign='center',
            size_hint=(1, 0.3)
        )
        action_label.bind(size=action_label.setter('text_size'))
        
        confirm_btn = Button(
            text='✓ XÁC NHẬN - Tôi đã tỉnh táo',
            font_size='18sp',
            bold=True,
            background_color=(0.2, 0.6, 0.2, 1),
            background_normal='',
            size_hint=(1, 0.2)
        )

        content.add_widget(warning_label)
        content.add_widget(title_label)
        content.add_widget(reason_label)
        content.add_widget(action_label)
        content.add_widget(confirm_btn)

        self.alert_popup = Popup(
            title='═══════════════════════════',
            content=content,
            size_hint=(0.85, 0.65),
            auto_dismiss=False,
            separator_height=2,
            separator_color=[1, 0.3, 0.3, 1]
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
            self.status_label.text = "Đã khôi phục cài đặt mặc định"
            self.status_label.color = (0.3, 0.8, 0.95, 1)
            self.detail_label.text = "Ngưỡng: EAR=0.25 | MAR=0.6"
            print("Reset EAR=0.25, MAR=0.6 thành công.")
        except Exception as e:
            print("❌ Lỗi khi đặt lại mặc định:", e)
            self.status_label.text = "❌ Lỗi khi đặt lại mặc định"
            self.status_label.color = (1, 0, 0, 1)

    def open_sensitivity_popup(self, instance):
        """
        Mở popup cho phép người dùng tùy chỉnh độ nhạy (EAR, MAR) - Phong cách cổ điển
        """
        # Lấy giá trị hiện tại
        current_ear = (getattr(self.camera_processor.drowsiness_detector, 'EAR_THRESHOLD', 0.25))
        current_mar = (getattr(self.camera_processor.drowsiness_detector, 'MAR_THRESHOLD', 0.6))
        
        # lam tron va ep kieu float de kivy nhan dung
        current_ear = float(round(current_ear, 3))
        current_mar = float(round(current_mar, 3))

        layout = BoxLayout(orientation='vertical', spacing=15, padding=25)
        
        # Nền popup
        with layout.canvas.before:
            Color(0.15, 0.15, 0.18, 1)
            layout.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda *args: setattr(layout.bg, 'pos', layout.pos),
                   size=lambda *args: setattr(layout.bg, 'size', layout.size))

        # GroupBox cho EAR
        ear_box = BoxLayout(orientation='vertical', spacing=8, size_hint=(1, 0.4))
        ear_label = Label(
            text=f"▼ Ngưỡng EAR (Phát hiện mắt nhắm): {current_ear:.2f}",
            font_size='16sp',
            bold=True,
            color=(0.5, 0.8, 1, 1)
        )
        ear_slider = Slider(min=0.15, max=0.35, value=current_ear, step=0.01)
        ear_slider.bind(value=lambda s, v: ear_label.setter('text')(ear_label, f"▼ Ngưỡng EAR (Phát hiện mắt nhắm): {v:.2f}"))
        
        ear_hint = Label(
            text='Giảm giá trị = Nhạy hơn | Tăng giá trị = Ít nhạy hơn',
            font_size='11sp',
            color=(0.6, 0.6, 0.65, 1),
            italic=True
        )
        
        ear_box.add_widget(ear_label)
        ear_box.add_widget(ear_slider)
        ear_box.add_widget(ear_hint)

        # GroupBox cho MAR
        mar_box = BoxLayout(orientation='vertical', spacing=8, size_hint=(1, 0.4))
        mar_label = Label(
            text=f"▼ Ngưỡng MAR (Phát hiện ngáp): {current_mar:.2f}",
            font_size='16sp',
            bold=True,
            color=(1, 0.75, 0.4, 1)
        )
        mar_slider = Slider(min=0.4, max=0.8, value=current_mar, step=0.01)
        mar_slider.bind(value=lambda s, v: mar_label.setter('text')(mar_label, f"▼ Ngưỡng MAR (Phát hiện ngáp): {v:.2f}"))
        
        mar_hint = Label(
            text='Giảm giá trị = Nhạy hơn | Tăng giá trị = Ít nhạy hơn',
            font_size='11sp',
            color=(0.6, 0.6, 0.65, 1),
            italic=True
        )
        
        mar_box.add_widget(mar_label)
        mar_box.add_widget(mar_slider)
        mar_box.add_widget(mar_hint)

        # Nút Lưu
        save_btn = Button(
            text='✓ Lưu cài đặt',
            background_color=(0.25, 0.6, 0.25, 1),
            background_normal='',
            size_hint=(1, 0.2),
            bold=True,
            font_size='18sp'
        )

        # Tạo popup trước
        popup = Popup(
            title='⚙ Tùy chỉnh độ nhạy phát hiện',
            content=layout,
            size_hint=(0.85, 0.7),
            auto_dismiss=True,
            separator_height=2,
            separator_color=[0.4, 0.4, 0.45, 1]
        )

        def save_thresholds(instance_btn):
            new_ear = ear_slider.value
            new_mar = mar_slider.value
            self.camera_processor.drowsiness_detector.EAR_THRESHOLD = new_ear
            self.camera_processor.drowsiness_detector.MAR_THRESHOLD = new_mar
            self.status_label.text = f"✓ Đã cập nhật độ nhạy"
            self.status_label.color = (0.3, 0.9, 0.6, 1)
            self.detail_label.text = f"Ngưỡng cài đặt: EAR={new_ear:.2f} | MAR={new_mar:.2f}"
            print(f"[INFO] Ngưỡng mới áp dụng: EAR={new_ear:.2f}, MAR={new_mar:.2f}")
            popup.dismiss()

        save_btn.bind(on_press=save_thresholds)

        # Ghép layout
        layout.add_widget(ear_box)
        layout.add_widget(mar_box)
        layout.add_widget(save_btn)

        popup.open()
        
        #==================================================================================
        #==================================================================================
        #==================================================================================
        #==================================================================================
        #==================================================================================
        # phan popup hieu chinh tu dong
        #==================================================================================
        #==================================================================================
        #==================================================================================
        #==================================================================================
        #==================================================================================
        #==================================================================================

    def start_calibration(self, instance):
        """Bắt đầu calibration tự động - Phong cách cổ điển"""
        if self.is_monitoring:
            self.status_label.text = "⚠ Vui lòng dừng giám sát trước khi hiệu chỉnh"
            self.status_label.color = (1, 0.5, 0, 1)
            return
        
        # Hiển thị popup hướng dẫn
        content = BoxLayout(orientation='vertical', padding=25, spacing=18)
        
        # Nền popup
        with content.canvas.before:
            Color(0.15, 0.15, 0.18, 1)
            content.bg = Rectangle(pos=content.pos, size=content.size)
        content.bind(pos=lambda *args: setattr(content.bg, 'pos', content.pos),
                    size=lambda *args: setattr(content.bg, 'size', content.size))
        
        title = Label(
            text='═══ HƯỚNG DẪN HIỆU CHỈNH ═══',
            font_size='20sp',
            bold=True,
            color=(0.7, 0.7, 0.75, 1),
            size_hint=(1, 0.15)
        )
        
        instruction = Label(
            text=(
                '┌─────────────────────────────┐\n'
                ' 1. Ngồi thẳng, thư giãn         │\n'
                ' 2. Nhìn thẳng vào camera      │\n'
                '│  3. Mở mắt bình thường (5s)  │\n'
                '│  4. KHÔNG chớp mắt liên tục   │\n'
                '└─────────────────────────────┘\n\n'
                'Hệ thống sẽ tự động tính ngưỡng tối ưu'
            ),
            font_size='15sp',
            halign='center',
            color=(0.85, 0.85, 0.9, 1),
            size_hint=(1, 0.6)
        )
        instruction.bind(size=instruction.setter('text_size'))
        
        start_btn = Button(
            text='▶ BẮT ĐẦU HIỆU CHỈNH',
            background_color=(0.25, 0.65, 0.25, 1),
            background_normal='',
            size_hint=(1, 0.25),
            bold=True,
            font_size='17sp'
        )
        
        content.add_widget(title)
        content.add_widget(instruction)
        content.add_widget(start_btn)
        
        popup = Popup(
            title='⊕ Hiệu chỉnh độ nhạy tự động',
            content=content,
            size_hint=(0.8, 0.65),
            auto_dismiss=False,
            separator_height=2,
            separator_color=[0.4, 0.4, 0.45, 1]
        )
        
        def begin_calibration(instance_btn):
            popup.dismiss()
            self._run_calibration()
        
        start_btn.bind(on_press=begin_calibration)
        popup.open()

    def _run_calibration(self):
        """Chạy quá trình calibration"""
        self.calibration_mode = True
        self.calibration_samples = {'ear': [], 'mar': []}
        self.calibration_frames = 0
        
        # Bật camera để thu thập dữ liệu
        if self.camera_processor.start():
            self.status_label.text = 'Đang hiệu chỉnh... Giữ mắt mở và nhìn thẳng!'
            self.status_label.color = (1, 1, 0, 1)
            
            # Disable các nút trong lúc calibration
            self.start_btn.disabled = True
            self.stop_btn.disabled = True
            self.calibrate_btn.disabled = True
            self.default_btn.disabled = True
            self.sensitivity_btn.disabled = True
            # hàm calibrate_update sẽ được gọi 30 lần mỗi giây
            Clock.schedule_interval(self._calibration_update, 1.0 / 30.0)
        else:
            self.status_label.text = 'Lỗi: Không thể mở camera'
            self.status_label.color = (1, 0, 0, 1)
            self.calibration_mode = False

    def _calibration_update(self, dt):
        """Cập nhật frame trong quá trình calibration"""
        if not self.calibration_mode:
            return False  # Dừng schedule
        
        success, frame, status = self.camera_processor.process_frame()
        
        if not success or frame is None or not status:
            return True  # Tiếp tục thử
        
        # Hiển thị frame
        self._display_frame(frame)
        
        # Thu thập mẫu EAR/MAR (chỉ khi phát hiện khuôn mặt)
        if status['alert_level'] != 'NO_FACE':
            self.calibration_samples['ear'].append(status['ear'])
            self.calibration_samples['mar'].append(status['mar'])
            self.calibration_frames += 1
            
            # Hiển thị tiến trình
            progress = int((self.calibration_frames / self.CALIBRATION_DURATION) * 100)
            self.detail_label.text = (
                f"Tiến trình: {progress}% ({self.calibration_frames}/{self.CALIBRATION_DURATION})\n"
                f"EAR hiện tại: {status['ear']:.3f} | MAR: {status['mar']:.3f}"
            )
        else:
            self.detail_label.text = "Không phát hiện khuôn mặt - Vui lòng nhìn thẳng vào camera"
        
        # Hoàn thành calibration
        if self.calibration_frames >= self.CALIBRATION_DURATION:
            self._finish_calibration()
            return False  # Dừng schedule
        
        return True  # Tiếp tục

    def _finish_calibration(self):
        """Hoàn thành calibration và tính ngưỡng"""
        self.calibration_mode = False
        self.camera_processor.stop()
        
        
        
        # Kiểm tra đủ mẫu
        if len(self.calibration_samples['ear']) < 50:
            self.status_label.text = 'Calibration thất bại: Không đủ dữ liệu'
            self.status_label.color = (1, 0, 0, 1)
            self.detail_label.text = 'Vui lòng thử lại và đảm bảo khuôn mặt hiện rõ'
            return
        
        # Tính EAR/MAR trung bình
        avg_ear = sum(self.calibration_samples['ear']) / len(self.calibration_samples['ear'])
        avg_mar = sum(self.calibration_samples['mar']) / len(self.calibration_samples['mar'])
        
        # Tính ngưỡng tối ưu (giảm 20% cho EAR, tăng 20% cho MAR)
        optimal_ear = avg_ear * 0.80  # Mắt nhắm khi EAR giảm 20%
        optimal_mar = avg_mar * 1.20  # Ngáp khi MAR tăng 20%
        
        # Giới hạn trong khoảng hợp lý
        optimal_ear = max(0.15, min(0.30, optimal_ear))
        optimal_mar = max(0.50, min(0.75, optimal_mar))
        
        # Áp dụng ngưỡng mới
        self.camera_processor.drowsiness_detector.EAR_THRESHOLD = optimal_ear
        self.camera_processor.drowsiness_detector.MAR_THRESHOLD = optimal_mar
        
        # Hiển thị kết quả
        self.status_label.text = 'Hiệu chỉnh thành công!'
        self.status_label.color = (0, 1, 0, 1)
        
        self.detail_label.text = (
            f"Kết quả Calibration:\n"
            f"EAR trung bình: {avg_ear:.3f} → Ngưỡng: {optimal_ear:.3f}\n"
            f"MAR trung bình: {avg_mar:.3f} → Ngưỡng: {optimal_mar:.3f}\n"
            f"Ngưỡng đã được tối ưu hóa cho bạn!"
        )
        
        print(f"[CALIBRATION] EAR: {avg_ear:.3f} → {optimal_ear:.3f}")
        print(f"[CALIBRATION] MAR: {avg_mar:.3f} → {optimal_mar:.3f}")
        
        # Hiển thị popup thành công
        self._show_calibration_success(avg_ear, avg_mar, optimal_ear, optimal_mar)

    def _show_calibration_success(self, avg_ear, avg_mar, new_ear, new_mar):
        """Hiển thị popup kết quả calibration - Phong cách cổ điển"""
        content = BoxLayout(orientation='vertical', padding=25, spacing=12)
        
        # Nền popup
        with content.canvas.before:
            Color(0.05, 0.2, 0.05, 1)
            content.bg = Rectangle(pos=content.pos, size=content.size)
        content.bind(pos=lambda *args: setattr(content.bg, 'pos', content.pos),
                    size=lambda *args: setattr(content.bg, 'size', content.size))
        
        success_icon = Label(
            text='✓',
            font_size='60sp',
            color=(0.3, 1, 0.3, 1),
            bold=True,
            size_hint=(1, 0.2)
        )
        
        title = Label(
            text='HIỆU CHỈNH THÀNH CÔNG!',
            font_size='24sp',
            bold=True,
            color=(0.5, 1, 0.5, 1),
            size_hint=(1, 0.15)
        )
        
        result = Label(
            text=(
                f'┌───────────────────────────────┐\n'
                f'│  Đặc điểm khuôn mặt của bạn:       │\n'
                f'EAR bình thường: {avg_ear:.3f}           │\n'
                f'MAR bình thường: {avg_mar:.3f}           │\n'
                f'├───────────────────────────────┤\n'
                f'│  Ngưỡng tối ưu đã cài đặt:          │\n'
                f'│  ◆ EAR: {new_ear:.3f} (phát hiện mắt nhắm)│\n'
                f'│  ◆ MAR: {new_mar:.3f} (phát hiện ngáp)      │\n'
                f'└───────────────────────────────┘'
            ),
            font_size='14sp',
            halign='center',
            color=(0.9, 0.9, 0.95, 1),
            size_hint=(1, 0.5)
        )
        result.bind(size=result.setter('text_size'))
        
        ok_btn = Button(
            text='✓ HOÀN TẤT',
            background_color=(0.25, 0.65, 0.25, 1),
            background_normal='',
            size_hint=(1, 0.15),
            bold=True,
            font_size='18sp'
        )
        
        content.add_widget(success_icon)
        content.add_widget(title)
        content.add_widget(result)
        content.add_widget(ok_btn)
        
        popup = Popup(
            title='═══════════════════════════',
            content=content,
            size_hint=(0.8, 0.7),
            auto_dismiss=False,
            separator_height=2,
            separator_color=[0.3, 0.7, 0.3, 1]
        )
        
        # Enable lại các nút
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        self.calibrate_btn.disabled = False
        self.default_btn.disabled = False
        self.sensitivity_btn.disabled = False
        
        ok_btn.bind(on_press=popup.dismiss)
        popup.open()
        
        #==================================================================================
        #==================================================================================
        #==================================================================================
        #==================================================================================
        #==================================================================================
        #==================================================================================
        #==================================================================================
        #==================================================================================
        #==================================================================================
        #==================================================================================
        #==================================================================================

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
