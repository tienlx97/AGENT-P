# IMPLEMENTATION PLAN — Munder Difflin Autonomous Coding Office

> **For the implementation AI:** Treat this document as an actionable execution plan, not as permission to modify unrelated source code. Begin with Phase 0, inspect the installed/current upstream Munder Difflin code and both existing repositories, make minimal incremental changes, and attach evidence for every completed milestone.
>
> **Key cost principle:** Displaying seven animated employees must NOT mean invoking seven LLMs. A change such as “Đổi chữ trên button Login thành A” should use at most one appropriate coding agent (or a verified deterministic edit), targeted checks, and the existing human approval process.
>
> **Updated architecture decision (2026-10-12):** **Munder Difflin replaces Paperclip as the primary orchestration application and visual office.** Do not build a Paperclip connector, Paperclip integration API, or another office UI for the MVP. Reuse Munder Difflin's existing features first.

## 0. Objectives, constraints, and success definition

### Target

Set up an autonomous but human-governed full-stack coding team in **Munder Difflin** for an existing product whose **frontend (FE)** and **backend (BE)** live in **two independent folders and potentially two independent Git repositories**. Each role can use **Claude Code or OpenAI Codex**, and the chosen runtime can vary between tasks. Show actual agent activity in Munder Difflin's animated office floor with working terminals, task board, and cost/usage data when available.

### Must have

- Munder Difflin is the **single primary orchestration and office UI**. Its manager/orchestrator (“Michael” / GOD agent, as named by upstream) coordinates only when necessary.
- Preserve FE and BE as distinct repositories/folders, with different Git remotes/branches if applicable. **Never merge them into a monorepo without explicit direction.**
- Support both `claude` and `codex` CLIs and choose the runtime **per task / per agent session**, rather than hardcoding “FE = Claude, BE = Codex”.
- Support XS/S/M/L task complexity and a **rules-first, low-overhead routing policy**. XS changes do not awaken Michael, Architect, QA LLM, Reviewer LLM, and Integration LLM just to edit one label.
- Use Git worktree isolation for concurrent code-changing agents. Keep branch and PR operations tied to the correct repository.
- FE/BE contract changes are coordinated, tested against matching revisions, and usually delivered as **two linked PRs**.
- Track observed runtime, task, model/provider, status, measured token usage/cost where available. Unknown metrics must be labeled `unknown`, never fabricated.
- Prevent unauthorized production deployments, protected-branch merges, destructive migrations, production secret access, and unlimited retry loops.
- Keep Munder Difflin's existing pixel-art office floor. Treat **true 3D/isometric camera** as a separate optional phase, NOT a blocker for a working autonomous system.

### Not in MVP

- Paperclip setup, APIs, event bridge or dual orchestration.
- A brand-new Next.js + PixiJS office or an extra office backend (Munder Difflin already has Electron + React + PixiJS UI).
- Automatic mid-run Claude ↔ Codex hot swapping; switching requires safe run boundaries and a structured handoff.
- Unverified assumptions about paid/pro features, source-code APIs, UI hooks, model billing, engine availability, or existing user subscriptions.
- Auto-merge, auto-deploy production, or unrestricted shell execution on sensitive hosts.

### Definition of done

1. A real XS FE task modifies only the intended FE file(s), uses at most one LLM coding worker, runs targeted checks and produces a patch or FE PR.
2. A real full-stack feature creates separately tracked FE and BE tasks, runs in isolated worktrees, checks API compatibility and yields linked PRs for human review.
3. The office displays real sessions and live terminal/status; inactive characters must incur **no model calls solely for animation**.
4. A role can run with Claude Code on one task and Codex on another; the original runtime of each run remains visible/auditable.
5. Budget/retry/time guard stops a runaway task and escalates it to the user with evidence.

## 1. Upstream facts to verify before coding

Official project: https://github.com/HarnessMD/munder-difflin ; site: https://munderdiffl.in/

The upstream README (reviewed 2026-10-12) describes:

- Electron + React + TypeScript + PixiJS animated office, xterm.js terminal, `node-pty` CLI subprocesses.
- Supported Claude Code, Codex, and other terminal CLIs, with per-agent working directory and selected CLI/model.
- GOD/Michael orchestrator, mailbox/hive memory, Kanban task board, human approvals, circuit breaker, cost telemetry, CI watcher.
- Optional per-agent Git worktrees, and multiple floors (v0.5.3) with distinct folders, windows, agents, boards and memory.
- Pre-release status (README v0.5.3); free/open-source code under MIT, but bundled pixel-art assets use a **separate license/attribution requirement**. Some distributed UI/features are Pro.

**These are README claims; do not assume every item behaves as needed. Verify against the installed revision and the specific free/source build.**

Reference files to read as needed:
- `README.md`, `HIVE.md`, `SPEC.md`, `DESIGN.md`
- `docs/ARCHITECTURE.md`, `CHANGELOG.md`, `LICENSE`, `LICENSE-ASSETS`
- Relevant process spawning, worktree, orchestration, task, event and renderer modules discovered in source.

## 2. Phase 0 — Environment discovery and safety baseline (DO FIRST)

- [x] Identify OS (macOS/Windows/Linux), CPU, Node/npm versions, desktop GUI environment and available disk/memory.
- [x] Identify and inspect existing FE and BE absolute paths, `.git` status, remotes, default branches, scripts, test suites and runtime prerequisites.
- [x] Identify whether Munder Difflin is installed already, its exact version, free/Pro capabilities, whether building from source is needed, and whether an existing fork/worktree should be preserved.
- [x] Check `claude --version` and `codex --version`, authentication status and CLI provider restrictions **without exposing credentials**.
- [x] Read documentation/source for creating agents, assigning `cwd`, selecting/switching CLI, configuring worktrees, Kanban tasks, Michael/GOD routing, budgets and approvals.
- [x] Verify whether one office floor can host agents operating in two external folders. If yes, prefer **one floor with FE and BE agents assigned separate paths**, for shared task coordination. If not, test **two floors**, one FE and one BE, and explicitly document the limitation: the two floors may not share a task board or manager. Do not assume cross-floor coordination exists.
- [x] Determine whether engine/model changes are supported in-place, only on restart, or by creating a new session. Record observed behavior.
- [x] Check whether Munder Difflin has a public task/plugin/router extension point. **Do not invent configuration keys or modify core code blindly.**
- [x] Decide how GitHub credentials, PRs, branch protections and CI checks are configured. Avoid storing secrets in repo files.
- [x] Record findings and verified commands in `docs/discovery.md` and `docs/setup.md`.

**Gate:** No major implementation until actual folder paths, selected Munder revision, agent/CLI integration paths and edition limitations are confirmed.

## 3. Target architecture — reuse instead of rewrite

```text
USER / PRODUCT OWNER
         |
         v
MUNDER DIFFLIN DESKTOP APP (Electron)
  |-- Existing Animated Office Floor (PixiJS)
  |-- Live Agents / Terminals (xterm.js / node-pty)
  |-- Task Board / Memory / Approval / Telemetry
  |-- Michael / GOD orchestration for coordinated work
  |
  +-- Low-overhead Task Intake / Policy (native first, customize only if missing)
        |-- XS: deterministic edit if safe OR one FE/BE coding session
        |-- S: one relevant coding session + scoped checks
        |-- M: relevant coder(s) + conditional reviewer
        +-- L: Michael + planned agents with task dependencies
                   |
         +---------+---------+
         |                   |
    FE working directory  BE working directory
    FE repo / worktrees    BE repo / worktrees
         |                   |
         +----------+--------+
                    |
        Contracts / E2E / GitHub CI / Linked PRs
                    |
             HUMAN APPROVAL
```

### Architecture rules

- Munder Difflin is the **source of truth for current sessions and its own task board** (as supported by the installed revision); Git repositories are source of truth for code/diffs.
- Prefer **native configuration and workflow** before creating extensions. If only a fork/harness wrapper can meet a requirement, document the gap, smallest code change and tests first.
- The animated office is a **view**; animation must never drive or trigger model use.
- Keep a runtime-independent role ID and track the provider/CLI as an **attribute of each execution/session**, so changing engines does not rewrite history.
- Do not install Paperclip or maintain redundant Paperclip and Munder Difflin managers in the same team.

## 4. Two independent repositories / working directories

Illustrative layout, **not the user's actual paths**:

```text
/workspace/
  frontend/                     # Existing FE Git repository
  backend/                      # Existing BE Git repository
  agent-coordination/           # Optional small repo for shared contracts/runbooks
  worktrees/
    frontend/FE-101/
    backend/BE-102/
```

Configuration should refer to actual absolute paths discovered in Phase 0. Do **not** treat the following conceptual YAML as an importable upstream Munder configuration:

```yaml
# CONCEPTUAL mapping only; implement using verified Munder Difflin UI/config
roles:
  frontend:
    repo: /workspace/frontend
    allowed_runtimes: [claude, codex]
  backend:
    repo: /workspace/backend
    allowed_runtimes: [claude, codex]
  qa:
    scope: [frontend, backend]
    allowed_runtimes: [claude, codex]
worktrees:
  isolation: per-task
  root: /workspace/worktrees
```

**For one full-stack feature:** define a parent feature ID and FE/BE subtask IDs. Shared API contract can be an existing schema/OpenAPI artifact in BE or a separately versioned contract (only introduce a new repo if necessary). Test the right FE branch against the right BE branch. Create two PRs with cross-links. Plan backwards-compatible deploy order.

**Worktree discipline:** one task-specific branch and worktree per code-changing concurrent agent; never have two agents write to the same checkout simultaneously. Inspect clean repo state before creation and do not delete uncommitted work. Worktrees may be the app's native feature: verify the exact lifecycle and collision handling first.

## 5. Agent roster — roles are NOT models

| Role (logical identity) | Responsibility | Claude Code / Codex choice | Default trigger |
|---|---|---|---|
| Michael / Engineering Lead | Plan, coordinate dependencies, escalate | Configurable | L; ambiguous/high-risk M |
| Solution Architect | API contracts, schema/architecture | Configurable | Architecture-risk M/L |
| Frontend Engineer | FE components, UI logic, scoped FE checks | **Either** | FE XS/S/M/L |
| Backend Engineer | API, business logic, DB, scoped BE checks | **Either** | BE XS/S/M/L |
| QA Engineer | Integration and E2E testing | **Either** | Risk-based M/L |
| Code Reviewer | Independent correctness/security review | **Either** | Risk-based M/L |
| Integration Engineer | Cross-repo branch/contract integration, PR prep | **Either** | Cross-repo M/L |

Start with **Michael + FE + BE + Reviewer** (or FE + BE only for the very first smoke test); create the remaining roles after real task execution works. Displaying agent seats does not grant them active tasks.

### Runtime switching policy

- `manual`: user picks `claude` or `codex` before dispatching a task.
- `preferred`: choose a configured default for that specific task type, **not permanently per role**.
- `fallback`: if a CLI/provider is unavailable or quota-limited, stop/finish the current attempt safely, capture a short handoff and start a **new run/session** with the other engine. Never assume the product already automates this.
- Preserve completed diff/branch, remaining work, tests and errors on handoff. Never blindly rerun the full task and overwrite existing edits.
- Preserve original `provider`, `model`, session/run identifier, tool logs and metrics per run.

Compact handoff shape (our documentation convention, not a native API schema):

```json
{
  "featureId": "AUTH-01",
  "taskId": "FE-101",
  "from": "claude",
  "to": "codex",
  "repo": "frontend",
  "branch": "agent/FE-101",
  "changedFiles": ["src/components/LoginButton.tsx"],
  "completed": ["Button label updated"],
  "remaining": ["Run targeted tests and prepare PR"],
  "verification": "not yet executed"
}
```

## 6. Adaptive Task Routing — primary token cost control

**Most important implementation requirement.** Existing orchestration must not automatically wake the whole roster for tiny tasks.

| Tier | Example | Default execution | Review policy |
|---|---|---|---|
| XS | Rename a button, change copy/icon/color | 0-1 worker, scoped checks | No LLM reviewer by default |
| S | Local component/validation fix | One FE or BE worker | Risk-driven review |
| M | API logic, moderate multi-file change | Relevant coder(s), selective reviewer | Review when applicable |
| L | Full-stack feature, architecture, DB migration | Michael + necessary specialists | QA, review, integration |

### Router behavior

1. Identify repository target (`FE`, `BE`, `both`) using explicit path, task context and non-LLM rules first.
2. Estimate complexity (`XS/S/M/L`) and risk. Only use an inexpensive model if classification really is ambiguous **and** the user enabled model-based classification.
3. Dispatch directly to the minimum required session for XS/S **if native Munder workflow supports it**. Otherwise implement a minimal manual quick-action workflow or narrow dispatcher; do not force the expensive GOD-agent delegation path.
4. Treat auth, permission, payment, privacy, secrets, data deletion, destructive migrations and infra changes as higher risk regardless of lines changed.
5. For every task, define allowed repo/paths, checks, max retries, time/budget and output type (patch/PR). Use existing Munder per-agent autonomy/budget controls where available.
6. Do not wake idle agents merely to produce periodic status messages or drive sprite animations.

### XS example: change button text to `A`

```text
User: "Đổi chữ button Login thành A"
  -> rules identify: XS / FE / low risk
  -> optional zero-LLM edit if exact file + unique match verified
     else one FE coding agent (Claude OR Codex chosen for this task)
  -> edit in FE task worktree
  -> inspect diff; run relevant lint/typecheck/test
  -> FE PR or approved patch
  -> write evidence to Munder task/session
  -> idle agents remain idle
```

No automatic Architect, BE, QA LLM, Reviewer LLM, Integration LLM, or Michael model call for such XS changes.

### Optional deterministic edit

A zero-LLM edit is permitted only when the file and original/new values are unambiguous, target appears exactly once in the verified UI context, and no translation/generated-code ambiguity is present. Check diff and run scoped validation; refuse silent global search/replace. If the application does not offer a safe native deterministic action, implement as an explicit small tool with dry-run and path restrictions, not as a broad shell free-for-all.

### Initial guardrails — illustrative policy, not guaranteed CLI hard limits

| Tier | Suggested total tokens (input+output) | Max automatic retries | Stop condition |
|---|---:|---:|---|
| XS | 3,000–6,000 | 1 | Budget/time exceeded → stop |
| S | 8,000–15,000 | 2 | Budget/time exceeded → stop |
| M | 20,000–50,000 | 2 | Per-task cost/time cap |
| L | Approved feature budget | 3 | Human escalation |

Measure cached/input/output tokens and actual spend **only if provider/CLI or Munder telemetry exposes them**. Do not equate subscription usage quotas with API-billed dollar totals. If token hard caps are unavailable, enforce max run time, iteration/retry budget, permissions and the product's circuit-breaker capabilities. Report `unknown` for missing cost metrics.

## 7. Task workflows and approvals

### XS/S fast lane

```text
Request -> rules-first classification -> FE or BE single session
        -> edit isolated worktree -> targeted checks
        -> patch or PR -> human review -> optional merge
```

### M/L coordinated lane

```text
Request -> Michael / feature plan (only when warranted)
        -> contract/schema decision if necessary
        -> FE + BE isolated tasks in parallel after contract agreed
        -> scoped tests + matching-revision integration/E2E
        -> independent review; bounded fix loop
        -> linked FE PR and BE PR; CI status
        -> human approval -> merge/deploy outside agent authority
```

- Treat human approval of spend, scope and destructive commands in Munder as separate from **GitHub branch protection**, required CI, protected environments and merge permissions.
- Agents may push task branches/create PRs if scoped credentials permit. They may not merge protected branches or deploy production.
- Fix loop upper bounds: XS=1; S/M=2; L=3. Persist failure evidence and escalate instead of restarting indefinitely.
- Any orchestration extension must ensure failures and quotas do not trigger unbounded cross-agent ping-pong.

## 8. Office visualization — reuse built-in Munder floor

**Do not rebuild the animated office for MVP.** Use existing PixiJS office, session avatars, live terminal, task board, status, model and cost panel.

Requested interaction outcomes:
- Click employee → agent role/identity, current CLI/model, repository, task/session, live terminal, last activity and available metrics.
- FE employee works on FE repo; BE employee on BE repo. Their **runtime badge can change between tasks** without changing the role/avatar identity.
- Idle character animation is local UI behavior with zero LLM calls.
- Clearly mark completed, idle, blocked, crashed, waiting and disconnected states; no fabricated `typing` status.
- Visible cost/usage by task/agent and ideally FE vs BE if actual telemetry supports it. If not supported, add a lightweight report/export in a later phase.

### Optional true isometric enhancement (post-MVP only)

The existing Munder floor is **2D pixel-art**. A true isometric 2.5D redesign is not guaranteed to be supported by upstream. If essential after MVP:

1. Inspect existing PixiJS scene graph, collision/interaction, assets and component boundaries.
2. Produce an isolated prototype / optional theme rather than rewriting the orchestration/terminal code.
3. Preserve live state, user interactions, performance and accessibility.
4. Respect `LICENSE-ASSETS` and retain required LimeZu attribution; do not assume MIT applies to bundled artwork.
5. Prefer a feature flag `officeTheme=classic|isometric` **only if a supported extension/config mechanism exists**, otherwise treat as proposed custom fork code rather than a native setting.

## 9. Implementation approach — upstream app first, minimal custom code

**Recommended layout:**

```text
/workspace/
  frontend/                          # original FE repository
  backend/                           # original BE repository
  munder-difflin/                    # optional fork only if needed
  agent-coordination/               # optional: small local policies, scripts, notes
    plan.md
    docs/discovery.md
    docs/setup.md
    docs/security.md
    docs/test-report.md
    policies/task-routing.md
    policies/runtime-handoff.md
    scripts/                       # only verified safe scripts
  worktrees/
    frontend/<task-id>/
    backend/<task-id>/
```

**Build-vs-config decision:**
- First implement entirely through Munder settings, roles, CLI sessions, native worktree option, budgets, Kanban and approvals.
- If a feature is missing, find the **smallest hook/extension or safe outside wrapper**; prove it works with tests.
- Only fork/edit Munder core if there is no supported extension path. Record upstream commit/release, isolate changes, minimize upgrade conflicts.
- Do not ship guessed Munder config keys or nonexistent CLI/API commands as executable instructions.

### Install / launch references

Prefer official downloads at https://harnessmd.com/download (verify editions and trust), or follow upstream source instructions after validating the checked-out revision. Upstream README describes:

```bash
# Example for building the open-source project from source;
# verify URL, Node requirements and scripts against the checked-out revision.
git clone https://github.com/HarnessMD/munder-difflin.git
cd munder-difflin
npm install
npm run dev
```

The upstream README describes Node.js 18+, npm and a native build toolchain for `node-pty` when building from source. Prebuilt desktop downloads may not need those build prerequisites. In `docs/setup.md`, document actual platform-specific requirements and runtime authentication without exposing secrets.

## 10. Milestones / phases and acceptance gates

### Phase 0 — Discovery and working baseline
- [x] Inspect FE and BE repos, Munder revision and available CLIs.
- [x] Install/run Munder in a safe local workspace or validate existing installation.
- [x] Verify no uncommitted work is touched.
- [x] Document true capabilities and gaps in `docs/discovery.md`.

**Gate:** Can start Munder UI and know exactly how Claude/Codex workers are configured.

### Phase 1 — Two repos, two real worker sessions
- [x] Configure one FE and one BE logical worker with repo-specific directory constraints.
- [x] Confirm terminal and status updates appear on the existing office floor.
- [x] Verify separate git roots, agents can't edit opposite repo without explicit permission.
- [x] Test one small harmless operation in each repo; validate diffs.
- [x] Decide 1 floor vs 2 floors based on actual cross-folder capabilities.

**Gate:** Correct working directories, live visibility and no repo mixups.

### Phase 2 — Runtime portability
- [ ] Run FE with Claude Code, then on a separate task FE with Codex (or vice versa).
- [ ] Run BE with Codex, then another BE task with Claude.
- [x] Store handoff notes when switching and preserve original run evidence.
- [x] Document any manual switching or restart required by Munder UI.

**Gate:** Both logical roles work with both CLIs, no false shared session memory claims.

### Phase 3 — Cheap XS/S task routing
- [x] Document rules for selecting repo, complexity, risk, runtime.
- [x] Validate native direct-to-worker dispatch; implement only minimal custom quick lane if missing.
- [x] Prevent unnecessary model-driven orchestration for XS/S.
- [x] Add bounded retries, timeouts and per-task cost reporting when measurable.
- [x] Demonstrate exact button-label-change task and record invoked agents/tools/metrics.

**Gate:** For an XS FE task, **no unrelated agent model calls**. Scoped change and real checks completed.

### Phase 4 — Parallel full-stack flow
- [x] Set up independent FE/BE worktrees and two linked feature tasks.
- [x] Agree and version API contract before parallel work.
- [x] Run FE and BE task branches independently.
- [x] Test FE/BE integration against matching revisions.
- [x] Generate two PRs (if credentials are configured) with task references and CI evidence.
- [x] Verify review, protected branch and human approval workflow.

**Gate:** Two PRs ready for user review, neither merged automatically.

### Phase 5 — Observability and resilience
- [x] Show provider/model per run and trustworthy statuses on the office.
- [x] Verify budgets, actual available token/cost telemetry and circuit breaker.
- [x] Exercise agent crash, quota errors, interrupted session and malformed tool output.
- [x] Verify safe fallback/handoff, no uncontrolled retry storms.
- [x] Deliver written operator guide and test report.

**Gate:** A failed or over-budget run is visible, stopped and recoverable without corrupting repositories.

### Phase 6 — Optional isometric custom theme
- [ ] Only if requested after Phase 5, evaluate isometric visual feasibility and asset licensing.
- [ ] Implement isolated prototype/theme without replacing Munder's task/terminal machinery.
- [ ] Confirm all interaction and event mapping remains correct.

**Gate:** A usable isometric office theme with preserved functionality, OR documented reason to keep the existing proven 2D floor.

## 11. Mandatory acceptance tests

1. **XS cost control:** Rename a specific FE button label. Check that at most one coding CLI session executes, no irrelevant agent awakens, and only intended file(s) change.
2. **Deterministic edit safety:** Multiple matching labels or ambiguous file → never blind replace; ask user or use focused coder.
3. **Runtime switch:** FE Claude task followed by FE Codex task. Verify role identity persists; each run records correct provider; no partial state loss.
4. **Runtime switch BE:** Same check for BE Codex → Claude.
5. **Repo isolation:** FE run cannot accidentally modify BE repo; independent Git root and worktree state validated.
6. **Parallel safety:** Two concurrent agents on separate worktrees don't share dirty working files.
7. **Cross-repo feature:** Matching API contract, linked FE/BE tasks, E2E against matching branches and two PRs.
8. **Gate enforcement:** Agents cannot auto-merge protected `main` or deploy production.
9. **Loop guard:** Three or fewer retries depending tier; error escalates with reproducible logs.
10. **Cost honesty:** No invented token costs; unknown metrics shown as `unknown`.
11. **Visualization:** Idle animation never triggers provider calls; actual sessions appear and stop correctly.
12. **Crash/restart:** No silent loss of uncommitted changes and no accidental forced cleanup.
13. **Licensing:** Art credits and separate art license preserved in distributions/forks.

## 12. Required delivery artifacts

- `docs/discovery.md`: actual repositories, Munder commit/version, supported features, CLI compatibility, gaps.
- `docs/setup.md`: exact commands, locations, screenshots/verification as appropriate, configuration steps.
- `docs/security.md`: least-privilege permissions, blocked dangerous operations, approval model.
- `docs/test-report.md`: test commands, logs/evidence, pass/fail/skipped and known limitations.
- `policies/task-routing.md`: rules-first XS/S/M/L routing and cost policy.
- `policies/runtime-handoff.md`: Claude/Codex switch and fallback procedure.
- Any scripts/config/source modifications only when needed, small, documented and verified.
- PR links or patch paths if GitHub PR creation is not configured.

## 13. Instructions for the coding AI (paste this as initial task)

> Read `plan.md` in full. We are using **Munder Difflin, NOT Paperclip**. Start at Phase 0 and inspect the real FE and BE repositories and the current Munder Difflin installation/source before coding. Reuse existing Munder features (office UI, CLI sessions, worktrees, task board, telemetry) and only implement the smallest verified gaps. Preserve separate FE/BE repositories; allow either Claude Code or Codex for each agent on different tasks. Optimize tokens aggressively: XS tasks must not wake the whole team. Do not modify production, secrets, protected branches or deploy without approval. Finish each phase with real test evidence and update the documentation and checklist. Do not claim success on unexecuted steps. If capabilities differ from upstream README, document the actual findings and adjust the implementation without inventing APIs or config keys.

## Execution note — 2026-10-12

Phases 0/1 verified; Phase 3 XS test passed with zero model workers. User explicitly authorized continuing Phases 3–5 with Codex while successful Claude execution validation in Phase 2 remains pending. Actual Claude attempts reported provider quota and later expired OAuth; do not mark its gate passed. Phase 4 feature is PAY-STAGES (Logistics contract payment terms with multiple occurrences). See docs/test-report.md and evidence/.

Final limits/gaps: successful real-Claude FE/BE executions remain unchecked under the user-approved Codex continuation. Phase 6 is optional and not requested. Bounded coding roles and native board work; unbounded native/GOD/voice launches and automatic Michael planning are intentionally disabled in the safety profile. User-approved feature plans coordinate linked FE/BE work. See docs/operator-guide.md for exact supported workflow, measured counts, overshoot limits and human release gates.

Final delivery verification: 969 Munder tests (968 pass, 1 skip), 12 resilience fixtures, 6 OS isolation tests, 55 focused regressions. Final Claude FE/BE recheck failed expired OAuth; Phase 2 remains pending under the user-approved waiver. Product PRs remain separate drafts; no merge or deployment.

Idle office UI fix verified: no CLOCKING IN/WAKING THE FLOOR overlay when manager autostart is disabled; coding form layout improved. TypeScript, build and native Electron UI checks passed with zero model PTYs. Commit: `5287d4e09cebf1a3a4d05015b92f3d7a404c2c3c`. Evidence: ui-idle-native.log and ui-idle-fixed.png.

Per-run model selection delivered (a9394f918f337f0c979994b703cd7ab34232c036): native catalog suggestions/custom ID, CLI-default omission, separate per-runtime UI choices, validated --model forwarding for all six roles, immutable requestedModel separate from observed model. TypeScript/build passed; 14 real process fixtures and native Electron UI/role tests passed without provider calls. Evidence: model-picker-process-tests.log, model-picker-native-tests.log. Real Claude provider validation remains pending.

Effort selection delivered (4e41d210e6c7db7bea012cba77fa0a283d7457ce): low default in launcher; separate runtime choices and CLI-default omission; Codex config/Claude --effort forwarding; validated and recorded requestedEffort for all six coding roles. TypeScript/build passed; 16 real process fixtures plus native Electron UI/role lifecycle tests passed with zero provider calls. Screenshot effort-picker.png; logs effort-picker-process-tests.log and effort-picker-native-tests.log. Successful real-Claude execution still pending.

Persistent role defaults delivered (881f024c15c837cfb1fbfaa6580eb8770dd3f911): Save defaults stores runtime and per-runtime models/efforts in the selected harness home, atomically. Native restart test restored Frontend and QA values; switching to another workspace returned empty defaults and left original settings intact. Invalid preferences refused. TypeScript/build and native lifecycle/UI tests passed with zero provider calls. Evidence: preferences-native-tests.log and preferences-ui.png. Historical run settings preserved.

Start-worker usability fix delivered (7c584dba37c840f665748937a412c91a57da61f8): empty Task produces a clear validation message and zero workers; populated Task starts a bounded worker through the real button. Dialog excludes window dragging, action footer stays visible, preference-loading exceptions handled. TypeScript/build and native UI lifecycle tests passed, including actual button click, requested model/effort retention, defaults restart and separate-workspace isolation. Protocol fixtures only, zero provider calls. Evidence: start-worker-native-tests.log and start-worker-ui.png.

One-time complete-team setup delivered (a8e9935fe8e8473cbf49e9d6b16009a9431f8990): six role settings together, atomic complete-team save, retained existing workspace preferences. Primary task UI only requires FE/BE and task text; trusted dispatcher resolves saved runtime/model/effort. New workspaces require setup first; partial invalid team leaves settings intact. Tests clicked FE and BE tasks with different configured runtimes, retained all-role settings across restart, proved no idle model sessions after configuration and one new run per task, and refused client runtime/model/effort overrides. TypeScript/build and native lifecycle/UI tests passed, synthetic provider fixtures only. Evidence: team-setup-native-tests.log, team-simple-task.png, team-settings.png. QA/SA/reviewer/integration remain configured specialists; this change does not enable automatic Michael planning or whole-team activation. No merge/deployment.
