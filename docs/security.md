# Current security boundary

The bounded **Coding task** entry point is the supported coding-office workflow.
It launches one selected runtime in a new Git worktree of the selected FE/BE root.
It rejects malformed requests, shared roots, dirty tracked files and missing
isolation prerequisites. Worktree creation failure aborts, never falls back.
The coding-office profile now rejects unbounded native Add agent/GOD/voice spawns,
so they cannot bypass the bounded dispatcher. Upstream behavior outside this profile
was not rewritten. Coordinated work uses an operator-approved native-board plan.

Linux bubblewrap exposes only operating-system tools, the chosen CLI binary,
Node/.NET runtimes, a private temporary login profile and the task worktree.
The opposite checkout, host home, SSH keys and gh credentials are absent.
Sensitive environment variables are not inherited. `.env*` local files and local
login notes inside the checkout are masked; samples/examples remain readable.
Git common metadata is read-only, preventing worker commits and branch merges.
The trusted host can later inspect the patch and prepare approved commits/PRs.
The worker has no push credentials and does not inherit production service keys.

Network is shared for provider access. This is a filesystem boundary, not a
network allowlist: unauthenticated services reachable from this machine are still
reachable. Run workers only on the development host. No production instance,
secret configuration, migration or environment was modified during setup.

Claude CLI bypass permissions and Codex CLI bypass sandbox are used ONLY INSIDE
this verified external OS sandbox. Do not reuse their inner argv directly on the
host. Authentication files are copied with mode 0600 into a temporary 0700 home;
that home is removed after each attempt. CLI-written OAuth refresh updates are
saved atomically only while the host profile still matches the starting revision;
managed attempts sharing that profile are serialized. A provider/login failure
still needs a manual login refresh. Lock wait counts toward the wall-clock cap.

Each attempt has a tier-specific wall-clock bound (XS 60s, S 180s, M 600s,
L 1800s) and zero automatic retries. Item-step and observed token caps are also
enforced. Total token telemetry may arrive at turn end, so a token cap is an
observed stop policy with possible overshoot, not a provider hard limit.
Timeout kills the process group. Quota/provider errors become blocked even if
provider JSON accompanies an exit code of zero. Runs are not automatically
continued, retried or sent to Michael. Generic restart for office run IDs is
rejected; use Coding task for a fresh session.

Manager autostart and scheduled standups are disabled for this isolated office.
No protected-branch merge, push, production deployment or destructive migration
was executed. FE main is unprotected and BE protection cannot be assumed.
Keep merge/deployment approval separate from Munder session permissions.

Remaining gates: adaptive tier budgets, interrupted-run recovery across app
restart, reviewed patch/PR preparation and full-stack approvals are later phases.
Do not advertise the partial implementation as an autonomous production system.

OAuth refresh correction: CLI login updates may rotate a refresh token. The
trusted wrapper now saves a changed authentication file atomically back to the
same host profile only if it has not changed since the run began. It never logs
its contents or replaces a concurrent login. A private Claude-profile lock serializes
managed Claude attempts; Codex workers can run concurrently on independent profiles. Temporary profiles are still removed;
GitHub/SSH/production credentials remain absent. This synchronization handles authentication lifecycle only.

Additional enforced boundaries: reviewer worktrees are read-only; continuation requires a stopped same-role/same-repo run and verifies worktree/Git provenance; attempts cannot exceed tier limits. Interrupted runs are marked blocked on application restart with code left in place. Generic restart is denied. Unknown metrics stay unknown; a valid provider completion is required for success. Output is capped at 8 MiB per attempt. Background reflection is disabled, preventing hidden-Claude summaries of idle desks.
