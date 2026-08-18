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
- **Status:** FIXED
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
- **Status:** FIXED
- **Found by:** Coder (data bughunt, Jul 23 2026)
- **File:** `assets/data/items.json`
- **Description:** 46 of 67 active items have no `recharge_time` value. Includes common items like Bomb, Box, Decoy, Molotov, Smoke Bomb, Teleporter Prototype. The item detail screen shows recharge time when present — these 46 items just omit it.
- **Fix proposal:** Populate `recharge_time` from wiki data for all active items.
- **Fix:** Extracted floor-1 damage recharge values from cached wiki.gg HTML for all 46 items. 44 use damage-based recharge (e.g., "200 dmg"), Busted Television is "None", Arcane Gunpowder is "Cannot be used" (quest item). All 67 active items now have recharge_time.
- **Commit:** d84690d

---

### BUG-022 — 289 synergies missing local icon assets
- **Severity:** MEDIUM
- **Status:** FIXED
- **Found by:** Coder (data bughunt, Jul 23 2026)
- **File:** `assets/images/synergies/` (106 of 395 webp files present)
- **Description:** Only 106 of 395 synergies have local `.webp` icon files. The remaining 289 show fallback letter icons. The `Synergy.fromJson` constructor uses `localSynergyIcon(name)` to resolve the path — missing files silently fall back.
- **Fix:** Parsed cached `cache_wikigg/Synergies.html` for dedicated sprite URLs — 108 synergies have unique sprites (106 already downloaded + 2 new). The remaining 287 synergies have no dedicated wiki sprite (they use the generic blue synergy arrow). Downloaded `Synergy.png` from wiki.gg and copied it as fallback for all 287 missing entries. Final count: 396 files (108 unique + 287 fallback + 1 fallback source). All synergies now show an icon instead of a letter placeholder.

---

### BUG-023 — 3 guns missing wiki notes content
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (data bughunt, Jul 23 2026)
- **File:** `assets/data/guns.json`
- **Description:** Poxcannon, Serious Cannon, and Silencer have no wiki notes content (empty `notes` array). All other 236 guns have notes.
- **Fix proposal:** Populate from wiki data or accept as "no trivia exists" if the wiki has none.
- **Fix:** Added wiki.notes sections from wiki.gg for all 3 guns. Poxcannon: 3 notes (PAX reference, POISON class, lousy t-shirt meme). Serious Cannon: 2 notes (Serious Sam reference, Kamikaze Attack synergy). Silencer: 3 notes (pillow silencer myth, thread count pun, Alben Smallbore/Dumbledore reference).
- **Commit:** 9eeda49

---

### BUG-024 — 2 items missing wiki content
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (data bughunt, Jul 23 2026)
- **File:** `assets/data/items.json`
- **Description:** "C4 (Item)" and "Ser Junkan 1" have no wiki sections (effects, item_interactions, notes all empty).
- **Fix proposal:** Populate from wiki data or accept if wiki has no content for these entries.
- **Fix:** Added full wiki objects from wiki.gg. C4: effects (60 damage, no secret rooms), item_interactions (Blank Companion's Ring / Ring of Triggers), 3 notes. Ser Junkan 1: 2 effects (form changes, de-leveling), 5 notes (shop, Ammonomicon, blanks, win screen, Ser Duncan reference).
- **Commit:** 9eeda49

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
- **Status:** FIXED (v1.9.0, commit `d9d6486`)
- **Found by:** Coder (UX bughunt, Jul 23 2026)
- **File:** `lib/screens/browse_screen.dart:820-838`
- **Description:** The `+` add button in grid view is a 10px icon inside a ~14px container with `padding: EdgeInsets.all(2)`. This is well below the 48×48 dp minimum tap target recommended by Material Design. On mobile this is hard to hit reliably.
- **Fix proposal:** Increase the container size and use `IconButton` with `constraints` or a `SizedBox` with `hitTestSize` to expand the tap area without changing visual size.

---

### BUG-027 — Item detail remove/add/favourite buttons lack haptic feedback
- **Severity:** LOW
- **Status:** FIXED (v1.9.0, commit `d9d6486`)
- **Found by:** Coder (UX bughunt, Jul 23 2026)
- **File:** `lib/screens/item_detail_screen.dart:273-324, 393-407`
- **Description:** The trash (remove), plus (add), and heart (favourite) buttons in item detail fire state changes but never call `Haptics`. Settings tiles, theme picker, shrine picker, and MP lobby all use `Haptics.selection()` consistently.
- **Fix proposal:** Add `Haptics.selection()` to the remove and add button `onPressed` handlers. Add `Haptics.light()` for favourite toggle.

---

### BUG-028 — Collapsible sections pop instead of animate height
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (UI bughunt, Jul 23 2026)
- **Files:** `compact_dashboards.dart` (12), `special_gun_dashboards.dart` (3), `junkan_dashboard.dart` (1), `robot_dashboard.dart` (1), `stats_detail_screen.dart` (1)
- **Description:** Collapsible sections use `if (!_collapsed) ...[children]` — content appears/disappears instantly. The chevron animates via `AnimatedRotation` but the content has no height transition. `AnimatedSize` wrapper would fix this with zero controller overhead.
- **Fix proposal:** Wrap collapsible content in `AnimatedSize(duration: 200ms, curve: Curves.easeOutCubic, child: _collapsed ? SizedBox.shrink() : Column(children: [...]))`.
- **Fix:** Wrapped all 18 collapsible sections in AnimatedSize with 200ms easeOutCubic. Content now smoothly expands/collapses instead of popping.
- **Commit:** 9eeda49

---

### BUG-029 — Quick Add sheet search results limited to 6, no scroll indicator
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (UX bughunt, Jul 23 2026)
- **File:** `lib/screens/active_run_screen.dart:461`
- **Description:** `combinedResults.take(6)` silently truncates results. If the user searches "gun" they see 6 of ~80+ matches with no indication there are more. No "showing 6 of N" hint, no scroll-to-see-more.
- **Fix proposal:** Either show a count ("6 of N results") or remove the limit and let the `Flexible` + `ListView` handle scrolling.
- **Fix:** Removed .take(6) — all results now show in a scrollable ListView. Added "N results — scroll to see more" hint when results exceed 6.
- **Commit:** 9eeda49

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
- **Status:** FIXED
- **Found by:** Coder (UX bughunt, Jul 23 2026)
- **Files:** `run_provider.dart` (24 sites), `app_theme.dart` (7 sites), `multiplayer_lobby_screen.dart` (5 sites), `run_tab.dart` (1), `item_detail_screen.dart` (1), `app_tab.dart` (1), `codex_detail_screen.dart` (1), `mp_request_listener.dart` (2)
- **Description:** All persistence operations use `try { ... } catch (_) {}` — silently eating errors. If SharedPreferences fails (e.g. disk full on older Android), the user gets no indication their run state isn't saving. Not a crash bug, but a data-loss UX risk.
- **Fix:** Replaced all 42 `catch (_) {}` with `catch (e) { debugPrint('[Tag] error: $e'); }` across 8 files. Each catch now logs the error with a file-specific tag. `debugPrint` is available via material.dart/foundation.dart — no new imports needed. flutter analyze: 0 issues on all 17 modified files.

---

### BUG-033 — Browse filter chips use emoji instead of Material icons
- **Severity:** LOW
- **Status:** DISPUTED — No emoji filter chips found in current `browse_screen.dart`. The browse screen uses a `TabBar` with text labels (All, Guns, Items, Favourites), not filter chips. The emoji chips were likely removed during a prior refactor. Closing as wontfix.

---

### BUG-034 — Favourites heart toggle clears all snackbars
- **Severity:** LOW
- **Status:** FIXED (v1.9.0, commit `d9d6486`)
- **Found by:** Coder (UX bughunt, Jul 23 2026)
- **File:** `lib/screens/item_detail_screen.dart:397`
- **Description:** `ScaffoldMessenger.of(context).clearSnackBars()` before showing the favourite toggled snackbar. If another important snackbar (e.g. synergy activated) was visible, it gets silently dismissed.
- **Fix proposal:** Remove `clearSnackBars()` call — SnackBar manager will queue/replace naturally.

---

### BUG-035 — PeriodicTile gun panel: gun type not below title, RANGE missing from periodic grid
- **Severity:** UX
- **Status:** FIXED (v1.9.0, commit `d9d6486`)
- **Found by:** User testing (Aug 12 2026)
- **Files:** `lib/widgets/periodic_tile.dart` (classicPeriodic branch 683–806, tacticalStats branch 570–682, `_corner` getter 185–219, `_typeTag` getter 224–267), `lib/widgets/active_run/player_page.dart` (`_tileGrid` 831–856, `childAspectRatio: 0.80` for classicPeriodic), `lib/models/gun.dart` (`range` field 18/47/128/155, `dpsValue` getter 59)
- **Description:** On the active-run inventory **Periodic grid** (the `classicPeriodic` display mode), gun tiles show the gun **type tag in the top-right corner** (small, ~7.5px, stacked with elemental icons at `Positioned(top:3, right:3)` lines 727–765) and only the **DPS** (or corner badge) at the bottom-center (lines 767–806). The user wants a rework of the gun tile design so that:
  1. The **gun type** (Pistol / Shotgun / Rifle / Beam / etc.) sits **below the gun title** as a dedicated, centered visual addon-panel — not a tiny corner tag.
  2. The **RANGE** number is shown **alongside the DPS** on the periodic grid (currently only DPS appears in the bottom-center `_corner` badge; RANGE is only visible in the `tacticalStats` 2×3 grid at line 657, not in `classicPeriodic`).
  - DPS display is already good and should be kept.
- **Root cause:**
  - `classicPeriodic` layout puts `_typeTag` in a `Positioned(top:3, right:3)` corner (lines 727–765) — there is no "title" row in this mode at all; the icon fills the card and the type is a corner overlay.
  - The bottom-center `_corner` badge (lines 767–806) only renders the `_corner` getter value (lines 185–192), which for guns returns only the DPS string/number. `gun.range` (a String field, `gun.dart:18`) is never read in `classicPeriodic` mode.
  - The `tacticalStats` mode (lines 570–682) already shows RANGE in its 2×3 `_StatGrid` (line 657) — that mode is fine, no change needed.
- **Fix proposal:**
  - **Type addon-panel:** In the `classicPeriodic` branch, for guns only, add a centered subtitle row beneath the icon area showing `_typeTag` (reuse the existing getter at lines 224–267) in a small pill/label, centered (`Center` widget). Remove the `_typeTag` `Positioned` corner overlay for guns (keep it for items, OR move items to the same subtitle pattern for consistency — prefer consistency). Keep elemental icons in the top-right corner regardless.
  - **RANGE alongside DPS:** Extend the bottom-center badge (lines 767–806) so guns show both DPS and RANGE. Two layout options:
    - (a) Side-by-side: `Row(mainAxisAlignment: center, children: [DPS badge, SizedBox(width:6), RANGE badge])` — compact, fits the existing bottom strip.
    - (b) Stacked: `Column` with DPS on top (bigger, the "hero" number) and RANGE beneath (smaller, secondary).
    - Prefer (a) side-by-side to preserve the current tile height. Use `_cleanStat(widget.gun!.range)` (the helper at lines 304–321 already truncates to 7 chars) for the RANGE value.
  - **Tile aspect ratio:** `childAspectRatio: 0.80` for classicPeriodic (`player_page.dart:842`). Adding a subtitle row eats vertical space — verify the gun tile doesn't clip at 4 columns on a 360px screen (tile width ≈ (360−12−12−3×8)/4 ≈ 78px, tile height ≈ 78/0.80 ≈ 97px). If the subtitle + bottom badge overflow, bump ratio to `0.72`–`0.75` for guns only (gates on `displayMode == classicPeriodic && isGun`), or use `SliverGridDelegateWithMaxCrossAxisExtent` instead. Test with a 6-gun loadout.
  - **Items:** Decide whether items get the same subtitle-row treatment. The `_typeTag` for items returns Active/Passive/Companion (lines 261–266) — surfacing it as a subtitle is a nice consistency win but optional. If skipping, keep the item corner tag as-is.
- **Edge cases:**
  - Gun with empty `range` (some entries): badge should hide, not render "0" or empty space. Guard with `if (rangeClean.isNotEmpty)`.
  - Gun with empty `dps`: `_corner` already returns `''` (line 188) and the badge renders `SizedBox.shrink()` (line 806) — preserve this; if DPS is empty, show RANGE alone.
  - `isTopDps` gun (lines 642–643, 798–803): the DPS badge gets a gold shimmer animation. Keep that on the DPS badge; the RANGE badge stays plain.
  - Synergy glow overlay (`_buildBody` 454–464) wraps the whole card — unaffected by internal layout changes.
- **Verification:**
  - `flutter analyze` on `periodic_tile.dart` and `player_page.dart`.
  - Visual: load a 6-gun run, switch to Periodic Grid mode, confirm type subtitle is centered under the icon, DPS + RANGE both visible bottom-center, no clipping at 4-col on 360px width.
  - Confirm `tacticalStats` mode is unchanged (still shows the 2×3 grid with RANGE).
  - Confirm items still render correctly (no regression if you only changed the gun path).

---

### BUG-036 — Active run HeaderMenu: no quick "Reset Player Items", Settings not in bottom section
- **Severity:** UX
- **Status:** FIXED (v1.9.0, commit `d9d6486`)
- **Found by:** User testing (Aug 12 2026)
- **Files:** `lib/widgets/active_run/active_run_helpers.dart` (`HeaderMenu` class 182–480, `itemBuilder` 289–390, `onSelected` switch 207–287), `lib/widgets/settings/run_tab.dart` (`_confirmClearInventory` 69–103, `RunTabState` 21–368)
- **Description:** Two related menu-structure issues on the active-run gear (`HeaderMenu` PopupMenu):
  1. **"Reset Player Items" is only reachable via Settings → Run tab → Inventory Maintenance** (`run_tab.dart:274–288`, calling `_confirmClearInventory` at 69–103). The user wants it available quicker — as a direct item in the active-run gear menu.
  2. **Settings is currently at the TOP of the gear menu** (`active_run_helpers.dart:299–306`, right after Favourites). The user wants Settings moved to the **final/lower section**, grouped with Leave Multiplayer and End Run (the "End & Leave" block at 360–388), so the top of the menu prioritizes in-run actions.
- **Root cause:** Menu ordering in `itemBuilder` (289–390) is: Favourites → Settings → Codex → divider → Dice Roll → divider → Save (MP or solo) → divider → Leave MP / End Run. Settings is a "destination" not an "in-run action" and is crowding the top. The reset-inventory action is not in the menu at all — it only lives in the Run tab.
- **Fix proposal:**
  - **Lift the confirm dialog to a shared location.** `_confirmClearInventory(BuildContext, RunProvider, PlayerSlot)` is currently a private method on `RunTabState` (`run_tab.dart:69–103`). Extract it to a top-level function in `active_run_helpers.dart` (e.g. `void confirmClearInventoryDialog(BuildContext, RunProvider, PlayerSlot)`) and have `RunTabState._confirmClearInventory` call it, so both the menu and the Run tab share one implementation. This avoids duplicating the dialog.
  - **Add reset items to the menu.** In the Actions section (after Dice Roll, before Save), add:
    - `reset_items_p1` — always visible, calls `confirmClearInventoryDialog(context, p, PlayerSlot.main)`.
    - `reset_items_p2` — visible only when `p.runState.hasCoop` (mirror the Run tab's conditional at 281–288), calls `confirmClearInventoryDialog(context, p, PlayerSlot.coop)`.
    - Use `Icons.restart_alt_rounded` (matches Run tab) and `Colors.cyanAccent` for P1 / `Colors.pinkAccent` for P2 (matches Run tab colors).
  - **Move Settings to the bottom.** Remove the `settings` `PopupMenuItem` from the top block (299–306) and add it as the **last** item, after the End/Leave block (after line 388), with a `PopupMenuDivider()` before it. Keep the `onSelected` switch case `'settings'` (215–220) unchanged.
  - **New menu order:** Favourites → Codex → divider → Dice Roll → divider → Reset P1 Items (+ Reset P2 Items if coop) → divider → Save (MP/solo) → divider → Leave MP / End Run → divider → Settings.
- **Edge cases:**
  - MP sidekick role: the End/Leave block (361–388) already branches on `mpActive && myRole == sidekick` vs else. The reset items items should be visible to both roles (a sidekick can reset their own inventory). Keep them outside the role-gated block.
  - `p.runState.hasCoop` is the correct gate for P2 reset (matches `run_tab.dart:281`). Don't gate on `mpActive` — local coop also has a P2.
  - The dialog uses `p.clearInventory(slot: slot)` (`run_tab.dart:91`) — confirm this method exists on `RunProvider` and is safe to call from the menu context (it is — the Run tab already calls it).
- **Verification:**
  - `flutter analyze` on `active_run_helpers.dart` and `run_tab.dart`.
  - Open the gear menu on a solo run: confirm Reset P1 Items is present, Settings is last.
  - Add a coop player: confirm Reset P2 Items appears.
  - Start an MP session as sidekick: confirm reset items still visible, Leave MP + End & Disconnect present, Settings last.
  - Tap Reset P1 Items: confirm the confirm dialog appears and clearing works (inventory resets to starter loadout).
  - Tap Settings: confirm it still navigates to `SettingsScreen`.

---

### BUG-037 — Remove Multiplayer Summary panel/tab
- **Severity:** UX
- **Status:** FIXED (v1.9.0, commit `d9d6486`)
- **Found by:** User testing (Aug 12 2026)
- **Files:** `lib/widgets/active_run/player_header.dart` (MP header Row 354–391, `SummaryTab` `Expanded` 381–388), `lib/screens/active_run_screen.dart` (PageView children 262–283, `MpSummaryPage()` at 281), `lib/widgets/active_run/summary_tab.dart` (`SummaryTab` class 17–79, `MpSummaryPage` class 84–663, `MpSummaryPageState` 91+)
- **Description:** The multiplayer header shows three tabs: P1, P2, and **SUMMARY** (the third tab, `SummaryTab` at `player_header.dart:381–388`, page index 2). The user wants the Summary panel **removed entirely** — "we do not tinker with it for now." It should not be reachable and the tab should not render.
- **Root cause:** The feature is wired in two places:
  1. **Tab UI:** `player_header.dart:381–388` — a third `Expanded(flex: 2, child: SummaryTab(active: currentPage == 2, onTap: () => onPick(2)))` in the MP header Row (inside the `if (hasCoop)` block at 354).
  2. **Page routing:** `active_run_screen.dart:281` — `if (isMpActive && hasCoop) const MpSummaryPage()` as the third child of the `PageView` (controller `_page`, 262–283). Page index 2 maps to it.
- **Fix proposal:**
  - **Remove the tab:** Delete the `SizedBox(width: 8)` (381) + `Expanded(flex: 2, child: SummaryTab(...))` (382–388) from `player_header.dart`. The two remaining `BigPlayerTab` `Expanded(flex: 2)` children (358–380) become the only tabs — they'll naturally take equal width. Optionally change their `flex` from 2 to 1 (cosmetic; 2:2 is already equal).
  - **Remove the page:** Delete `if (isMpActive && hasCoop) const MpSummaryPage(),` (281) from `active_run_screen.dart`. The `PageView` now has at most 2 children (P1, P2 if coop).
  - **Clamp the page index:** The `onPick` callback and any `currentPage` state in `active_run_screen.dart` that could be set to 2 must be clamped to 0–1. Search for `onPick: (i) =>` and any `_page.jumpToPage(2)` / `animateToPage(2)` calls — if the user was on page 2 when the build runs, the PageView with only 2 children will throw. Add a guard: `if (currentPage > 1) currentPage = 0` on rebuild, or clamp in the `onPick` handler.
  - **Leave `summary_tab.dart` on disk.** Per Safety S4, do NOT delete files you didn't create. The `SummaryTab` and `MpSummaryPage` classes become unreferenced. Mark them with a `// TODO(BUG-037): re-evaluate Summary panel` comment at the top of each class so a future session knows they're dormant, not forgotten. `flutter analyze` will flag them as unused — that's expected and acceptable (or add `// ignore: unused_element` if the linter complains).
  - **Remove the `summary_tab.dart` import** from `player_header.dart` (line 8: `import 'summary_tab.dart';`) and from `active_run_screen.dart` (search for the import) — unused imports are an analyze warning.
- **Edge cases:**
  - **Stale page index:** If a user was on the Summary page (index 2) and the code is updated, the persisted `_selectedIndex` / `currentPage` could still be 2 on first rebuild. The clamp guard above handles this.
  - **Local coop (non-MP):** The `PlayerSwitcher` (player_header.dart 13–55) already has no Summary tab — only the `MpHeader` (179+) had it. No change needed for local coop.
  - **`MpSummaryPageState` is public** (line 88, `createState() => MpSummaryPageState()`). Grep for any external references to `MpSummaryPageState` before removing the page — if something else references it, leave the class but remove the routing.
- **Verification:**
  - `flutter analyze` on `player_header.dart` and `active_run_screen.dart` — confirm no unused import warnings remain (after removing the imports).
  - Start an MP session with coop: confirm the header shows only P1 + P2 tabs, swiping the PageView only cycles between P1 and P2, no Summary page is reachable.
  - Start a local coop (non-MP) run: confirm the `PlayerSwitcher` is unchanged (P1 + P2 only).
  - Grep: `grep -r "MpSummaryPage\|SummaryTab" lib/` should return only the definitions in `summary_tab.dart` (dormant) — no active references.

---

### BUG-038 — Unicorn theme: no particle effects + palette selector scrolls + no per-palette particle previews
- **Severity:** HIGH
- **Status:** FIXED (v1.9.0, commit `d9d6486`)
- **Found by:** User testing (Aug 12 2026)
- **Files:**
  - `lib/services/app_theme.dart` — `UnicornPalette` enum (776–849, 6 values: cottonCandy/neon/dreamy/sunset/bubblegum/mulberry), `setUnicornPalette` (2598–2606), `AppTheme.mode` getter, `VisualPrefs` (2100–2560: `particlesEnabled` default false at 2208, `particlePreset` default `gungeonDust` at 2209, `setParticlePreset` at 2389–2392)
  - `lib/widgets/theme_overlay.dart` — `ParticleField` instantiation (147–157, reads `prefs.particlePreset` / `prefs.particlesEnabled`)
  - `lib/widgets/particle_engine.dart` — `ParticlePreset` enum (16–66), `unicornSparkles` config (168–178), `PresetConfig` class (299–310, has `colors`/`shape`/`glowEffect`/`lineLinks`), `ParticleField` widget (352–540, has `glowOverride` + `lineLinksOverride` params but **NO `colorsOverride`** — this is a blocker for per-palette particles)
  - `lib/screens/theme_picker_screen.dart` — `_PaletteSelector` (1090–1195, horizontal `ListView.separated` height 64), unicorn palette cards (256–277), `_DashboardPreview` (225)
- **Description:** Three intertwined theme issues, all centered on the Unicorn megapack:
  1. **Unicorn theme shows no particle effects.** The particle field is driven by the *global* `VisualPrefs.particlePreset` (a single user-chosen preset, default `gungeonDust` at 2209), NOT by the active theme. Selecting the Unicorn theme does **not** switch the preset to `unicornSparkles`, and `particlesEnabled` defaults to `false` (2208) — so unless the user manually enabled particles AND picked the unicorn preset in Settings → Theme Visuals, the unicorn theme shows nothing. There is **no binding** between `AppThemeMode.unicorn` / `UnicornPalette` and `ParticlePreset`.
  2. **Palette selector requires horizontal scrolling.** `_PaletteSelector` (1090–1195) renders palette cards in a horizontal `ListView.separated` inside a `SizedBox(height: 64)`. The Unicorn megapack has **6 palettes** — each card is ~110–140px wide (3 color swatches × 16px + label + padding), so 6 cards ≈ 750–840px, wider than most phone screens. The user can't see all palettes without scrolling. User wants all palettes visible on screen without scrolling.
  3. **No per-palette preset particle previews.** User wants each Unicorn palette (especially Bubblegum) to show a **preset particle effect made just for it** in the preview panel, mixed into the theme preview. Currently there's only one `unicornSparkles` preset (168–178) for the whole megapack — no per-palette particle config exists.
- **Root cause:**
  - Particle preset is a flat global pref with no theme coupling. `theme_overlay.dart:150` reads `prefs.particlePreset` directly — it never consults `AppTheme.mode`.
  - Palette selector uses a horizontal scroll list (`ListView.separated` with `scrollDirection: Axis.horizontal`) instead of a wrap/grid.
  - `ParticleField` has no `colorsOverride` param (only `glowOverride` + `lineLinksOverride`, 357–358) — so even if you wanted per-palette colors, you can't override them without adding a param or a new preset per palette.
- **Fix proposal:**
  - **(1) Auto-bind particles to theme — overlay-side override (preferred, non-destructive).** In `theme_overlay.dart` around line 147, compute the effective preset based on theme:
    ```dart
    final isUnicorn = AppTheme.mode == AppThemeMode.unicorn;
    final effectivePreset = isUnicorn && prefs.particlePreset != ParticlePreset.unicornSparkles
        ? ParticlePreset.unicornSparkles
        : prefs.particlePreset;
    final particlesOn = prefs.particlesEnabled || isUnicorn; // force on for unicorn
    ```
    Then use `effectivePreset` in the `ParticleField` at 150. This way the user's global preset is untouched when they switch back to another theme. If you want the user to be able to disable unicorn particles, keep `particlesEnabled` as an opt-out: `particlesOn = isUnicorn ? prefs.particlesEnabled || true : prefs.particlesEnabled` — but consider just forcing on for unicorn and letting them turn it off globally.
    - Alternative (destructive): auto-set `VisualPrefs.setParticlePreset(unicornSparkles)` + `setParticlesEnabled(true)` when the user picks the unicorn theme in `setMode`/`setUnicornPalette`. This clobbers their global choice — only do this if you add a "reset particles on theme switch" opt-in. Prefer the overlay-side override.
  - **(2) Palette selector — no-scroll layout.** Replace the `SizedBox(height: 64) + ListView.separated` (1107–1191) with a `Wrap` or a 2-row `GridView`:
    - Option A (Wrap): `Wrap(spacing: 8, runSpacing: 8, children: items.map((item) => card).toList())` — cards size to content, wrap to next line. 6 cards in 2 rows on most screens.
    - Option B (Grid): `GridView.count(crossAxisCount: 3, shrinkWrap: true, physics: NeverScrollableScrollPhysics(), childAspectRatio: 2.2, children: ...)` — 3×2 grid, all visible.
    - Prefer Option A (Wrap) — simpler, no aspect-ratio tuning. Keep the existing card design (1120–1187) intact, just change the parent from `ListView` to `Wrap`.
    - Verify on a 360px screen: 6 cards in 2 rows of 3, no clipping.
  - **(3) Per-palette particle previews.** Two sub-parts:
    - **(3a) Add per-palette particle config.** Add a `ParticlePreset` getter or a `PresetConfig` getter on `UnicornPalette`:
      ```dart
      PresetConfig get particleConfig => switch (this) {
        cottonCandy => ParticlePreset.unicornSparkles.config, // default pink/purple/cyan
        bubblegum => PresetConfig(colors: [Color(0xFFFF80AB), Color(0xFFE040FB), Color(0xFFB388FF)], shape: ParticleShape.circle, /* ... bubble-like */),
        mulberry => PresetConfig(colors: [Color(0xFFC2185B), Color(0xFF9C27B0), Color(0xFFF06292)], /* ... */),
        neon => /* ... */, dreamy => /* ... */, sunset => /* ... */,
      };
      ```
      Use the palette's `flair` colors (793–848) as the particle colors for visual coherence.
    - **(3b) Add `colorsOverride` to `ParticleField`.** The widget (352–540) passes `widget.preset.config` to the painter (533). Add a `final List<Color>? colorsOverride;` param and use `colorsOverride ?? widget.preset.config.colors` in the painter config. Then in `theme_overlay.dart`, pass `colorsOverride: isUnicorn ? AppTheme.unicornPalette.particleConfig.colors : null` to the `ParticleField`.
    - **(3c) Preview panel.** In the theme picker's unicorn page (`_buildPage`, 170+), add a small live `ParticleField` (height ~80–100px) inside the `_DashboardPreview` or as a separate preview strip, using the active palette's particle config. This shows the user what the particles will look like before they apply.
  - **(4) Assess other themes.** While here, check if other themes (Forge Master, Frost, etc.) have the same "no particles because preset is global" issue. If so, apply the same overlay-side override pattern: map each `AppThemeMode` to a sensible default `ParticlePreset` when the user hasn't explicitly chosen one. Consider a `kThemeParticleDefaults` map: `{AppThemeMode.unicorn: ParticlePreset.unicornSparkles, AppThemeMode.forgeMaster: ParticlePreset.forgeEmbers, ...}`.
- **Edge cases:**
  - User explicitly disabled particles (`particlesEnabled: false`) but selects unicorn — should unicorn force them on? Recommend: yes, but show a one-time hint "Particles enabled for Unicorn theme. Disable in Settings." Or respect their choice and stay off. Pick one and document with a `ponytail:` comment.
  - User manually picked a different preset (e.g. `cosmicDust`) while on unicorn — the overlay override should respect their explicit choice (only auto-apply if they're still on the default `gungeonDust`). The code sketch above handles this.
  - `ParticleField` with `colorsOverride` — ensure the painter (around line 533) actually uses the overridden colors, not the preset's. Trace `config.colors` usage in the painter.
  - Palette `Wrap` on very narrow screens (320px) — 6 cards might wrap to 3 rows. Acceptable (still no scroll). Test.
  - Per-palette `PresetConfig` — don't add 6 new `ParticlePreset` enum values (that bloats the enum + persistence). Use a getter on `UnicornPalette` returning a `PresetConfig` directly, and pass colors via `colorsOverride`. Keep the enum stable.
- **Verification:**
  - `flutter analyze` on all 4 files.
  - Select Unicorn theme: confirm particles appear immediately (no manual Settings toggle needed).
  - Open theme picker → Unicorn page: confirm all 6 palette cards visible without scrolling.
  - Switch between palettes (cottonCandy → bubblegum → mulberry): confirm the particle colors in the preview change to match the palette.
  - Switch back to a non-unicorn theme: confirm the user's previously-chosen global preset is restored (not stuck on unicornSparkles).
  - Disable particles globally in Settings: confirm behavior is sensible (either unicorn overrides it with a hint, or respects the disable — per your decision above).
  - Test on 360px and 320px screen widths.

---

### BUG-039 — S-tier chest/quality colors unreadable (gold pill + white text, dark chest label)
- **Severity:** MEDIUM
- **Status:** FIXED (v1.9.0, commit `d9d6486`)
- **Found by:** User testing (Aug 12 2026)
- **Files:**
  - `lib/widgets/quality_badge.dart` — class doc (4–5: intended "S → black pill, white label, golden glow"), `colorFor` (28–46, returns gold `0xFFFFD700` for S at line 32), `_isS` (22–25), build (88–140: badge Container 96–116, white text at 110, silver border at 104, animated glow 118–139 — glow is currently **white/silver**, not gold)
  - `lib/widgets/item_detail/header.dart` — `_ChestChip` (334–419: `_colors` map 338–345 with `'black': Color(0xFF222222)`, `_ranks` map 347–354 with `'black': 'S'`, build 357–419, `isS = key == 'black'` at 362, label color at 393 `color.withValues(alpha: 0.85)`, icon color at 386 `color`, rank letter white at 412)
  - `lib/widgets/periodic_tile.dart` — S-tier handling (471–485: `isS` at 471, `qColor = 0xFFFFD700` at 472, gold border at 479, border width 1.9 at 481, `cardBgColor = 0xFF14120E` at 485), `QualityBadge` usage via `maybeQualityBadge` (507–510)
- **Description:** The S-tier rendering has drifted from its intended design and is hard to read in three places:
  1. **`QualityBadge.colorFor('S')` returns bright gold `0xFFFFD700`** (line 32) — but the class doc (lines 4–5) says the intended design is *"S → black pill, white label, golden glow (animated)"*. The badge paints the **letter white on bright gold** (line 110 `color: Colors.white`), which is low-contrast (white on bright gold ≈ 1.7:1 ratio, below WCAG 4.5:1). The user explicitly wants **S tier = black pill, white text**.
  2. **`_ChestChip` for the black/S chest** (`header.dart:338–419`) uses `color = 0xFF222222` (near-black, line 342) and renders the "Chest" label in `color.withValues(alpha: 0.85)` (line 393) — i.e. **near-black text at 85% alpha on a near-black translucent chip background** (`color.withValues(alpha: 0.12)` at line 367). The label is nearly invisible. The icon (line 386) is also `color` (near-black). The rank letter is white (line 412, fine). The "Chest" word and the icon are dark-on-dark.
  3. **`PeriodicTile` S-tier** (lines 471–485) mirrors the gold drift: `qColor = 0xFFFFD700` (472), gold border (479), dark card bg `0xFF14120E` (485). The gold border is fine, but the embedded `QualityBadge` (via `maybeQualityBadge` 507–510) inherits the gold-pill problem from issue 1.
- **Root cause:** Someone changed S from the documented black-pill design to a gold pill (likely to "make it pop"), trading readability for flash. The animated glow at lines 118–139 is currently **white/silver** (`Color(0xFFFFFFFF).withValues(alpha: 0.3 + 0.4 * t)` at line 129), not gold — so even the "golden glow" from the doc isn't actually gold. The chest chip then compounds the readability problem with dark-on-dark label text.
- **Fix proposal:** Revert S-tier to the documented "black pill, white text, golden glow" design across all three sites:
  - **`QualityBadge`:**
    - `colorFor('S')` / `colorFor('1S')` (line 32) → return near-black `Color(0xFF1A1A1A)` (darker than the chest's `0xFF222222` so the badge reads as distinct from the chip).
    - Keep the **white** label text (line 110, already white — no change).
    - Keep the silver/white border (`Color(0xFFE0E0E0)` at line 104, 1.6px — no change).
    - **Change the glow to gold** (lines 129–132): replace `Color(0xFFFFFFFF).withValues(alpha: 0.3 + 0.4 * t)` with `Color(0xFFFFD700).withValues(alpha: 0.25 + 0.45 * t)` — this gives the documented "golden glow" and makes the black pill read as premium against any background.
  - **`_ChestChip`:**
    - For `isS` (line 362), render the "Chest" label (line 393) and icon (line 386) in **white** instead of `color.withValues(alpha: 0.85)`. Add a branch: `color: isS ? Colors.white : color.withValues(alpha: 0.85)` for the label, and `color: isS ? Colors.white70 : color` for the icon (icon slightly dimmed so the label is the primary read).
    - Keep the chip background dark (`color.withValues(alpha: 0.12)` at 367 — for S this is `0xFF222222` at 12%, which is a subtle dark tint, fine).
    - Keep the white border + white glow (370–381, already there for `isS`).
    - The rank letter is already white (412) — no change.
  - **`PeriodicTile`:**
    - Keep the gold **border** for S (line 479, `0xFFFFD700`, 1.9px — this is the "golden glow" framing and reads well).
    - The embedded `QualityBadge` (via `maybeQualityBadge` 507–510) will now show black-pill/white-text automatically once `QualityBadge.colorFor` is fixed — no change needed here.
    - `cardBgColor = 0xFF14120E` (485) — fine to keep (dark warm bg makes the gold border pop).
    - The `qColor` variable at 472 (`0xFFFFD700`) is only used for the border/shadow, not the badge — keep it.
- **Edge cases:**
  - `1S` data artifact (BUG-020): `_isS` (22–25) already handles `'1S'` → true, and `_displayLetter` (16–20) maps `'1S'` → `'S'`. The `colorFor` fix must keep both `'S'` and `'1S'` cases (30–32) returning the new near-black. No change to the case structure, just the returned color.
  - Contrast check: white text (`Colors.white`) on `0xFF1A1A1A` bg ≈ 17:1 ratio — excellent. White text on `0xFF222222` (chest chip bg tint) — the chip bg is `0xFF222222` at 12% alpha over the screen bg, so effective bg is lighter; the white label will still read fine.
  - The glow is animated (1.8s repeat, line 62). Gold glow on a black pill against a dark Gungeon bg — verify it doesn't look "yellow jaundiced" at low alpha. Tune the alpha floor (0.25) if it looks off.
  - `QualityBadge` is used in: `periodic_tile.dart` (507–510), `item_detail/header.dart` (101), browse screen, and possibly others. The color fix is centralized in `colorFor` so all call sites benefit. Grep `QualityBadge(` to confirm no call site hardcodes a gold override.
- **Verification:**
  - `flutter analyze` on `quality_badge.dart`, `item_detail/header.dart`, `periodic_tile.dart`.
  - Visual: open an S-tier gun (e.g. a black-chest gun) in the item detail screen — confirm the quality badge is a **black pill with white "S" and a gold pulsing glow**, and the chest chip shows "Chest ⬤ S" with the "Chest" label clearly readable in white.
  - Open the active run inventory (Periodic Grid) with an S-tier gun — confirm the tile has a gold border, dark bg, and the corner quality badge is black-pill/white-text (not gold).
  - Confirm A/B/C/D/N tiers are unchanged (they don't use `isS` path).
  - Confirm the glow animation still pulses (1.8s) and is now gold, not white.

---

### BUG-040 — Periodic grid gun badge: no "DMG" / "RANGE" text labels on the numeric values
- **Severity:** UX
- **Status:** FIXED (v1.9.0)
- **Found by:** User testing (Aug 12 2026)
- **Files:**
  - `lib/widgets/periodic_tile.dart` — `_buildGunStatsBadge` (lines 323–390), dpsBadge (330–361), rangeBadge (363–380), Row layout (382–389)
- **Description:** On the active-run inventory **Periodic grid** (`classicPeriodic` display mode), the bottom-center gun stats badge shows the DPS and RANGE values as **bare numbers with no unit labels**. The user sees e.g. "56.0" and "1000" but has to infer which is damage and which is range. The user wants explicit labels like **"56.0 DMG"** and **"1000 RANGE"** so the values are immediately understandable.
- **Current behavior:**
  - dpsBadge (lines 330–361): renders only the numeric value from `_corner` getter (185–219). Font 12.5px, weight 900, gold if top DPS else white, on semi-transparent black bg. No "DMG" label.
  - rangeBadge (lines 363–380): renders only the cleaned range string from `_cleanStat(widget.gun!.range)` (304–321). Font 10px, weight 700, `Colors.white70`, on semi-transparent black bg. No "RANGE" label.
  - Layout: side-by-side `Row` with 4px gap (line 386). Grid `childAspectRatio: 0.75` (player_page.dart line 841).
- **Fix proposal:** Add small unit labels inline with the numeric values:
  - **dpsBadge:** append `" DMG"` after the numeric value (or render the label as a smaller suffix within the same badge). Keep the number as the primary visual element (larger/bolder), label as a smaller suffix. Example: `56.0 DMG` where "56.0" is the existing 12.5px gold/white and "DMG" is ~8px, weight 700, slightly dimmed (white60).
  - **rangeBadge:** append `" RANGE"` after the cleaned range value. Example: `1000 RANGE` where "1000" is the existing 10px white70 and "RANGE" is ~7px, weight 700, white54.
  - The badges are already in a horizontal Row with 4px gap — the labels fit inline without changing the Row layout or the grid aspect ratio.
  - Keep the gold shimmer animation on top-DPS badges (354–359) — it animates the whole badge, label included.
- **Edge cases:**
  - Guns with empty `dps` or empty `range`: the existing `if (dps.isNotEmpty && range.isNotEmpty)` guard (line 385) and individual emptiness checks already handle this — only show the label when the value is present.
  - Very long range strings (e.g. "10.5 (charged)"): `_cleanStat` already truncates to 7 chars. Adding " RANGE" (6 chars) makes the worst case ~13 chars. At 10px font in a badge with 4px horizontal padding, this fits within the tile width (tiles are ~90px wide at 4 columns on a 360px screen). Verify on narrow screens (3 columns at <360px width).
  - The `_corner` getter formats DPS as integer when ≥100 (e.g. "150") and 1-decimal when <100 (e.g. "22.5"). The "DMG" label works for both formats.
- **Verification:**
  - `flutter analyze` on `periodic_tile.dart`.
  - Visual: open the Periodic Grid with a gun that has both DPS and RANGE — confirm "DMG" and "RANGE" labels are visible next to the numbers, readable, and don't overflow the tile.
  - Confirm top-DPS gold shimmer still animates correctly with the label.
  - Confirm guns with missing DPS or RANGE still show only the available stat.

---

### BUG-041 — Active-run header icons: no text labels, hard to tell what each icon does
- **Severity:** UX
- **Status:** FIXED (v1.9.0)
- **Found by:** User testing (Aug 12 2026)
- **Files:**
  - `lib/widgets/active_run/player_page.dart` — `GungeoneerHeader` trailing Row (lines 222–322), calculator icon (230–250), effects icon (252–271), shrine icon (274–297), special panels icon (299–318)
- **Description:** The active-run header has 4 toggle icons in a horizontal row (Damage Calculator, Effects Panel, Shrine Picker, Special Panels). Each is a bare `IconButton` with only a tooltip — **no visible text label**. New users can't tell what each icon does without tapping them blindly. The user wants **small text labels below each icon** for immediate discoverability.
- **Current behavior:**
  - All 4 icons are `IconButton` widgets, size 20, in a horizontal `Row` wrapped in `SingleChildScrollView(scrollDirection: Axis.horizontal)` (line 223).
  - Color: `Colors.amberAccent` when ON, `Colors.white38` when OFF.
  - Constraints: `BoxConstraints(minWidth: 36, minHeight: 36)`, padding `EdgeInsets.zero`.
  - Tooltips exist but are only visible on long-press/hover — not discoverable on mobile.
  - The Row also contains `SpongeButton` (line 227, conditional) and `HeaderMenu` (line 320, gear icon) — these are not part of the labeling task.
- **Fix proposal:** Wrap each of the 4 `IconButton`s in a `Column` with a tiny text label below:
  - **Calculator** → label "Calc" (short for "Damage Calculator")
  - **Effects** → label "Effects"
  - **Shrine** → label "Shrine"
  - **Special Panels** → label "Panels"
  - Label style: ~8px, weight 600, `Colors.white54` (or amber-tinted when ON to match the icon state), `letterSpacing: 0.5`, `GoopText` for font consistency.
  - Keep the `ListenableBuilder` wrappers, `IconButton` tooltips, tap/long-press actions, and amber/white38 color scheme unchanged.
  - Keep the `SingleChildScrollView` horizontal scroll — adding labels makes each column slightly wider (~36px → ~36px, label is narrower than the icon). If the Row gets too wide, the scroll handles it.
  - Consider tightening the `SizedBox(width: 4)` gaps between labeled columns if needed.
- **Edge cases:**
  - Narrow screens (≤360px): the Row already scrolls horizontally. Labels don't add significant width since they're shorter than the icons. Verify the Row doesn't push the `HeaderMenu` gear off-screen on narrow devices — the scroll handles overflow.
  - The `SpongeButton` (line 227) is conditional and has its own layout — don't label it, only the 4 toggle icons.
  - The `HeaderMenu` (line 320) is a separate gear icon with a popup menu — don't label it.
  - Label color should match the icon state: amber-tinted when ON, white38/white54 when OFF. Use the same `ListenableBuilder` value to drive both icon and label color.
- **Verification:**
  - `flutter analyze` on `player_page.dart`.
  - Visual: open the active run screen — confirm 4 icons each have a small text label below them, labels are readable but not overpowering, and the header doesn't overflow on narrow screens.
  - Toggle each icon ON/OFF — confirm both the icon and label color shift between amber and white38.
  - Confirm tooltips, tap actions, and long-press actions still work.

---

## Fixed Bugs

*(Fixed bugs are moved here with commit hash and date. Open bugs above with `FIXED` status are awaiting move.)*

---

### BUG-042 — Auto-reconnect loop dies silently when `_busyTransition` is true
- **Severity:** HIGH
- **Status:** FIXED (v1.9.0, commit `d6556d9`)
- **Found by:** User testing (Aug 12 2026) — "gf leaves for 15 min and when coming back i sometimes cant reconnect as sidekick"
- **Files:**
  - `lib/services/multiplayer_session.dart` — `_tryAutoReconnect()` (lines 1637–1662), timer callback at 1652–1661
- **Description:** In `_tryAutoReconnect()`, the timer callback checks `_busyTransition` and bails without rescheduling:
  ```dart
  _autoReconnectTimer = Timer(delay, () {
    _autoReconnectTimer = null;
    if (_status != MpStatus.disconnected) return;
    if (_busyTransition) return;  // <-- KILLS THE LOOP
    unawaited(reconnect());
  });
  ```
  If a previous `reconnect()` call is still running (it has an 800ms native radio cooldown + async permission checks + `startAsSidekick`/`startAsMain`), the next auto-reconnect timer fires during the busy window and returns without scheduling a new timer. The auto-reconnect loop **dies silently** — no new attempts are ever scheduled. The only recovery paths are a new `MpDisconnected` event (but the transport is already down), the watchdog (but it's stopped during disconnect), or the user manually tapping reconnect.
- **Root cause:** The `_busyTransition` guard was added to prevent overlapping `reconnect()` calls, but it doesn't reschedule when it bails. The guard in `reconnect()` itself (line 747: `if (_busyTransition) return;`) is sufficient to prevent overlaps — the timer-side guard is redundant and causes the loop death.
- **Fix proposal:** When `_busyTransition` is true in the timer callback, reschedule a short retry (2s) instead of bailing:
  ```dart
  if (_busyTransition) {
    _autoReconnectTimer = Timer(const Duration(seconds: 2), _tryAutoReconnect);
    return;
  }
  ```

### BUG-043 — No immediate reconnect when app returns to foreground
- **Severity:** MED
- **Status:** FIXED (v1.9.0, commit `d6556d9`)
- **Found by:** User testing (Aug 12 2026) — "gf leaves for 15 min and when coming back i sometimes cant reconnect as sidekick"
- **Files:**
  - `lib/services/multiplayer_session.dart` — no `WidgetsBindingObserver` wiring
- **Description:** When the app is backgrounded, OS doze mode stops Dart timers from firing. The auto-reconnect timer, watchdog, and search timeout all stop. When the app returns to foreground, the timers resume but may fire late (or the timer may have already expired during background and won't fire again). The user has to wait for the next scheduled retry (which could be 30s away) or manually tap reconnect.
- **Root cause:** No `WidgetsBindingObserver` to detect app resume and trigger an immediate reconnect attempt when status is `disconnected`.
- **Fix proposal:** Add `WidgetsBindingObserver` to `MultiplayerSession`:
  ```dart
  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.resumed &&
        _status == MpStatus.disconnected &&
        canReconnect && !_busyTransition) {
      _log('App resumed — triggering immediate reconnect attempt...');
      _cancelAutoReconnect();
      _startAutoReconnect();
    }
  }
  ```
  Register in constructor: `WidgetsBinding.instance.addObserver(this);`
  Unregister in dispose: `WidgetsBinding.instance.removeObserver(this);`

### BUG-044 — Search timeout (60s) too long during auto-reconnect
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** User testing (Aug 12 2026) — "gf leaves for 15 min and when coming back i sometimes cant reconnect as sidekick"
- **Files:**
  - `lib/services/multiplayer_session.dart` — `_startSearchTimeout()`, `_searchTimeoutMs`, `_reconnectSearchTimeoutMs`
- **Description:** During auto-reconnect, `reconnect()` calls `startAsSidekick()`/`startAsMain()` which starts a 60s search timeout. If the peer isn't advertising yet (their app is also backgrounded), those 60s are wasted before the next attempt. After 15 minutes, only ~10-12 attempts have been made (60s search + 30s backoff = 90s per cycle). A shorter timeout during reconnection would allow more attempts.
- **Root cause:** The search timeout is a single constant (60s) used for both initial connection and reconnection. No distinction between fresh search and reconnect search.
- **Fix proposal:** Add an optional `timeoutMs` parameter to `_startSearchTimeout()` and use a shorter value (20-25s) during auto-reconnect. Or: during auto-reconnect, skip the search timeout entirely and let the auto-reconnect loop's backoff timer act as the timeout — if no connection within the backoff window, the next attempt restarts the search.
- **Fix:** Added `_isReconnecting` flag set in `reconnect()`, reset on connection or timeout. `_startSearchTimeout()` uses 20s for reconnect (vs 60s fresh). Reconnect timeout silently retries instead of showing error. ~3x more reconnect attempts in the same time window (20s + 30s backoff = 50s per cycle vs 90s).
- **Commit:** 9eeda49

---

### BUG-045 — 17 dashboard collapse toggles non-functional (onTap: null, no chevron)
- **Severity:** MEDIUM
- **Status:** FIXED
- **Found by:** Coder (analyzer audit, Aug 13 2026)
- **Files:** `lib/widgets/dashboards/compact_dashboards.dart` (12 dashboards), `lib/widgets/dashboards/special_gun_dashboards.dart` (3 dashboards), `lib/widgets/dashboards/junkan_dashboard.dart` (1), `lib/widgets/dashboards/robot_dashboard.dart` (1)
- **Description:** 17 special dashboards (Shellegun, Chamber Gun, Platinum Bullets, Iron Coin, Spice, Metronome, Sprun, Boxing Glove, Cigarettes, Polaris, Gunther, Gun Soul, Gunderfury, Triple Gun, Evolver, Junkan, Robot) declared `_collapsed`/`_expanded` boolean fields and wrapped their content in `if (!_collapsed) ...[...]` / `if (_expanded) ...[...]`, but:
  1. The `InkWell` `onTap` was `null` — making the header non-tappable.
  2. No `setState` was ever called — the fields were never reassigned.
  3. No chevron/expand icon was rendered — no visual indication the header was tappable.
  The analyzer flagged all 17 as `prefer_final_fields` because the fields were never reassigned. The collapse feature was scaffolded but never wired up.
- **Root cause:** Incomplete feature implementation. The `_collapsed`/`_expanded` fields, `InkWell` wrappers, and `if (!_collapsed)` guards were added but the tap handlers, state mutation, and visual indicators were never connected.
- **Fix:** Wired all 17 `onTap` handlers to `setState(() => _collapsed = !_collapsed)` (or `_expanded`) with `Haptics.selection()`. Added `Icon(_collapsed ? Icons.expand_more : Icons.expand_less)` chevrons to all 17 header rows. Analyzer now reports 0 issues on the dashboards directory (down from 17 `prefer_final_fields` warnings).
- **Commit:** 1be09e1

---

### BUG-046 — Junkan + 3 special gun dashboards: inverted `_expanded` variable, chevron points wrong way, starts collapsed
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (bughunt, Aug 14 2026)
- **Files:** `lib/widgets/dashboards/junkan_dashboard.dart`, `lib/widgets/dashboards/special_gun_dashboards.dart`
- **Description:** The Junkan dashboard and all 3 special gun dashboards (Gunderfury, Triple Gun, Evolver) used a boolean field named `_expanded`, but the logic was inverted: `_expanded = true` meant COLLAPSED. The chevron pointed the wrong way and dashboards started collapsed.
- **Fix:** Applied Option B — renamed `_expanded` → `_collapsed` in all 4 dashboards, inverted all references (`_collapsed ? SizedBox.shrink() : Column(...)`, `_collapsed ? Icons.expand_more : Icons.expand_less`), default `_collapsed = false` (starts expanded). Now matches `compact_dashboards.dart` pattern. flutter analyze: 0 issues.

---

### BUG-047 — Robot dashboard missing 4 tracked fields: Armor, Fireplace, Battery, Fuse Disarmer
- **Severity:** MEDIUM
- **Status:** FIXED
- **Found by:** Coder (bughunt, Aug 14 2026)
- **Files:** `lib/widgets/dashboards/robot_dashboard.dart`, `lib/providers/run_provider.dart`
- **Description:** The Robot dashboard only showed Junk count, Gold Junk toggle, and Lies toggle. 4 additional Robot-specific fields were tracked in RunProvider with full persistence but no UI.
- **Fix:** Added all 4 fields to the Robot dashboard:
  - **Armor:** +/- counter row (like Junk counter), default 6, clamped 0-99.
  - **Fireplace Extinguished:** toggle (blueAccent), uses `setFireplaceExtinguished`.
  - **Battery Bullets Synergy:** toggle (greenAccent), uses `setBatteryBulletsSynergy`.
  - **Fuse Disarmer:** full-width toggle (orangeAccent), uses `setFuseDisarmer`.
  All 4 fields now visible and editable. flutter analyze: 0 issues.

---

### BUG-048 — Rad Gun has empty `type` field in guns.json
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (data bughunt, Aug 14 2026)
- **File:** `assets/data/guns.json` — Rad Gun entry
- **Description:** Rad Gun had `"type": ""` (empty string). No type pill in browse, no subtitle in detail.
- **Fix:** Set Rad Gun's `type` to "Semiautomatic".

---

### BUG-049 — Gunderfury has garbage `type` field: "Semiautomatic Automatic Semiautomatic Semiautomatic Automatic Automatic"
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (data bughunt, Aug 14 2026)
- **File:** `assets/data/guns.json` — Gunderfury entry, `lib/widgets/item_detail/gun_stats.dart`
- **Description:** Gunderfury's `type` field contained a concatenation of all its form types. Browse pill showed raw garbage. Detail screen special-cased it with `isGunderfury ? '???'`.
- **Fix:** Set Gunderfury's `type` to "Variable". Removed the `isGunderfury` special case in `gun_stats.dart` — `displayType` now uses `gun.type` directly. The dynamic DPS calculation (which depends on `p.gunderfuryLevel`) is preserved via inline `gun.name.toLowerCase() == 'gunderfury'` check.

---

### BUG-050 — 2 guns have non-standard `type` variants inconsistent with the 5 standard types
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (data bughunt, Aug 14 2026)
- **File:** `assets/data/guns.json` — Deck4rd, Mr. Accretion Jr.
- **Description:** Deck4rd had `"Semiautomatic (functionally Automatic)"` and Mr. Accretion Jr. had `"Semi-Automatic"` — non-standard variants that wouldn't match exact string filters.
- **Fix:** Normalized both to `"Semiautomatic"`.

---

### BUG-051 — 3 IconButtons with sub-minimum tap targets (BoxConstraints() + padding zero)
- **Severity:** MEDIUM
- **Status:** FIXED
- **Found by:** Coder (UI bughunt, Aug 14 2026)
- **Files:** `lib/screens/multiplayer_lobby_screen.dart`, `lib/widgets/active_run/player_header.dart`, `lib/widgets/item_detail/header.dart`
- **Description:** Three IconButton widgets used `constraints: const BoxConstraints()` and `padding: EdgeInsets.zero`, removing the default 48x48 minimum tap target. The 16px delete button was the worst — destructive action with tiny tap target.
- **Fix:** Replaced `BoxConstraints()` with `BoxConstraints(minWidth: 44, minHeight: 44)` and removed `padding: EdgeInsets.zero` from all 3. Added tooltips to all 3 (delete session, close, favorite toggle). flutter analyze: 0 issues.

---

### BUG-052 — 27 IconButtons missing tooltips (accessibility)
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (UI bughunt, Aug 14 2026)
- **Files:** Multiple — 11 files
- **Description:** 18 standalone IconButton widgets were missing the `tooltip` parameter. Screen reader users could not identify what these buttons do.
- **Fix:** Added `tooltip:` to all 18 IconButtons across 11 files:
  - robot_dashboard.dart: 4 tooltips (junk +/-, armor +/-)
  - compact_dashboards.dart: 14 tooltips (platinum bullets, iron coin, spice, metronome, boxing glove, cigarettes, Polaris, Gunther +/-)
  - theme_picker_screen.dart, settings_screen.dart: back buttons
  - active_run_screen.dart: search clear
  - all_synergies_screen.dart, main_menu_screen.dart, mp_request_listener.dart, app_tab.dart, run_tab.dart: close buttons
  - multiplayer_lobby_screen.dart: back-to-lobby arrow
  Plus 3 tooltips added as part of BUG-051 (delete session, close, favorite toggle). flutter analyze: 0 issues.

---

### BUG-053 — Dashboard GestureDetector controls missing haptics + Material ripple
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (UI bughunt, Aug 14 2026)
- **Files:** `lib/widgets/dashboards/robot_dashboard.dart`, `lib/widgets/dashboards/junkan_dashboard.dart`, `lib/widgets/dashboards/special_gun_dashboards.dart`
- **Description:** Dashboard increment/decrement and toggle controls used `GestureDetector` without `Haptics.light()` calls, inconsistent with compact_dashboards.dart which uses haptics on all state-changing actions.
- **Fix:** Added `Haptics.light()` to all 10 GestureDetector onTap handlers:
  - robot_dashboard.dart: 4 IconButtons (junk +/-, armor +/-) + 1 GestureDetector toggle (_buildCompactToggle)
  - junkan_dashboard.dart: 2 GestureDetectors (junk add/remove)
  - special_gun_dashboards.dart: 6 GestureDetectors (Gunderfury +/-, Triple Gun +/-, Evolver +/-)
  flutter analyze: 0 issues.

---

### BUG-054 — Emote bottom sheet missing SafeArea (hardcoded bottom: 32)
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (UI bughunt, Aug 14 2026)
- **File:** `lib/screens/active_run_screen.dart`
- **Description:** The emote bottom sheet used hardcoded 32px bottom padding without SafeArea, risking obscurement by system nav bars on some devices.
- **Fix:** Added `useSafeArea: true` to the `showModalBottomSheet` call and reduced bottom padding from 32 to 12 (SafeArea handles the rest).

---

### BUG-055 — stats_detail_screen large stat value (fontSize 52) not responsive
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (UI bughunt, Aug 14 2026)
- **File:** `lib/screens/stats_detail_screen.dart`
- **Description:** The main stat value display used `fontSize: 52` without scaling or `FittedBox`, risking overflow on high text scale settings.
- **Fix:** Wrapped the GoopText in `FittedBox(fit: BoxFit.scaleDown)` so it shrinks gracefully on narrow screens / high text scale, matching the main menu title pattern.

### BUG-056 — Briefcase of Cash effect text truncated
- **Severity:** HIGH
- **Status:** FIXED
- **Found by:** Coder (data audit, Aug 14 2026)
- **File:** `assets/data/items.json`
- **Description:** Effect read `"Grants 250 and 3 ."` — wiki ref tokens were stripped during data import, losing "coins" and "Hegemony Credits".
- **Fix:** Restored to `"Grants 250 coins and 3 Hegemony Credits."` based on wiki effects section.

### BUG-057 — 12 guns had empty notes field
- **Severity:** MEDIUM
- **Status:** FIXED
- **Found by:** Coder (data audit, Aug 14 2026)
- **File:** `assets/data/guns.json`
- **Description:** 12 guns (AK-47, Derringer, M1911, Machine Pistol, Magnum, Makarov, Regular Shotgun, Thompson Sub-Machinegun, Trank Gun, Void Marshal, Vulcan Cannon, Winchester Rifle) had completely empty `notes` fields, leaving the detail view with no effect description.
- **Fix:** Populated all 12 with concise descriptions sourced from wiki.gg pages.

### BUG-058 — Synergy name mismatch: "Thermal Imaging" → "Thermal Imagine"
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (synergy audit, Aug 14 2026)
- **File:** `assets/data/synergies.json`
- **Description:** Our JSON used "Thermal Imaging" but the official wiki/game name is "Thermal Imagine" (a pun). This could cause synergy lookup mismatches.
- **Fix:** Renamed to "Thermal Imagine" to match the wiki.

### BUG-059 — GungeonHeader multiple tickers crash (SingleTickerProviderStateMixin + 2 AnimationControllers)
- **Severity:** CRITICAL
- **Status:** FIXED
- **Found by:** Maintainer (Playwright QA sweep, Aug 15 2026)
- **File:** `lib/widgets/gungeoneer_header.dart` (line 81)
- **Description:** `_GungeoneerHeaderState` used `SingleTickerProviderStateMixin` but created TWO `AnimationController`s (`_wobbleController` + `_borderPulseController`), both with `vsync: this`. `SingleTickerProviderStateMixin` only supports one ticker. When the GungeonHeader mounted (immediately after character select → active run screen), Flutter threw a "Multiple tickers" assertion error, crashing the app.
- **Fix:** Changed `SingleTickerProviderStateMixin` → `TickerProviderStateMixin` (supports multiple tickers). Verified all other 18 `SingleTickerProviderStateMixin` usages in the codebase — they each correctly use only one controller.
- **Repro:** Main Menu → Local Run → select any character → crash.

### BUG-060 — Main menu shows hardcoded "v1.9.11" despite pubspec being v1.9.15
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Maintainer (Playwright QA sweep, Aug 15 2026)
- **File:** `lib/screens/main_menu_screen.dart` (lines 185, 254, 309, 726)
- **Description:** The main menu had 4 hardcoded `'v1.9.11'` strings. After version bumps to v1.9.15, the menu still showed "v1.9.11" and "Changelog (v1.9.11)". No central version constant exists — version is manually hardcoded in 4 places.
- **Fix:** Updated all 4 strings to 'v1.9.15'. Note: these will need manual updating on each version bump until a central constant is introduced.

### BUG-061 — Browse pill says "synergys" instead of "synergies" (plural typo)
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Maintainer (Playwright QA sweep, Aug 15 2026)
- **File:** `lib/widgets/browse/browse_pills.dart` (line 178)
- **Description:** The synergy count pill used `'$count synergy${count == 1 ? "" : "s"}'` which produced "1 synergy" (correct) but "2 synergys" (wrong — should be "synergies"). The English plural of "synergy" is "synergies", not "synergys".
- **Fix:** Changed to `'$count ${count == 1 ? 'synergy' : 'synergies'}'`.

### BUG-062 — Stripped wiki ref tokens causing " ." and " ," patterns in gun notes and item effects
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (deep data audit, Aug 16 2026)
- **Files:** `assets/data/guns.json` (22 entries), `assets/data/items.json` (9 entries)
- **Description:** During original data import, wiki ref tokens (e.g. `[[Stun]]`, `[[Burn]]`) were stripped from text fields, leaving behind a space before the punctuation mark. This produced patterns like `'chance to stun .'` and `'Starting gun of The Convict .'` across 22 gun notes and 9 item effects — 31 entries total.
- **Fix:** Replaced all `' .'` → `'.'` and `' ,'` → `','` in notes and effect fields. No semantic content was lost — only the orphaned space was removed.

### BUG-063 — 12 guns had empty "class" field
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (deep data audit, Aug 16 2026)
- **File:** `assets/data/guns.json`
- **Description:** 12 guns had `"class": ""` — A.W.P., Alien Sidearm, Anvillain, Balloon Gun, Bee Hive, Big Iron, Big Shotgun, Blunderbuss, Brick Breaker, Budget Revolver, Bullet, Cold 45. The class field is used by `ElementalTagger` and gun classification logic.
- **Fix:** Populated all 12 with wiki-verified gun classes: A.W.P.→RIFLE, Alien Sidearm→PISTOL, Anvillain→CHARGE, Balloon Gun→FULLAUTO, Bee Hive→SILLY, Big Iron→PISTOL, Big Shotgun→EXPLOSIVE, Blunderbuss→CHARGE, Brick Breaker→SILLY, Budget Revolver→SHITTY, Bullet→PISTOL, Cold 45→ICE.

### BUG-064 — 3 entries with missing icon URLs
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (deep data audit, Aug 16 2026)
- **Files:** `assets/data/items.json` (Master Round I, Master Round II), `assets/data/guns.json` (Rusty Sidearm)
- **Description:** Master Round I, Master Round II, and Rusty Sidearm had `"icon": ""` while their siblings (Master Round III/IV/V) had proper URLs. This caused blank images in the browse and detail views.
- **Fix:** Populated all 3 with correct Fandom CDN image URLs sourced from the wiki.

### BUG-065 — 11 synergy effects with stripped wiki ref tokens (" ." and " ," patterns)
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (deep data audit round 2, Aug 16 2026)
- **File:** `assets/data/synergies.json`
- **Description:** Same root cause as BUG-062 — wiki ref tokens stripped during import left orphaned spaces before punctuation. Affected 11 synergies: Behold!, Cormorant, Fairy Bow, Five O'Clock Somewhere, Kung Fu Hippie Rappin' Surfer, Pinker Guon Stone, Resourceful Indeed, Rubenstein's Monster, Shield Night, Tears of Blood, Whiter Guon Stone.
- **Fix:** Replaced all `' .'` → `'.'` and `' ,'` → `','` in synergy effect fields.

### BUG-066 — 56 guns with empty range field
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (deep data audit round 2, Aug 16 2026)
- **File:** `assets/data/guns.json`
- **Description:** 56 guns had `"range": ""` while the wiki shows `[Infinity.png]` for all of them. This caused the gun stats UI to display an empty range value. Includes AK-47, Bullet Bore, Deck4rd, Eye of the Beholster, Pitchfork, and 51 more.
- **Fix:** Set all 56 to `"range": "∞"` to match the wiki's infinite range notation. 6 guns already used `"∞"` — now all 62 infinite-range guns are consistent.

### BUG-067 — 6 beam weapons with empty shot_speed field
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (deep data audit round 2, Aug 16 2026)
- **File:** `assets/data/guns.json`
- **Description:** 6 beam-type guns had `"shot_speed": ""` — Abyssal Tentacle, Gamma Ray, Life Orb, Moonscraper, Mourning Star, Raiden Coil. Beam weapons fire instant-hit beams, so shot speed is effectively infinite. The wiki shows `[Infinity.png]` for these.
- **Fix:** Set all 6 to `"shot_speed": "∞"`.

### BUG-068 — 10 guns with spaces inside number values in stat fields
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (wiki accuracy audit, Aug 16 2026)
- **File:** `assets/data/guns.json`
- **Description:** 10 guns had spaces inside number values (e.g. `"16. 6"` instead of `"16.6"`) in DPS, damage, and spread fields. Caused by wiki scraping artifacts. Affected Flare Gun (dps), Lower Case r (damage), Mailbox (dps), Makarov (dps), Pea Shooter (dps), Shellegun (dps), Sling (dps), Starpew (dps), Trashcannon (dps), Triple Gun (dps).
- **Fix:** Removed spaces after decimal points in all numeric stat fields.

### BUG-069 — 3 guns with double degree symbols in spread field
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (wiki accuracy audit, Aug 16 2026)
- **File:** `assets/data/guns.json`
- **Description:** 3 guns had `°°` (double degree symbol) in spread field — Crescent Crossbow (`"0°°"`), Gunbow (`"0°°"`), M1911 (`"4°°"`). The M1911 wiki page itself has this typo, which was scraped into our data.
- **Fix:** Replaced all `°°` with `°`.

### BUG-070 — 7 active items with inconsistent recharge_time values
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (wiki accuracy audit, Aug 16 2026)
- **File:** `assets/data/items.json`
- **Description:** 7 active items had inconsistent `recharge_time` values. 6 items had `"-Use"` (truncated from `"Single-Use"` during scraping) — Meatbun, Medkit, Ration, Spice, Supply Drop, Weird Egg. 1 item had `"Single Use"` (missing hyphen) — Duct Tape. The wiki consistently uses `"Single-Use"`.
- **Fix:** All 7 normalized to `"Single-Use"`.

### BUG-071 — 10 guns with reload_time missing "s" suffix
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (wiki accuracy audit, Aug 16 2026)
- **File:** `assets/data/guns.json`
- **Description:** 10 guns had `reload_time` values without the `"s"` suffix (e.g. `"1.2"` instead of `"1.2s"`), while 205 other guns consistently use the `"s"` suffix. Affected Barrel, Cold 45, Devolver, Directional Pad, Evolver, Flash Ray, Railgun, Sawed-Off, Strafe Gun, Vorpal Gun.
- **Fix:** Added `"s"` suffix to all 10 values.

### BUG-072 — 3 items with vague effect text missing key mechanics
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (wiki accuracy audit, Aug 16 2026)
- **File:** `assets/data/items.json`
- **Description:** 3 items had vague effect text that omitted important mechanics, confirmed by wiki.gg comparison:
  - Galactic Medal of Valor: said "Deal more damage to Bosses. Increases reload speed and accuracy." — missing the specific 30% damage boost, halves reload time, halves shot spread, and cannot be dropped.
  - Number 2: said "Boosts stats when alone." — missing the specific +2 movement speed and +41% damage values.
  - Gungeon Pepper: said "Deals damage to nearby enemies." — missing the specific 5 damage per second rate.
- **Fix:** Updated all 3 with wiki-accurate effect text including specific mechanics.

---

### BUG-073 — 13 passive items with vague effects missing specific values
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (items wiki audit, Aug 16 2026)
- **File:** `assets/data/items.json`
- **Description:** 13 passive items had vague effect text that omitted specific values and mechanics. Confirmed by wiki.gg comparison. Affected: Ballistic Boots, Shotga Cola, Shotgun Coffee, Bionic Leg, Military Training, Battle Standard, Coin Crown, Gold Ammolet, Wolf, Bullet Idol, Eyepatch, Unity, Book of Chest Anatomy.
- **Fix:** Updated all 13 with wiki-accurate effect text including specific values.

### BUG-074 — 6 bullet upgrade items with missing chance percentages
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (items wiki audit, Aug 16 2026)
- **File:** `assets/data/items.json`
- **Description:** 6 bullet upgrade items said "adds a chance" without specifying the percentage. Wiki.gg lists specific values. Affected: Charming Rounds (7.5%), Hot Lead (20%), Homing Bullets (20%), Irradiated Lead (50%, 2.5s), Explosive Rounds (8.5%, 25 damage), Shadow Bullets (15%).
- **Fix:** Added wiki-accurate percentages and damage values.

### BUG-075 — 4 active items with vague effects missing duration
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (items wiki audit, Aug 16 2026)
- **File:** `assets/data/items.json`
- **Description:** 4 active items with temporary effects didn't specify duration or key limitations. Affected: Stuffed Star (9s, pits/traps still harm), Double Vision (10s, reduces accuracy), Bullet Time (3s), Potion of Lead Skin (6s).
- **Fix:** Added wiki-accurate durations and missing mechanics.

### BUG-076 — 10 more items with vague effects missing key details
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (items wiki audit, Aug 16 2026)
- **File:** `assets/data/items.json`
- **Description:** 10 items had vague effect text missing important details. Affected: Pig (sacrifices itself, removes item), Heart of Ice (8-12 bullets, freeze), Cat Bullet King Throne (flight, roll direction), Table Tech Rage (3s), Omega Bullets (final two shots, not one), Shock Rounds (connects bullets), Snowballets (further travel), Angry Bullets (no ammo cost), Macho Brace (double damage), Turkey (same gun).
- **Fix:** Updated all 10 with wiki-accurate effect text.

---

### BUG-077 — 11 more items with vague effects missing specific values (round 2)
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (items wiki audit round 2, Aug 16 2026)
- **File:** `assets/data/items.json`
- **Description:** 11 more items had vague effect text missing specific percentages and mechanics. Confirmed by wiki.gg. Affected: Gilded Bullets (100% at 500), Platinum Bullets (250s/500s, max triple), Stout Bullets (50% larger, 12.5%-75%, -30% speed), Ammo Synthesizer (10%, 5% ammo), Armor Synthesizer (10%, no damage), Heart Synthesizer (20%, half heart, not full health), Master of Unlocking (20%, free key), Ring of Chest Friendship (50% more, halves D-tier), Chaos Ammolet (50% each, stun 1s, 25 tiles), Antibody (50%, extra half heart), Bloody 9mm (8%/s, homing/piercing/bouncing).
- **Fix:** Updated all 11 with wiki-accurate effect text including specific values and conditions.

---

### BUG-078 — 14 more items with vague effects missing specific values (round 3)
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (items wiki audit round 3, Aug 16 2026)
- **File:** `assets/data/items.json`
- **Description:** 14 more items had vague effect text missing specific values and mechanics. Confirmed by wiki.gg. Affected: Copper/Frost/Uranium Ammolet (stun 1s, 25 tiles, 50% chance), Lodestone Ammolet (stun 3s, 400% knockback), Wingman (20 dmg rockets, 5s, blocks bullets), R2G2 (6 bullets, 5 dmg, 4s cooldown), Super Space Turtle (5 dmg bullets), Melted Rock (15 dmg), Singularity (8s duration), Air Strike (25 dmg per explosion), Fortune's Favor (8s duration), Proximity Mine (60 dmg), Bumbullets (bee every second, 3 dmg + 1/s for 2s, no ammo), Crutch (slight homing).
- **Fix:** Updated all 14 with wiki-accurate effect text including specific values, durations, and damage numbers.

---

### BUG-079 — 12 more items with vague effects missing specific values (round 4)
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (items wiki audit round 4, Aug 16 2026)
- **File:** `assets/data/items.json`
- **Description:** 12 more items had vague effect text missing specific values and mechanics. Confirmed by wiki.gg. Affected: Frost Bullets (slower weapons higher chance), Devolver Rounds (Arrowkin, beam double dmg), Hungry Bullets (blue, 1.5 tiles, +10%/bullet, cap 80%, beam x2), Magic Bullets (4% transmog), Zombie Bullets (33% refund, no beam), Chance Bullets (no ammo cost), Katana Bullets (curse +1, 100% beam, 50%/s beam double), Table Tech Sight (3s, grammar fix), Green Guon Stone (20% heal, 50% lethal), Ruby Bracelet (30 dmg), Mustache (Bello 15% cheaper), Ice Bomb (8 dmg).
- **Fix:** Updated all 12 with wiki-accurate effect text including specific values, percentages, and mechanics.

---

### BUG-080 — 23 final items with vague effects missing specific values (round 5)
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (items wiki audit round 5 final, Aug 16 2026)
- **File:** `assets/data/items.json`
- **Description:** 23 final items had vague effect text missing specific values and mechanics. Confirmed by wiki.gg. Affected: Table Tech Heat (5 tiles, 10s), Table Tech Money (40%, 1-4 coins), Table Tech Rocket (30+30 dmg), Table Tech Shotgun (10 bullets, 6 dmg, 4 bounces), Bomb (60 dmg), Molotov (4 DPS, 4s), Magazine Rack (10s), Charm Horn (10s), Aged Bell (5s), Potion of Gun Friendship (+30% dmg, x2 fire rate, -70% reload, x10 knockback), Cluster Mine (60 dmg), Chaff Grenade (10s stun), Daruma (recharge), Orbital Bullets (wall hit, bounce fallback), Ring of Chest Vampirism (half heart, mimics), Cartographer's Ring (50%, no secret rooms), Chaos Bullets (10% pierce/bounce/status, 25% beam), Gundromeda Strain (bosses too), Baby Good Shelleton (12.5 DPS), Honeycomb (12-20 bees, 3+1/s), Enraging Photo (4s), Blue Guon Stone (33% shot speed, 5s), Portable Table Device (Table Tech trigger).
- **Fix:** Updated all 23 with wiki-accurate effect text including specific values, durations, and damage numbers. Completes the items accuracy audit.

---

### BUG-086 — 5 more synergy effects corrected in deeper audit
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (synergies deep audit, Aug 16 2026)
- **File:** `assets/data/synergies.json`
- **Description:** Deeper synergies audit focusing on long effects (>100 chars) accuracy. 5 effects corrected: blade (missing "and bosses"), Praise the Gun (missing "Old Crest room"), Firing With Flair (incorrect "permanently burning" vs wiki's "Green Fire 120s 4 DPS"), Why's Bullet Crying? (missing 75 damage value and no-repeat mechanic), Jotun Time (missing "rapidly" qualifier). Also verified 20+ other long effects as already accurate against wiki.gg.
- **Fix:** Updated all 5 with wiki-accurate effect text.

---

### BUG-085 — 105 missing gun stats filled with wiki-accurate values
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (gun stats audit, Aug 16 2026)
- **File:** `assets/data/guns.json`
- **Description:** Comprehensive gun stats audit found 106 missing/empty stat fields across 56 guns. 105 were filled with wiki-accurate values: infinite-ammo guns now show ∞, beam weapons show N/A for reload_time, special guns have appropriate placeholder values. Yari Launcher damage corrected from 8/8 to 10/15 per wiki. Big Shotgun and Yari Launcher DPS filled. Multiple missing fire_rate, shot_speed, force, and spread values filled.
- **Fix:** Updated all 105 missing stats with wiki-verified values.

---

### BUG-084 — 30 gun notes enriched with wiki-accurate mechanics
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (gun notes wiki audit, Aug 16 2026)
- **File:** `assets/data/guns.json`
- **Description:** First gun notes accuracy audit. Of 239 guns, 62 had short notes (<50 chars). After verifying against wiki.gg, 30 were confirmed as missing useful mechanics, damage values, or form details. Key additions: AU Gun (100 dmg), Bundle of Wands (10% transmogrify, 3 projectiles), Chamber Gun (10 forms), Triple Gun (ammo thresholds), Evolver (6 forms, 5 kills each), AC-15 (two forms), Frost Giant (ice cone), Megahand (6/45 dmg, modes), Plague Pistol (50% poison), Teapot (final shot), RC Rocket (100+30 dmg), Prototype Railgun (150 dmg, secret rooms), Snakemaker (25%), and more. The remaining 32 short notes were already accurate per wiki.
- **Fix:** Updated all 30 with wiki-accurate notes text.

---

### BUG-083 — 16 synergy effects enriched with wiki-accurate mechanics
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (synergies wiki audit, Aug 16 2026)
- **File:** `assets/data/synergies.json`
- **Description:** First synergies accuracy audit. Of 395 synergies, 121 had short effects (<60 chars). After verifying against wiki.gg, 16 were confirmed as missing useful details — specific values, conditions, side effects, or mechanics. Key additions: Klobbering Time (two shots), Iron Slug (explosive), Kalibreath (loses piercing, +knockback), Beta Ray (no longer instant), Two Kinds of People (10 digs, better loot, no bombs), Battery Powered (1 ammo/4s), Massive Effect (explodes into more projectiles), Telefrag (+extra active slot), Savior of the Universe (+double magazine), Sniper Woof (1s stand), Hidden Tech Time (only on-screen enemies), Pinker Guon Stone (grows, fixed rotation), Solar Flare (meteor), Chance On Hit (Shock Rounds effect), Chicken Arise (+bullet size), Nailed It! (larger nails). The remaining ~105 short effects were already accurate (e.g. "The guns are dual-wielded." is the complete wiki description).
- **Fix:** Updated all 16 with wiki-accurate effect text.

---

### BUG-082 — 98 final items enriched in complete comprehensive sweep (round 6 final)
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (items wiki audit round 6 complete, Aug 16 2026)
- **File:** `assets/data/items.json`
- **Description:** Final batch of the comprehensive sweep of all 130 remaining potentially enrichable items. 98 items confirmed as having missing mechanics, values, or could be made more concise/accurate. All verified against wiki.gg. Covers bullets (12), companions (6), Guon Stones (4), active items (35), and passives (41). Key additions: specific damage values, durations, chances, cooldowns, mechanics, and conditions. The remaining ~30 items were already accurate or intentionally concise (heart containers, immunity, ingredients, "No effect" items).
- **Fix:** Updated all 98 with wiki-accurate effect text. This completes the items accuracy audit — all 270 items in items.json have now been reviewed.

---

### BUG-081 — 27 more items enriched in comprehensive sweep (round 6)
- **Severity:** LOW
- **Status:** FIXED
- **Found by:** Coder (items wiki audit round 6 comprehensive, Aug 16 2026)
- **File:** `assets/data/items.json`
- **Description:** Final comprehensive sweep of all 130 remaining potentially enrichable items. 27 items confirmed as having missing mechanics or values, verified against wiki.gg. Affected: Space Friend (5 dmg), Orange Guon Stone (5 dmg, 1s CD), Red Guon Stone (dodge speed+distance), Owl (mini-blanks, blocks), Blank Bullets (beam x2), Vorpal Bullets (100 dmg crit, beam), Bouncy Bullets (2 bounces), Scattershot (55% dmg, +65% effective), Roll Bomb (5+20 dmg), C4 (60 dmg, no secret rooms), Boomerang (5s stun), Relodestone (6s), Bracket Key (150 dmg, no waves), Bottle (store/drop), Coolant Leak (Robot starter), Bloodied Scarf (-30% reload), Sprun (random trigger, ~10s), Ice Cube (recharge while active), Metronome (+2%/kill, max +150%), Scouter (+10% dmg, -10% spread), Broccoli (+1 speed), Gunboots (8 dmg, +1 speed), Sunglasses (55% slow, 25% dodge, 2s, 10s CD), Cloranthy Ring (15.8% dodge), Hip Holster (perfect accuracy), Brick of Cash (Snitch Brick), Portable Turret (blocks, room clear).
- **Fix:** Updated all 27 with wiki-accurate effect text. The remaining ~100 items were reviewed and confirmed as already accurate or intentionally concise (heart containers, immunity, ingredients).

---

### BUG-087 — ShrineActivationSheet missing SafeArea wrapper
- **Severity:** MEDIUM
- **Status:** OPEN
- **Found by:** UNIVERSAL WORKER (bughunt, Aug 18 2026)
- **File:** `lib/screens/shrine_picker_screen.dart`
- **Lines:** 392–402 (`ShrineActivationSheet.build` → `DraggableScrollableSheet` builder)
- **Description:** `ShrineActivationSheet` is shown via `showModalBottomSheet` without `useSafeArea: true`, and its `DraggableScrollableSheet` builder returns a `Container` → `Column` with no `SafeArea` wrapper. The `ListView` inside has `padding: EdgeInsets.fromLTRB(18, 14, 18, 18)` — only 18px bottom padding. On Android devices with gesture nav or 3-button nav (24–48px safe area inset), the bottom content (activation buttons, curse info) can be partially hidden under the system nav bar.
- **Root cause:** Missing `SafeArea` wrapper. Same pattern as BUG-009/010 (previously fixed in other sheets).
- **Fix proposal:** Wrap the `Container` in `SafeArea(child: ...)` inside the `DraggableScrollableSheet` builder, OR add `useSafeArea: true` to the `showModalBottomSheet` call at line 141.

---

### BUG-088 — Dice roll dialog close button sub-minimum tap target
- **Severity:** LOW
- **Status:** OPEN
- **Found by:** UNIVERSAL WORKER (bughunt, Aug 18 2026)
- **File:** `lib/widgets/active_run/dice_roll.dart`
- **Lines:** 334–343
- **Description:** The dice roll dialog close button is an `IconButton` with `padding: EdgeInsets.zero` and `constraints: const BoxConstraints()` — empty constraints mean no minimum size, so the tap target is only 20px (the icon size). This is well below the 48×48dp Material Design minimum. On mobile this is hard to hit reliably. Also missing `tooltip`.
- **Root cause:** `BoxConstraints()` with no arguments = no minimum constraint. Same pattern as BUG-051 (previously fixed in other files).
- **Fix proposal:** Add `constraints: const BoxConstraints(minWidth: 44, minHeight: 44)` and `tooltip: 'Close'`.

---

### BUG-089 — DPS calculator GestureDetector missing haptics
- **Severity:** LOW
- **Status:** OPEN
- **Found by:** UNIVERSAL WORKER (bughunt, Aug 18 2026)
- **File:** `lib/widgets/active_run/player_page.dart`
- **Lines:** 397–398
- **Description:** The DPS calculator tile in the inventory section uses a `GestureDetector` with `onTap: () => _showDamageCalcSheet(context, _slot)` — no `Haptics.selection()` call. The same action triggered from the header icon (line 264–266) correctly calls `Haptics.selection()` before showing the sheet. The inventory tile should match.
- **Root cause:** Missing `Haptics.selection()` call in the `onTap` handler.
- **Fix proposal:** Add `Haptics.selection();` before `_showDamageCalcSheet(context, _slot)` in the `onTap` callback.

---

### BUG-090 — "View All" synergies button missing haptics
- **Severity:** LOW
- **Status:** OPEN
- **Found by:** UNIVERSAL WORKER (bughunt, Aug 18 2026)
- **File:** `lib/widgets/active_run/player_page.dart`
- **Lines:** 1180–1189
- **Description:** The "View All" text button in the synergies section uses a `GestureDetector` with `onTap: () => Navigator.push(...)` — no `Haptics.selection()` call. All other navigation actions in the app use haptics for consistency.
- **Root cause:** Missing `Haptics.selection()` call.
- **Fix proposal:** Add `Haptics.selection();` before `Navigator.push` in the `onTap` callback.

---

### BUG-091 — "Remember Pick" checkbox missing haptics
- **Severity:** LOW
- **Status:** OPEN
- **Found by:** UNIVERSAL WORKER (bughunt, Aug 18 2026)
- **File:** `lib/widgets/active_run/modes/mode_picker_onboarding.dart`
- **Lines:** 438–439 (GestureDetector), 443–446 (Checkbox)
- **Description:** The "Remember Pick" checkbox in the mode picker onboarding dialog has no haptic feedback. The `GestureDetector` `onTap` at line 439 calls `setState` without `Haptics`, and the `Checkbox` `onChanged` at line 445 also has no haptics. All other toggle/selection actions in the app use `Haptics.selection()`.
- **Root cause:** Missing `Haptics.selection()` in both the `GestureDetector.onTap` and `Checkbox.onChanged` callbacks.
- **Fix proposal:** Add `Haptics.selection();` at the start of both callbacks.

---

### BUG-092 — End Run button in settings missing haptics
- **Severity:** LOW
- **Status:** OPEN
- **Found by:** UNIVERSAL WORKER (bughunt, Aug 18 2026)
- **File:** `lib/widgets/settings/settings_tab.dart`
- **Lines:** 532–533
- **Description:** The "End Run" button in the Settings tab Danger Zone uses a `GestureDetector` with `onTap: () => _confirmEndRun(context, p)` — no `Haptics` call. The `_confirmEndRun` method (line 35) opens the `EndRunConfirmDialog` which has haptics on its internal confirm/cancel buttons, but the initial tap on the End Run button itself has no feedback. Destructive actions should have haptic feedback on tap to confirm the user feels the interaction.
- **Root cause:** Missing `Haptics.warning()` or `Haptics.selection()` call.
- **Fix proposal:** Add `Haptics.warning();` (or `Haptics.selection()`) before `_confirmEndRun(context, p)` in the `onTap` callback.

---

## Disputed / Wontfix

*(None yet.)*
