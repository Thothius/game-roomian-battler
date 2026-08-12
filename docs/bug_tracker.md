# Open Bug Tracker

> **Shared across all agents.** Any agent that finds a bug during review, bughunt, or testing MUST add it here. Any agent that fixes a bug MUST update its status. No exceptions.
>
> See `AGENTS.md` → **Bug Tracker Rules (B1–B4)** for the protocol.

---

## Status Legend

| Status | Meaning |
|--------|---------|
| **OPEN** | Confirmed bug, not yet fixed |
| **FIXED** | Fix committed; includes commit hash |
| **WONTFIX** | Intentionally not fixing (includes reason) |
| **DISPUTED** | Needs investigation — may not be a real bug |

---

## Severity Legend

| Severity | Meaning |
|----------|---------|
| **CRITICAL** | Data loss, crash, security vulnerability |
| **HIGH** | Incorrect behavior affecting users or data integrity |
| **MEDIUM** | UX degradation or edge case with real impact |
| **LOW** | Minor issue, cosmetic, or non-standard pattern |
| **UX** | Design concern, not a code bug |

---

## Open Bugs

### BUG-001 — `sendAddToPeer` + `cancel()` duplicates items in inventory
- **Severity:** HIGH
- **Status:** FIXED
- **Found by:** Coder (code review, Jul 22 2026)
- **File:** `lib/services/multiplayer_session.dart`
- **Lines:** 840–848 (sendAddToPeer), 599–614 (cancel restoration)
- **Description:** `sendAddToPeer` adds a `_PendingGift` entry without removing the item from local inventory (correct by design). However, `cancel()` unconditionally restores ALL pending gifts to inventory via `addGun`/`addItem` with `force: true`. For `sendAddToPeer` items, the item was never removed — so this duplicates it.
- **Root cause:** `_PendingGift` has no `localRemoval` flag to distinguish "gift from self" (item was removed, restore on cancel) from "add-to-peer" (item was NOT removed, don't restore).
- **Fix:** Added `localRemoval` flag to `_PendingGift` (default `true`). Set `false` in `sendAddToPeer`. Skip restoration in `cancel()` when `localRemoval == false`.
- **Commit:** 1448315

---

### BUG-002 — `AppTheme.notifier.value = AppTheme.notifier.value` is a no-op
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (code review, Jul 22 2026)
- **File:** `lib/screens/theme_picker_screen.dart`
- **Lines:** 464, 916
- **Description:** `ValueNotifier` suppresses notification when `newValue == oldValue`. For enum values, `==` is identity, so this self-assignment never triggers a rebuild. The custom theme card won't visually refresh after saving colors in the editor sheet.
- **Fix:** Replaced self-assignment with `AppTheme.notifier.notifyListeners()` at both call sites.
- **Commit:** 1448315

---

### BUG-003 — 180ms hold duration too aggressive for long-press
- **Severity:** UX
- **Status:** FIXED
- **Found by:** Coder (code review, Jul 22 2026)
- **File:** `lib/widgets/periodic_tile.dart`
- **Lines:** 71
- **Description:** Platform standards use 400–500ms for long-press. At 180ms, scrolling through a grid of tiles risks accidental long-press triggers. The shake animation also has very little time to communicate feedback.
- **Fix:** Raised to 250ms — compromise between snappiness and safety.
- **Commit:** 013c2bc

---

### BUG-004 — Snapshot loss race condition in `_onRunChanged`
- **Severity:** MEDIUM
- **Status:** FIXED
- **Found by:** Coder (code review, Jul 22 2026)
- **File:** `lib/services/multiplayer_session.dart`
- **Lines:** 1343–1357 (`_onRunChanged`), 1386–1392 (`_broadcastSnapshot` finally)
- **Description:** When `_snapshotInFlight` is true and the debounce timer fires, `_onRunChanged` returns without rescheduling. If no further state changes occur, the final state is never sent to the peer — causing temporary desync. The `_onGift` method (line 1324–1327) tries to work around this with `force: true`, but a subsequent `_onRunChanged` from user input can cancel the force-snapshot debounce timer and replace it with a non-force one that gets silently skipped.
- **Root cause:** The `_snapshotInFlight` guard at line 1339 returns without rescheduling. The `_onGift` force-snapshot can be cancelled by `_onRunChanged`'s debounce cancel at line 1337.
- **Fix:** Added `_needsResend` flag. When `_snapshotInFlight` is true, `_onRunChanged` sets `_needsResend = true` instead of dropping. The `_broadcastSnapshot` `finally` block checks `_needsResend` and triggers another broadcast if flagged. Also cleared in `cancel()`.
- **Commit:** 013c2bc

---

### BUG-005 — `_HypnoticBg` stuck in loading state on asset load error
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (code review, Jul 22 2026)
- **File:** `lib/widgets/theme_overlay.dart`
- **Lines:** 860–862 (`_loadGif` catch block), 908–909 (build check)
- **Description:** If `_loadGif()` catches an exception (corrupt/missing GIF asset), `_isLoading` is never set to `false`. The build method at line 908 checks `_isLoading || _frames.isEmpty` and renders `SizedBox.shrink()` forever — the animated background is permanently blank with no error feedback.
- **Root cause:** The catch block at line 860–862 only calls `debugPrint` but doesn't update `_isLoading`.
- **Fix:** Added `if (mounted) setState(() => _isLoading = false);` in the catch block.
- **Commit:** 1448315

---

### BUG-006 — Missing `mounted` check before `setState` after `await Navigator.push` in `_pickCharacter`
- **Severity:** MEDIUM
- **Status:** FIXED
- **Found by:** Coder (code review, Jul 22 2026)
- **File:** `lib/screens/multiplayer_lobby_screen.dart`
- **Lines:** 166–175
- **Description:** `_pickCharacter()` awaits `Navigator.push<Gungeoneer>(...)` then calls `setState(() => _selectedCharacter = picked)` at line 174 without checking `mounted` first. If the lobby screen is disposed while the character select screen is open (e.g., system back navigation, parent widget rebuild), this throws `A setState() was called after dispose()`.
- **Root cause:** Missing `if (!mounted) return;` guard between the `await` and `setState`.
- **Fix:** Added `if (!mounted) return;` before the `if (picked != null)` block.
- **Commit:** 1448315

---

### BUG-007 — Video player controller leak in `_AnimatedWallpaperBackground` on rapid asset switch
- **Severity:** MEDIUM
- **Status:** FIXED
- **Found by:** Coder (code review, Jul 22 2026)
- **File:** `lib/widgets/theme_overlay.dart`
- **Lines:** 1389–1443 (`_initializeVideo` method)
- **Description:** If `didUpdateWidget` fires twice in quick succession (e.g., user rapidly cycles wallpapers), the second `_initializeVideo()` call overwrites `_controller` with a new `VideoPlayerController` before the first call's `await controller.initialize()` completes. The first call's controller is orphaned — its `setState` at line 1417 runs on the wrong controller instance, and the first controller is never disposed, leaking native video resources.
- **Root cause:** No guard against concurrent `_initializeVideo()` calls. The `oldController` capture at line 1390 only captures the immediately previous `_controller` value, not any in-flight controllers.
- **Fix:** Added `_videoInitToken` counter. Incremented at start of `_initializeVideo()`. After each `await`, check if token still matches. If not, dispose the orphaned controller and return early. Error path also checks token before `setState`.
- **Note:** Same race condition pattern exists in `_HypnoticBg._loadGif()` (lines 827–862) — if `didUpdateWidget` fires while GIF frames are decoding, old frames overwrite new ones via `setState`. Lower severity due to fast GIF decoding and timer cancellation.
- **Commit:** 013c2bc

---

### BUG-008 — Dice sparkle particles use hardcoded screen positions
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (UI bug hunt, Jul 22 2026)
- **File:** `lib/screens/active_run_screen.dart`
- **Lines:** 7454–7461 (`_stopDie` method), 7705 (dice Row GlobalKey)
- **Description:** `_spawnSparkles` is called with `xPos = 60.0 + index * 80.0` and `y = 160.0`. These hardcoded pixel coordinates assume a fixed dialog width and dice spacing. The actual dice are laid out with `Row(mainAxisAlignment: spaceEvenly)`, so their real positions vary with dialog width. On wider screens, sparkles appear too far left; on narrower screens, too far right. The visual effect is misaligned with the dice.
- **Root cause:** No `GlobalKey` or `RenderBox` lookup is used to find actual dice positions. Hardcoded offsets are a magic-number guess.
- **Fix:** Added `GlobalKey _diceRowKey` on the rolling state dice `Row`. In `_stopDie`, use `findRenderObject()` to get actual `RenderBox` width and compute `xPos = rowWidth * (index + 0.5) / 3`. y remains hardcoded with `ponytail:` comment noting the upgrade path.
- **Commit:** 013c2bc

---

### BUG-009 — `_DamageCalcSheet` missing `SafeArea` wrapper
- **Severity:** MEDIUM
- **Status:** FIXED
- **Found by:** Coder (UI bug hunt, Jul 22 2026)
- **File:** `lib/screens/active_run_screen.dart`
- **Lines:** 3766–3958 (`_DamageCalcSheet.build`)
- **Description:** `_DamageCalcSheet` is shown via `showModalBottomSheet` without `useSafeArea: true` and its build method returns a `Padding` without wrapping in `SafeArea`. The bottom padding uses `MediaQuery.of(context).viewInsets.bottom` (keyboard height) but does not account for the system navigation bar inset. On Android devices with gesture nav or 3-button nav, the "TOTAL DPS" row and bottom content can be clipped or hidden under the system nav bar.
- **Root cause:** Missing `SafeArea` wrapper. All other bottom sheets in this file (`_SortPickerSheet`, `_TransferSheet`, `_StatAdjusterSheet`) correctly wrap with `SafeArea`.
- **Fix:** Wrapped `Padding` in `SafeArea(child: ...)`.
- **Commit:** 1448315

---

### BUG-010 — `_showMpDiagnosticsDialog` missing `SafeArea` wrapper
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (UI bug hunt, Jul 22 2026)
- **File:** `lib/screens/active_run_screen.dart`
- **Lines:** 1062–1063 (`_showMpDiagnosticsDialog` builder)
- **Description:** The MP diagnostics bottom sheet uses `Padding(EdgeInsets.fromLTRB(20, 20, 20, MediaQuery.of(ctx).viewInsets.bottom + 24))` without `SafeArea`. `viewInsets.bottom` is 0 when no keyboard is present, so bottom padding is only 24px. On Android devices with system navigation bars (24–48px safe area inset), the close button and bottom content can be partially hidden under the nav bar.
- **Root cause:** Same as BUG-009 — missing `SafeArea` wrapper. The `showModalBottomSheet` call at line 1019 also lacks `useSafeArea: true`.
- **Fix:** Wrapped `Padding` in `SafeArea(child: ...)`.
- **Commit:** 1448315

---

### BUG-011 — Dice row overflow on narrow screens (≤360px)
- **Severity:** MEDIUM
- **Status:** FIXED
- **Found by:** Coder (UI bug hunt, Jul 22 2026)
- **File:** `lib/screens/active_run_screen.dart`
- **Lines:** 7680–7693 (rolling state dice Row), 7990 (dice Container width)
- **Description:** The Gunfortuna dice dialog lays out three `_DiceWidget` instances in a `Row` with `spaceEvenly`. Each dice widget has an inner `Container(width: 72)` with `padding: EdgeInsets.all(14)`, making each widget ~100px wide. Three dice = 300px minimum. The dialog has `insetPadding: horizontal 16` and content `Padding: horizontal 24`, leaving 280px of content width on a 360px screen (360 - 32 - 48 = 280). 300 > 280 causes a `RenderFlex overflowed by 20 pixels` error. On 320px screens, the overflow is 60px.
- **Root cause:** Fixed-width dice containers (72px + 14px padding) with no `Flexible`/`Expanded` wrapper. The `Row` has no `shrinkWrap` or overflow handling.
- **Fix:** Wrapped both dice `Row` widgets in `FittedBox(fit: BoxFit.scaleDown)`.
- **Commit:** 6cd257d

---

### BUG-012 — Dice challenge decline leaves challenger stuck in `challenging` state
- **Severity:** MEDIUM
- **Status:** FIXED
- **Found by:** Coder (code review, Jul 22 2026)
- **File:** `lib/screens/active_run_screen.dart`
- **Lines:** 96–100 (DECLINE button handler)
- **Description:** When a user declines a Gunfortuna dice challenge, the DECLINE button only calls `Navigator.pop(ctx)` — it doesn't send any message to the challenger. There is no `sendDiceDecline()` method in `MultiplayerSession`. The challenger's `onDiceAccept` callback never fires, so their dice dialog stays in `_DiceStatus.challenging` forever with no way to cancel or know they were declined.
- **Root cause:** Missing decline protocol message and handler. The MP message protocol has `MpDiceAccept` but no `MpDiceDecline` equivalent.
- **Fix:** Added `MpDiceDecline` message class + deserialization. Added `sendDiceDecline()` to `MultiplayerSession`. Added `onDiceDecline` callback handler in message switch. Wired DECLINE button to call `sendDiceDecline()`. `_DiceRollDialogState` handles `onDiceDecline` → resets to idle with "Challenge declined." announcement. Saves/restores `_prevDecline` in dispose.
- **Commit:** 6cd257d

---

### BUG-013 — Character select loadout view: too short, excessive padding, tiny in-game graphic
- **Severity:** UX
- **Status:** FIXED
- **Found by:** User testing (Jul 23 2026)
- **File:** `lib/screens/character_select_screen.dart`
- **Lines:** 93 (childAspectRatio), 404-447 (_buildInGameSprite), 758-801 (_buildInGameSprite in _CharacterCard)
- **Description:** The character select cards have `childAspectRatio: 0.56` which makes them too short to show full loadout content. The in-game sprite view has `padding: EdgeInsets.all(16)` which shrinks the GIF to a tiny size. The "IN-GAME" label wastes vertical space. User requests: taller cards, less left/right padding, 100% bigger in-game graphic.

### BUG-014 — Dashboard toggle icon hidden in active run header
- **Severity:** HIGH
- **Status:** FIXED
- **Found by:** User testing (Jul 23 2026)
- **File:** `lib/screens/active_run_screen.dart`, `lib/widgets/gungeoneer_header.dart`
- **Lines:** 1554-1655 (trailing row), gungeoneer_header.dart:287-291 (Spacer + Flexible)
- **Description:** The trailing row of header icons uses `SingleChildScrollView(horizontal)` inside `Flexible`. The `Spacer()` between avatar and trailing forces the Flexible to shrink, hiding the dashboard toggle icon (5th of 6 icons) off-screen. User cannot see the dashboard settings icon. The horizontal scroll is not discoverable.
- **Root cause:** `Spacer()` + `Flexible` combination shrinks the trailing widget, and `SingleChildScrollView` hides overflow icons.

### BUG-015 — Avatar cycling removes rectangular outline for modes 1 and 2
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** User testing (Jul 23 2026)
- **File:** `lib/widgets/gungeoneer_header.dart`
- **Lines:** 270-285 (avatar Container + ClipRRect)
- **Description:** Tapping the avatar to cycle graphics removes the rectangular border outline for the in-game GIF (mode 1) and animated card art (mode 2). The border is visible for mode 0 (static icon) because the small icon doesn't fill the container. For modes 1 and 2, the image fills the ClipRRect area and paints over the border.
- **Root cause:** `ClipRRect` with same radius as `Container` border clips child to outer edge, allowing image to paint over the 1.2px border.

### BUG-016 — Settings missing from bottom navigation bar
- **Severity:** MEDIUM
- **Status:** FIXED
- **Found by:** User testing (Jul 23 2026)
- **File:** `lib/screens/home_screen.dart`
- **Lines:** 128-149 (NavigationBar destinations)
- **Description:** The bottom NavigationBar only has 2 tabs: Inventory and Browse. Settings is only accessible via the _HeaderMenu popup (gear icon) on the active run screen, which is not discoverable. User expects a Settings tab in the bottom menu.

---

### BUG-017 — "Max Pane" synergy missing "Glass Guon Stone" from items array
- **Severity:** HIGH
- **Status:** FIXED
- **Found by:** Coder (data bughunt, Jul 23 2026)
- **File:** `assets/data/synergies.json`
- **Description:** The synergy "Max Pane" has `"items": ["Glass Cannon"]` only, but the effect text and `effect_tokens` reference both "Glass Guon Stone" and "Glass Cannon". The `matchesItems()` logic checks the `items` array — it will never flag this synergy as active when the player has both items.
- **Fix:** Added `"Glass Guon Stone"` to the `items` array: `"items": ["Glass Cannon", "Glass Guon Stone"]`.
- **Commit:** e0f928b

---

### BUG-018 — Browse screen has no empty-search state
- **Severity:** MEDIUM
- **Status:** OPEN
- **Found by:** Coder (UX bughunt, Jul 23 2026)
- **File:** `lib/screens/browse_screen.dart`
- **Lines:** 695–1098 (all list builders)
- **Description:** When search/filters yield zero results in Browse (Guns, Items, or All tabs), the list renders empty — no "No results found" message. The Quick Add bottom sheet and Codex screen both have empty states, but Browse does not. Users get a blank screen with no feedback.
- **Fix proposal:** Add an empty-state widget (similar to `_CodexList`'s empty state at codex_screen.dart:269-278) to each list builder when results are empty.

---

### BUG-019 — No "Connection Restored" feedback after MP reconnect
- **Severity:** HIGH
- **Status:** FIXED
- **Found by:** Coder (UX bughunt, Jul 23 2026)
- **File:** `lib/widgets/mp_request_listener.dart:283-288`
- **Description:** When MP reconnect succeeds, the drop dialog closes silently. No snackbar, no haptic, no visual confirmation. User has to infer reconnection from the dialog disappearing. Identified as P0 gap #1 in `docs/mp_auto_reconnect_plan.md`.
- **Fix:** In the `else if (!shouldShow && _dropDialogShowing)` branch, after closing the dialog, check `session.status` — if `connected` or `handshaking` (real reconnect, not teardown to `idle`/`error`), call `Haptics.success()` and show a floating "Connection restored — sync resumed" snackbar (1800ms).
- **Commit:** e0f928b

---

### BUG-020 — Quality value `1S` instead of `S` in data
- **Severity:** MEDIUM
- **Status:** FIXED
- **Found by:** Coder (data bughunt, Jul 23 2026)
- **File:** `assets/data/guns.json` (19 entries), `assets/data/items.json` (17 entries)
- **Description:** 36 entries use `"quality": "1S"` instead of `"quality": "S"`. The browse filter handles this with a special case (`q == 'S' || q == '1S'`), but the raw value is displayed in UI metadata chips — users see "1S" instead of "S" on screen. The `1` prefix appears to be a data pipeline artifact.
- **Fix:** Global replace `"quality": "1S"` → `"quality": "S"` in both JSON files (19 + 17 = 36 replacements). Removed the `'1S': 0` alias from `_qualityOrder` in `browse_screen.dart`. Note: defensive `1S` normalizations in `quality_badge.dart`, `run_provider.dart`, `item.dart`, `gun.dart`, `sort_picker.dart`, `browse_pills.dart`, `periodic_tile.dart`, `inventory_list_row.dart` are now harmless dead branches — left in place as a separate cleanup task.
- **Commit:** e0f928b

---

### BUG-021 — 46 active items missing `recharge_time`
- **Severity:** MEDIUM
- **Status:** OPEN
- **Found by:** Coder (data bughunt, Jul 23 2026)
- **File:** `assets/data/items.json`
- **Description:** 46 of 67 active items have no `recharge_time` value. Includes common items like Bomb, Box, Decoy, Molotov, Smoke Bomb, Teleporter Prototype. The item detail screen shows recharge time when present — these 46 items just omit it.
- **Fix proposal:** Populate `recharge_time` from wiki data for all active items.

---

### BUG-022 — 289 synergies missing local icon assets
- **Severity:** MEDIUM
- **Status:** OPEN
- **Found by:** Coder (data bughunt, Jul 23 2026)
- **File:** `assets/images/synergies/` (106 of 395 webp files present)
- **Description:** Only 106 of 395 synergies have local `.webp` icon files. The remaining 289 show fallback letter icons. The `Synergy.fromJson` constructor uses `localSynergyIcon(name)` to resolve the path — missing files silently fall back.
- **Fix proposal:** Batch-generate or download synergy icons for the 289 missing entries. Alternatively, improve the fallback to use a synergy-specific placeholder instead of a letter.

---

### BUG-023 — 3 guns missing wiki notes content
- **Severity:** LOW
- **Status:** OPEN
- **Found by:** Coder (data bughunt, Jul 23 2026)
- **File:** `assets/data/guns.json`
- **Description:** Poxcannon, Serious Cannon, and Silencer have no wiki notes content (empty `notes` array). All other 236 guns have notes.
- **Fix proposal:** Populate from wiki data or accept as "no trivia exists" if the wiki has none.

---

### BUG-024 — 2 items missing wiki content
- **Severity:** LOW
- **Status:** OPEN
- **Found by:** Coder (data bughunt, Jul 23 2026)
- **File:** `assets/data/items.json`
- **Description:** "C4 (Item)" and "Ser Junkan 1" have no wiki sections (effects, item_interactions, notes all empty).
- **Fix proposal:** Populate from wiki data or accept if wiki has no content for these entries.

---

### BUG-025 — `webview_flutter` dependency unused — dead dependency
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (asset audit, Jul 23 2026)
- **File:** `pubspec.yaml:40`
- **Description:** `webview_flutter: ^4.10.0` was listed as a dependency but never imported in any Dart file.
- **Fix:** Removed `webview_flutter` from `pubspec.yaml` dependencies.
- **Commit:** 4a6b276

---

### BUG-026 — Browse grid add-button tap target too small
- **Severity:** MEDIUM
- **Status:** OPEN
- **Found by:** Coder (UX bughunt, Jul 23 2026)
- **File:** `lib/screens/browse_screen.dart:820-838`
- **Description:** The `+` add button in grid view is a 10px icon inside a ~14px container with `padding: EdgeInsets.all(2)`. This is well below the 48×48 dp minimum tap target recommended by Material Design. On mobile this is hard to hit reliably.
- **Fix proposal:** Increase the container size and use `IconButton` with `constraints` or a `SizedBox` with `hitTestSize` to expand the tap area without changing visual size.

---

### BUG-027 — Item detail remove/add/favourite buttons lack haptic feedback
- **Severity:** LOW
- **Status:** OPEN
- **Found by:** Coder (UX bughunt, Jul 23 2026)
- **File:** `lib/screens/item_detail_screen.dart:273-324, 393-407`
- **Description:** The trash (remove), plus (add), and heart (favourite) buttons in item detail fire state changes but never call `Haptics`. Settings tiles, theme picker, shrine picker, and MP lobby all use `Haptics.selection()` consistently.
- **Fix proposal:** Add `Haptics.selection()` to the remove and add button `onPressed` handlers. Add `Haptics.light()` for favourite toggle.

---

### BUG-028 — Collapsible sections pop instead of animate height
- **Severity:** LOW
- **Status:** OPEN
- **Found by:** Coder (UI bughunt, Jul 23 2026)
- **Files:** `stats_detail_screen.dart`, `multiplayer_lobby_screen.dart`, `wiki_sections.dart`, `browse_screen.dart`
- **Description:** Collapsible sections use `if (!_collapsed) ...[children]` — content appears/disappears instantly. The chevron animates via `AnimatedRotation` but the content has no height transition. `AnimatedSize` wrapper would fix this with zero controller overhead.
- **Fix proposal:** Wrap collapsible content in `AnimatedSize(duration: 200ms, curve: Curves.easeOutCubic, child: _collapsed ? SizedBox.shrink() : Column(children: [...]))`.

---

### BUG-029 — Quick Add sheet search results limited to 6, no scroll indicator
- **Severity:** LOW
- **Status:** OPEN
- **Found by:** Coder (UX bughunt, Jul 23 2026)
- **File:** `lib/screens/active_run_screen.dart:316`
- **Description:** `combinedResults.take(6)` silently truncates results. If the user searches "gun" they see 6 of ~80+ matches with no indication there are more. No "showing 6 of N" hint, no scroll-to-see-more.
- **Fix proposal:** Either show a count ("6 of N results") or remove the limit and let the `Flexible` + `ListView` handle scrolling.

---

### BUG-030 — `active_run_screen.dart` megafile at 391KB / 9953 lines
- **Severity:** HIGH
- **Status:** FIXED
- **Found by:** Coder (architecture assessment, Jul 23 2026)
- **File:** `lib/screens/active_run_screen.dart`
- **Description:** The file had grown to 391KB/9953 lines with 60+ classes.
- **Fix:** Extracted 60+ classes into 15 widget files under `widgets/active_run/`, `widgets/dashboards/`, `widgets/sheets/`. File reduced to 566 lines.
- **Commit:** 05dc81d

---

### BUG-031 — `item_detail_screen.dart` megafile at 134KB / 3582 lines
- **Severity:** MEDIUM
- **Status:** FIXED
- **Found by:** Coder (architecture assessment, Jul 23 2026)
- **File:** `lib/screens/item_detail_screen.dart`
- **Description:** File had grown to 134KB/3582 lines with 15+ classes.
- **Fix:** Extracted 11 classes into 6 widget files under `widgets/item_detail/`. File reduced to 332 lines.
- **Commit:** 84fd11f

---

### BUG-032 — `catch (_) {}` silently swallows SharedPreferences errors across 30+ sites
- **Severity:** LOW
- **Status:** OPEN
- **Found by:** Coder (UX bughunt, Jul 23 2026)
- **Files:** `run_provider.dart` (20+ sites), `app_theme.dart` (6 sites), `multiplayer_lobby_screen.dart` (4 sites), `active_run_screen.dart` (3 sites)
- **Description:** All persistence operations use `try { ... } catch (_) {}` — silently eating errors. If SharedPreferences fails (e.g. disk full on older Android), the user gets no indication their run state isn't saving. Not a crash bug, but a data-loss UX risk.
- **Fix proposal:** At minimum, log errors with `debugPrint`. For critical saves (run state), show a snackbar on failure.

---

### BUG-033 — Browse filter chips use emoji instead of Material icons
- **Severity:** LOW
- **Status:** OPEN
- **Found by:** Coder (UX bughunt, Jul 23 2026)
- **File:** `lib/screens/browse_screen.dart:432-439`
- **Description:** Filter chips use emoji (🎯, 💥, ❄️, 🥶, 🔥, 🤢, 💫, 🕵️) while every other UI element uses Material `Icon` widgets. Emoji rendering varies by device/OS and breaks visual consistency.
- **Fix proposal:** Replace emoji with appropriate `Icons` constants.

---

### BUG-034 — Favourites heart toggle clears all snackbars
- **Severity:** LOW
- **Status:** OPEN
- **Found by:** Coder (UX bughunt, Jul 23 2026)
- **File:** `lib/screens/item_detail_screen.dart:397`
- **Description:** `ScaffoldMessenger.of(context).clearSnackBars()` before showing the favourite toggled snackbar. If another important snackbar (e.g. synergy activated) was visible, it gets silently dismissed.
- **Fix proposal:** Remove `clearSnackBars()` call — SnackBar manager will queue/replace naturally.

---

### BUG-035 — PeriodicTile gun panel: gun type not below title, RANGE missing from periodic grid
- **Severity:** UX
- **Status:** OPEN
- **Found by:** User testing (Aug 12 2026)
- **Files:** `lib/widgets/periodic_tile.dart` (classicPeriodic branch ~683–806, tacticalStats branch ~570–682), `lib/models/gun.dart`
- **Description:** On the active-run inventory **Periodic grid** (the `classicPeriodic` display mode), gun tiles show the gun **type tag in the top-right corner** (small, ~7.5px, stacked with elemental icons) and only the **DPS** (or corner badge) at the bottom-center. The user wants a rework of the gun tile design so that:
  1. The **gun type** (Pistol / Shotgun / Rifle / Beam / etc.) sits **below the gun title** as a dedicated, centered visual addon-panel — not a tiny corner tag.
  2. The **RANGE** number is shown **alongside the DPS** on the periodic grid (currently only DPS appears in the bottom-center `_corner` badge; RANGE is only visible in the `tacticalStats` 2×3 grid, not in `classicPeriodic`).
  - DPS display is already good and should be kept.
- **Root cause:** `classicPeriodic` layout puts `_typeTag` in a `Positioned(top:3, right:3)` corner (lines 727–765) and the bottom-center `_corner` badge (lines 767–806) only renders DPS (via `_corner` getter, lines 185–192, which returns the DPS value for guns). RANGE is never surfaced in this mode.
- **Fix proposal:** Rework the `classicPeriodic` gun tile: move the type tag from the top-right corner to a centered subtitle row directly beneath the gun name/title area; add a RANGE value next to (or beneath) the DPS in the bottom-center badge so both DPS and RANGE are visible on the periodic grid. Keep the elemental icons in the top-right. Verify the `tacticalStats` mode already shows RANGE (it does, line 657) — no change needed there. Watch tile height in `SliverGrid` `childAspectRatio` so the added row doesn't clip.

---

### BUG-036 — Active run HeaderMenu: no quick "Reset Player Items", Settings not in bottom section
- **Severity:** UX
- **Status:** OPEN
- **Found by:** User testing (Aug 12 2026)
- **Files:** `lib/widgets/active_run/active_run_helpers.dart` (`HeaderMenu` ~182–420), `lib/widgets/settings/run_tab.dart` (has the reset logic, ~274–288)
- **Description:** Two related menu-structure issues on the active-run gear (`HeaderMenu` PopupMenu):
  1. **"Reset Player Items" is only reachable via Settings → Run tab → Inventory Maintenance.** The user wants it available quicker — as a direct item in the active-run gear menu (it already exists as `_confirmClearInventory` in `run_tab.dart` and can be reused).
  2. **Settings is currently at the TOP of the gear menu** (lines 299–306, right after Favourites). The user wants Settings moved to the **final/lower section**, grouped with Leave Multiplayer and End Run (the "End & Leave" block at lines 360+), so the top of the menu prioritizes in-run actions.
- **Root cause:** Menu ordering in `itemBuilder` (lines 289–420) places Favourites/Settings/Codex first, then actions, then save/session, then end/leave. Settings is a "destination" not an "in-run action" and is crowding the top.
- **Fix proposal:**
  - Add a `reset_items` (and `reset_items_p2` when coop active) `PopupMenuItem` in the Actions section, calling the existing `_confirmClearInventory(context, p, PlayerSlot.main)` helper (lift it to a shared location or call `RunProvider` directly — `run_tab.dart` already has the confirm dialog, consider extracting to `active_run_helpers.dart` so both the menu and the Run tab share it).
  - Move the `settings` `PopupMenuItem` down into the final section (after the End/Leave block) so the menu reads: Favourites → Codex → Dice Roll → Save → Reset Items → Leave MP / End Run → Settings. Keep the `onSelected` switch case.

---

### BUG-037 — Remove Multiplayer Summary panel/tab
- **Severity:** UX
- **Status:** OPEN
- **Found by:** User testing (Aug 12 2026)
- **Files:** `lib/widgets/active_run/player_header.dart` (lines 354–391, the `SummaryTab` in the MP header Row), `lib/widgets/active_run/summary_tab.dart` (`SummaryTab` + `MpSummaryPage`), and the page-switcher wiring that maps page index 2 → `MpSummaryPage`
- **Description:** The multiplayer header shows three tabs: P1, P2, and **SUMMARY** (the third tab, `SummaryTab` at `player_header.dart:381–388`, page index 2). The user wants the Summary panel **removed entirely** — "we do not tinker with it for now." It should not be reachable and the tab should not render.
- **Root cause:** Feature is wired into the MP header Row as a third `Expanded(flex:2)` child and the page controller maps index 2 to `MpSummaryPage`.
- **Fix proposal:** Remove the `SummaryTab` `Expanded` from the MP header Row (lines 381–388) so only P1 + P2 remain (each can go back to `flex:1` / equal width). Remove/stop routing page index 2 to `MpSummaryPage` in the active-run page switcher. Leave `summary_tab.dart` on disk for now (do NOT delete the file — per Safety S4, only delete files you created; mark the classes as unused or leave for later re-introduction). Confirm the local-coop `PlayerSwitcher` (non-MP) is unaffected — it already has no Summary tab.

---

### BUG-038 — Unicorn theme: no particle effects + palette selector scrolls + no per-palette particle previews
- **Severity:** HIGH
- **Status:** OPEN
- **Found by:** User testing (Aug 12 2026)
- **Files:** `lib/services/app_theme.dart` (`UnicornPalette` enum ~776, `setUnicornPalette` ~2598, `VisualPrefs.particlePreset` ~2120/2389), `lib/widgets/theme_overlay.dart` (ParticleField uses `prefs.particlePreset` ~147–157), `lib/widgets/particle_engine.dart` (`unicornSparkles` preset ~168–178), `lib/screens/theme_picker_screen.dart` (`_PaletteSelector` ~1090–1195, unicorn palette cards ~256–277)
- **Description:** Multiple intertwined theme issues:
  1. **Unicorn theme shows no particle effects.** The particle field is driven by the *global* `VisualPrefs.particlePreset` (a single user-chosen preset, default `gungeonDust`), NOT by the active theme. Selecting the Unicorn theme does **not** switch the preset to `unicornSparkles`, and `particlesEnabled` defaults to `false` (VisualPrefs ~2208) so unless the user manually enabled particles + picked the unicorn preset, the unicorn theme shows nothing. There is no binding between `AppThemeMode.unicorn` / `UnicornPalette` and `ParticlePreset`.
  2. **Palette selector requires horizontal scrolling.** `_PaletteSelector` (theme_picker_screen.dart ~1107–1115) renders palette cards in a horizontal `ListView.separated` with `SizedBox(height: 64)`. The Unicorn megapack has **6 palettes** (cottonCandy, neon, dreamy, sunset, bubblegum, mulberry) — they don't all fit on screen at once and the user can't see them all without scrolling. User wants all palettes visible on screen without scrolling.
  3. **No per-palette preset particle previews.** User wants each Unicorn palette (especially Bubblegum) to show a **preset particle effect made just for it** in the preview panel, mixed into the theme preview.
- **Root cause:** Particle preset is a flat global pref with no theme coupling; palette selector uses a horizontal scroll list instead of a wrap/grid; no per-palette particle config exists (only one `unicornSparkles` preset for the whole megapack).
- **Fix proposal:**
  - **Particles:** When `AppThemeMode.unicorn` is active, auto-apply a unicorn-appropriate `ParticlePreset` (enable particles + set preset) — either override `ParticleField`'s preset based on theme (read `AppTheme.mode` in `theme_overlay.dart` and map unicorn → `unicornSparkles`), or auto-set `VisualPrefs.particlePreset` when the user picks the unicorn theme. Prefer the overlay-side override so it doesn't clobber the user's global choice when they switch back.
  - **Palette layout:** Replace the horizontal `ListView` in `_PaletteSelector` with a `Wrap` or a 2-row `GridView`/`Row` of `Expanded` cards so all 6 palettes are visible without scrolling. Verify on small screens.
  - **Per-palette particles:** Add a per-`UnicornPalette` particle color/config mapping (e.g. Bubblegum → pink bubble particles, Mulberry → purple) and surface a small live `ParticleField` preview in the theme preview panel for the active palette. Reuse `ParticleField` with a per-palette color override.
  - Assess and fix any other theme whose particles don't show for the same global-preset reason while here.

---

### BUG-039 — S-tier chest/quality colors unreadable (gold pill + white text, dark chest label)
- **Severity:** MEDIUM
- **Status:** OPEN
- **Found by:** User testing (Aug 12 2026)
- **Files:** `lib/widgets/quality_badge.dart` (`colorFor` ~28–46, build ~88–116), `lib/widgets/item_detail/header.dart` (`_ChestChip` ~334–419), `lib/widgets/periodic_tile.dart` (S-tier handling ~471–485)
- **Description:** The S-tier rendering has drifted from its intended design and is hard to read:
  1. **`QualityBadge.colorFor('S')` returns bright gold `0xFFFFD700`** (line 32) — but the class doc (lines 4–5) says the intended design is *"S → black pill, white label, golden glow (animated)"*. The badge paints the **letter white on bright gold** (line 110 `color: Colors.white`), which is low-contrast and hard to read. The user explicitly wants **S tier = black pill, white text**.
  2. **`_ChestChip` for the black/S chest** (`header.dart:338–419`) uses `color = 0xFF222222` (near-black) and renders the "Chest" label in `color.withValues(alpha: 0.85)` (line 393) — i.e. near-black text at 85% alpha on a near-black translucent chip background (`color.withValues(alpha:0.12)`). The label is nearly invisible. The rank letter is white (fine), but the "Chest" word and the icon are dark-on-dark.
  3. **`PeriodicTile` S-tier** (lines 471–485) mirrors the gold drift: `qColor = 0xFFFFD700`, gold border, dark card bg `0xFF14120E`. The gold border is fine, but the quality badge inside inherits the gold-pill problem.
- **Root cause:** Someone changed S from the documented black-pill design to a gold pill (likely to "make it pop"), trading readability for flash. The chest chip then compounds it with dark-on-dark label text.
- **Fix proposal:** Revert S-tier to the documented design across all three sites:
  - `QualityBadge.colorFor('S')` → return near-black (`0xFF1A1A1A` or `0xFF222222`); keep the **white** label text; keep the existing silver/white border (`E0E0E0`, line 104) and the animated golden **glow** (the `_glow` controller at lines 118+) — that gives "black pill, white text, gold glow" as intended.
  - `_ChestChip`: for `isS`, render the "Chest" label and icon in **white** (not `color.withValues(alpha:0.85)`); keep the chip background dark with the white border + white glow (already there). The rank letter is already white.
  - `PeriodicTile`: keep the gold **border/glow** for S but ensure the embedded `QualityBadge` now shows black-pill/white-text (it will inherit the `QualityBadge` fix). Re-evaluate `cardBgColor = 0xFF14120E` — fine to keep.
  - Verify readability on both the inventory grid and the item/gun detail header pill.

---

## Fixed Bugs

*(Fixed bugs are moved here with commit hash and date. Open bugs above with `FIXED` status are awaiting move.)*

---

## Disputed / Wontfix

*(None yet.)*
