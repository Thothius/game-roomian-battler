---
trigger: model_decision
description: Enforce full release checklist whenever the app version is bumped
---

Whenever `gungeon_mate/pubspec.yaml`'s `version:` field is changed, the same
task/commit must also update, in lockstep — never bump version alone:

1. `gungeon_mate/VERSION_HISTORY.md` — new entry prepended, matching version + build number.
   (`assets/data/changelog.json` was removed — it had no runtime consumer;
   VERSION_HISTORY.md is the changelog of record and `version_lockstep_test`
   enforces its top heading matches `kAppVersion`.)
2. `gungeon_mate/lib/utils/asset_paths.dart` — `kAppVersion` must match.
3. `gungeon_mate/lib/screens/main_menu_screen.dart` — reads `kAppVersion`
   dynamically; verify no stale `vX.Y.Z` literals remain.

If asked to build a release APK, follow `.devin/workflows/release-build.md`
step order exactly (non-blocking build + polling, not a blocking build call).

If asked to modify `guns.json`, `items.json`, or `synergies.json` data content
(not just code), recommend running `.devin/workflows/verify-data.md` before
and after the edit.
