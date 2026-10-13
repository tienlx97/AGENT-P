# Kết quả chỉnh sửa Agent Office — 2026-10-13

## Đã triển khai

- Gom app, scripts, policies, docs, runtime state, evidence và toolchain vào
  `agent-office/`. Chuyển kế hoạch cũ vào archive. Giữ symlink tương thích, backup
  profile trước migration. FE-P và BE-P vẫn là hai repo riêng.
- UI đội ngũ có danh sách sáu vai trò và một form đang chọn; áp dụng cấu hình cho
  cả đội, trạng thái chưa lưu, footer cố định, bàn phím/Escape và bố cục cửa sổ nhỏ.
- Gear Settings dùng cùng màn hình cấu hình office. Bỏ Add agent/Restore không áp
  dụng ở profile này; workspace paths và diagnostics nằm trong cấu hình đội ngũ.
- Task thường vẫn chỉ chọn FE/BE và nhập yêu cầu. Continue dùng danh sách run;
  exact edit chỉ xuất hiện cho FE; thêm chế độ chỉ đọc được sandbox cưỡng chế.
- Lịch sử có token mới/cache/output, mở thư mục diff/evidence, chạy gate và chấp nhận
  kết quả đã review. CLI thành công không đủ để đánh dấu code task done. Kiểm chứng
  stale, failed và interrupted không được chấp nhận. Read-only cần input không đổi.
- Tái sử dụng runner/evidence/workflow của FE-P có ghi revision nguồn; gate office
  chạy typecheck, lifecycle/fingerprint/context tests, worker/isolation tests và build.
  Gate còn fingerprint các script ngoài app. Gate FE/BE chạy trong sandbox không
  mang provider credentials, không dùng model.
- Context chứa task và đường dẫn tài liệu liên quan, không lặp toàn bộ roster/hồ sơ.
  Manifest được lưu trong từng run. Continue cộng token toàn bộ chuỗi; dữ liệu usage
  không rõ bị từ chối thay vì giả định bằng 0. Usage nhiều turn được cộng dồn.
- Bổ sung AGENTS.md ngắn tại LOG và agent-office để hướng các lần làm việc sau tới
  đúng nguồn, tránh đọc toàn bộ cache/toolchain/history.

## Bằng chứng kiểm tra

- Bộ Node test tổng: 974 pass, 1 skipped, 0 fail (975 tests).
- Gate office: typecheck + regression + sandbox/process tests + build thành công;
  xem `app/harness/runs/` cho báo cáo cuối cùng.
- Electron UI test với profile tạm: lưu cấu hình theo vai trò, FE/BE dùng mặc định,
  Settings thống nhất, diagnostics, Escape, không tràn ngang; zero provider sessions.
- Native Electron/PTy fixtures: dispatch FE/BE, runtime/model/effort, các vai trò,
  quota, giữ diff khi dừng, continuation, restart và tách workspace đều đạt.
- Kiểm kê migration: 13 checkout/worktree FE và 7 BE vẫn truy cập được; giữ nguyên
  16 run records. Xem `.local/evidence/layout-check.json`.
- Ảnh UI mới: `.local/evidence/office-team-desktop.png` và `office-team-small.png`.

## Giới hạn được giữ rõ

Không tuyên bố phần trăm tiết kiệm token hoặc chi phí: chưa benchmark lại bằng
provider thật. Kiểm thử lần này dùng local fixtures để không phát sinh model calls.
Tổng token lịch sử có nhiều cache, không chuyển thành số tiền ước đoán.

Nguồn UI upstream (blog, landing, prototypes, voice implementation) vẫn còn trong
repo; chỉ các entry point không áp dụng bị ẩn. Chưa có bằng chứng đủ để xóa hẳn
chúng mà không ảnh hưởng chế độ upstream. Cache/toolchain và worktree cũng được
bảo toàn, không xóa theo tuổi dữ liệu.

Trần token/step/time vẫn được khai báo bằng code policy và hiển thị read-only.
Chấp nhận kết quả cần người dùng xem yêu cầu cụ thể, diff và browser/HTTP evidence;
gate chung không tự chứng minh mọi yêu cầu sản phẩm. Historical done records không
được gán lại chứng nhận kiểm thử mới.
