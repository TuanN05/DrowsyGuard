"""
DrowsyGuard - Ứng dụng phát hiện buồn ngủ khi lái xe
Phiên bản: 2.0 (Modular)
Yêu cầu: Python 3.8+, Kivy, OpenCV, Mediapipe, SciPy

Tác giả: DrowsyGuard Team
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
    print("=" * 60)
    print("DrowsyGuard v2.0 - Hệ thống cảnh báo buồn ngủ")
    print("=" * 60)
    print("\nKhởi động ứng dụng...")
    print("\nHướng dẫn sử dụng:")
    print("1. Nhấn 'Bắt đầu giám sát' để bắt đầu")
    print("2. Đảm bảo khuôn mặt bạn hiện rõ trước camera")
    print("3. Ứng dụng sẽ phân tích và cảnh báo khi phát hiện buồn ngủ")
    print("4. Nhấn 'Dừng' để kết thúc giám sát")
    print("\nChỉ số quan trọng:")
    print("- EAR < 0.25: Mắt đang nhắm")
    print("- MAR > 0.6: Đang ngáp")
    print("- Điểm buồn ngủ > 100: Cảnh báo nghiêm trọng")
    print("\n" + "=" * 60 + "\n")
    
    try:
        app = DrowsyGuardApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\nỨng dụng đã dừng bởi người dùng")
    except Exception as e:
        print(f"\n\nLỗi: {e}")
        print("Vui lòng kiểm tra:")
        print("- Camera có hoạt động không?")
        print("- Đã cài đặt đủ thư viện chưa? (pip install -r requirements.txt)")
    finally:
        print("\nĐã đóng ứng dụng. Lái xe an toàn!")


if __name__ == '__main__':
    main()
