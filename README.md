# DrowsyGuard v2.0 - Hệ thống Cảnh báo Buồn ngủ

Ứng dụng phát hiện và cảnh báo trạng thái buồn ngủ khi lái xe bằng công nghệ nhận diện khuôn mặt và phân tích hành vi.

## 🌟 Tính năng

- ✅ Nhận diện khuôn mặt theo thời gian thực
- 👁️ Phát hiện mắt nhắm bằng chỉ số EAR (Eye Aspect Ratio)
- 🥱 Phát hiện ngáp bằng chỉ số MAR (Mouth Aspect Ratio)
- 🧠 Thuật toán thông minh đánh giá trạng thái buồn ngủ
- 🔊 Cảnh báo âm thanh khi phát hiện buồn ngủ
- 📊 Hiển thị chi tiết các chỉ số EAR, MAR và điểm buồn ngủ

## 📁 Cấu trúc Module

```
DrowsyGuard/
├── main.py                    # File chạy ứng dụng
├── gui.py                     # Giao diện người dùng (Kivy)
├── camera_processor.py        # Xử lý video từ camera
├── face_detector.py           # Nhận diện khuôn mặt (Mediapipe)
├── ear_calculator.py          # Tính chỉ số EAR
├── mar_calculator.py          # Tính chỉ số MAR
├── drowsiness_detector.py     # Thuật toán phát hiện buồn ngủ
├── requirements.txt           # Thư viện cần thiết
└── README.md                  # Tài liệu hướng dẫn
```

## 🔧 Cài đặt

### Yêu cầu hệ thống

- Python 3.8 trở lên
- Camera (webcam hoặc camera điện thoại)
- Hệ điều hành: Windows, macOS, Linux

### Các bước cài đặt

1. **Clone repository**

```bash
git clone https://github.com/TuanN05/DrowsyGuard.git
cd DrowsyGuard
```

2. **Tạo môi trường ảo (khuyến nghị)**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Cài đặt thư viện**

```bash
pip install -r requirements.txt
```

## 🚀 Sử dụng

### Chạy ứng dụng

```bash
python main.py
```

### Hướng dẫn sử dụng

1. Khởi động ứng dụng
2. Nhấn nút **"Bắt đầu giám sát"**
3. Đặt camera sao cho khuôn mặt hiện rõ trong khung hình
4. Ứng dụng sẽ tự động phân tích và cảnh báo khi phát hiện buồn ngủ
5. Nhấn **"Dừng"** để kết thúc giám sát

## 📊 Chỉ số quan trọng

### EAR (Eye Aspect Ratio)

- **Mắt mở**: EAR > 0.25
- **Mắt nhắm**: EAR < 0.25
- Công thức: `EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)`

### MAR (Mouth Aspect Ratio)

- **Bình thường**: MAR < 0.6
- **Đang ngáp**: MAR > 0.6
- Công thức: `MAR = (||p2-p8|| + ||p3-p7|| + ||p4-p6||) / (2 * ||p1-p5||)`

### Mức cảnh báo

- 🟢 **SAFE**: Tỉnh táo, không có dấu hiệu buồn ngủ
- 🟡 **WARNING**: Có dấu hiệu mệt mỏi (ngáp nhiều lần, điểm buồn ngủ > 50)
- 🔴 **DANGER**: Buồn ngủ nghiêm trọng (mắt nhắm quá lâu hoặc điểm buồn ngủ > 100)

## 🛠️ Chi tiết Module

### 1. face_detector.py

Sử dụng Mediapipe Face Mesh để:

- Phát hiện khuôn mặt trong video
- Trích xuất 468 điểm landmark trên khuôn mặt
- Lấy tọa độ các điểm quan trọng: mắt trái, mắt phải, miệng

### 2. ear_calculator.py

Tính toán Eye Aspect Ratio:

- So sánh khoảng cách dọc và ngang của mắt
- Xác định trạng thái mắt mở/nhắm

### 3. mar_calculator.py

Tính toán Mouth Aspect Ratio:

- Đo độ mở miệng theo chiều dọc và ngang
- Phát hiện hành vi ngáp

### 4. drowsiness_detector.py

Thuật toán phát hiện buồn ngủ:

- Đếm số frame mắt nhắm liên tục
- Đếm số lần ngáp
- Tính điểm buồn ngủ tích lũy
- Đưa ra mức độ cảnh báo (SAFE/WARNING/DANGER)

### 5. camera_processor.py

Xử lý video:

- Đọc frame từ camera
- Kết hợp các module để phân tích
- Vẽ thông tin lên frame

### 6. gui.py

Giao diện Kivy:

- Hiển thị video real-time
- Hiển thị trạng thái và các chỉ số
- Nút điều khiển (Bắt đầu/Dừng)
- Phát âm thanh cảnh báo

## 🎵 Âm thanh cảnh báo (Tùy chọn)

Để kích hoạt âm thanh cảnh báo, đặt file `alarm.wav` hoặc `alarm.mp3` vào thư mục gốc.

Tạo file âm thanh đơn giản bằng Python:

```python
# Cần cài: pip install numpy soundfile
import numpy as np
import soundfile as sf

# Tạo âm beep 1kHz, 1 giây
fs = 44100  # Tần số lấy mẫu
duration = 1  # Giây
frequency = 1000  # Hz
t = np.linspace(0, duration, int(fs * duration))
audio = 0.5 * np.sin(2 * np.pi * frequency * t)

sf.write('alarm.wav', audio, fs)
```

## 🧪 Kiểm thử

Chạy các module riêng lẻ để kiểm thử:

```python
# Test Face Detector
python -c "from face_detector import FaceDetector; import cv2; fd = FaceDetector(); cap = cv2.VideoCapture(0); ret, frame = cap.read(); print(fd.detect_face(frame))"

# Test EAR Calculator
python -c "from ear_calculator import EARCalculator; print(EARCalculator.calculate_ear([(0,0), (0,10), (0,12), (20,0), (0,-10), (0,-12)]))"

# Test MAR Calculator
python -c "from mar_calculator import MARCalculator; print(MARCalculator.calculate_mar([(0,0), (0,5), (0,7), (0,8), (15,0), (0,-8), (0,-7), (0,-5)]))"
```

## ⚠️ Lưu ý

- Ứng dụng chỉ mang tính chất hỗ trợ, KHÔNG thay thế việc nghỉ ngơi đầy đủ
- Cần có đủ ánh sáng để camera hoạt động tốt
- Khuôn mặt cần hiện rõ, không bị che khuất
- Không đeo kính râm khi sử dụng
- Nên nghỉ ngơi sau mỗi 2 giờ lái xe

## 🤝 Đóng góp

Mọi đóng góp đều được hoan nghênh! Vui lòng:

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📄 License

Dự án này được phát hành theo giấy phép MIT. Xem file `LICENSE` để biết thêm chi tiết.

## 📞 Liên hệ

- GitHub: [@TuanN05](https://github.com/TuanN05)
- Email: your.email@example.com

## 🙏 Acknowledgments

- [Mediapipe](https://mediapipe.dev/) - Face detection library
- [Kivy](https://kivy.org/) - Python UI framework
- [OpenCV](https://opencv.org/) - Computer vision library

---

**Lái xe an toàn! 🚗💨**
