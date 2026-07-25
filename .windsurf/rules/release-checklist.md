---
trigger: model_decision
description: Enforce full release checklist whenever the app version is bumped
---

Whenever `gungeon_mate/pubspec.yaml`'s `version:` field is changed, the same
task/commit must also update, in lockstep — never bump version alone:

1. `gungeon_mate/assets/data/changelog.json` — new entry prepended, matching version.
2. `gungeon_mate/VERSION_HISTORY.md` — new entry prepended, matching version + build number.
3. `gungeon_mate/lib/screens/main_menu_screen.dart` — ALL version strings must match:
   - The `'Changelog (vX.Y.Z)'` button label string.
   - The home screen version `Text` widget (e.g. `'vX.Y.Z'`).
   - The changelog dialog header subtitle (e.g. `'vX.Y.Z — Title'`).
   Search for every `vX.Y.Z` / `v1.` / `v2.` literal in this file and update them ALL.

If asked to build a release APK, follow `.devin/workflows/release-build.md`
step order exactly (non-blocking build + polling, not a blocking build call).

If asked to modify `guns.json`, `items.json`, or `synergies.json` data content
(not just code), recommend running `.devin/workflows/verify-data.md` before
and after the edit, since these files are validated against a cached wiki
source of truth in `cache_wikigg/`.
