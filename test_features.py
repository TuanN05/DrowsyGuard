"""
Script test các tính năng mới của DrowsyGuard v2.1
Mô phỏng các tình huống phát hiện buồn ngủ
"""

from drowsiness_detector import DrowsinessDetector
from ear_calculator import EARCalculator
from mar_calculator import MARCalculator


def test_yawn_detection():
    """Test phát hiện ngáp nhiều lần"""
    print("\n" + "="*60)
    print("TEST 1: Phát hiện ngáp 2 lần")
    print("="*60)
    
    detector = DrowsinessDetector()
    
    # Mô phỏng 40 frame (khoảng 1.3 giây)
    for frame in range(1, 41):
        # Frame 5-20: Ngáp lần 1 (MAR cao)
        # Frame 25-40: Ngáp lần 2 (MAR cao)
        if 5 <= frame <= 20 or 25 <= frame <= 40:
            ear = 0.30  # Mắt mở
            mar = 0.70  # Miệng mở to (ngáp)
        else:
            ear = 0.30  # Mắt mở
            mar = 0.40  # Miệng bình thường
        
        status = detector.update(ear, mar)
        
        if frame in [5, 20, 25, 40] or status['drowsy']:
            print(f"\nFrame {frame}:")
            print(f"  - EAR: {ear:.2f}, MAR: {mar:.2f}")
            print(f"  - Số lần ngáp: {status['total_yawns']}")
            print(f"  - Điểm buồn ngủ: {status['drowsiness_score']}")
            print(f"  - Mức cảnh báo: {status['alert_level']}")
            print(f"  - Lý do: {status['reason']}")
            
            if status['drowsy']:
                print(f"  - ⚠️ CẢNH BÁO NGHIÊM TRỌNG! Cần xác nhận!")
                break
    
    print(f"\n✅ Kết quả: Phát hiện buồn ngủ sau {status['total_yawns']} lần ngáp")


def test_eye_closure():
    """Test phát hiện nhắm mắt lâu"""
    print("\n" + "="*60)
    print("TEST 2: Phát hiện nhắm mắt quá lâu")
    print("="*60)
    
    detector = DrowsinessDetector()
    
    # Mô phỏng nhắm mắt 25 frame liên tục
    for frame in range(1, 26):
        ear = 0.20  # Mắt nhắm (< 0.25)
        mar = 0.40  # Miệng bình thường
        
        status = detector.update(ear, mar)
        
        if frame % 5 == 0 or status['drowsy']:
            print(f"\nFrame {frame}:")
            print(f"  - EAR: {ear:.2f} (Mắt nhắm)")
            print(f"  - Số frame mắt nhắm: {status['eye_closed_frames']}")
            print(f"  - Điểm buồn ngủ: {status['drowsiness_score']}")
            print(f"  - Mức cảnh báo: {status['alert_level']}")
            
            if status['drowsy']:
                print(f"  - ⚠️ CẢNH BÁO! Mắt nhắm quá lâu!")
                break
    
    print(f"\n✅ Kết quả: Phát hiện buồn ngủ sau {status['eye_closed_frames']} frame")


def test_score_accumulation():
    """Test tích lũy điểm buồn ngủ"""
    print("\n" + "="*60)
    print("TEST 3: Tích lũy điểm buồn ngủ")
    print("="*60)
    
    detector = DrowsinessDetector()
    
    # Mô phỏng: nhắm mắt ngắn nhiều lần + ngáp 1 lần
    for frame in range(1, 101):
        # Mỗi 10 frame nhắm mắt 3 frame
        if frame % 10 <= 3:
            ear = 0.20  # Mắt nhắm
            mar = 0.40
        # Frame 50-65: Ngáp 1 lần
        elif 50 <= frame <= 65:
            ear = 0.30  # Mắt mở
            mar = 0.70  # Ngáp
        else:
            ear = 0.30  # Mắt mở
            mar = 0.40
        
        status = detector.update(ear, mar)
        
        if frame % 20 == 0 or status['drowsy']:
            print(f"\nFrame {frame}:")
            print(f"  - Điểm buồn ngủ: {status['drowsiness_score']}")
            print(f"  - Số lần ngáp: {status['total_yawns']}")
            print(f"  - Mức cảnh báo: {status['alert_level']}")
            
            if status['drowsy']:
                print(f"  - ⚠️ CẢNH BÁO! Điểm buồn ngủ quá cao!")
                break
    
    print(f"\n✅ Kết quả: Phát hiện buồn ngủ ở điểm {status['drowsiness_score']}")


def test_ear_calculator():
    """Test tính toán EAR"""
    print("\n" + "="*60)
    print("TEST 4: Tính toán EAR")
    print("="*60)
    
    # Mô phỏng tọa độ 6 điểm mắt
    # [góc_ngoài, trên1, trên2, góc_trong, dưới1, dưới2]
    
    # Mắt mở rộng
    eye_open = [(0, 0), (10, 10), (20, 10), (30, 0), (20, -10), (10, -10)]
    ear_open = EARCalculator.calculate_ear(eye_open)
    print(f"\nMắt mở rộng:")
    print(f"  - EAR: {ear_open:.3f}")
    print(f"  - Trạng thái: {EARCalculator.get_eye_state(ear_open)}")
    
    # Mắt hơi nhắm
    eye_half = [(0, 0), (10, 5), (20, 5), (30, 0), (20, -5), (10, -5)]
    ear_half = EARCalculator.calculate_ear(eye_half)
    print(f"\nMắt hơi nhắm:")
    print(f"  - EAR: {ear_half:.3f}")
    print(f"  - Trạng thái: {EARCalculator.get_eye_state(ear_half)}")
    
    # Mắt nhắm kín
    eye_closed = [(0, 0), (10, 1), (20, 1), (30, 0), (20, -1), (10, -1)]
    ear_closed = EARCalculator.calculate_ear(eye_closed)
    print(f"\nMắt nhắm kín:")
    print(f"  - EAR: {ear_closed:.3f}")
    print(f"  - Trạng thái: {EARCalculator.get_eye_state(ear_closed)}")


def test_mar_calculator():
    """Test tính toán MAR"""
    print("\n" + "="*60)
    print("TEST 5: Tính toán MAR")
    print("="*60)
    
    # Mô phỏng tọa độ 8 điểm miệng
    # [góc_trái, trên1, trên2, trên3, góc_phải, dưới1, dưới2, dưới3]
    
    # Miệng bình thường
    mouth_normal = [(0, 0), (10, 2), (20, 2), (30, 2), (40, 0), (30, -2), (20, -2), (10, -2)]
    mar_normal = MARCalculator.calculate_mar(mouth_normal)
    print(f"\nMiệng bình thường:")
    print(f"  - MAR: {mar_normal:.3f}")
    print(f"  - Trạng thái: {MARCalculator.get_mouth_state(mar_normal)}")
    
    # Miệng hơi mở
    mouth_open = [(0, 0), (10, 5), (20, 5), (30, 5), (40, 0), (30, -5), (20, -5), (10, -5)]
    mar_open = MARCalculator.calculate_mar(mouth_open)
    print(f"\nMiệng hơi mở:")
    print(f"  - MAR: {mar_open:.3f}")
    print(f"  - Trạng thái: {MARCalculator.get_mouth_state(mar_open)}")
    
    # Miệng mở to (ngáp)
    mouth_yawn = [(0, 0), (10, 15), (20, 15), (30, 15), (40, 0), (30, -15), (20, -15), (10, -15)]
    mar_yawn = MARCalculator.calculate_mar(mouth_yawn)
    print(f"\nMiệng mở to (ngáp):")
    print(f"  - MAR: {mar_yawn:.3f}")
    print(f"  - Trạng thái: {MARCalculator.get_mouth_state(mar_yawn)}")


def main():
    """Chạy tất cả các test"""
    print("\n" + "="*60)
    print("DrowsyGuard v2.1 - Test Suite")
    print("Kiểm tra các tính năng phát hiện buồn ngủ")
    print("="*60)
    
    try:
        test_ear_calculator()
        test_mar_calculator()
        test_yawn_detection()
        test_eye_closure()
        test_score_accumulation()
        
        print("\n" + "="*60)
        print("✅ TẤT CẢ TEST ĐÃ HOÀN THÀNH")
        print("="*60)
        print("\nKết luận:")
        print("- Ngưỡng phát hiện ngáp: 2 lần (giảm từ 3)")
        print("- EAR < 0.25: Mắt nhắm")
        print("- MAR > 0.6: Đang ngáp")
        print("- Cảnh báo nghiêm trọng → Popup xác nhận")
        print("\nChạy ứng dụng chính: python main.py")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Lỗi khi chạy test: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
