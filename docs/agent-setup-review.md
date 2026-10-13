# Đánh giá cấu hình AI Agent — 2026-10-13

Phạm vi: fork Munder Difflin, launcher/worker, profile office và harness FE-P trong LOG. Đây là đề xuất, chưa di chuyển cấu hình hoặc sửa ứng dụng. Đã đọc mã, cấu hình chọn lọc, metadata của 16 run và ảnh kiểm thử `evidence/team-settings.png`; chưa chạy lại UI trực tiếp. Ảnh chứa model fixture, không phải bằng chứng model đang cấu hình thật.

## Kết luận

Giữ Munder làm giao diện và điều phối, FE/BE là hai repo riêng. Gom setup vào `agent-office/`. Dùng một màn hình cấu hình đội ngũ, một luồng nhập task FE/BE. Chuyển các ý tưởng tốt của harness FE-P sang harness kiểm tra ứng dụng office; vẫn chạy harness FE tại repo FE. Không sao chép nguyên bộ quy tắc Next.js/StyleX vào Electron.

## Phát hiện có bằng chứng

| Mức | Hiện trạng | Hệ quả / chỉnh sửa đề xuất |
|---|---|---|
| P0 | `codingOffice.ts:finish` đánh dấu done khi CLI exit 0 và báo done; không kiểm chứng báo cáo harness | Phân biệt worker-completed, verifying, review-needed, done. Chỉ hoàn tất task khi gate phù hợp có bằng chứng còn hiệu lực; task chỉ đọc dùng tiêu chí riêng. |
| P1 | `CodingTaskLauncher.tsx` cấu hình sáu fieldset runtime/model/effort trong panel cuộn 560px | Danh sách vai trò bên trái, chi tiết vai trò đang chọn bên phải; mặc định chung và override theo vai trò; footer lưu cố định. |
| P1 | `ready` yêu cầu đủ cả sáu vai trò dù task chỉ dùng FE/BE | Khởi tạo sáu vai trò bằng mặc định chung; chỉ chặn chạy nếu vai trò cần dùng thiếu cấu hình hợp lệ. |
| P1 | `AgentStrip.tsx:238` vẫn mở Add agent, trong khi profile office chặn native launch theo tài liệu setup | Ẩn hành động không áp dụng khi codingOffice bật; Settings, task launcher và backend cùng dùng một capability map. |
| P1 | Có Agent settings riêng và SettingsModal với Agents & Models, Autonomy & Budgets, Voice… | Một cửa cấu hình office; chỉ hiển thị chức năng có hiệu lực với worker hiện tại. Giữ chế độ upstream riêng nếu vẫn cần hỗ trợ. |
| P1 | `TASK_LIMITS` đặt XS/S/M/L là 150k/500k/1.5m/3m token mỗi lượt | Đây là trần bảo vệ, không phải tối ưu token. Đo fresh input, cached input, output, thời gian, số lần tiếp tục và tỷ lệ hoàn thành trước khi chỉnh trần. |
| P1 | Worker chỉ nhận task + chỉ dẫn ngắn, chưa gọi context builder FE-P | Chuẩn bị context theo task/repo; nạp quy tắc chung ngắn và tài liệu liên quan qua đường dẫn, không nhồi toàn bộ lịch sử. |
| P2 | Setup nằm ở scripts, policies, docs, office-tools, office-state; launcher/profile có phụ thuộc đường dẫn | Gom bộ setup, thêm kiểm tra đường dẫn và migration có backup. |
| P2 | `docs/setup.md` phần đầu nói chọn runtime mỗi task, phần cuối nói dùng cấu hình đã lưu | Sửa tài liệu theo luồng cuối cùng; chuyển lịch sử triển khai sang archive. |

Các phần đã tốt cần giữ: manager/autoMode/orchestratorMaySpawn đang tắt; một worker cho task thường; không retry tự động; worktree riêng; runtime/model/effort gắn với từng run. `reviewRequired` trong policy cần được nối tới bước review thực tế, không chỉ lưu metadata.

## Token: số liệu và giới hạn kết luận

- 16 run lưu tại thời điểm đọc: 7 done, 9 blocked. Bao gồm smoke/fixture và thao tác dừng; không dùng tỷ lệ này làm tỷ lệ thành công sản phẩm.
- FE `office-frontend-03466818`: 34.579 tổng, 28.544 cached input.
- BE `office-backend-802ca13c`: 31.530 tổng, 27.776 cached input.
- BE `office-backend-67a571a3`: 1.488.543 tổng, 1.413.760 cached input, bị chặn do vượt ngân sách quan sát được.
- Không suy ra số tiền từ tổng token; dữ liệu lịch sử ghi cost/model unknown. Không thể quy toàn bộ token thừa cho AGENTS.md hoặc prompt đội ngũ: launcher hiện đã tránh chèn toàn bộ roster và worker dùng profile tạm.

Đề xuất: giữ một worker mặc định; specialist chỉ theo nhu cầu. Context builder chạy bằng mã, xuất manifest tài liệu đã nạp và kích thước; trích đoạn có giới hạn. Tóm tắt lần chạy trước bằng diff, lỗi và check còn thiếu. Chạy kiểm thử xác định bằng runner, chỉ gửi tóm tắt lỗi liên quan cho model. Giới hạn cả chuỗi attempt để không nhân ngân sách qua Continue. UI hiển thị rõ trần token là trần quan sát, có thể vượt khi provider báo usage muộn. Chưa hứa tỷ lệ tiết kiệm trước khi benchmark các task tương đương.

## Cấu trúc thư mục đề xuất

```text
LOG/
  FE-P/
  BE-P/
  agent-office/
    README.md
    AGENTS.md                 # bản đồ ngắn dành cho phát triển office
    app/                      # repo munder-difflin hiện tại
    config/                   # cấu hình khai báo có schema/version
    scripts/                  # launcher, worker, migration, doctor
    policies/                 # routing, context, verification
    harness/                  # kiểm tra app office và evidence contract
    docs/                     # setup, vận hành, quyết định kiến trúc
    .local/                   # ignored: runtime state, logs, toolchain cache
```

Mục tiêu là một bộ setup dễ hiểu, không tạo thêm nguồn cấu hình cạnh tranh. Repo FE/BE được tham chiếu từ workspace root, resolve thành absolute path lúc chạy. Cấu hình khai báo và preferences trong ứng dụng cần một adapter/schema thống nhất; không duy trì hai bản có thể chỉnh độc lập. Runtime history vẫn do ứng dụng quản lý. Không đưa thông tin đăng nhập vào thư mục cấu hình versioned.

Di chuyển worktree phải dùng Git worktree move/repair theo từng repo, cập nhật đường dẫn trong profile và run metadata khi cần; không dùng mv hàng loạt. Dừng worker trước migration, backup state, giữ launcher cũ chuyển tiếp, kiểm tra khởi động lại và khả năng quay lại cấu hình cũ.

## Áp dụng harness FE-P

| Nguồn | Cách áp dụng |
|---|---|
| `AGENTS.md` | Sao chép cấu trúc map-of-truth, thay nội dung bằng Electron/React/main/preload/worker. Không mang ngoại lệ react-dev-docs-shell/Astryx sang office. |
| `harness/lib/runner.sh`, `lib/evidence.mjs` | Tái sử dụng có kiểm tra phụ thuộc: timeout, lock, log, trạng thái interrupted, fingerprint. |
| `task.mjs`, `lib/workflow.mjs` | Adapt context/status/handoff theo task ID của office. Bản FE hiện phụ thuộc OpenSpec; không ép người dùng viết OpenSpec cho một task đổi chữ. |
| `verify.sh` | Thay gate FE bằng typecheck, test liên quan worker/routing/preferences, build app và UI flows. FE task vẫn dùng harness FE trong worktree FE. |
| Golden rules | Viết lại cho ranh giới main/preload/renderer, config persistence, UX form và bằng chứng kiểm thử. |
| Checks logistics/Next.js/StyleX | Giữ tại FE-P, không copy vào office. |

Lưu nguồn và revision của phần tái sử dụng để có thể cập nhật. Chọn một nơi sở hữu phần harness dùng chung; tránh hai bản sao tự phát triển không đồng bộ.

## Hướng UI/UX

Giữ office pixel-art làm màn hình hoạt động. Các form cấu hình dùng typography, khoảng cách và control đồng nhất, dễ đọc; không dùng sáu form HTML dài đè lên bản đồ.

- Điều hướng chính: Công việc, Đội ngũ, Cấu hình. Tác vụ thường: chọn FE/BE → nhập yêu cầu → bắt đầu → xem tiến độ, diff và bằng chứng.
- Đội ngũ: sáu vai trò đã khởi tạo; chọn một vai trò để sửa runtime, model, effort và xem nguồn mặc định/override. Có nút kiểm tra runtime; báo rõ cấu hình đã lưu và thay đổi chưa lưu.
- Cấu hình: repo FE/BE, mặc định model/effort, ngân sách, harness. Tính năng không dùng trong codingOffice không xuất hiện.
- Tùy chọn nâng cao: chọn run để tiếp tục bằng danh sách dễ hiểu thay vì nhập ID; chỉ hiện Exact FE edit khi repo là FE; branch/parent task giữ trong phần nâng cao.
- Accessibility: focus khi mở, Escape để đóng, hoàn trả focus, thông báo lỗi sát trường nhập, điều hướng bàn phím và kiểm thử kích thước cửa sổ nhỏ.
- Lịch sử: nhóm run theo task; phân biệt CLI hoàn thành, kiểm thử đạt, cần review, dừng do budget. Hiển thị cached/fresh/output riêng khi có dữ liệu.

## Dọn phần thừa

Ẩn trước các entry point không áp dụng. Xóa implementation sau khi rà import, IPC, test và xác định còn hỗ trợ upstream mode hay không. Blog, landing-remotion, prototypes là ứng viên tách khỏi checkout vận hành, chưa đủ bằng chứng để gọi là dead code. Toolchain/debs là cache build có vai trò đã ghi nhận; chuyển ra khu runtime trước khi xem xét xóa. Worktree, patch, log phải được kiểm kê và đối chiếu task còn hoạt động; không tự xóa chỉ vì cũ.

## Thứ tự triển khai và nghiệm thu

1. Thống nhất nguồn cấu hình + gom thư mục bằng migration có dry-run; mở lại app giữ đúng repo, vai trò, model/effort, lịch sử và worktree.
2. Làm lại màn hình đội ngũ/task, ẩn chức năng không áp dụng; người dùng chạy FE/BE sau cấu hình ban đầu mà không chọn lại model.
3. Adapt harness và nối trạng thái kiểm thử; CLI exit 0 không đủ để đóng task sửa mã; evidence stale phải bị từ chối.
4. Thêm context/usage instrumentation; benchmark task chỉ đọc, đổi nhãn, sửa UI, lỗi BE và task FE-BE. So sánh chất lượng, token và thời gian trước/sau, phân biệt fixture với run thật.
5. Dọn tài liệu, cache và mã không dùng sau kiểm kê. Giữ khả năng rollback và các bằng chứng cần review.

Ưu tiên cải thiện cấu hình và kiểm chứng hoàn thành trước khi mở rộng tự động phối hợp nhiều agent. Yêu cầu người dùng chỉ nhập task FE/BE từ phiên trước vẫn là tiêu chí UX chính.
