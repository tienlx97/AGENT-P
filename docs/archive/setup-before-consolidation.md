# Local setup

The FE/BE repositories remain unchanged. Munder source lives in sibling
`munder-difflin/`. Coordination docs and evidence live at this workspace root.
Do not initialize this root as a monorepo or deploy any of these changes.

Verified discovery commands: `uname -a`, `node --version`, `npm --version`,
`dotnet --version`, `git -C FE-P status --short`, equivalent BE commands,
`claude --version`, `codex --version`, `claude auth status`, `codex login status`.
Never paste credential files into evidence. Authentication summaries need only
provider and logged-in status, not personal identifiers.

Source build commands are package scripts: `npm ci`, `npm run build`,
`npm run typecheck`, `npm run test:focused`, `npm run dev`.
Native addons need make, a C++ compiler, Python and Electron headers. This WSL
machine lacks the compiler; see discovery and toolchain-download evidence.

One native floor supports FE/BE workers with separate cwd selections. Runtime
selection belongs to each session. Keep autoMode off, orchestratorMaySpawn off,
hourly standup off, background reflection off and heartbeat off until explicit coordinated work is started.

## Verified source-build office

```bash
cd /home/capybara/projects/work/LOG
./scripts/launch-office.sh
```

Click **open** in the hive picker, then **Coding task**. Pick FE or BE and choose
Codex or Claude Code for that attempt. Enter a scoped task; the launcher creates
a separate branch/worktree and shows the worker on the ORIGINAL animated floor.
The terminal is real native xterm/node-pty. Runtime/model/repository and observed
usage appear in the selected worker detail. Review the native task board and
`office-state/home/office-runs/<run-id>/run.json` for results. CLI defaults are
used; a missing model name or invoice cost displays `unknown`.

This is a **local source fork** on `office/adaptive-routing`, not an upstream
configuration feature. The added keys are implemented in the actual
main/preload/renderer types: `managerAutostart`, `codingOffice.FE/BE/worker`.
They are set in the isolated source-build profile:
`office-state/config/Electron/config.json`. Existing user profiles are untouched.
The native `harnessHome`, `registeredRepos`, `autoMode`, `missions`, seeding flags,
telemetry, update and semantic-memory fields were checked against config.ts.

Our external helper is `scripts/office-worker.py`; it is called from Munder's
PTY, not an additional server, manager, task database or office UI. It requires
Linux bubblewrap. Windows/macOS launch is deliberately refused until equivalent
OS isolation has been implemented/tested. Preserve the helper path when moving
this source checkout. Do not launch a packaged upstream build against this fork's
profile and expect the added policy keys to take effect.

The first local install failed without make/g++. Ubuntu compiler packages were
downloaded into `office-tools/debs` and extracted with `dpkg-deb -x` into
`office-tools/root`, using wrappers in `office-tools/bin`. Exact download output
is in evidence/toolchain-download.log. The cached updates linux-libc-dev URL was
404; the verified fallback was `apt-get download linux-libc-dev=7.0.0-14.14`.
No sudo/system package installation occurred.

Verified build commands with that toolchain:

```bash
cd /home/capybara/projects/work/LOG/munder-difflin
npm ci --ignore-scripts
PATH="/home/capybara/projects/work/LOG/office-tools/bin:$PATH" npm run postinstall
npm run typecheck
npm run build
npm run test:focused
```

Electron 32.3.3 was extracted from its verified npm download cache into
node_modules/electron/dist and its executable permissions restored. GUI smoke
tests use Playwright installed locally with `npm install --no-save --ignore-scripts
playwright`; package.json and package-lock.json remain unchanged. Test commands:
`node tools/office-smoke.cjs`, `node tools/office-portability.cjs`, and from this
workspace `python3 scripts/test-office-worker.py`.

Task worktrees remain under `office-state/home/worktrees/{FE,BE}/<run-id>`.
They are never automatically removed. Original repos and smoke worktrees under
`worktrees/` remain separate. Inspect `git -C <worktree> diff` for any edits; worker
Git metadata is read-only so host-side reviewed commits are a later workflow.

## Acceptance status

Phases 0, 1 and 3–5 are verified. Phase 2 remains pending: the final real Claude
FE/BE recheck again reported expired OAuth that could not be refreshed. The user
approved proceeding with Codex. Restore Claude login before repeating
`node tools/office-portability.cjs`; a logged-in status alone does not prove a
successful provider request. All six roles passed both-runtime lifecycle fixtures.
PAY-STAGES produced linked draft FE #9 and BE #6, with full local gates and real
paired HTTP/browser verification. Phase 6 is optional and was not requested.

CLI output for subsequent runs is retained with mode 0600 as `terminal.log` next
to `run.json`, even after the temporary runtime profile is deleted. The host owns
this log; it is not writable from inside the worker sandbox. Old smoke runs made
before durable CLI logging was added retain their summary/task notes and external
smoke evidence, but not a full per-run terminal log.

## Final office workflow

Configure the six roles once in **Agent settings**, then save the complete team. For routine work use **Coding task**, choose FE or BE and enter the task. Runtime/model/effort come from saved workspace settings. Specialist overrides live under Advanced options. Optional base branch allows reviewing a feature branch in a fresh isolated checkout. **Continue stopped run** uses a preserved same-repo worktree at a safe boundary and records a compact handoff; active runs and exhausted attempt chains are rejected. Use **Task board** to open the existing native kanban without starting Michael.

For this safety profile, native Add agent/GOD/voice process launches are denied. Michael automatic planning/spawning is disabled; known cross-repo features use an operator-approved parent/contract and separate bounded FE/BE tasks. The approved PAY-STAGES flow produced two linked draft PRs. This is a working bounded coding office, not a claim of fully unattended autonomous management.

Native role/avatar IDs remain stable across attempts; run/PTY IDs remain distinct and preserve original runtime history. Bounded terminals accept one task; stop using the employee close control, then hand off rather than typing a hot engine switch. Observed input/output/cache tokens are retained when provided; actual invoice cost/model may remain unknown.
