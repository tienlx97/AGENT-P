# Layout migration

`python3 agent-office/scripts/migrate-layout.py` prints the mapping.
`--apply` migrates only when the office/worker processes are stopped, backs up the
profile, retains legacy symlinks and runs Git worktree repair for FE and BE.
The migration on 2026-10-13 moved app, scripts, policies, docs and local state/toolchain.
No existing worktree content, patch or run history was removed.

Legacy paths are deliberately retained: historical run records and Git worktree
metadata can still reference them. They resolve to the same files. New runs use the
canonical `.local/state/home`. Do not remove those links merely to tidy LOG.

For rollback, close the app, restore the backed-up config and move each target back
to its original path after removing ONLY its compatibility symlink. For scripts,
retain the migration utility separately; restore the prior launcher from the archive
or point its root to the moved app. Run `git -C FE-P worktree repair` and its BE
counterpart, then check every worktree with `git status` before restarting.
Runtime backups are in `.local/backups/`; no provider credentials are in the backup.

Blog, landing-remotion and prototypes remain in the upstream app repository because
the audit did not establish they were unused. Build toolchain and downloaded packages
remain in `.local/toolchain` because the source build depends on them.
