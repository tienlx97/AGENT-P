# How to install AGENT-P

Hướng dẫn cài mới từ GitHub. Chạy các lệnh trong terminal Linux, bằng tài khoản
người dùng thông thường. Máy đã cài và đang dùng được chỉ cần phần **Cập nhật**;
không khởi tạo lại profile.

## 1. Yêu cầu môi trường

| Thành phần | Yêu cầu của bộ setup này |
|---|---|
| Hệ điều hành | Linux có desktop hoặc WSL2 có WSLg. Worker hiện từ chối Windows/macOS native. |
| GUI | Electron cần X11/Wayland hoạt động; SSH headless đơn thuần chưa đủ. |
| Node/npm | Baseline đã kiểm tra: Node 24.16.0, npm 11.13.0. Dùng Node 24; phiên bản khác chưa được xác nhận ở đây. |
| Build native | Python 3, make và compiler C/C++; npm postinstall rebuild node-pty/better-sqlite3 cho Electron. |
| Isolation | bubblewrap tại `/usr/bin/bwrap`, kernel cho phép user namespace. |
| Git | Hai repo FE/BE độc lập, mỗi repo có ít nhất một commit. |
| Runtime AI | Ít nhất Codex hoặc Claude Code đã cài và đăng nhập trong chính Linux/WSL đang chạy office. |
| Product tools | pnpm/Node của FE và .NET SDK theo `BE-P/global.json`; làm theo README/AGENTS của từng repo. |

Với Ubuntu, cài công cụ build và sandbox:

```bash
sudo apt update
sudo apt install git curl build-essential python3 pkg-config bubblewrap
```

Cài Node 24 bằng công cụ quản lý Node bạn đang dùng, sau đó kiểm tra:

```bash
node --version
npm --version
python3 --version
git --version
bwrap --version
```

Kiểm tra user namespace mà không chạy model:

```bash
bwrap --ro-bind / / --unshare-user -- /bin/true
```

Nếu lệnh này lỗi `Operation not permitted`, cần sửa policy user namespace của
máy/WSL trước. Không bỏ sandbox để vượt qua lỗi. Electron còn cần các thư viện
GUI của distro; xem phần xử lý lỗi nếu máy tối giản thiếu thư viện.

## 2. Clone repo và submodule

Ví dụ cấu trúc thư mục:

```text
~/projects/LOG/
  agent-office/       # AGENT-P
    app/              # submodule munder-difflin
  FE-P/               # repo sản phẩm frontend
  BE-P/               # repo sản phẩm backend
```

```bash
mkdir -p ~/projects/LOG
cd ~/projects/LOG
git clone --recurse-submodules https://github.com/tienlx97/AGENT-P.git agent-office
cd agent-office
git submodule status
```

Nếu đã clone mà quên submodule:

```bash
git submodule update --init --recursive
```

`app` được ghim vào commit đã chọn. Detached HEAD trong submodule sau khi clone
là bình thường. Không dùng `git submodule update --remote` cho cài đặt thông thường.

FE/BE có thể đã nằm ở đường dẫn khác. Nếu chưa có, clone từ thư mục `LOG`:

```bash
cd ~/projects/LOG
git clone https://github.com/tienlx97/FE-P.git FE-P
git clone https://github.com/tienlx97/BE-P.git BE-P
cd agent-office
```

Repo private cần đăng nhập GitHub bằng tài khoản có quyền truy cập. Cài dependencies
của FE/BE theo hướng dẫn riêng; AGENT-P không cài chúng thay bạn. Nếu có thay đổi
tracked chưa commit trong repo gốc, giữ lại/commit đúng công việc đó trước khi
chạy task: dispatcher sẽ từ chối tạo worker từ checkout có tracked edits.

## 3. Cài và đăng nhập CLI

### Codex

Dùng standalone installer theo [OpenAI Docs — Codex CLI](https://learn.chatgpt.com/docs/codex/cli):

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
codex --version
codex -c 'cli_auth_credentials_store="file"' login
codex -c 'cli_auth_credentials_store="file"' login status
test -f "$HOME/.codex/auth.json"
```

Thêm `$HOME/.local/bin` vào PATH trong cấu hình shell nếu chưa có. Đăng nhập bằng
phương thức tài khoản của bạn hỗ trợ. Cấu hình lưu bằng file ở trên cần thiết cho
worker hiện tại: nó đọc `~/.codex/auth.json`, không đọc OS keychain hay `CODEX_HOME`
tùy chỉnh. Đây là yêu cầu của wrapper AGENT-P, không phải hạn chế chung của Codex.
Xem [OpenAI Docs — authentication](https://learn.chatgpt.com/docs/auth).
Không đưa file đăng nhập vào Git hoặc `.local/` dùng để chia sẻ.

Worker tìm executable ở `~/.local/bin/codex` và resolve symlink tới binary.
Ưu tiên standalone; không mặc định rằng npm launcher/wrapper sẽ hoạt động trong
sandbox. Kiểm tra đường dẫn:

```bash
readlink -f "$HOME/.local/bin/codex"
file -L "$HOME/.local/bin/codex"
```

Máy phát triển đã kiểm tra Codex CLI 0.162.1. Installer có thể cài phiên bản mới hơn;
việc `--version` thành công chưa chứng minh mọi flag của wrapper vẫn tương thích.

### Claude Code — tùy chọn

Cài bản native theo hướng dẫn cài đặt chính thức của Claude Code rồi đăng nhập
bằng CLI. Wrapper hiện yêu cầu:

```text
~/.local/bin/claude
~/.claude/.credentials.json
```

Kiểm tra bằng `claude --version`, `claude auth status` và
`test -f "$HOME/.claude/.credentials.json"`. Nếu dùng credential store khác hoặc
chỉ cấu hình API key trong môi trường, wrapper hiện chưa tự hỗ trợ đường đó.
Có thể cấu hình toàn bộ vai trò dùng Codex trước; không cần cài cả hai runtime.

Các CLI và authentication phải nằm trong Linux/WSL, không chỉ trong Windows host.
Worker không kế thừa toàn bộ environment/config/MCP của CLI ngoài sandbox.

## 4. Cài dependencies và build ứng dụng

Từ thư mục `agent-office`:

```bash
cd app
npm ci
npm run typecheck
npm run build
cd ..
```

`npm ci` chạy postinstall để rebuild native modules. Không dùng `sudo npm ci`.
Kiểm tra build đã tạo launcher và bundle:

```bash
test -x app/node_modules/electron/dist/electron
test -f app/out/main/index.js
```

## 5. Tạo profile local lần đầu

Bước này bật chế độ coding office và khai báo hai repo. **Đóng ứng dụng trước khi
chạy.** Từ thư mục `agent-office`, đặt đường dẫn thực tế:

```bash
export OFFICE_FE_REPO="$(realpath ../FE-P)"
export OFFICE_BE_REPO="$(realpath ../BE-P)"
```

Nếu FE/BE ở nơi khác, thay bằng absolute path tương ứng. Chạy đoạn sau một lần;
đoạn mã sẽ từ chối ghi đè profile đã có:

```bash
python3 - <<'PY'
import json, os, pathlib, subprocess

root = pathlib.Path.cwd().resolve()
worker = root / 'scripts/office-worker.py'
if not (root / 'app/package.json').is_file() or not worker.is_file():
    raise SystemExit('Run this command from the agent-office repository root')
repos = {name: pathlib.Path(os.environ[f'OFFICE_{name}_REPO']).expanduser().resolve()
         for name in ('FE', 'BE')}
for name, repo in repos.items():
    top = subprocess.check_output(
        ['git', '-C', str(repo), 'rev-parse', '--show-toplevel'], text=True).strip()
    if pathlib.Path(top).resolve() != repo:
        raise SystemExit(f'{name} must point to the Git repository root')
    subprocess.run(['git', '-C', str(repo), 'rev-parse', '--verify', 'HEAD'],
                   check=True, stdout=subprocess.DEVNULL)
if repos['FE'] == repos['BE']:
    raise SystemExit('FE and BE must be different repositories')
profile = root / '.local/state/config/Electron/config.json'
if profile.exists():
    raise SystemExit('Profile already exists. Use Agent settings; no file changed.')
home = root / '.local/state/home'
home.mkdir(parents=True, exist_ok=True)
profile.parent.mkdir(parents=True, exist_ok=True)
config = {
    'onboardingComplete': True,
    'harnessHome': str(home),
    'recentHives': [str(home)],
    'registeredRepos': [str(repo) for repo in repos.values()],
    'codingOffice': {**{name: str(repo) for name, repo in repos.items()},
                     'worker': str(worker)},
    'managerAutostart': False,
    'autoMode': False,
    'orchestratorMaySpawn': False,
    'semanticMemory': False,
    'reflectEnabled': False,
    'missions': [],
    'opsStandupSeeded': True,
    'heartbeatSeeded': True,
    'compactMaintenanceSeeded': True,
    'autoUpdate': False,
    'telemetryEnabled': False,
}
with profile.open('x') as stream:
    json.dump(config, stream, indent=2)
    stream.write('\n')
profile.chmod(0o600)
print('Created:', profile)
print('Workspace:', home)
PY
```

Không cần tạo `office-preferences.json` bằng tay. Màn hình Agent settings sẽ lưu
sáu vai trò khi bạn cấu hình lần đầu. Profile và lịch sử ở `.local/` được Git ignore.
Không chạy `migrate-layout.py` trên bản clone mới; script đó chỉ dành cho layout
LOG cũ có `munder-difflin/`, `office-state/` và các thư mục tương ứng.

## 6. Mở office và cấu hình đội ngũ

Vẫn từ thư mục `agent-office`:

```bash
./scripts/launch-office.sh
```

1. Nếu có workspace picker, mở đúng thư mục `.local/state/home` vừa tạo.
2. Mở **Agent settings**. Chọn vai trò, runtime, model và effort theo tài khoản.
3. Dùng **Apply this configuration to all roles** nếu muốn cùng cấu hình cho cả đội.
4. Bấm **Save team configuration**.
5. Trong **Workspace configuration & diagnostics**, kiểm tra đường dẫn FE/BE và
   bấm **Check runtimes**. Nút này không gọi model, cũng không xác nhận quota/login.
6. Mở **Coding task**, chọn FE hoặc BE, nhập yêu cầu và bấm **Start worker**.

Task kiểm tra đầu tiên: bật **Advanced options → Read-only analysis**, nhập
`Đọc README và tóm tắt cách chạy dự án. Không sửa file.` Đây là một lần gọi model
thật và có usage; chỉ mở UI/cấu hình đội ngũ không khởi chạy cả đội.

Với task sửa mã: **Task board → Open diff & evidence folder → Run repository checks**,
sau đó review yêu cầu cụ thể và **Accept reviewed result**. Gate dùng
`harness/verify.sh` của repo FE/BE; repo thiếu gate hoặc thiếu service/dependencies
sẽ không được coi là đã kiểm chứng. Read-only task có thể hoàn tất khi input không đổi.

## 7. Kiểm tra cài đặt và giới hạn test

Các kiểm tra không gọi provider, từ `agent-office`:

```bash
cd app
npm run typecheck
npm run test:focused
cd ..
python3 scripts/test-office-verification.py
```

Kiểm thử UI tùy chọn (cần GUI và profile ở bước 5):

```bash
cd app
npm install --no-save --package-lock=false playwright@1.64.0
node tools/office-ui-review.cjs
cd ..
```

Test UI dùng profile tạm và không chạy model. Playwright chỉ phục vụ kiểm thử,
không bắt buộc để mở ứng dụng bình thường. `npm ci` có thể gỡ dependency cài tạm này.

**Lưu ý về full harness:** `./harness/verify.sh` hiện còn gọi hai suite worker cũ
phụ thuộc layout LOG ban đầu, symlink `LOG/scripts` và worktree `LOG/worktrees/fe-smoke`
(và `be-smoke`). Chúng chưa độc lập trên một clone mới. Không coi thiếu những fixture
này là lỗi cài ứng dụng, và không tuyên bố full harness đã pass trên máy mới khi
chưa thiết lập fixtures. Các lệnh độc lập phía trên là bước kiểm tra cài đặt.

## 8. Cập nhật

Dừng worker và đóng office; kiểm tra `git status` trong repo chính và `app` trước.
Giữ lại các thay đổi đang làm, không reset/clean để cập nhật:

```bash
git status --short
git -C app status --short
git pull --ff-only
git submodule sync --recursive
git submodule update --init --recursive
cd app
npm ci
npm run build
cd ..
./scripts/launch-office.sh
```

Chạy từ `agent-office`. Lệnh cập nhật ghim submodule theo AGENT-P, không tự lấy HEAD
mới nhất của upstream. `.local/` được giữ lại. Không di chuyển cả thư mục đang dùng
mà chỉ sửa một đường dẫn: profile, run history và Git worktree có absolute paths.

## 9. Lỗi thường gặp

| Triệu chứng | Kiểm tra / xử lý |
|---|---|
| `app` trống hoặc thiếu package.json | `git submodule update --init --recursive`. |
| Không có Coding task / Agent settings | Profile ở bước 5 chưa tồn tại hoặc đang chạy trực tiếp Electron bằng profile khác; dùng launcher. |
| `electron: No such file`, thiếu `out/main/index.js` | Chạy `npm ci`, `npm run build` trong `app`. |
| Lỗi node-gyp, make, g++, node-pty hoặc ABI | Cài toolchain; sau khi đổi Node chạy `npm ci` để rebuild native modules cho Electron. |
| `error while loading shared libraries` | Chạy `ldd app/node_modules/electron/dist/electron` từ repo root, cài package GUI của distro cung cấp thư viện đang thiếu. |
| Không mở cửa sổ | Kiểm tra `DISPLAY`/`WAYLAND_DISPLAY`, WSLg hoặc phiên desktop. Không chạy app bằng sudo. |
| `bwrap ... Operation not permitted` | Kiểm tra user namespace / policy của distro; worker yêu cầu sandbox hoạt động. |
| `authentication unavailable` | Kiểm tra file auth và binary trong Linux như bước 3; không in nội dung auth ra log. |
| CLI chạy ngoài terminal nhưng lỗi trong worker | Worker dùng native executable tại `~/.local/bin`, profile tạm và environment hạn chế; npm wrappers, custom CODEX_HOME, MCP/global config không tự được kế thừa. |
| BE không tìm thấy dotnet | Wrapper mount `~/.dotnet` và `~/.nuget/packages`; cài SDK khớp global.json tại đường dẫn được wrapper hỗ trợ. |
| FE thiếu pnpm/dependencies | Cài theo FE README; worker PATH gồm thư mục bin của Node. Đảm bảo pnpm/shim chạy được từ đó, không chỉ qua alias shell. |
| Tracked edits exist | Repo gốc có thay đổi chưa commit; bảo toàn/commit đúng công việc trước khi dispatch. |
| Gate bị blocked | Mở verification.log; kiểm tra service, SDK và dependencies của repo. Không đổi status thành done để bỏ qua lỗi. |
| Model/effort bị provider từ chối | Chọn model/effort tài khoản hỗ trợ hoặc CLI default; wrapper không tự thay model. |

## 10. Dữ liệu nào cần giữ

- Git lưu source, scripts và docs; `app` là submodule.
- `.local/state/home/office-preferences.json`: cấu hình đội ngũ.
- `.local/state/home/office-runs/`: log, diff và metadata từng lượt chạy.
- `.local/state/home/worktrees/`: mã đang làm trong các worktree.
- `.local/state/config/Electron/config.json`: profile máy hiện tại.

Backup local state khi cần; không đưa nó vào commit. Khôi phục trên máy khác cần
đối chiếu absolute paths và Git worktrees. Repo clone mới không mang lịch sử chạy
hoặc thông tin đăng nhập từ máy cũ.
