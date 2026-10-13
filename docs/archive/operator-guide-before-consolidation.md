# Operating the bounded Munder Difflin office

Launch from the workspace: `./scripts/launch-office.sh`, then click **open**.
The original animated office and native terminals remain in use. **Task board**
opens the existing native kanban without a coordinator model call.

## Configure once, then dispatch

Open **Agent settings** to configure FE Developer, BE Developer, SA / Solution
Architect, QA Engineer, Code Reviewer and Integration Engineer together. Each role
has its own Runtime, Model and Effort. Native model suggestions remain available;
custom model IDs are allowed. Codex offers low/medium/high/xhigh effort; Claude
also offers max. Choose CLI default to omit a model/effort override. Availability
depends on the selected model/account; provider rejection never triggers a silent
substitution. Both engines' settings remain stored when switching a role's runtime.

Click **Save team configuration** once. Values are validated as a complete team
and written atomically into `<harnessHome>/office-preferences.json`. This configures
all roles without launching any model sessions. Existing complete configurations
are retained. A new workspace opens team setup before its first task; configurations
remain separate between workspaces and survive application restarts.

For routine work, use **Coding task**, select **FE** or **BE**, enter a nonempty
**Task**, then click **Start worker**. The main process resolves the configured
FE/BE role and its saved runtime/model/effort. The task screen has no model/effort
or role selection in the primary flow. FE and BE retain independent Git roots,
worktrees, branches and PRs. A trivial task launches only its scoped coder.

**Advanced options** retain specialist override, parent task ID, base branch,
stopped-run continuation and the deterministic exact-edit lane. Specialists use
their configured defaults; reviewer checkouts are read-only. Advanced overrides
reset when opening a new task. QA/SA/review/integration model sessions are not
automatically activated for every task; automatic Michael planning remains off.

`requestedModel` and `requestedEffort` describe each immutable run's requested
settings, separately from the provider-observed `model`. Unknown observed model
or cost stays unknown. Editing team settings never changes earlier run records.
The launch action stays visible while scrolling; an empty task shows an explanatory
validation message and starts zero workers.

For XS button copy, choose the exact-edit option and provide the verified source
file plus complete original/replacement JSX `label="..."` attributes. Exactly one
Button context must match. The tool refuses ambiguity/path escape, runs scoped
ESLint and exports a patch with zero provider calls. General tasks use one worker,
rules-first tier/risk classification, a per-task worktree and bounded checks.
Authentication/payment/privacy/migration/infra changes require elevated review.

For coordinated work, create an approved parent/contract in the native board,
then enter its ID on separately scoped FE/BE requests. Keep contract revisions
matched and prepare linked PRs. This profile uses human-approved plans; automatic
Michael planning and unbounded Add agent/GOD/voice process launches are disabled.
Do not mistake an inactive desk or avatar for a live model session.

## Boundaries and evidence

Final raw-token caps: XS 150k, S 500k, M 1.5m, L 3m per attempt. Exact XS edits
use zero. Item-step limits: 8/25/80/200. Wall times: 60/180/600/1800 seconds.
Output cap: 8 MiB. Automatic retries: zero (below the permitted tier maxima).
Codex multi-agent tools and Claude's Agent tool are disabled. Reflection, standups
and heartbeat model wakeups are off.

Usage often arrives at turn completion: a token cap can overshoot before the
stop is observed. Time/step/output guards stop active processes independently.
Never treat cached tokens as free or subscription limits as an API invoice.
Unknown model/cost metrics display `unknown`; provider cost estimates, when
reported, are separate from invoice spend.

Runs live under `office-state/home/office-runs/<run-id>/`: `run.json`,
`terminal.log`, `change.patch` and, for continuations, `handoff.json`. Original
provider/model/session fields and observed input/output/cache counts remain
attributed to that attempt. The native task board remains the current task source.
Inspect the worktree as well as the patch, especially newly created files.

## Stop, recovery and engine fallback

Use the employee close control to stop a run. Bounded terminals accept one task;
use a new attempt to change instructions. Generic restart is deliberately denied.
Enter the stopped run ID in **Continue stopped run** and choose the next engine.
The dispatcher verifies role/repository/branch provenance, retains the SAME dirty
worktree and records a compact handoff. It rejects active runs and exhausted
attempt chains. It never resets, force-cleans or deletes uncommitted work.

After an application interruption, surviving `running` records become blocked.
Inspect their worktrees and logs before an explicit continuation. No model is
restarted automatically. Provider authentication may require a fresh login;
OAuth updates from normally completed attempts are synchronized only while the
host auth profile still matches the starting revision.

Real Claude execution remains pending: the account first reported a weekly limit,
then expired OAuth. Restore its login/quota before claiming both-runtime acceptance.
Native fixture switching tests prove the launch/history/handoff mechanics, not
successful Claude provider execution. The user approved continuing with Codex.

## Review and release

PAY-STAGES is ready as two linked draft PRs:
[FE #9](https://github.com/tienlx97/FE-P/pull/9),
[BE #6](https://github.com/tienlx97/BE-P/pull/6).
Both full local gates and paired real HTTP/UI tests passed; CI remains manual-only.
Neither PR was merged. A new forward migration is included but was applied only
to the disposable test database, not to a live environment.

Merge/deployment needs separate human approval. Workers have no GitHub/SSH
credentials, Git common metadata is read-only, and no production configuration
is exposed. Host credentials are broader; the trusted operator prepares reviewed
commits and PRs, never an automatic protected-branch merge or deployment.
