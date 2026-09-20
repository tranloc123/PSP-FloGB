# PSP Live FloGB V0.5.8C - Royal Unicode + Portrait Mapping Fix

## Mục tiêu bản này

V0.5.8C sửa đúng hai lỗi đã thấy trên bản test trước:

1. Dynamic text/số trông như font debug mặc định của PPSSPP.
2. Portrait trong BXH Top Nhân Vật bị đảo vì atlas auto-pick đã bị dùng nhầm cho atlas BXH.

Bản này quay về **clean build lane V0.5.7C4R1 đã build thành công**, sau đó mới áp patch V0.5.8C. Không build chồng lên APK V0.5.8B đã patch trực tiếp.

## Khóa portrait thành hai hệ độc lập

### A. Ranking / Top Nhân Vật

- Asset production: `branding/SCBD_character_portraits_ranking_v058c.png`
- Workflow cài vào: `assets/scbd/characters/character_portraits_atlas.png`
- SHA-256 khóa: `061c03df2fff58334fd28f9d061aa98741723ba8c6d3005b6dbb0a9ce3a5e871`
- Kích thước: `1260 x 480`
- Mapping theo tên/ID của BXH, giữ đúng thứ tự C4R1:
  `ALGOL, AMY, ASTAROTH, CASSANDRA, CERVANTES, DAMPIERRE, HILDE, IVY, KILIK, KRATOS, ... ZASALAMEL`.

### B. Winner Pick / Locked In

- Asset production: `branding/SCBD_pick_portraits_exact_v058c.png`
- Workflow cài vào: `assets/scbd/winner_asset_v058c/pick_portraits_exact.png`
- SHA-256 khóa: `c07ff0a7a1ab36c80e3f0107b6a0bb3c0d7be28461b3639877bd0c6b237daea2`
- Kích thước: `896 x 512`, grid `7 x 4`
- Đây là 28 portrait lấy trực tiếp từ Character Select gốc đã duyệt.
- Custom và Random bị loại khỏi `/pick 1-28`.
- Kratos auto-pick giữ ở **ID 14** trong hệ auto-pick.

Hai atlas này cố tình khác nhau. Workflow preflight sẽ dừng build nếu ranking atlas hoặc auto-pick atlas bị thay/nhầm.

## Hệ font V0.5.8C

### Royal Unicode atlas

- `branding/SCBD_royal_unicode_atlas_v058c.png`
- `1280 x 2016`, 16 cột, cell `80 x 96`
- 329 glyph
- Hỗ trợ ASCII, Latin Extended, tiếng Việt có dấu và các symbol phổ biến.
- Text production Winner / Pick / Locked / Ranking / Top5 sử dụng texture glyph renderer thay cho PPSSPP `DrawText()` mặc định ở các vị trí đã nâng cấp.
- Tên dài tự co theo `maxWidth`.
- Glyph không có sẽ fallback an toàn sang `◇` thay vì làm hỏng cả username.

### Timer digits

- `branding/SCBD_timer_digits_v058c.png`
- `1440 x 148`
- 12 cell: `0-9`, dấu `.`, `s`
- Timer dùng atlas riêng và pulse theo thời gian còn lại.

**Không có file font TTF/OTF trong package. Chỉ có PNG texture atlas đã render.**

## Những phần giữ nguyên

- Native Input Core đã test.
- Match Top5 logic.
- Winner phase/timing logic C4R1.
- TIME OUT chỉ là thông báo. APK không tự chọn nhân vật Random.
- C4R1 Victory/Pick/Locked/Timeout base artwork vẫn được giữ làm nền đã test.

## File cần upload vào root repo

Giải nén ZIP rồi upload giữ nguyên cây thư mục:

```text
.github/workflows/build-psp-live-flogb-v0.5.8c.yml
tools/apply_psp_live_flogb_v0_5_8c.py
branding/SCBD_character_portraits_ranking_v058c.png
branding/SCBD_pick_portraits_exact_v058c.png
branding/SCBD_royal_unicode_atlas_v058c.png
branding/SCBD_timer_digits_v058c.png
branding/SCBD_v058c_font_mapping.json
README_V0_5_8C.md
```

Push lên `main` sẽ kích hoạt workflow mới.

## APK đầu ra

```text
PSP_Live_FloGB_V0_5_8C_Royal_Unicode_Portrait_Fix.apk
```

GitHub artifact:

```text
PSP-Live-FloGB-V0.5.8C-Royal-Unicode-Portrait-Fix-APK
```

## Preflight bắt buộc

Workflow kiểm tra trước khi tốn thời gian Gradle:

- hash + kích thước ranking atlas
- hash + kích thước auto-pick atlas
- hai atlas không được giống nhau
- Unicode atlas `1280 x 2016`
- timer atlas `1440 x 148`
- Winner chỉ dùng auto-pick atlas
- Ranking chỉ dùng ranking atlas
- Locked In dùng auto-pick `characterId - 1`
- Kratos auto-pick ID 14
- Virtual Input + Match Top5 markers vẫn tồn tại

## Phạm vi chưa thay đổi

Avatar TikTok thật vẫn cần Bridge cung cấp texture/avatar data. Nếu Bridge chưa cung cấp ảnh, UI vẫn dùng placeholder/initial ở nơi tương ứng. V0.5.8C tập trung vào font/số và khóa đúng portrait mapping trước.
