# DrowsyGuard - Hệ thống Cảnh báo Buồn ngủ khi Lái xe

## Tổng quan

DrowsyGuard là ứng dụng phát hiện và cảnh báo trạng thái buồn ngủ khi lái xe sử dụng công nghệ thị giác máy tính và trí tuệ nhân tạo. Hệ thống phân tích khuôn mặt người lái xe theo thời gian thực thông qua camera để nhận diện các dấu hiệu buồn ngủ như mắt nhắm kéo dài, ngáp nhiều lần, từ đó đưa ra cảnh báo kịp thời.

## Mục tiêu dự án

Mục tiêu chính của dự án là xây dựng một hệ thống hỗ trợ tài xế giảm thiểu nguy cơ tai nạn do buồn ngủ khi lái xe. Hệ thống hoạt động dựa trên các nguyên lý khoa học về phân tích hành vi và sinh trắc học khuôn mặt, kết hợp với thuật toán xử lý ảnh tiên tiến.

## Tính năng chính

- Phát hiện và theo dõi khuôn mặt theo thời gian thực
- Tính toán chỉ số EAR để phát hiện trạng thái mắt nhắm
- Tính toán chỉ số MAR để phát hiện hành vi ngáp
- Thuật toán tích hợp đánh giá mức độ buồn ngủ dựa trên nhiều yếu tố
- Hệ thống cảnh báo phân cấp theo mức độ nghiêm trọng
- Cảnh báo âm thanh khi phát hiện buồn ngủ
- Giao diện trực quan hiển thị các chỉ số và trạng thái real-time
- Khả năng ghi nhận và phân tích lịch sử trạng thái

## Yêu cầu hệ thống

### Phần cứng

- Camera webcam hoặc camera tích hợp trên laptop với độ phân giải tối thiểu 640x480
- CPU: Intel Core i3 hoặc tương đương trở lên
- RAM: Tối thiểu 4GB (khuyến nghị 8GB)
- Đủ ánh sáng để camera hoạt động hiệu quả

### Phần mềm

- Hệ điều hành: Windows 7 trở lên, macOS 10.12 trở lên, hoặc Linux (Ubuntu 18.04 trở lên)
- Python phiên bản 3.8, 3.9, 3.10 hoặc 3.11
- Các thư viện Python được liệt kê trong file requirements.txt

## Cài đặt

### Bước 1: Cài đặt Python

Tải và cài đặt Python 3.10 từ trang chủ python.org. Đảm bảo chọn tùy chọn "Add Python to PATH" khi cài đặt trên Windows.

### Bước 2: Tải mã nguồn

Tải xuống hoặc clone mã nguồn dự án về máy tính:

```bash
git clone <repository-url>
cd DrowsyGuard
```

### Bước 3: Tạo môi trường ảo

Tạo môi trường ảo Python để cô lập các thư viện:

```bash
python -m venv venv
```

Kích hoạt môi trường ảo:

- Trên Windows:

```bash
venv\Scripts\activate
```

- Trên macOS/Linux:

```bash
source venv/bin/activate
```

### Bước 4: Cài đặt thư viện

Cài đặt tất cả các thư viện cần thiết:

```bash
pip install numpy<2.0
pip install opencv-python opencv-contrib-python
pip install mediapipe
pip install scipy
pip install kivy
```

Hoặc sử dụng file requirements.txt nếu có:

```bash
pip install -r requirements.txt
```

### Bước 5: Kiểm tra cài đặt

Kiểm tra xem tất cả thư viện đã được cài đặt thành công:

```python
python -c "import cv2, mediapipe, scipy, kivy; print('Tat ca thu vien da duoc cai dat thanh cong')"
```

## Hướng dẫn sử dụng

### Khởi động ứng dụng

Chạy file chính để khởi động ứng dụng:

```bash
python main.py
```

### Các bước sử dụng

1. Khởi động ứng dụng bằng lệnh trên
2. Giao diện chính sẽ hiển thị với các thành phần:
   - Cửa sổ hiển thị video từ camera
   - Bảng điều khiển với các nút chức năng
   - Bảng thông tin hiển thị các chỉ số
3. Nhấn nút "Bắt đầu giám sát" để bắt đầu theo dõi
4. Điều chỉnh vị trí ngồi sao cho khuôn mặt hiển thị rõ ràng trong khung hình
5. Hệ thống sẽ tự động phân tích và hiển thị:
   - Khung viền các điểm landmark trên mắt và miệng
   - Chỉ số EAR và MAR hiện tại
   - Điểm buồn ngủ tích lũy
   - Trạng thái hiện tại (SAFE, WARNING, DANGER)
6. Khi phát hiện buồn ngủ, hệ thống sẽ:
   - Hiển thị cảnh báo màu đỏ trên màn hình
   - Phát âm thanh cảnh báo (nếu có)
   - Ghi nhận sự kiện vào lịch sử
7. Nhấn nút "Dừng" để kết thúc phiên giám sát

### Các chế độ hoạt động

Ứng dụng có thể điều chỉnh độ nhạy cảnh báo thông qua các ngưỡng trong mã nguồn:

- Chế độ tiêu chuẩn: Cảnh báo khi có dấu hiệu buồn ngủ rõ ràng
- Chế độ nhạy cao: Cảnh báo sớm hơn với ngưỡng thấp hơn
- Chế độ khoan dung: Chỉ cảnh báo khi buồn ngủ nghiêm trọng

## Kiến trúc hệ thống

### Cấu trúc thư mục

```
DrowsyGuard/
│
├── main.py                    # Điểm khởi động ứng dụng
├── gui.py                     # Module giao diện người dùng
├── camera_processor.py        # Module xử lý video và tích hợp các thành phần
├── face_detector.py           # Module phát hiện khuôn mặt
├── ear_calculator.py          # Module tính toán EAR
├── mar_calculator.py          # Module tính toán MAR
├── drowsiness_detector.py     # Module thuật toán phát hiện buồn ngủ
├── requirements.txt           # Danh sách thư viện cần thiết
├── README.md                  # Tài liệu hướng dẫn
├── CHANGELOG.md              # Lịch sử thay đổi phiên bản
└── __pycache__/              # Thư mục cache Python
```

### Luồng dữ liệu

```
Camera → Face Detector → Landmarks Extraction
                              ↓
                    ┌─────────┴─────────┐
                    ↓                   ↓
              EAR Calculator      MAR Calculator
                    ↓                   ↓
                    └─────────┬─────────┘
                              ↓
                   Drowsiness Detector
                              ↓
                    ┌─────────┴─────────┐
                    ↓                   ↓
              GUI Display          Alert System
```

## Chi tiết các module

### 1. main.py

File chính khởi động ứng dụng. Chức năng:

- Khởi tạo và chạy ứng dụng GUI
- Hiển thị thông tin hướng dẫn sử dụng
- Xử lý các ngoại lệ và lỗi trong quá trình chạy
- In ra console các thông tin hướng dẫn và chỉ số quan trọng

### 2. face_detector.py

Module phát hiện khuôn mặt sử dụng Mediapipe Face Mesh. Chức năng:

**Khởi tạo:**

- Khởi tạo Mediapipe Face Mesh với các tham số cấu hình
- Hỗ trợ tối đa 1 khuôn mặt trong frame
- Ngưỡng tin cậy phát hiện: 0.5 (mặc định)
- Ngưỡng tin cậy theo dõi: 0.5 (mặc định)

**Phương thức chính:**

`detect_face(frame)`

- Nhận frame ảnh BGR từ camera
- Chuyển đổi sang RGB cho Mediapipe
- Phát hiện khuôn mặt và trích xuất 468 điểm landmark
- Trả về trạng thái phát hiện và dictionary chứa landmarks

`draw_landmarks(frame, landmarks_dict, draw_eyes, draw_mouth)`

- Vẽ các đường viền lên frame
- Mắt trái: polyline màu xanh lá
- Mắt phải: polyline màu xanh lá
- Miệng: polyline màu xanh dương

**Landmarks quan trọng:**

- Mắt trái: 6 điểm [362, 385, 387, 263, 373, 380]
- Mắt phải: 6 điểm [33, 160, 158, 133, 153, 144]
- Miệng: 8 điểm [78, 308, 13, 14, 81, 178, 311, 402]

### 3. ear_calculator.py

Module tính toán Eye Aspect Ratio để xác định trạng thái mắt. Chi tiết:

**Công thức EAR:**

```
EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)
```

Trong đó:

- p1, p4: Điểm góc ngoài và góc trong mắt (khoảng cách ngang)
- p2, p3, p5, p6: Các điểm trên và dưới mắt (khoảng cách dọc)

**Ngưỡng phân loại:**

- EAR >= 0.25: Mắt mở
- EAR < 0.25: Mắt nhắm

**Phương thức:**

`calculate_ear(eye_landmarks)`

- Tính EAR cho một mắt
- Sử dụng khoảng cách Euclidean từ scipy.spatial.distance
- Trả về giá trị float (thường trong khoảng 0.15-0.35)

`calculate_avg_ear(left_eye_landmarks, right_eye_landmarks)`

- Tính EAR trung bình của cả hai mắt
- Giảm nhiễu bằng cách lấy trung bình

`is_eyes_closed(ear_value)`

- Kiểm tra trạng thái mắt dựa trên ngưỡng
- Trả về True nếu mắt nhắm, False nếu mắt mở

`get_eye_state(ear_value)`

- Trả về trạng thái dạng chuỗi: "CLOSED" hoặc "OPEN"

**Ý nghĩa khoa học:**
EAR đo tỷ lệ giữa chiều cao và chiều rộng của mắt. Khi mắt nhắm, chiều cao giảm xuống gần 0, làm EAR giảm đáng kể. Chỉ số này ổn định và ít bị ảnh hưởng bởi hướng nhìn hoặc góc nghiêng đầu nhẹ.

### 4. mar_calculator.py

Module tính toán Mouth Aspect Ratio để phát hiện ngáp. Chi tiết:

**Công thức MAR:**

```
MAR = (||top-bottom|| + ||top_left-bottom_left|| + ||top_right-bottom_right||) / (3 * ||left-right||)
```

Trong đó:

- Các khoảng cách dọc đo độ mở miệng theo chiều cao
- Khoảng cách ngang đo chiều rộng miệng

**Ngưỡng phân loại:**

- MAR <= 0.6: Bình thường
- MAR > 0.6: Đang ngáp

**Phương thức:**

`calculate_mar(mouth_landmarks)`

- Tính MAR từ 8 điểm landmark miệng
- Sử dụng 3 cặp điểm dọc và 1 cặp điểm ngang
- Trả về giá trị float (thường trong khoảng 0.2-0.8)

`is_yawning(mar_value)`

- Kiểm tra trạng thái ngáp dựa trên ngưỡng
- Trả về True nếu đang ngáp, False nếu bình thường

`get_mouth_state(mar_value)`

- Trả về trạng thái dạng chuỗi: "YAWNING" hoặc "NORMAL"

**Các điểm landmark miệng:**

- Góc trong trái: 78
- Góc trong phải: 308
- Trên giữa: 13
- Dưới giữa: 14
- Điểm phụ trên trái: 81
- Điểm phụ dưới trái: 178
- Điểm phụ trên phải: 311
- Điểm phụ dưới phải: 402

**Ý nghĩa khoa học:**
Ngáp là dấu hiệu quan trọng của buồn ngủ. Khi ngáp, miệng mở rộng theo cả hai chiều dọc và ngang, làm MAR tăng đáng kể. Công thức sử dụng nhiều điểm đo để tăng độ chính xác.

### 5. drowsiness_detector.py

Module chứa thuật toán chính phát hiện buồn ngủ. Chi tiết:

**Các ngưỡng và tham số:**

```python
EYE_CLOSED_FRAMES_THRESHOLD = 90    # ~3 giây ở 30 FPS
YAWN_FRAMES_THRESHOLD = 60          # ~2 giây ở 30 FPS
YAWN_COUNT_THRESHOLD = 4            # Số lần ngáp cảnh báo
YAWN_RESET_FRAMES = 600             # 20 giây reset đếm ngáp
DROWSINESS_SCORE_THRESHOLD = 200    # Điểm buồn ngủ cảnh báo
```

**Biến trạng thái:**

- `eye_closed_frames`: Đếm số frame mắt nhắm liên tục
- `yawn_frames`: Đếm số frame đang ngáp
- `total_yawns`: Tổng số lần ngáp trong khoảng thời gian
- `drowsiness_score`: Điểm buồn ngủ tích lũy
- `alert_active`: Trạng thái cảnh báo có đang kích hoạt
- `pause_scoring_frames`: Số frame tạm dừng tính điểm sau reset
- `frames_since_last_yawn`: Đếm frame từ lần ngáp cuối

**Thuật toán tính điểm buồn ngủ:**

1. Mỗi frame mắt nhắm: +0.5 điểm
2. Mỗi frame mắt mở: -0.3 điểm (giảm dần về 0)
3. Mỗi lần ngáp (kéo dài đủ thời gian): +50 điểm
4. Sau 20 giây không ngáp: Reset số lần ngáp về 0

**Phương thức chính:**

`update(ear_value, mar_value)`

- Nhận giá trị EAR và MAR hiện tại
- Cập nhật các biến đếm và điểm số
- Xác định mức độ cảnh báo
- Trả về dictionary chứa đầy đủ thông tin trạng thái

**Mức độ cảnh báo:**

SAFE:

- Không có dấu hiệu buồn ngủ
- Điểm buồn ngủ < 100
- Màu xanh lá

WARNING:

- Có dấu hiệu mệt mỏi
- Điểm buồn ngủ >= 100 và < 200
- Màu cam

DANGER:

- Mắt nhắm >= 90 frame liên tục (3 giây), HOẶC
- Ngáp >= 4 lần trong 20 giây, HOẶC
- Điểm buồn ngủ >= 200
- Màu đỏ, kích hoạt âm thanh cảnh báo

**Cơ chế tạm dừng:**
Sau khi reset (khi người dùng tỉnh lại), hệ thống tạm dừng tính điểm trong 90 frame (3 giây) để tránh cảnh báo nhầm ngay sau khi phục hồi.

### 6. camera_processor.py

Module tích hợp xử lý video và các thành phần phân tích. Chi tiết:

**Khởi tạo:**

- Tạo đối tượng VideoCapture của OpenCV
- Khởi tạo các module: FaceDetector, DrowsinessDetector
- Quản lý trạng thái chạy/dừng

**Phương thức chính:**

`start()`

- Khởi động camera với index được chỉ định (mặc định 0)
- Kiểm tra camera có mở thành công không
- Reset các biến đếm của DrowsinessDetector
- Trả về True nếu thành công, False nếu thất bại

`stop()`

- Dừng xử lý và giải phóng camera
- Reset tất cả trạng thái về mặc định

`process_frame()`

- Đọc một frame từ camera
- Lật ảnh theo chiều ngang (hiệu ứng gương)
- Gọi FaceDetector để phát hiện khuôn mặt
- Nếu phát hiện khuôn mặt:
  - Tính EAR từ landmarks mắt
  - Tính MAR từ landmarks miệng
  - Cập nhật DrowsinessDetector
  - Vẽ landmarks lên frame
  - Vẽ thông tin trạng thái
- Nếu không phát hiện: Vẽ cảnh báo "Không phát hiện khuôn mặt"
- Trả về tuple (success, frame, status)

`_draw_info_on_frame(frame, status)`

- Vẽ text trạng thái chính (SAFE/WARNING/DANGER)
- Hiển thị giá trị EAR và MAR ở góc phải trên
- Hiển thị số lần ngáp nếu > 0
- Vẽ thanh progress điểm buồn ngủ ở dưới cùng:
  - Màu xanh lá: < 50%
  - Màu cam: >= 50% và < 100%
  - Màu đỏ: >= 100%
- Vẽ cảnh báo lớn ">>> BUON NGU! <<<" khi ở mức DANGER

`_draw_no_face_warning(frame)`

- Vẽ text cảnh báo không phát hiện khuôn mặt
- Màu vàng để dễ nhận biết

`get_current_status()`

- Trả về trạng thái hiện tại của hệ thống
- Dùng để các module khác truy vấn thông tin

### 7. gui.py

Module giao diện người dùng sử dụng framework Kivy. Chi tiết:

**Kiến trúc giao diện:**

```
DrowsyGuardApp (Kivy App)
    └── MainLayout (BoxLayout)
        ├── HeaderLabel (Label)
        ├── VideoArea (BoxLayout)
        │   └── VideoImage (Image)
        ├── InfoPanel (GroupBox)
        │   ├── StatusPanel (GroupBox)
        │   ├── MetricsPanel (GroupBox)
        │   └── ScorePanel (GroupBox)
        └── ControlPanel (BoxLayout)
            ├── StartButton (Button)
            ├── StopButton (Button)
            └── ResetButton (Button)
```

**GroupBox Widget:**

- Widget tùy chỉnh mô phỏng GroupBox kiểu cổ điển
- Có viền và tiêu đề
- Màu nền tối với viền sáng
- Sử dụng để nhóm các thành phần liên quan

**Các panel thông tin:**

StatusPanel:

- Hiển thị trạng thái hiện tại (SAFE/WARNING/DANGER)
- Màu sắc thay đổi theo mức độ cảnh báo
- Font chữ lớn, in đậm để dễ nhìn

MetricsPanel:

- Hiển thị chỉ số EAR và ngưỡng
- Hiển thị chỉ số MAR và ngưỡng
- Hiển thị trạng thái mắt và miệng
- Cập nhật theo thời gian thực

ScorePanel:

- Hiển thị điểm buồn ngủ hiện tại
- Hiển thị số lần ngáp
- Hiển thị số frame mắt nhắm
- Progress bar trực quan

**Xử lý video:**

`update_video(dt)`

- Được gọi 30 lần/giây bởi Clock.schedule_interval
- Lấy frame từ CameraProcessor
- Chuyển đổi frame BGR sang RGB
- Tạo texture Kivy từ frame
- Cập nhật Image widget
- Cập nhật các panel thông tin

**Xử lý cảnh báo:**

`check_alert(status)`

- Kiểm tra mức độ cảnh báo từ status
- Nếu DANGER và âm thanh chưa phát:
  - Phát file âm thanh cảnh báo
  - Đặt cờ sound_playing = True
- Nếu không còn DANGER:
  - Reset cờ sound_playing = False

**Nút điều khiển:**

Start Button:

- Khởi động camera và bắt đầu giám sát
- Vô hiệu hóa khi đang chạy
- Enable Stop và Reset buttons

Stop Button:

- Dừng giám sát và giải phóng camera
- Enable Start button
- Vô hiệu hóa khi đang dừng

Reset Button:

- Reset tất cả điểm số và đếm về 0
- Dừng âm thanh cảnh báo nếu đang phát
- Có thể dùng khi đang chạy hoặc dừng

**Cấu hình âm thanh:**

- Tự động tìm file alarm.wav hoặc alarm.mp3
- Nếu không tìm thấy, in cảnh báo nhưng vẫn chạy bình thường
- Âm thanh chỉ phát một lần cho mỗi sự kiện cảnh báo

## Nguyên lý khoa học

### 1. Eye Aspect Ratio (EAR)

EAR là chỉ số đo tỷ lệ giữa chiều cao và chiều rộng của mắt. Nghiên cứu cho thấy:

- Khi người tỉnh táo, EAR dao động trong khoảng 0.25-0.35
- Khi chớp mắt hoặc nhắm mắt, EAR giảm xuống dưới 0.25
- Khi buồn ngủ, tần suất chớp mắt tăng và thời gian mắt nhắm kéo dài

Ưu điểm của EAR:

- Không phụ thuộc vào độ phân giải ảnh
- Ít bị ảnh hưởng bởi ánh sáng
- Tính toán nhanh, phù hợp xử lý real-time
- Ổn định với các góc nhìn khác nhau

### 2. Mouth Aspect Ratio (MAR)

MAR đo độ mở miệng, đặc biệt hữu ích trong phát hiện ngáp:

- Miệng bình thường: MAR khoảng 0.2-0.4
- Khi ngáp: MAR tăng lên trên 0.6
- Ngáp là dấu hiệu rõ ràng của mệt mỏi và buồn ngủ

Đặc điểm ngáp:

- Thường kéo dài 5-10 giây
- Miệng mở rộng cả chiều dọc và ngang
- Người buồn ngủ thường ngáp nhiều lần liên tiếp

### 3. Thuật toán tích hợp

Hệ thống không chỉ dựa vào một chỉ số mà kết hợp nhiều yếu tố:

**Phát hiện mắt nhắm kéo dài:**

- Đếm số frame liên tục mắt nhắm
- Nếu >= 90 frame (3 giây) → Cảnh báo DANGER
- Đây là dấu hiệu buồn ngủ nghiêm trọng

**Phát hiện ngáp nhiều lần:**

- Đếm số lần ngáp thực sự (kéo dài >= 2 giây)
- Reset số đếm sau 20 giây không ngáp
- Nếu >= 4 lần ngáp → Cảnh báo DANGER

**Điểm buồn ngủ tích lũy:**

- Tăng dần khi có dấu hiệu buồn ngủ
- Giảm dần khi tỉnh táo
- Phản ánh xu hướng tổng thể
- Cảnh báo khi vượt ngưỡng

Sự kết hợp này giúp:

- Giảm false positive (cảnh báo nhầm)
- Tăng độ tin cậy
- Phát hiện sớm các giai đoạn buồn ngủ khác nhau

## Các thông số có thể điều chỉnh

Người dùng có thể tinh chỉnh hệ thống bằng cách sửa các hằng số trong mã nguồn:

### Trong ear_calculator.py:

```python
EYE_CLOSED_THRESHOLD = 0.25  # Ngưỡng mắt nhắm
```

- Giảm giá trị: Nhạy hơn, phát hiện mắt nhắm sớm hơn
- Tăng giá trị: Khoan dung hơn, chỉ phát hiện khi mắt nhắm chặt

### Trong mar_calculator.py:

```python
YAWN_THRESHOLD = 0.6  # Ngưỡng ngáp
```

- Giảm giá trị: Phát hiện ngáp dễ hơn
- Tăng giá trị: Chỉ phát hiện ngáp rất rõ ràng

### Trong drowsiness_detector.py:

```python
EYE_CLOSED_FRAMES_THRESHOLD = 90  # Số frame mắt nhắm cảnh báo
YAWN_FRAMES_THRESHOLD = 60        # Số frame ngáp tối thiểu
YAWN_COUNT_THRESHOLD = 4          # Số lần ngáp cảnh báo
YAWN_RESET_FRAMES = 600           # Thời gian reset đếm ngáp
DROWSINESS_SCORE_THRESHOLD = 200  # Ngưỡng điểm buồn ngủ
```

Điều chỉnh các tham số này cho phép tùy chỉnh độ nhạy phù hợp với từng người dùng.

## Xử lý lỗi và khắc phục sự cố

### Lỗi: Camera không khởi động được

Nguyên nhân và giải pháp:

- Camera đang được sử dụng bởi ứng dụng khác → Đóng các ứng dụng camera khác
- Không có camera → Kết nối camera USB hoặc sử dụng camera tích hợp
- Camera bị vô hiệu hóa → Bật camera trong Device Manager (Windows)
- Quyền truy cập camera bị từ chối → Cấp quyền cho ứng dụng Python

### Lỗi: Không phát hiện khuôn mặt

Nguyên nhân và giải pháp:

- Ánh sáng không đủ → Tăng độ sáng phòng
- Khuôn mặt quá xa camera → Di chuyển gần hơn (60-100cm)
- Góc chụp không phù hợp → Điều chỉnh camera nhìn thẳng vào mặt
- Camera bị mờ → Lau sạch ống kính

### Lỗi: Import module thất bại

Nguyên nhân và giải pháp:

- Chưa cài đặt thư viện → Chạy pip install -r requirements.txt
- Cài đặt sai phiên bản Python → Sử dụng Python 3.8-3.11
- Môi trường ảo chưa kích hoạt → Kích hoạt venv trước khi chạy

### Lỗi: Ứng dụng chậm, lag

Nguyên nhân và giải pháp:

- CPU yếu → Giảm độ phân giải camera
- Nhiều ứng dụng chạy → Đóng các ứng dụng không cần thiết
- Driver camera cũ → Cập nhật driver mới nhất

### Cảnh báo nhầm quá nhiều

Giải pháp:

- Tăng các ngưỡng trong drowsiness_detector.py
- Đảm bảo ánh sáng đủ và đồng đều
- Điều chỉnh góc camera phù hợp

## Hạn chế và phát triển tương lai

### Hạn chế hiện tại:

1. Phụ thuộc điều kiện ánh sáng
2. Yêu cầu khuôn mặt phải hiện rõ và chính diện
3. Có thể bị ảnh hưởng bởi kính mát hoặc khẩu trang
4. Chưa có khả năng lưu trữ và phân tích lịch sử dài hạn
5. Chỉ hỗ trợ một người tại một thời điểm

### Hướng phát triển:

1. Tích hợp thêm các chỉ số sinh học khác:

   - Tần suất chớp mắt
   - Tốc độ chớp mắt
   - Độ nghiêng đầu
   - Hướng nhìn

2. Sử dụng deep learning:

   - CNN để nhận dạng trạng thái buồn ngủ trực tiếp
   - LSTM để phân tích chuỗi thời gian
   - Transfer learning từ các mô hình pretrained

3. Tính năng bổ sung:

   - Ghi log chi tiết và xuất báo cáo
   - Gửi cảnh báo qua email/SMS
   - Tích hợp với hệ thống xe hơi
   - Kết nối với thiết bị đeo tay theo dõi sức khỏe
   - Hỗ trợ multi-camera
   - Cloud sync để phân tích xu hướng

4. Cải thiện thuật toán:

   - Adaptive threshold theo từng cá nhân
   - Machine learning để học pattern buồn ngủ của người dùng
   - Phát hiện sớm hơn dựa trên micro-expressions

5. Tối ưu hiệu năng:
   - Sử dụng GPU acceleration
   - Tối ưu code cho embedded systems
   - Giảm độ trễ xử lý

## Bảo mật và quyền riêng tư

Ứng dụng được thiết kế với nguyên tắc bảo vệ quyền riêng tư:

- Không lưu trữ hình ảnh hoặc video
- Không truyền dữ liệu lên internet
- Chỉ xử lý trên thiết bị local
- Không thu thập thông tin cá nhân
- Không có kết nối mạng

Người dùng có toàn quyền kiểm soát dữ liệu của mình.

## Kiểm thử

### Kiểm thử từng module:

**Test Face Detector:**

```python
from face_detector import FaceDetector
import cv2

fd = FaceDetector()
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
face_detected, landmarks = fd.detect_face(frame)
print(f"Phat hien khuon mat: {face_detected}")
if landmarks:
    print(f"So diem mat trai: {len(landmarks['left_eye'])}")
    print(f"So diem mat phai: {len(landmarks['right_eye'])}")
    print(f"So diem mieng: {len(landmarks['mouth'])}")
cap.release()
```

**Test EAR Calculator:**

```python
from ear_calculator import EARCalculator

# Giả lập landmarks mắt mở
open_eye = [(0,0), (5,15), (10,18), (40,0), (10,-18), (5,-15)]
ear_open = EARCalculator.calculate_ear(open_eye)
print(f"EAR mat mo: {ear_open:.3f}")
print(f"Trang thai: {EARCalculator.get_eye_state(ear_open)}")

# Giả lập landmarks mắt nhắm
closed_eye = [(0,0), (5,2), (10,2), (40,0), (10,-2), (5,-2)]
ear_closed = EARCalculator.calculate_ear(closed_eye)
print(f"EAR mat nham: {ear_closed:.3f}")
print(f"Trang thai: {EARCalculator.get_eye_state(ear_closed)}")
```

**Test MAR Calculator:**

```python
from mar_calculator import MARCalculator

# Giả lập landmarks miệng bình thường
normal_mouth = [(0,0), (100,0), (50,10), (50,-10), (25,8), (25,-8), (75,8), (75,-8)]
mar_normal = MARCalculator.calculate_mar(normal_mouth)
print(f"MAR binh thuong: {mar_normal:.3f}")
print(f"Trang thai: {MARCalculator.get_mouth_state(mar_normal)}")

# Giả lập landmarks miệng ngáp
yawn_mouth = [(0,0), (100,0), (50,35), (50,-35), (25,30), (25,-30), (75,30), (75,-30)]
mar_yawn = MARCalculator.calculate_mar(yawn_mouth)
print(f"MAR ngap: {mar_yawn:.3f}")
print(f"Trang thai: {MARCalculator.get_mouth_state(mar_yawn)}")
```

**Test Drowsiness Detector:**

```python
from drowsiness_detector import DrowsinessDetector

dd = DrowsinessDetector()

# Mô phỏng mắt mở
for i in range(10):
    status = dd.update(ear_value=0.30, mar_value=0.3)
    print(f"Frame {i}: {status['alert_level']} - {status['reason']}")

# Mô phỏng mắt nhắm kéo dài
for i in range(100):
    status = dd.update(ear_value=0.20, mar_value=0.3)
    if i % 30 == 0:
        print(f"Frame {i}: {status['alert_level']} - Score: {status['drowsiness_score']:.1f}")
```

### Kiểm thử tích hợp:

Chạy ứng dụng đầy đủ và thực hiện các kịch bản:

1. Ngồi tỉnh táo trước camera trong 1 phút
2. Nhắm mắt 3 giây liên tục
3. Ngáp 4 lần trong vòng 30 giây
4. Kiểm tra cảnh báo có xuất hiện đúng lúc

## Câu hỏi thường gặp

**Hỏi: Ứng dụng có hoạt động trong tối không?**
Đáp: Không hiệu quả. Cần có đủ ánh sáng để camera phát hiện khuôn mặt rõ ràng.

**Hỏi: Có thể sử dụng camera điện thoại không?**
Đáp: Có, nếu kết nối điện thoại làm webcam qua USB hoặc IP Camera.

**Hỏi: Ứng dụng có tốn pin không?**
Đáp: Có, xử lý video real-time tiêu tốn CPU đáng kể.

**Hỏi: Có thể chạy trên Raspberry Pi không?**
Đáp: Có nhưng cần model nhẹ hơn hoặc giảm FPS để tránh lag.

**Hỏi: Dữ liệu có được lưu lại không?**
Đáp: Không, ứng dụng không lưu video hoặc hình ảnh.

**Hỏi: Độ chính xác như thế nào?**
Đáp: Phụ thuộc điều kiện, thường đạt 85-95% trong điều kiện tốt.

**Hỏi: Có thể tùy chỉnh âm thanh cảnh báo không?**
Đáp: Có, thay file alarm.wav hoặc alarm.mp3 bằng âm thanh mong muốn.

## Đóng góp

Dự án hoan nghênh mọi đóng góp từ cộng đồng. Các hình thức đóng góp:

- Báo cáo lỗi và đề xuất tính năng qua Issues
- Cải thiện mã nguồn và gửi Pull Requests
- Viết tài liệu và hướng dẫn
- Chia sẻ kinh nghiệm sử dụng
- Thử nghiệm trên các môi trường khác nhau

Khi đóng góp code, vui lòng:

1. Fork repository
2. Tạo branch mới cho tính năng: `git checkout -b feature/TinhNangMoi`
3. Commit với message rõ ràng: `git commit -m 'Them tinh nang X'`
4. Push lên branch: `git push origin feature/TinhNangMoi`
5. Tạo Pull Request với mô tả chi tiết

## Giấy phép

Dự án được phát hành dưới giấy phép MIT. Điều này có nghĩa:

- Tự do sử dụng cho mục đích cá nhân và thương mại
- Tự do sửa đổi và phân phối
- Không có bảo hành, sử dụng với trách nhiệm của bản thân
- Phải giữ nguyên thông tin giấy phép khi phân phối

## Tuyên bố miễn trừ trách nhiệm

Ứng dụng này được phát triển cho mục đích nghiên cứu và hỗ trợ. Nó KHÔNG THỂ thay thế:

- Nghỉ ngơi đầy đủ trước khi lái xe
- Ý thức an toàn của người lái xe
- Các biện pháp an toàn giao thông khác

Người dùng hoàn toàn chịu trách nhiệm về an toàn khi lái xe. Nhà phát triển không chịu trách nhiệm về bất kỳ thiệt hại nào phát sinh từ việc sử dụng ứng dụng.

## Tài nguyên tham khảo

Các nghiên cứu và công trình có liên quan:

1. Soukupova T. and Cech J., "Real-Time Eye Blink Detection using Facial Landmarks", 21st Computer Vision Winter Workshop, 2016

2. Drutarovsky T. and Fogelton A., "Eye Blink Detection using Variance of Motion Vectors", Computer Vision - ECCV 2014 Workshops, 2014

3. Zhang W., et al., "Driver Drowsiness Recognition Based on Computer Vision Technology", Tsinghua Science and Technology, 2012

4. Mediapipe Face Mesh Documentation: https://google.github.io/mediapipe/solutions/face_mesh.html

5. OpenCV Documentation: https://docs.opencv.org/

6. Kivy Framework Documentation: https://kivy.org/doc/stable/

## Lịch sử phiên bản

Chi tiết về các phiên bản xem file CHANGELOG.md

---

Cảm ơn bạn đã sử dụng DrowsyGuard. Lái xe an toàn!
