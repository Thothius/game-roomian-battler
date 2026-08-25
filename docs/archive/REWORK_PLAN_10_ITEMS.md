# 10-Item Rework Plan — 2026-08-25

> Split into 4 parallel parts so multiple agents can work simultaneously.
> Each part is self-contained — no file overlap between parts.

## User's 10 Requests

1. **No PINs** — Remove the PIN system from MP entirely
2. **Role selection first** — Pick nickname + role (Main/Sidekick) before showing options. Main → HOST button, Sidekick → JOIN button. Main can't pick Cultist.
3. **MP visual overhaul + Quick-add UX** — Assess why MP looks bad. Quick-add: search box on bottom with keyboard already open, tap to add + auto-clear search for rapid adding.
4. **Remove How to Use** from home screen
5. **Character select padding** — 10% padding around panels, remove "?" buttons (deets in Codex)
6. **Gungeoneer detail** — Fix 2-row layout → 1 row smaller. Name + graphic on top, no extra labels. Loadout needs REAL guns/items, linkable for all gungeoneers.
7. **Active run toolbar** — Move Effects/Shrine/Panels under MORE. Remove "More" label, make prefs icon bigger.
8. **Settings DANGER ZONE** — Remove collapsible. END RUN + RESET DATA full-width, always visible.
9. **Codex left panels** — Show graphics always (not just when active). Better padding, visual polish.
10. **Map icons** — Use wiki map icons (e.g. Marine_map.png) instead of animated sprites on active run views.

---

## Part A: MP Lobby Rework (Items 1, 2, 3-MP)

**Agent:** Slot 2 (Coder-Maintainer)
**Branch:** `slot2-coder/mp-lobby-rework`
**Files:**
- `lib/screens/mp_lobby_screen.dart` — full rewrite
- `lib/screens/mp_connect_screen.dart` — remove PIN display
- `lib/services/mp_session.dart` — remove PIN from startAsMain/startAsSidekick
- `lib/services/mp/mp_sync.dart` — remove PIN matching
- `lib/services/mp/mp_recovery.dart` — remove PIN from session info
- `lib/services/mp/mp_link.dart` — remove PIN from advertising/discovery
- `lib/models/multiplayer_messages.dart` — remove PIN from messages if present
- `test/helpers/fake_mp_link.dart` — update fake transport
- `test/mp_integration_test.dart` — update tests
- `test/mp_reliability_test.dart` — update tests
- `test/widget/mp_lobby_screen_test.dart` — update tests
- `test/widget/mp_connect_screen_test.dart` — update tests

**Design:**
```
┌─────────────────────────────┐
│      MULTIPLAYER            │
│                             │
│  ┌─ YOUR CHARACTER ──────┐  │
│  │ [sprite] The Marine   │  │
│  │ Tap to change         │  │
│  └───────────────────────┘  │
│                             │
│  NICKNAME                   │
│  [_____________________]    │
│                             │
│  YOUR ROLE                  │
│  [ MAIN ]  [ SIDEKICK ]     │
│                             │
│  ┌─ if MAIN ────────────┐   │
│  │  [ HOST GAME ]       │   │
│  │  (Cultist disabled)  │   │
│  └──────────────────────┘   │
│  ┌─ if SIDEKICK ────────┐   │
│  │  [ JOIN GAME ]       │   │
│  └──────────────────────┘   │
│                             │
│  How to Play                │
└─────────────────────────────┘
```

**Key changes:**
- Remove `_pinCtrl` and PIN field entirely
- Add role toggle (Main/Sidekick) — two segmented buttons
- If Main: show HOST button, filter out Cultist from character picker
- If Sidekick: show JOIN button
- `startAsMain` no longer generates a PIN — advertises with just nickname
- `startAsSidekick` no longer takes a PIN — discovers and auto-connects to first matching endpoint
- `MpLink.startAdvertising` takes just the nickname (no `#PIN`)
- `MpLink.startDiscovery` uses `AutoConnectModeNone` or matches by nickname
- Connect screen no longer shows a PIN display
- **Visual overhaul:** atmospheric background, better spacing, character identity prominent

**MP visual assessment (item 3-MP):**
The MP lobby looks "bad" because:
1. It's a plain form with no atmosphere — just text fields and buttons on a flat background
2. The character preview card is small and doesn't feel like a "breach point"
3. No visual distinction between HOST and JOIN — both are just buttons
4. The connect screen is a bare spinner with no personality
5. No Gungeon-themed iconography or atmospheric particles

**Fix:** Add ambient particle background, larger character portrait with glow, themed role cards (Main = crown/host icon, Sidekick = shield/companion icon), better typography hierarchy.

---

## Part B: Quick-Add UX + Active Run Toolbar (Items 3-QuickAdd, 7)

**Agent:** Slot 1 (XEENU-ANIMATOR) or Slot 4
**Branch:** `slot1-xeenu/quick-add-toolbar`
**Files:**
- `lib/screens/active_run_screen.dart` — rework `_showQuickAddBottomSheet`
- `lib/widgets/active_run/player_page.dart` — rework trailing Row (toolbar)
- `lib/widgets/active_run/active_run_helpers.dart` — enlarge HeaderMenu icon, remove "More" label

**Quick-add redesign (item 3-QuickAdd):**
```
┌─────────────────────────────┐
│  QUICK ADD TO RUN    [X]    │
│                             │
│  ┌─ Results (scroll) ────┐  │
│  │ +1 Bullets      [ADD] │  │
│  │ 38 Special      [ADD] │  │
│  │ A.W.P.          [ADD] │  │
│  │ ...               ↑   │  │
│  └───────────────────────┘  │
│                             │
│  [Search items, guns...  ]  │  ← keyboard open, at bottom
└─────────────────────────────┘
```

**Key changes:**
- Move search TextField to the BOTTOM of the sheet (above keyboard)
- Results list fills the space above (scrollable)
- `autofocus: true` already exists — keyboard opens automatically
- Tapping ADD: adds item → clears search field → results refresh → keyboard stays open
- No need to close and reopen — rapid-fire adding
- Add a brief "Added: [name]" toast that auto-dismisses in 1s

**Toolbar redesign (item 7):**
- Move Effects, Shrine, Panels toggles INTO the HeaderMenu popup (under a "PANELS" section)
- Remove the "More" text label from HeaderMenu
- Make the HeaderMenu gear icon bigger (36→44px) so users know it's tappable
- The trailing Row now has just: SpongeButton + HeaderMenu (much cleaner)

---

## Part C: Character Select + Gungeoneer Detail + Main Menu (Items 4, 5, 6)

**Agent:** Slot 3 (Planner-Architect) or Slot 4
**Branch:** `slot3-planner/char-select-detail`
**Files:**
- `lib/screens/main_menu_screen.dart` — remove How to Use button + method
- `lib/screens/character_select_screen.dart` — add 10% padding, remove "?" button, add long-press for detail
- `lib/screens/gungeoneer_detail_screen.dart` — fix loadout layout, add "Start Run" button, name+graphic on top

**Main menu (item 4):**
- Remove the "How to Use" TextButton and the `_showHowToUse` method and `_howToStep` widget
- Keep the version label

**Character select (item 5):**
- Add 10% padding around the grid (use `EdgeInsets.all(width * 0.10)` or `Insets.xl`)
- Remove the `Positioned` "?" button entirely
- Add `onLongPress` to the card → opens `GungeoneerDetailScreen`
- Keep tap = start run (or pick for MP)

**Gungeoneer detail (item 6):**
- Fix the 2-row issue: Weapons and Items are in separate `Wrap` sections with labels. Make them fit in ONE row by:
  - Removing the "Weapons" and "Items" sub-labels
  - Using smaller tiles (icon + name in a compact chip)
  - Using a single `Wrap` for all guns + items + armor
- Top of screen: just the gungeoneer name + graphic (no extra labels/fluff)
- Loadout tiles: use real gun/item icons from `GameIcon` widget, linkable to `ItemDetailScreen`
- Add a "PLAY AS [NAME]" button at the bottom (starts a run with this character)

---

## Part D: Settings + Codex + Map Icons (Items 8, 9, 10)

**Agent:** Slot 4 (Universal Worker) or Slot 1
**Branch:** `slot4-universal/settings-codex-maps`
**Files:**
- `lib/widgets/settings/settings_tab.dart` — remove DANGER ZONE collapsible, show END RUN + RESET full-width
- `lib/screens/codex_screen.dart` — fix left panel padding, show graphics always
- `lib/widgets/codex/ammonomicon_tabs.dart` — show tab icons at full opacity always (not dimmed when inactive)
- `lib/utils/asset_paths.dart` — add `gungeoneerMapIconPath()` function
- `lib/widgets/active_run/player_header.dart` — use map icon instead of sprite
- `lib/widgets/home/rotating_gungeoneer.dart` — use map icon (if applicable)
- `assets/images/gungeoneers/` — download 9 map icons from wiki
- `pubspec.yaml` — register new map icon assets

**Settings (item 8):**
- Remove the `_CollapsibleCard` wrapper for DANGER ZONE
- Show END RUN and RESET DATA as full-width buttons, always visible (no expand/collapse)
- Style: END RUN = red accent, RESET DATA = deep orange
- Both buttons get confirmation dialogs (already exist)

**Codex (item 9):**
- `_BookmarkTab`: show icon at full opacity even when inactive (remove `color.withValues(alpha: 0.6)` for inactive)
- Show the colored border at `alpha: 0.5` even when inactive (not `0.25`)
- Increase tab size: inactive 52→56, active 64→68
- Better padding: `left: 72` → `left: 80` for content area
- Add `Insets.sm` padding inside each tab for breathing room

**Map icons (item 10):**
- Download from wiki URLs:
  - `https://enterthegungeon.wiki.gg/images/Marine_map.png`
  - `https://enterthegungeon.wiki.gg/images/Pilot_map.png`
  - `https://enterthegungeon.wiki.gg/images/Convict_map.png`
  - `https://enterthegungeon.wiki.gg/images/Hunter_map.png`
  - `https://enterthegungeon.wiki.gg/images/Bullet_map.png`
  - `https://enterthegungeon.wiki.gg/images/Robot_map.png`
  - `https://enterthegungeon.wiki.gg/images/Cultist_map.png`
  - `https://enterthegungeon.wiki.gg/images/Paradox_map.png`
  - `https://enterthegungeon.wiki.gg/images/Gunslinger_map.png`
- Save to `assets/images/gungeoneers/[slug]_map.png`
- Add `gungeoneerMapIconPath(String name)` to `asset_paths.dart`
- Use in `player_header.dart` instead of the animated sprite
- Fallback to existing sprite if map icon not found

---

## Dependency Graph

```
Part A (MP Lobby)     ──────────────→ independent
Part B (Quick-Add)    ──────────────→ independent
Part C (Char Select)  ──────────────→ independent
Part D (Settings+Codex+Maps) ───────→ independent
```

All 4 parts can run in parallel. No file overlap between parts.

**Note on Part A + Part C overlap:**
- Part A touches `mp_lobby_screen.dart` which has a character preview card
- Part C touches `character_select_screen.dart` which is opened from the lobby
- These don't overlap in files, but the character picker behavior (long-press for detail, no "?") should be consistent. Part C changes the picker; Part A uses it. Run Part C first if sequential, or coordinate the `CharacterSelectScreen.multiplayerPick()` contract.

---

## Test Updates Required

- **Part A:** Update all MP tests (lobby, connect, integration, reliability) — remove PIN assertions
- **Part B:** Update `home_screen_test.dart` if toolbar changes affect it
- **Part C:** Update `character_select_screen_test.dart` (remove "?" button tests, add long-press tests), `main_menu_test.dart` (remove How to Use tests)
- **Part D:** Update `settings_screen_test.dart` (DANGER ZONE no longer collapsible), `codex_screen_test.dart` (tab visibility)

---

## Verification

After all parts merge:
1. `flutter analyze` — clean
2. `flutter test` — all pass
3. `flutter build web --release` — succeeds
4. Playwright: verify all screens render correctly
5. Playwright: verify quick-add flow (search → add → auto-clear)
6. Playwright: verify MP lobby (no PIN, role selection)
7. Playwright: verify Codex tabs (graphics always visible)
8. Playwright: verify Settings (END RUN + RESET full-width)
