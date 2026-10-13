# Layout migration and cleanup

Current layout: LOG contains FE-P, BE-P and agent-office. Root-level aliases such
as docs, evidence, scripts, office-state and munder-difflin have been removed.
Use `agent-office/scripts/launch-office.sh` from LOG, or `scripts/launch-office.sh`
from inside agent-office.

## Initial consolidation

`scripts/migrate-layout.py` documents the original move into agent-office. It moved
app, scripts, policies, docs and local state/toolchain, backed up the profile, and
initially kept aliases for historical paths. This is an upgrade utility for the
old layout, not an installer for a new clone. Fresh installs use docs/install.md.

## Removing the old aliases

`scripts/remove-legacy-links.py` previews known aliases; `--apply` first migrates
runtime JSON paths, corrects toolchain wrappers and repairs every Git worktree at
its physical location, then unlinks the aliases. Close the office and stop workers
first. Unexpected symlink targets are rejected; ordinary directories at legacy
paths are never removed. Original changed metadata and the cleanup report are
under `.local/backups/remove-aliases-*/`. Log and patch contents remain historical.

Cleanup on 2026-10-13 removed all nine root aliases. Two clean persistent smoke
worktrees were also removed using Git. Tests now create disposable repositories
and do not require those old fixtures. The 16 task worktrees and run records remain;
FE/BE source checkouts are unchanged.

## What remains

- `docs/`: installation, operation, design decisions and archived implementation context.
- `.local/evidence/`: verification artifacts and screenshots used to review previous work.
- `.local/state/`: profile, task history and task worktrees; preserve uncommitted work.
- `.local/toolchain/`: compiler/runtime files still used for source builds.
- `.local/backups/`: metadata before migrations, retained for recovery.

Recovery requires closing the app, restoring the relevant backed-up metadata and
recreating the old aliases if restoring old absolute paths. Run Git worktree repair
for both product repositories before reopening. Do not move or delete task worktrees
with an ordinary recursive filesystem command.
