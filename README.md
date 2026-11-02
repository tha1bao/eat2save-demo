# Eat2Save – demo (EXE101, Nhóm 1)

Bản demo web cho 3 vai trò: khách hàng (`/khach-hang/`), cửa hàng (`/cua-hang/`) và quản trị (`/quan-tri/`).

| Thư mục | Nội dung |
| --- | --- |
| `site/` | Bản triển khai lên Vercel (HTML + `assets/d0..d9.bin`) |
| `src/` | Mã nguồn đọc được (CSS + JS) đã đóng gói vào `site/assets` |
| `original/` | Bản chụp nguyên trạng demo trước khi sửa (02/11/2026) |
| `tools/` | `pack.py` đóng gói `src/` → `site/assets`; `patch_mon_le.py` là bản vá thêm món lẻ |

Đóng gói lại sau khi sửa `src/`: `python3 tools/pack.py src site`

## Thay đổi 02/11/2026
- Thêm hình thức **Món lẻ**: cửa hàng tự đặt giá, giảm 20–40% so với giá niêm yết; khách lọc được theo "Món lẻ".
- Bậc hoa hồng 5% → 10% → 15% áp dụng cho **mọi cửa hàng mới** (khớp mô hình tài chính Phần 7).
- Dữ liệu mẫu thêm 2 món lẻ; khóa lưu trữ trình duyệt đổi sang `e2s.db.v5` để tải dữ liệu mới.
