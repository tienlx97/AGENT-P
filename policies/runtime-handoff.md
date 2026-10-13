# Runtime handoff — Phase 2

Frontend/backend are durable logical roles. `claude` or `codex` is selected on
**every task**, never assigned permanently to a repository. Each attempt records
its original runtime, role, branch/worktree, timestamps, observed metrics and
status under `office-state/home/office-runs/<run-id>/run.json` and in the native
Munder task ledger. Provider selection on a later task never edits prior runs.

Switch only after the previous process has stopped. Do not send an instruction to
switch engines inside a live CLI. Current UI starts a new task worktree, rather
than automatically resuming an unfinished branch. Fallback is manual and must
preserve the old worktree and its patch. Before a continuation, record:

```json
{"taskId":"example","from":"claude","to":"codex","repo":"FE","branch":"agent/example","worktree":"/absolute/task/path","changedFiles":[],"completed":[],"remaining":[],"verification":"not yet executed"}
```

Inspect `git diff` and the old evidence, then explicitly move the reviewed patch
or use the preserved worktree in a separately approved continuation workflow.
Automatic continuation/fallback is not implemented yet; do not overwrite partial
work or claim shared session memory.

2026-10-12: Claude authentication exists, but the first real attempt reported
`usage_limit_reached` / weekly limit, with reset **23:00 UTC** (06:00 Bangkok next
day according to that provider message). No automatic retry was attempted.
Phase 2 successful-execution gate cannot pass until Claude quota is restored.

The temporary CLI login/session profile is deleted after an attempt for isolation.
Do not rely on provider CLI `resume` to find it later. Subsequent launches retain
`terminal.log` beside the immutable-runtime `run.json`; these logs, the preserved
worktree and the compact handoff are the available continuation evidence.

User explicitly authorized continuing Phases 3–5 with Codex on 2026-10-12, keeping successful Claude execution validation pending. The FE/BE roles are runtime portable by launch schema, but both successful real-Claude role tests remain unverified.
