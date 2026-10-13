# One configuration authority

Use Agent settings in the app. The gear button opens the same screen in office mode.

- Workspace profile: `../.local/state/config/Electron/config.json`
- Team runtime/model/effort: `../.local/state/home/office-preferences.json`
- Routing limits: `../app/src/shared/codingOfficePolicy.ts` (validated code policy,
  shown read-only in the UI; not a second editable JSON budget).

These are distinct data, not competing copies: workspace owns paths/platform
preferences, team owns per-role runtime settings. The UI saves through the existing
main-process API. Repository paths are validated as two distinct Git roots.
No credential files are copied here. Do not commit runtime profiles.
