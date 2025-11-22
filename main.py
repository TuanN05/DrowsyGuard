"""
DrowsyGuard - Ứng dụng phát hiện buồn ngủ khi lái xe
Phiên bản: 2.0 (Modular)
Yêu cầu: Python 3.8+, Kivy, OpenCV, Mediapipe, SciPy

Mô tả: 
    Ứng dụng sử dụng camera để phát hiện dấu hiệu buồn ngủ thông qua:
    - Eye Aspect Ratio (EAR): Phát hiện mắt nhắm
    - Mouth Aspect Ratio (MAR): Phát hiện ngáp
    - Thuật toán tích hợp: Đánh giá tổng thể trạng thái buồn ngủ

Cấu trúc module:
    - face_detector.py: Nhận diện khuôn mặt bằng Mediapipe
    - ear_calculator.py: Tính chỉ số EAR
    - mar_calculator.py: Tính chỉ số MAR
    - drowsiness_detector.py: Thuật toán phát hiện buồn ngủ
    - camera_processor.py: Xử lý video từ camera
    - gui.py: Giao diện người dùng
    - main.py: File khởi chạy ứng dụng
"""

from gui import DrowsyGuardApp


def main():
    """Hàm chính để chạy ứng dụng"""
    
    try:
        app = DrowsyGuardApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\n Ứng dụng đã dừng bởi người dùng")
    except Exception as e:
        print(f"\n\nLỗi: {e}")
        print("Vui lòng kiểm tra:")
        print("- Camera có hoạt động không?")
        print("- Đã cài đặt đủ thư viện chưa?  (Xem file requirements.txt)")
    finally:
        print("\nĐã đóng ứng dụng. Lái xe an toàn!")


if __name__ == '__main__':
    main()
