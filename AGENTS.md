# Agent office — map of truth

- App: `app/` (Electron main/preload, React renderer; its own Git repo).
- Runtime launch: `scripts/launch-office.sh`; isolated helper: `scripts/office-worker.py`.
- Configuration: one live profile under `.local/state/config/Electron/config.json`;
  per-role model/effort preferences under `.local/state/home/office-preferences.json`.
- Development verification: `harness/verify.sh`; UI evidence: app/tools/office-ui-review.cjs.
- Design and operating instructions: `docs/`; routing policy: `policies/`.
- Runtime data, toolchain, evidence and backups: `.local/`, not source code.
- FE/BE remain independent sibling repos in LOG. Follow each repo's instructions.

Read only task-relevant sources. Preserve main/preload/renderer boundaries.
A CLI success is not a verified code change. Do not bypass failed checks.
For UI changes, run the real screen and inspect screenshots at desktop and small sizes.
Keep legacy symlinks until historical paths have been deliberately migrated.
