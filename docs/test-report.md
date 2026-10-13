# Implementation evidence

| Phase | Result | Evidence |
| --- | --- | --- |
| 0 | Passed: discovery, source build, real Electron GUI | discovery.md; phase0-ui.png; native-build.log |
| 1 | Passed: FE/BE Codex workers, independent worktrees, animated office/terminals, clean diffs | phase1-native-smoke-final.log; phase1-office.png; phase1-complete.png |
| 2 | Pending successful Claude runs; real quota/auth failures observed | phase1-fe-claude.jsonl; phase2-portability.log |
| 3 | Passed XS zero-worker button edit, scoped ESLint, ambiguity/path/dry-run tests | phase3-xs.log; phase3-policy-tests.log; native office-runs patch/checks logs |
| 4 | Passed: two linked draft PRs, full gates, real paired HTTP/UI, disposable MySQL import | phase4-worktrees.json; phase4-roundtrip.json; phase4-live-browser.json; phase4-seed-import.log |
| 5 | Passed with local protocol fixtures and native Electron lifecycle tests | phase5-resilience-final.log; phase5-isolation-final.log; phase5-native-final.log |
| 6 | Optional, not requested; keep existing classic art | LICENSE-ASSETS retained |

User authorized proceeding with Codex while Claude validation remains pending.
The first Phase 2 error-only assertion expected weekly-limit failure; it failed
when both native Claude attempts instead reported expired OAuth. The failed test
log is preserved. The error handling, blocked task status and runtime histories
were real; successful Claude execution is NOT certified.

Munder full baseline regression: **964 pass, 0 fail, 1 skip** (965 tests),
43.48s, `npm run test:focused`, evidence/munder-tests-phase1.log. After lifecycle
changes, relevant provider/role/task/worker/config/restart regressions: **48 pass**,
evidence/munder-regression-final.log. TypeScript node/web and source builds passed.
Final routing policy: 4 tests passed; final focused regressions: 55 passed (phase5-regressions-final.log). OS sandbox checks: 6 passed.

Product source checkouts still preserve original memory notes. Phase 1 smoke
runs read only; no product full harness was needed. XS demonstration is an isolated
reviewable patch with scoped checks, not a merged product change. Product feature
completion requires both repositories' full gates and browser/HTTP evidence.

Phase 4: BE full gate passed 1,350 tests; FE full gate passed 441 unit tests plus all structural/harness/build/quality checks. Final FE gate current: `harness/runs/20261012-203857-Ij3dxk`, freshness true. The shared dependency symlink failed Turbopack; replaced only that task symlink, task-local init.sh passed, then full build/gate passed. This limitation is documented. Native coder attempts each exceeded the observed 500k total-token cap at turn completion and were stopped/flagged without retries; host completed verification from their preserved worktrees. BE tokens 1,488,543 (1,413,760 cached); FE tokens 1,483,189 (1,381,376 cached). Costs/models unknown.

Linked draft PRs: [FE #9](https://github.com/tienlx97/FE-P/pull/9), [BE #6](https://github.com/tienlx97/BE-P/pull/6). CI is manual-only, local test evidence is supplied; neither PR was merged.

Paired real FE adapter → BE HTTP verified create/update/get, ordered 40/60 children within a 30% stage, legacy 100% default, and invalid update rejection without version/data loss. Real UI edit/save/reload persisted the condition and order against the paired BE test image; desktop/mobile screenshots inspected. Synthetic browser tests additionally cover receipt-count independence, add/remove, retained child identity, invalid shares and last-child protection. Test assumptions corrected: Astryx required labels include a required marker, and the Drawer is not exposed as `[role=dialog]`; fixtures now target the visible controls correctly.

Phase 5: 12 real process/OS resilience fixture tests passed (good completion, quota exit-zero refusal, malformed output, crash, iteration stop, wall-time stop, observed token stop, bounded output, conditional OAuth refresh, missing/invalid usage remaining unknown, immediate provider retry suppression). Six OS isolation tests passed, including opposite-repo/secret/env exclusion, read-only Git metadata and read-only reviewer checkout. Native Electron fixture tests passed: stable identity with per-run runtime attributes for all six coding roles and both CLI fixtures, native board without model sessions, quota escalation, active-handoff refusal, retained dirty patch on continuation, reviewer/base ref and interrupted-record recovery. Fixture CLI protocol is synthetic and generates **zero provider calls**; it does not certify real Claude execution.

Final Munder full regression on the delivery source: **968 pass, 0 fail, 1 skip (969 tests)**, evidence/munder-tests-delivery.log; 55 focused regressions also passed. Node/web TypeScript and production source builds passed. Licensed art files/credits were preserved; no isometric redesign was attempted.

Final real Claude FE/BE recheck: provider rejected both attempts with expired OAuth; no retries. Evidence: phase2-final-recheck.log. Successful Claude execution remains unchecked.

Munder source delivery commit: `f0f983574ed04b77d73c7ab905d2531f8c68dbc7` on `office/adaptive-routing`; local only. Reviewable source patch: evidence/munder-implementation.patch. Temporary FE port 3002 server and seedcheck API/database/privileges removed after verification; original development/production containers retained.

Idle office UI fix verified: no CLOCKING IN/WAKING THE FLOOR overlay when manager autostart is disabled; coding form layout improved. TypeScript, build and native Electron UI checks passed with zero model PTYs. Commit: `5287d4e09cebf1a3a4d05015b92f3d7a404c2c3c`. Evidence: ui-idle-native.log and ui-idle-fixed.png.

Per-run model selection delivered (a9394f918f337f0c979994b703cd7ab34232c036): native catalog suggestions/custom ID, CLI-default omission, separate per-runtime UI choices, validated --model forwarding for all six roles, immutable requestedModel separate from observed model. TypeScript/build passed; 14 real process fixtures and native Electron UI/role tests passed without provider calls. Evidence: model-picker-process-tests.log, model-picker-native-tests.log. Real Claude provider validation remains pending.

Effort selection delivered (4e41d210e6c7db7bea012cba77fa0a283d7457ce): low default in launcher; separate runtime choices and CLI-default omission; Codex config/Claude --effort forwarding; validated and recorded requestedEffort for all six coding roles. TypeScript/build passed; 16 real process fixtures plus native Electron UI/role lifecycle tests passed with zero provider calls. Screenshot effort-picker.png; logs effort-picker-process-tests.log and effort-picker-native-tests.log. Successful real-Claude execution still pending.

Persistent role defaults delivered (881f024c15c837cfb1fbfaa6580eb8770dd3f911): Save defaults stores runtime and per-runtime models/efforts in the selected harness home, atomically. Native restart test restored Frontend and QA values; switching to another workspace returned empty defaults and left original settings intact. Invalid preferences refused. TypeScript/build and native lifecycle/UI tests passed with zero provider calls. Evidence: preferences-native-tests.log and preferences-ui.png. Historical run settings preserved.

Start-worker usability fix delivered (7c584dba37c840f665748937a412c91a57da61f8): empty Task produces a clear validation message and zero workers; populated Task starts a bounded worker through the real button. Dialog excludes window dragging, action footer stays visible, preference-loading exceptions handled. TypeScript/build and native UI lifecycle tests passed, including actual button click, requested model/effort retention, defaults restart and separate-workspace isolation. Protocol fixtures only, zero provider calls. Evidence: start-worker-native-tests.log and start-worker-ui.png.

One-time complete-team setup delivered (a8e9935fe8e8473cbf49e9d6b16009a9431f8990): six role settings together, atomic complete-team save, retained existing workspace preferences. Primary task UI only requires FE/BE and task text; trusted dispatcher resolves saved runtime/model/effort. New workspaces require setup first; partial invalid team leaves settings intact. Tests clicked FE and BE tasks with different configured runtimes, retained all-role settings across restart, proved no idle model sessions after configuration and one new run per task, and refused client runtime/model/effort overrides. TypeScript/build and native lifecycle/UI tests passed, synthetic provider fixtures only. Evidence: team-setup-native-tests.log, team-simple-task.png, team-settings.png. QA/SA/reviewer/integration remain configured specialists; this change does not enable automatic Michael planning or whole-team activation. No merge/deployment.
