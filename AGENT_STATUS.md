# Agent Status Board

> **Single source of truth for agent coordination.**
> Every agent MUST update this file at session start, when switching tasks, and at session end.
> If you're about to start work, read this file FIRST.

---

## Task Queue

Numbered tasks waiting to be done. Agents claim a task by adding their name to "Claimed by".
When done, mark status as `DONE` and move to Session Log.

| # | Task | Claimed by | Status | Blocked by |
|---|------|------------|--------|-------------|
| 1 | BUG-035: Rework PeriodicTile gun panel — gun type below title (centered addon-panel) + add RANGE number alongside DPS on the periodic grid | — | TODO | — |
| 2 | BUG-036: Active run HeaderMenu — surface "Reset Player Items" quick action + move Settings to the bottom section (with Leave MP / End Run) | — | TODO | — |
| 3 | BUG-037: Remove MP Summary panel/tab (SummaryTab + MpSummaryPage) from multiplayer header | — | TODO | — |
| 4 | BUG-038: Unicorn theme particle effects broken + palette selector scroll + per-palette preset particle previews | — | TODO | — |
| 5 | BUG-039: S-tier chest/quality colors unreadable — revert to black pill + white text + gold glow (QualityBadge + _ChestChip + PeriodicTile S handling) | — | TODO | — |

---

## Active Agents (up to 3 concurrent slots)

### Slot 1

| Field | Value |
|-------|-------|
| **Agent** | _(none)_ |
| **Branch** | master |
| **Session started** | 2026-08-12 17:53 UTC+3 |
| **Last board update** | 2026-08-12 18:01 UTC+3 |
| **Working on** | — |
| **Files in progress** | — |
| **Uncommitted changes** | — |
| **Last commit** | `e0f928b` (gungeon_mate) — v1.8.39: fix BUG-017/019/020 — synergy data, MP reconnect feedback, quality cleanup |

### Slot 2

| Field | Value |
|-------|-------|
| **Agent** | Maintainer |
| **Branch** | master |
| **Session started** | 2026-08-12 18:00 UTC+3 |
| **Last board update** | 2026-08-12 18:00 UTC+3 |
| **Working on** | Formalizing 5 user-reported bugs (BUG-035–039) into bug tracker + Task Queue for Coder pickup |
| **Files in progress** | docs/bug_tracker.md, AGENT_STATUS.md |
| **Uncommitted changes** | — |
| **Last commit** | `9abddc0` — Bughunt fixes: remove duplicate dice card from AppTab, remove dead DebugTab class, fix dice preview glow alpha, remove redundant header, fix stale comment + settings doc comment |

### Slot 3

| Field | Value |
|-------|-------|
| **Agent** | _(none)_ |
| **Branch** | — |
| **Session started** | — |
| **Last board update** | 2026-07-23 15:05 UTC+3 |
| **Working on** | — |
| **Files in progress** | — |
| **Uncommitted changes** | — |
| **Last commit** | `(see git log)` refactor: remove still wallpaper system + dead webview_flutter dep + bughunt docs |

---

## How To Use This File

### Session Start (BEFORE any work)
1. Read this file
2. Find an empty slot (Agent is `_(none)_`)
3. If all slots are full, check for stale sessions (see below). If none are stale, STOP and ask the user.
4. Set **Agent** to your role (`Coder`, `Coder #2`, or `Maintainer`)
5. Set **Session started** and **Last board update** to current timestamp
6. Set **Working on** to your task description (or claim a task from the Task Queue)
7. If another agent is active in a different slot, create a git branch: `git checkout -b <agent-type>/<task-slug>` (see AC5)
8. Leave **Files in progress** and **Uncommitted changes** empty (fill as you go)

### During Session
- Update **Files in progress** when you start editing a new file
- Update **Uncommitted changes** when you have uncommitted work
- Update **Last board update** timestamp every time you modify this file (helps stale detection distinguish active from crashed)
- Other agents' **Files in progress** are off-limits (AC4)

### Session End / Agent Switch (AFTER commit)
1. Set **Agent** back to `_(none)_`
2. Update **Last board update** to current timestamp
3. Fill **Last commit** with the SHA and message
4. Clear **Working on**, **Files in progress**, **Uncommitted changes**
5. If you have WIP that can't be committed, note it under **Uncommitted changes** with `WIP:` prefix
6. Append a structured handoff row to the Session Log (see format below)
7. If you were on a branch, merge to master and delete the branch (see AC5)

### Stale Session Detection
- Check **Last board update** first — if it's recent (< 10 min ago), the agent is likely still active even without commits.
- If **Last board update** is more than 30 minutes old AND **Last commit** is empty or also stale, the slot is likely dead. A new agent may ask the user: "Slot N shows `<agent>` — last board update `<time>`, last commit `<time or none>` — looks stale. Should I take over?"
- The user confirms before claiming a stale slot.

---

## Session Log (append-only, structured handoff)

Format: `| Agent | Date | Branch | Commit | Task | Files | Status | Next | Watch out for |`

> **Archiving:** Keep only the last 20 entries. When the log exceeds 20 rows, move older entries to `docs/session_log_archive.md` (create if needed). This keeps the board readable.

| Agent | Date | Branch | Commit | Task | Files | Status | Next | Watch out for |
|-------|------|--------|--------|------|-------|--------|------|---------------|
| Coder | 2026-07-23 | master | `14020f4` | Debug tab + special items grid | settings_screen.dart, run_provider.dart | DONE | — | removeGun/removeItem now have `force` param |
| Coder | 2026-07-23 | master | _(user)_ | Main menu polish | main_menu_screen.dart, pubspec.yaml | DONE | — | Version bumped to 1.6.7+68 |
| Coder #2 | 2026-07-23 | master | `48d3d21` | Phase 2: _Header redesign | item_detail_screen.dart | DONE | Phase 3 (summary string) next | Commit went to master instead of branch — branch was empty, deleted |
| Coder | 2026-07-23 | master | `300eaab` | v1.7.0 release — assessment + version bump + APK build + push | pubspec.yaml, main_menu_screen.dart, changelog.json, README.md | DONE | — | VERSION_HISTORY.md is gitignored (builds/ dir), updated locally only |
| Coder | 2026-07-23 | master | `da0b82e` | v1.7.1 release — UI polish + clipping fixes + detail redesign + APK build + push | active_run_screen.dart, character_select_screen.dart, item_detail_screen.dart, main_menu_screen.dart, gungeoneer_header.dart, home_screen.dart, pubspec.yaml, changelog.json | DONE | — | APK at app-releases/GungeonMate-v1.7.1.apk (46.9MB) |
| Coder | 2026-07-23 | master | `47900c8` | README v1.7.1 badge/link fix + GitHub Release with APK asset | README.md | DONE | — | Tag v1.7.1 pushed, release created via gh CLI |
| Coder | 2026-07-23 | master | _(uncommitted)_ | 3-session bughunt: UX + UI/Nav + Data completeness | docs/bug_tracker.md, docs/reorg_plan.md | DONE | Megafile reorg (BUG-030/031) | 18 new bugs logged (BUG-017–034). Reorg plan updated with current sizes. `webview_flutter` is dead dep. `theme_overlay.dart` already split down to 34KB. |
| Coder | 2026-07-23 | master | `84fd11f` | Phase 3: Split item_detail_screen.dart megafile | item_detail_screen.dart, widgets/item_detail/{header,gun_stats,item_body,synergies_section,destroy_banner,quick_jump_button}.dart | DONE | Settings screen split (assessed: 95.6KB, 12 classes, 7-file split recommended) | 3582→332 lines. flutter analyze clean. No controllers/async in extracted widgets. |
| Coder | 2026-07-23 | master | `dcf6891` | Split settings_screen.dart megafile | settings_screen.dart, widgets/settings/{theme_visuals_tab,run_tab,app_tab,swipe_picker,run_log_screen,debug_tab}.dart | DONE | Phase 1: active_run_screen.dart split (391KB, pending) | 2390→64 lines. 12 classes → 6 files. SwipePicker has PageController+dispose(). RunTab/AppTab have context.mounted checks. flutter analyze clean. |
| Coder | 2026-07-23 | master | `05dc81d` | Phase 1: Split active_run_screen.dart megafile | active_run_screen.dart, widgets/active_run/{player_header,player_page,active_run_helpers,stat_sheets,sort_picker,starter_hint,dice_roll,summary_tab}.dart, widgets/dashboards/{dashboard_swiper,robot_dashboard,junkan_dashboard,special_gun_dashboards,huntress_dashboard,compact_dashboards}.dart, widgets/sheets/damage_calc_sheet.dart | DONE | Phase 2+4 reorg | 9520→566 lines. 60+ classes → 15 files across 3 dirs. All dispose()/mounted checks preserved. flutter analyze clean. |
| Coder | 2026-07-23 | master | `7c8012b` | Phase 2: Split theme_overlay.dart | theme_overlay.dart, widgets/particles/{touch_particle,ambient_glow,curse_fog,curse_breath,crimson_drip}.dart, widgets/backgrounds/{page_frame,animated_wallpaper}.dart, widgets/easter_eggs/cat_throne.dart | DONE | Phase 4 next | 951→312 lines. 10 classes → 8 files. CurseFog/CurseBreath/CrimsonDrip are dead code (not referenced in build). CatThrone easter egg extracted. All AnimationControllers have dispose(). flutter analyze clean. |
| Coder | 2026-07-24 | master | `104e842` | Item detail chest chip + duplicate sell price + Gunderfury fixes + mojibake cleanup + dashboard tab system | lib/widgets/item_detail/{header,gun_stats,item_body}.dart, lib/screens/item_detail_screen.dart, lib/widgets/active_run/player_page.dart, lib/widgets/active_run/{sort_picker,stat_sheets,active_run_helpers,dice_roll,player_header,starter_hint,summary_tab}.dart, lib/widgets/dashboards/{dashboard_swiper,junkan_dashboard,special_gun_dashboards,robot_dashboard,huntress_dashboard,compact_dashboards}.dart, lib/widgets/sheets/damage_calc_sheet.dart, lib/screens/active_run_screen.dart, lib/widgets/item_detail/synergies_section.dart, lib/widgets/gungeoneer_header.dart, lib/screens/synergies_overview_screen.dart, lib/widgets/active_run/summary_tab.dart, assets/data/{back_refs,guns,synergies}.json | DONE | Test dashboard tab system on real device/emulator | DashboardSwiper now uses PageController + dispose() correctly. Tab chips show item/gun icons. Panel height is 22% of screen. Gunderfury DPS now dynamic in item detail and active run. |
| Coder | 2026-07-24 | master | `3090780` | Resolve prior uncommitted changes | lib/screens/{multiplayer_lobby_screen,theme_picker_screen}.dart, lib/services/app_theme.dart, lib/widgets/{particle_engine.dart,settings/theme_visuals_tab.dart}, macos/Flutter/GeneratedPluginRegistrant.swift | DONE | — | MP lobby has numeric keypad PIN bottom sheet. HSV color picker added. ThemeRemix supports full ThemeFlair override. Particle cosmic dust palette brightened. webview_flutter plugin registration removed from macOS. |
| Coder | 2026-07-24 | master | `062da94` | Dice roll UX: cancel challenge protocol, per-die sparkle keys, VS overflow | lib/widgets/active_run/dice_roll.dart, lib/services/multiplayer_session.dart, lib/models/multiplayer_messages.dart, lib/screens/active_run_screen.dart | DONE | — | Added MpDiceCancel message/session/handler, cancel challenge button, per-die GlobalKey sparkle positioning, FittedBox score overflow. flutter analyze clean. |
| Coder | 2026-07-24 | master | `881f374` | v1.8.19 release build + APK | gungeon_mate/pubspec.yaml, gungeon_mate/assets/data/changelog.json, gungeon_mate/VERSION_HISTORY.md, gungeon_mate/lib/screens/main_menu_screen.dart | DONE | — | Bumped to 1.8.19+74, updated changelog/history/main_menu version strings, built release APK (45.3MB), merged coder/playwright-setup into master and pushed to origin. |
| Coder | 2026-07-24 | coder/synergy-ui | `d396a81` | Synergy + special dashboard UX | lib/widgets/{active_run/player_page,gungeoneer_header,item_detail/{header,item_body,gun_stats}}, lib/screens/{all_synergies,item_detail}, lib/widgets/dashboards/{dashboard_swiper,junkan_dashboard,special_gun_dashboards,robot_dashboard,huntress_dashboard,compact_dashboards} | DONE | Merge to master once Coder #2 WIP is cleared | Coder #2 has uncommitted WIP (app_theme.dart, web/index.html); merge to master only after their changes are committed/stashed; flutter analyze clean; all expand icons removed from dashboards |
| Coder | 2026-07-24 | coder/synergy-ui | `6b8060f` | S-tier chest chip readability glow | lib/widgets/item_detail/header.dart | DONE | Merge to master once Coder #2 WIP is cleared | Same Coder #2 block as above; S-tier chip now has white/grey border + subtle white glow |
| Coder | 2026-07-24 | coder/synergy-ui | `0921264` | Shrine picker UX: USE buttons, used-shrines log popup, formatted effect bodies | lib/screens/shrine_picker_screen.dart, assets/data/changelog.json | DONE | Merge to master once Coder #2 WIP is cleared | Initial commit landed on coder/playwright-setup; moved to coder/synergy-ui and restored Coder #2's WIP. flutter analyze clean on modified file. |
| Coder | 2026-07-24 | coder/synergy-ui | `b966104` | Bigger end-active-run dialog with clearer buttons | lib/widgets/active_run/active_run_helpers.dart, assets/data/changelog.json | DONE | Merge to master once Coder #2 WIP is cleared | AlertDialog inset/content/actions padding increased, title/content/button text scaled up, added warning icon. flutter analyze clean. |
| Coder | 2026-07-24 | coder/synergy-ui | `eee8811` | Scale up and bottom-align gungeoneer picker graphics | lib/screens/character_select_screen.dart, assets/data/changelog.json | DONE | Merge to master once Coder #2 WIP is cleared | Character card art scaled to 1.35x and aligned to bottomCenter of the image area; added changelog item. flutter analyze clean. |
| Coder #2 | 2026-07-24 | coder/playwright-setup → master | `9abddc0` | Bughunt: remove duplicate dice card from AppTab, remove dead DebugTab class, fix dice preview glow alpha, remove redundant header, fix stale comment + settings doc comment | lib/widgets/settings/{app_tab,theme_visuals_tab,debug_tab}.dart, lib/screens/settings_screen.dart | DONE | — | Merged both coder branches to master. 6 bughunt fixes applied. flutter analyze clean (0 issues). Branches deleted. |
| Coder | 2026-07-24 | master | `de99f43` | v1.8.22 release — merge branches, fix 2 crit bugs, bump version, APK build + push | lib/screens/item_detail_screen.dart, lib/widgets/dashboards/huntress_dashboard.dart, lib/screens/main_menu_screen.dart, pubspec.yaml, assets/data/changelog.json | DONE | — | Merged coder/synergy-ui into coder/playwright-setup then into master. Fixed missing `elements` param in ItemDetailHeader call site (crash bug) and broken InkWell in huntress_dashboard.dart. APK 45.6MB at app-releases/gungeonon-mate-v1.8.22.apk. 0 analyze errors, 21 info warnings (all pre-existing). |
| Coder | 2026-07-24 | master | `729ead5` | v1.8.23: fix mojibake, zoom app icon 15%, redesign item detail header | lib/screens/{browse_screen,character_select_screen,item_detail_screen}.dart, lib/widgets/{theme_overlay,item_detail/header}.dart, assets/images/app_icon.png, android+ios launcher icons | DONE | — | Fixed 11 mojibake across 4 files. Zoomed app icon 15% (crop+rescale, regenerated all platform icons). Redesigned ItemDetailHeader: rank badge top-left (36px), fav button 50% bigger (36px), no ring on icon, all tags inline in single Wrap, quote at bottom with accent gradient divider. Replaced _TypeAndElementsRow with _TagChip + _AccentDivider. flutter analyze: 0 issues. |
| Coder | 2026-07-24 | master | `5b3cc94` | v1.8.38: Huntress health stats toggle, item detail header redesign, mojibake fixes, app icon zoom, release APK | lib/widgets/dashboards/huntress_dashboard.dart, lib/widgets/item_detail/header.dart, lib/screens/{browse_screen,character_select_screen,item_detail_screen,main_menu_screen}.dart, lib/widgets/{theme_overlay,active_run/player_page}.dart, pubspec.yaml, assets/data/changelog.json, assets/images/app_icon.png, android+ios launcher icons | DONE | — | User added Huntress ALL/HP toggle (StatefulWidget). Bumped to v1.8.38+77. APK 47.8MB at app-releases/gungeonon-mate-v1.8.38.apk + Desktop. flutter analyze: 0 errors, 0 warnings, 20 info (pre-existing). All changes pushed to origin/master. |
| STALE — taken over by Coder | 2026-08-12 | master | — | Roomian Battler slot (last board update 2026-07-26, 17 days stale) cleared per AC6; user confirmed takeover. New Coder session started for bugfix batch (BUG-017/019/020). | — | DONE | — | `roomian_battler/` dir has uncommitted new commits with no .gitmodules mapping — left untouched per user. `git log` only shows 3 commits; older session-log commits not in history (repo appears reset/squashed at some point). |
| Coder | 2026-08-12 | master | `e0f928b` (gungeon_mate) | v1.8.39 bugfix batch: BUG-017 (Max Pane synergy data), BUG-019 (MP reconnect snackbar+haptic), BUG-020 (1S→S quality cleanup) | assets/data/{synergies,guns,items,changelog}.json, lib/widgets/mp_request_listener.dart, lib/screens/{browse_screen,main_menu_screen}.dart, pubspec.yaml, VERSION_HISTORY.md | DONE | Next: 12 OPEN bugs remain (BUG-018/021/022/023/024/026/027/028/029/032/033/034). UX polish batch (BUG-018/026/027/028/029/033/034) is the next logical group. | `gungeon_mate/` is a nested git repo (not a submodule) — commits land there, not in outer repo. Two pre-existing uncommitted changes in `lib/widgets/item_detail/header.dart` + `lib/widgets/periodic_tile.dart` (UI tweaks from prior session) were left unstaged. flutter at `C:\src\flutter\bin\flutter.bat` (X:\flutter is gone). flutter analyze: 0 issues on 3 modified Dart files. |
