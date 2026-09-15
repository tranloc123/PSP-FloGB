# SCBD Viewer Emulator V0.1

Đây là bootstrap project để build một APK Android riêng dựa trên PPSSPP, nhưng có package/app identity riêng và module SCBD riêng.

## V0.1 làm được gì?

- Clone PPSSPP upstream mới nhất.
- Build bản Android `NormalOptimized`.
- Đổi tên launcher thành `SCBD Viewer Emulator`.
- Đổi applicationId thành `com.scbd.vieweremulator`, vì vậy có thể cài song song với PPSSPP chính thức.
- Nhúng module `SCBD/SCBDViewer.h` vào native C++ build.
- Ghi sẵn game ID `ULUS10457` và các địa chỉ RAM SCBD đã xác nhận.
- Vẫn mở ISO/CSO/CHD như PPSSPP.
- KHÔNG chứa game/ISO.

## Build không cần PC

1. Tạo repository GitHub trống, ví dụ `SCBD-Viewer-Emulator`.
2. Upload toàn bộ nội dung của thư mục này lên repository.
3. Mở tab **Actions**.
4. Chọn **Build SCBD Viewer Emulator APK**.
5. Bấm **Run workflow**.
6. Chờ build xong.
7. Mở run thành công.
8. Trong **Artifacts**, tải `SCBD-Viewer-Emulator-V0.1-APK`.
9. Giải nén và cài `SCBD_Viewer_Emulator_V0_1.apk`.
10. Mở app, cấp quyền thư mục game như PPSSPP.
11. Chọn Soulcalibur: Broken Destiny và chạy.

## PASS V0.1 khi

- Cài được song song với PPSSPP chính thức.
- Tên app là `SCBD Viewer Emulator`.
- App mở bình thường.
- Chọn được ISO/CSO/CHD.
- Soulcalibur ULUS-10457 boot và vào game bình thường.

Sau khi PASS, V0.2 sẽ đọc P1 HP, P2 HP, MODE, STATE, COMBAT, VICTORY trực tiếp trong native emulator process.

## License

PPSSPP là GPL-2.0-or-later. Builder này không phân phối ISO/game. Khi build, GitHub Actions clone source PPSSPP upstream và áp dụng patch source có trong repository này.
