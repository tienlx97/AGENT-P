# Agent Office

Start from LOG:

```bash
./agent-office/scripts/launch-office.sh
```

Open the existing workspace `.local/state/home` if the picker is shown.
Choose **Agent settings** once, select a role and set runtime/model/effort.
**Apply this configuration to all roles** copies the selected settings to the
whole team; save to persist. Existing model choices are preserved.
Then use **Coding task**: select FE or BE, enter a task, start the worker.

**Task board** shows run history, fresh/cache/output usage, repository checks
and acceptance. A completed code worker needs repository verification and a
reviewed result before Done. **Open diff & evidence folder** opens its evidence.
Read-only analysis is available in Advanced options and uses read-only isolation.

Folders: `app/` is the existing Munder Git repo, `scripts/` launches isolated
workers, `harness/` points to the app's verification harness, `policies/` and
`docs/` describe behavior, `.local/` holds state, worktrees, toolchain and evidence.
FE-P and BE-P remain outside this folder as independent repositories.
Old LOG paths are compatibility symlinks, not extra copies.

```bash
./agent-office/harness/verify.sh
cd agent-office/app && node tools/office-ui-review.cjs
```

See [setup](docs/setup.md), [configuration](config/README.md) and
[migration notes](docs/layout-migration.md).

## Clone with the application source

```bash
git clone --recurse-submodules https://github.com/tienlx97/AGENT-P.git agent-office
```

`app` is pinned to a reviewed commit in the `tienlx97/munder-difflin` fork.
Runtime state and credentials are not included. Configure local FE/BE repository
paths and CLI authentication before running on a new machine.

After editing the app, commit and push in `app` first. Then commit the updated
`app` submodule pointer in this repository and push it. Do not use `git add .local`.
Legacy PAY-STAGES integration scripts require `OFFICE_TEST_PASSWORD` for their
disposable local test account; no password is stored in source.
