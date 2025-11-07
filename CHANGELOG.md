# Cập nhật DrowsyGuard v2.1 - Cảnh báo Nghiêm Ngặt Hơn

## 🔄 Thay đổi mới (07/11/2025)

### 1. Giảm ngưỡng phát hiện buồn ngủ

- **Trước**: Cảnh báo nghiêm trọng khi ngáp ≥ 3 lần
- **Sau**: Cảnh báo nghiêm trọng khi ngáp ≥ 2 lần ⚠️

### 2. Popup xác nhận bắt buộc

Khi phát hiện buồn ngủ nghiêm trọng:

- ✋ Ứng dụng **TẠM DỪNG** giám sát tự động
- 🔊 Phát âm thanh cảnh báo liên tục (loop)
- 📱 Hiển thị popup cảnh báo toàn màn hình
- ✅ Người dùng **BẮT BUỘC** phải bấm "XÁC NHẬN" để tiếp tục
- 🔄 Reset tất cả các chỉ số sau khi xác nhận

### 3. Điều kiện cảnh báo nghiêm trọng (DANGER)

Ứng dụng sẽ hiển thị popup khi:

1. **Mắt nhắm quá lâu**: ≥ 20 frame liên tục (~0.67 giây)
2. **Ngáp nhiều lần**: ≥ 2 lần ⚠️ (giảm từ 3 lần)
3. **Điểm buồn ngủ cao**: ≥ 100 điểm

## 🎯 Cách hoạt động

### Quy trình phát hiện buồn ngủ:

```
1. Camera phát hiện khuôn mặt
   ↓
2. Tính EAR (mắt) và MAR (miệng)
   ↓
3. Đếm số lần ngáp và frame mắt nhắm
   ↓
4. Tích lũy điểm buồn ngủ
   ↓
5. Nếu ≥ 2 lần ngáp HOẶC điều kiện khác
   ↓
6. 🚨 HIỂN THỊ POPUP CẢNH BÁO
   ↓
7. ⏸️ TẠM DỪNG giám sát
   ↓
8. Đợi người dùng bấm XÁC NHẬN
   ↓
9. 🔄 Reset điểm, tiếp tục giám sát
```

### Màn hình popup cảnh báo:

```
┌─────────────────────────────────┐
│            ⚠️                    │
│    CẢNH BÁO BUỒN NGỦ!          │
│                                 │
│  Đã ngáp 2 lần - Buồn ngủ!     │
│                                 │
│    Vui lòng nghỉ ngơi!         │
│ Bấm XÁC NHẬN để tiếp tục.      │
│                                 │
│  [XÁC NHẬN - Tôi đã tỉnh táo]  │
└─────────────────────────────────┘
```

## 📊 Thống kê điểm buồn ngủ

### Cách tính điểm:

- Mỗi frame mắt nhắm: **+2 điểm**
- Mỗi frame mắt mở: **-1 điểm** (giảm dần)
- Mỗi lần ngáp: **+10 điểm**

### Mức cảnh báo:

- 🟢 **0-49 điểm**: SAFE (Tỉnh táo)
- 🟡 **50-99 điểm**: WARNING (Có dấu hiệu mệt)
- 🔴 **≥100 điểm**: DANGER (Popup cảnh báo)

## 🔧 File đã thay đổi

### 1. `drowsiness_detector.py`

```python
# Thêm ngưỡng số lần ngáp
YAWN_COUNT_THRESHOLD = 3  # tang so lan ngap len 3

# Cập nhật logic cảnh báo
# Ưu tiên: Mắt nhắm → Ngáp → Điểm tổng
```

### 2. `gui.py`

```python
# Thêm biến trạng thái
self.is_paused = False
self.alert_popup = None

# Thêm các phương thức mới
def _show_drowsiness_alert(self, status)
def _on_confirm_alert(self, instance)

# Cập nhật update() để kiểm tra popup
# Cập nhật stop_monitoring() để cleanup popup
```

## 🚀 Chạy ứng dụng đã cập nhật

```bash
# Không cần cài đặt thêm thư viện
python main.py
```

## 📝 Lưu ý quan trọng

### ⚠️ An toàn:

- Popup **KHÔNG THỂ BỎ QUA** (auto_dismiss=False)
- Âm thanh cảnh báo phát **LIÊN TỤC** cho đến khi xác nhận
- Giám sát **TẠM DỪNG** hoàn toàn khi có cảnh báo
- **BẮT BUỘC** phải bấm xác nhận để tiếp tục

### 💡 Khuyến nghị:

- Khi nhận cảnh báo, **HÃY NGHỈ NGƠI**
- Đừng chỉ bấm xác nhận rồi tiếp tục lái xe
- Nên dừng xe an toàn, uống nước, nghỉ ngơi 10-15 phút
- Nếu cảnh báo lặp lại nhiều lần, **DỪNG LÁI XE**

### 🎵 Âm thanh:

- Đặt file `alarm.wav` hoặc `alarm.mp3` vào thư mục gốc
- Âm thanh sẽ lặp lại liên tục khi có popup
- Tự động dừng khi xác nhận hoặc dừng giám sát

## 🧪 Test các tình huống

### Test 1: Ngáp 2 lần

1. Bắt đầu giám sát
2. Ngáp lần thứ nhất (mở miệng to ~0.5 giây)
3. Ngáp lần thứ hai
4. → **Popup hiển thị ngay lập tức**

### Test 2: Nhắm mắt lâu

1. Bắt đầu giám sát
2. Nhắm mắt liên tục trong ~0.67 giây
3. → **Popup hiển thị**

### Test 3: Tích lũy điểm

1. Bắt đầu giám sát
2. Nhắm mắt ngắn nhiều lần + ngáp 1 lần
3. Khi điểm đạt 100
4. → **Popup hiển thị**

## 📞 Debug

### Xem điểm buồn ngủ:

Trong ứng dụng, xem ở phần thông tin chi tiết:

```
EAR: 0.28 | MAR: 0.45 | Ngáp: 1 lần | Điểm: 45
```

### Nếu popup không hiện:

1. Kiểm tra `status['drowsy'] == True`
2. Kiểm tra `status['alert_active'] == True`
3. Kiểm tra `self.is_paused == False`

### Nếu không thể đóng popup:

- Chỉ có thể đóng bằng nút "XÁC NHẬN"
- HOẶC bấm nút "Dừng" để dừng hoàn toàn

## 🎉 Kết luận

Phiên bản này **NGHIÊM NGẶT HƠN** trong việc phát hiện buồn ngủ:

- ✅ Phát hiện sớm hơn (2 lần ngáp thay vì 3)
- ✅ Bắt buộc xác nhận (không thể bỏ qua)
- ✅ Tạm dừng giám sát (đảm bảo người dùng chú ý)
- ✅ Reset điểm sau xác nhận (bắt đầu lại từ đầu)

**→ MỤC TIÊU: Bảo vệ an toàn tính mạng người lái xe! 🚗💨**
