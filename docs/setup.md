# Current setup

Launch `./agent-office/scripts/launch-office.sh` from LOG. The old
`./scripts/launch-office.sh` remains valid through a compatibility symlink.
Select the existing `.local/state/home` workspace if the picker appears.

Configure roles once in Agent settings. Select a role, choose runtime/model/effort,
optionally apply it to all roles, then save. Workspace configuration on the same
screen edits FE/BE paths and checks CLI versions without making a provider call.
The check does not prove authentication; a real task may still fail on login/quota.

Routine tasks only require FE/BE and a prompt. Advanced options contain a specialist,
base branch, parent ID, prior stopped run and read-only mode. Exact FE label edits
are visible only for writable FE tasks. All attempts retain their original model
and effort. Worker inputs include bounded source pointers, not the whole roster.

Task history distinguishes running, review-needed, verifying, blocked and done.
Code changes require Run repository checks and then Accept reviewed result. Inspect
the diff and any task-specific UI/HTTP evidence first. File edits invalidate the
acceptance fingerprint. CLI success alone cannot close a code task. Read-only
sessions complete only with unchanged inputs. Historical Done entries remain
historical; no new verification claim is retroactively attached.

Repository gates execute in bubblewrap without login credentials, with a 20-minute
outer bound. A test requiring unavailable external services or credentials may fail;
inspect verification.log instead of treating that as a pass. No model is used for
running the gate. Token caps cover the whole continuation chain; unknown historical
usage cannot safely be continued under a new chain cap. Existing standalone tasks
retain their old run evidence.

Auto manager, spawning, heartbeat and idle model activity remain disabled. Native
Add agent and restore entry points are hidden for this profile. The upstream mode
remains available in source; its unrelated features were not deleted blindly.

Build: `cd agent-office/app && npm run build`. Development gate:
`./agent-office/harness/verify.sh`. UI test:
`cd agent-office/app && node tools/office-ui-review.cjs` (disposable profile, no LLM).
The prior setup/install history is under archive/setup-before-consolidation.md.
