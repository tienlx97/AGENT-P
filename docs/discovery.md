# Discovery — Phase 0

Inspected 2026-10-12, Ubuntu 26.04 on WSL2, x86_64. Node 24.16.0,
npm 11.13.0, .NET 8.0.424; 15 GiB RAM, 848 GiB free disk. X11 `:0`
and Wayland `wayland-0` are available. No existing Munder installation found
in the user configuration directory or a four-level home-directory search.

| Repository | Root | Remote | Current/default branch |
| --- | --- | --- | --- |
| FE | `/home/capybara/projects/work/LOG/FE-P` | `tienlx97/FE-P` | main/main |
| BE | `/home/capybara/projects/work/LOG/BE-P` | `tienlx97/BE-P` | main/main |

Both Git roots are independent. Baseline untracked files: FE memory notes
2026-10-11/12, BE memory note 2026-10-12. Do not modify or remove them.
FE uses Next.js, pnpm, Node tests, ESLint, TypeScript and an existing harness.
BE uses .NET 8 and Domain/Application/API/MySQL test projects. Both repository
AGENTS.md require their full harness gate before marking product tasks complete.
FE dev must use port 3001; port 3000 may serve production.

Claude Code 2.1.296 is authenticated via first-party subscription. Codex
0.162.1 is authenticated via ChatGPT. No paid model call has been made during
discovery. GitHub CLI is authenticated; its credentials have broad permissions,
so worker isolation must not inherit them. Repository protections remain to be
queried. Authentication availability does not prove provider quota availability.

## Verified source, rather than README assumptions

Source: https://github.com/HarnessMD/munder-difflin, commit
`241d1e593a28d30e7150fff2cc2de0e54c031a3b`. Package version **0.4.6**;
README advertises **0.5.3**. The selected source build is free; no Pro license
or Pro-only functionality is assumed. MIT covers source, LICENSE-ASSETS covers
LimeZu artwork and requires its attribution. Preserve both and existing assets.

* `src/main/index.ts` `pty:spawn` and `spawnAgentCore` accept an absolute cwd,
  provider, arguments, hive metadata and optional worktree isolation.
* Each worker can have its own cwd on ONE floor; FE and BE need no cross-floor
  coordination. This source's config describes process-global hive state across
  windows, unlike the README's independently rooted floors. Use one floor.
* `workerLaunch.ts` and `agentProvider.ts` support Claude and Codex per spawn.
  Switching requires a stopped session and a new launch; never rewrite run history.
* `hive.ts`, taskLedger.ts, preload and renderer supply registry, task board,
  terminal and durable roster. No public third-party router/plugin API was found.
  Internal IPC is an application boundary, not a published external API.
* `useHive.ts` boots Michael automatically and submits an orientation prompt.
  Native XS direct worker dispatch alone therefore does not ensure zero manager calls.
* `config.ts` seeds an ENABLED hourly ops standup. Disable it for this office;
  heartbeat and scheduled compaction are already opt-in. Animation is local PixiJS.
* Native worktree creation logs errors and FALLS BACK to the shared cwd. This
  violates fail-closed isolation; do not rely on it without hardening.
* Claude autoMode bypasses CLI permissions; Codex autoMode keeps workspace-write.
  cwd alone is NOT filesystem isolation. Both need equivalent bounded access.
* Breaker hardStop defaults false. Although config comments claim heartbeat is
  required, index.ts actually installs an always-on breaker beat. Source behavior
  takes precedence. Enable hardStop to enforce a native token stop; the bounded
  worker adds a separate wall-clock limit without manager heartbeat calls.
* Existing token/cost collection is provider dependent. Unobserved run usage and
  subscription-billed cost must remain `unknown`.

## Installation evidence

Initial `npm ci` failed: no `make`/C++ compiler. Passwordless sudo is unavailable.
A local, extracted Ubuntu build toolchain is being prepared in `office-tools/`;
no global system install or settings change is required. Phase 0 UI gate remains
open until the real Electron application launches and is inspected.

Phase 0 UI gate passed: real Electron onboarding rendered; screenshot
`evidence/phase0-ui.png`. Native addons rebuilt using the locally extracted
compiler. Branch protection: FE main unprotected (404); BE protection API reports
403, requiring a GitHub plan upgrade/public visibility. Do not assume protection.

## Phase 1 verified result

A narrow local-fork `office:start` IPC launches a selected CLI via the existing
native PTY and uses native hive task persistence and avatar spawn events.
The installed source had no public task-router extension seam; local keys and
hook are explicitly implemented, not presented as upstream configuration.
Worker process sandboxing uses `scripts/office-worker.py` / Linux bubblewrap.
Actual FE/BE Codex smoke runs completed in separate worktrees on one floor.
See phase1-native-smoke logs and screenshots. Five OS isolation checks passed.
Both product working checkouts remain at their initial baseline. Their gates are
not required for these read-only smoke checks; no product code was changed.

## Selected Phase 4 feature

User requested: **Logistics > Chi tiết hợp đồng > cập nhật MỐC ĐIỀU KHOẢN THANH
TOÁN: 1 đợt có thể chia thành nhiều lần thanh toán**. Preserve this requirement
for Phase 4: one payment stage can contain multiple payment transactions. Inspect
existing contract/payment models before defining a compatible FE/BE contract.
Do not substitute the earlier disposable fixture proposal; the user chose a real
product feature. Phase 4 implementation has not begun while the Phase 2 gate is open.

Phase 2 actual native attempts: both FE and BE Claude sessions were launched,
but reported **OAuth session expired and could not be refreshed**. Earlier
isolated CLI discovery reached the provider and reported the weekly quota limit.
Do not conflate this later authentication failure with a successful execution.
See `evidence/phase2-portability.log`; the initial assertion expected only quota
failure and failed correctly when a different provider error occurred.

A copied OAuth profile can rotate a refresh token; throwing away its updated
copy would lose that refresh. The helper now synchronizes CLI-written credential
updates only if the host profile still matches the original revision, atomically,
without logging secret contents. Managed attempts using one provider profile are
serialized to prevent refresh races. Existing exhausted/expired authentication
still requires restoring the Claude profile; no successful Claude gate is claimed.

Source inspection also found `reflectEnabled` defaults true and can invoke hidden Claude for memory summaries. It is explicitly disabled in this isolated profile, alongside standups/heartbeat, so quiet desks do not incur background summarization calls.

Final local safety profile rejects unbounded native/GOD/voice launches; all coding roles use the bounded Coding task entry point. This is an intentional source-fork restriction, not an upstream feature. Coordinated L work uses an operator-approved contract/parent task on the native board. Automatic Michael planning/spawning is disabled; no claim of fully unattended team management is made. Six bounded logical roles (FE, BE, Architect, QA, Reviewer, Integration) can select either CLI for each attempt, with a stable avatar identity and immutable per-run provider history. Reviewer checkouts are read-only.

Installed Codex feature inspection (`codex features list`) showed `multi_agent` is stable and enabled by default. Final worker argv explicitly disables `multi_agent` and `multi_agent_v2`; Claude tool allowlist omits its Agent tool. Earlier real task logs contained no collaboration tool events. This reinforces minimum-worker routing rather than trusting animation/roster size or prompts alone.
