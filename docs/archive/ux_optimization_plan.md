# GungeonMate UX Optimization Gameplan

> Generated from a full Playwright screen tour (July 2026) covering every screen, dialog, and interaction flow.

---

## Current Screen Inventory (15 files, 8.7M total)

| Screen | Lines | KB | Status |
|--------|-------|----|--------|
| active_run_screen.dart | 7374 | 285 | **Megafile** — 20+ inline classes |
| item_detail_screen.dart | 3028 | 114 | **Megafile** — 15+ inline classes |
| browse_screen.dart | 1627 | 57 | Functional |
| settings_screen.dart | 1332 | 56 | Functional |
| multiplayer_lobby_screen.dart | 1325 | 48 | Functional |
| shrine_picker_screen.dart | 803 | 31 | Functional |
| settings_sheet.dart | 864 | 30 | **ORPHANED** — never imported |
| theme_picker_screen.dart | 796 | 29 | Functional |
| main_menu_screen.dart | 608 | 29 | Functional |
| stats_detail_screen.dart | 755 | 26 | Functional |
| effects_summary_screen.dart | 388 | 12 | **Hidden entry point** — tiny icon button |
| synergies_overview_screen.dart | 349 | 11 | **ORPHANED** — never imported |
| favourites_screen.dart | 291 | 10 | Functional (via Run Options only) |
| character_select_screen.dart | 208 | 7 | Functional |
| home_screen.dart | — | — | Shell / background host |

---

## Findings by Category

### A. Dead Code & Orphaned Screens

1. **`SynergiesOverviewScreen`** — fully built (349 lines, filter chip, expansion tiles, active/inactive synergy display) but **never navigated to** from anywhere. Players cannot see all their synergies in one place.
2. **`SettingsSheet`** (864 lines) — a bottom-sheet version of settings, **never imported or used**. `SettingsScreen` (the tabbed version) replaced it.
3. **Stale doc comment** in `settings_screen.dart:14-16` claims "Tab 3: Survival Help Directories & Tips" but only 2 tabs exist (`length: 2`).

### B. Navigation & Discoverability Issues

4. **Synergies Overview is invisible** — The SYN counter on the dashboard shows a number but tapping it does nothing. Players have no way to see *which* synergies are active or what they need.
5. **Effects Summary is hidden** — Accessible only via a tiny 16px `Icons.open_in_new` button inside an expandable effects section. Most users will never find it.
6. **Favourites has two entry points** — "My Favourites" in Run Options opens a full-screen `FavouritesScreen`, AND the Browse tab has a "Favs" tab showing the same empty state. Redundant.
7. **Run Options popup is a flat list** — 9 items in a vertical popup menu with no grouping. Shrine, Dice, Steal, Cursula, Reset, Co-op, End Run, Favourites, Help are all at the same visual weight despite very different importance levels.
8. **No back button on main menu** — The main menu has a button (ref e821/e846) with no label in the accessibility tree. Unclear what it does.

### C. Layout & Density Issues

9. **Active Run screen is extremely dense** — The Hunter's dashboard shows: header (name, 6 stat chips, 2 action buttons), Huntress HUD (3 tabs with tables), Damage Calculator, Guns section (2 guns with pickup/layout buttons), Items section, Add to Inventory button, and 3 bottom tabs — all in one scroll. No visual hierarchy separating "dashboard" from "inventory management".
10. **Settings Theme & Font tab is a long scroll** — 6 sections (Active Palette, Wallpaper Lab, Typography Tuning, Inventory Grid Tuning, Particle Overlay, Particle Count, Ambient Glow) all stacked vertically with no sub-navigation. User must scroll through everything to reach one control.
11. **Theme Picker shows one theme at a time** — Swipe-to-preview is nice for browsing, but there's no grid view for quick comparison. 10+ themes require 10+ swipes.
12. **Stats Detail (Curse) table is very tall** — The curse effect table shows all 10 rows (curse 0-10) with 6 columns each. On mobile, this is a very long scroll. No way to jump to a specific curse level.
13. **Browse list cards are information-dense** — Each card shows: Neckbear badge, quality tier, type, DPS, fire mode, sell price, synergy count. Good for power users but visually noisy for casual browsing.

### D. Duplication & Redundancy

14. **Theme controls exist in 3 places** — Settings → Theme & Font tab, Theme Picker screen (from main menu "Customize"), and the Theme Picker button inside Settings ("CHOOSE THEME PALETTE"). All three expose the same wallpaper, particle, and font controls.
15. **Favourites empty state duplicated** — `FavouritesScreen` and Browse "Favs" tab both show "No favourites yet / Tap the ♥ heart..." — same text, same logic, two separate widgets.
16. **"Reset Player 1 Items" appears twice** — In Run Options popup AND in Settings → Run Utilities → Inventory Maintenance. Same action, two entry points.
17. **"Add Player (Co-op)" in Run Options** duplicates Settings → Run Utilities → Multiplayer → "Add Co-op" button.

### E. Missing UX Patterns

18. **No search in Settings** — 6+ sections of controls with no search or filter. Hard to find a specific toggle.
19. **No quick-access toolbar on Active Run** — The most common actions (add item, add gun, use shrine) are buried in the Run Options popup. A bottom action bar or FAB would be faster.
20. **No undo on destructive actions** — "Reset Items", "End Run", "Steal Item" all have confirmation dialogs but no undo. A snackbar with undo would be safer.
21. **No onboarding/first-run experience** — New users land on the main menu with no guidance. The Help & Tips dialog exists but is buried in Run Options (only accessible during a run).
22. **No tab persistence** — Switching between Inventory/Browse/Settings tabs resets scroll position and filter state each time.

---

## Proposed Optimization Plan

### Phase 1: Quick Wins — Dead Code & Discoverability (Low effort, high impact)

| # | Task | Effort | Impact |
|---|------|--------|--------|
| 1.1 | **Wire up SynergiesOverviewScreen** — Make the SYN counter on the dashboard tappable to push this screen. It's already built, just orphaned. | 1 line | High — players finally see their synergies |
| 1.2 | **Delete SettingsSheet** (864 lines) — orphaned, replaced by SettingsScreen | Delete | Medium — removes 864 lines of dead code |
| 1.3 | **Fix stale doc comment** in settings_screen.dart | 1 line | Low |
| 1.4 | **Surface EffectsSummaryScreen** — Add a "View All Effects" button in the effects section header instead of the tiny icon | 1 widget swap | Medium |
| 1.5 | **Remove FavouritesScreen** — Use Browse "Favs" tab as the single entry point. Remove "My Favourites" from Run Options. | Delete + 1 line | Medium — removes redundancy |

### Phase 2: Run Options Reorganization (Medium effort, high impact)

| # | Task | Effort | Impact |
|---|------|--------|--------|
| 2.1 | **Group Run Options into categories** — Split the flat 9-item list into grouped sections: **Run Actions** (Shrine, Dice, Steal, Cursula), **Inventory** (Reset, Add Co-op), **Reference** (Favourites, Help), **Session** (End Run) | Restyle | High — much cleaner menu |
| 2.2 | **Add visual icons to Run Options** — Currently text-only buttons. Add leading icons for quick scanning. | Restyle | Medium |
| 2.3 | **Move "End Run" to bottom with danger styling** — Separate it from the action group with a divider and red accent. | Restyle | High — prevents accidental taps |

### Phase 3: Active Run Dashboard Restructure (High effort, high impact)

| # | Task | Effort | Impact |
|---|------|--------|--------|
| 3.1 | **Split Active Run into collapsible zones** — Header (always visible), Character HUD (collapsible), Damage Calc (collapsible), Inventory (always visible). Use `ExpansionTile` or a custom collapsible to let users focus on what matters. | Refactor | High |
| 3.2 | **Add a quick-action FAB or bottom bar** — "Add Item", "Add Gun", "Use Shrine" as persistent quick actions instead of buried in Run Options. | New widget | High |
| 3.3 | **Make SYN counter tappable** — Opens SynergiesOverviewScreen (pairs with 1.1) | 1 line | High |
| 3.4 | **Sticky mini-header on scroll** — When scrolling down through inventory, keep a slim version of the character name + key stats (DPS, Curse) pinned at top. | New widget | Medium |

### Phase 4: Settings Reorganization (Medium effort, medium impact)

| # | Task | Effort | Impact |
|---|------|--------|--------|
| 4.1 | **Add sub-section navigation to Settings** — Instead of one long scroll, use a horizontal scrollable chip bar: [Palette] [Wallpaper] [Typography] [Grid] [Particles] [Glow]. Tapping a chip scrolls to or expands only that section. | Refactor | High |
| 4.2 | **Deduplicate Theme controls** — Settings → Theme & Font should be a *launcher* that opens the Theme Picker for full customization, not a duplicate set of controls. Keep only "Active Palette" display + "Choose Theme" button in Settings. Move all wallpaper/particle/font sliders to Theme Picker only. | Refactor | Medium — reduces confusion |
| 4.3 | **Add Settings search** — A search bar at the top that filters to matching sections/toggles. | New widget | Medium |

### Phase 5: Browse & Theme Picker Polish (Medium effort, medium impact)

| # | Task | Effort | Impact |
|---|------|--------|--------|
| 5.1 | **Add grid view toggle to Browse** — Currently list-only. A 2-column grid would show more items per screen and reduce scrolling. Toggle between list/grid. | New widget | Medium |
| 5.2 | **Add theme grid view to Theme Picker** — Swipe-to-preview is nice but slow for 10+ themes. Add a "Grid" toggle showing all theme cards at once for quick comparison. | New widget | Medium |
| 5.3 | **Persist Browse tab + scroll position** — Save the active tab (All/Guns/Items/Favs), search query, and scroll offset when switching away from Browse. | State fix | Medium |
| 5.4 | **Add "compact mode" to Browse cards** — Hide DPS/fire-mode/sell-price on cards by default, show on tap/expand. Reduces visual noise for casual browsing. | Restyle | Low |

### Phase 6: Quality of Life (Low effort, medium impact)

| # | Task | Effort | Impact |
|---|------|--------|--------|
| 6.1 | **Add undo snackbar after destructive actions** — "Reset Items", "Steal Item", "Cursula Buy" should show a snackbar with "Undo" for 5 seconds. | New widget | Medium |
| 6.2 | **Move Help & Tips to main menu** — Currently only accessible during a run via Run Options. Add a "How to Play" button on the main menu for new users. | 1 button | Medium |
| 6.3 | **Add first-run onboarding hint** — On first launch, show 3-4 tooltip overlays highlighting: Start Run, Browse Database, Customize Theme, Changelog. | New widget | Medium |
| 6.4 | **Label the unlabeled main menu button** — The button at ref e821/e846 has no accessibility label. Investigate and add a semanticLabel. | 1 line | Low |

---

## Recommended Priority Order

1. **Phase 1** (Quick Wins) — 1-2 hours, immediately improves discoverability and removes dead code
2. **Phase 2** (Run Options Reorg) — 1-2 hours, high visual impact for every play session
3. **Phase 3** (Active Run Restructure) — 3-4 hours, the biggest UX win but most work
4. **Phase 4** (Settings Reorg) — 2-3 hours, reduces confusion from duplication
5. **Phase 5** (Browse Polish) — 2-3 hours, nice-to-have improvements
6. **Phase 6** (QoL) — 1-2 hours, polish layer

**Total estimated effort: 10-16 hours for all 6 phases.**

---

## Architecture Note

Phases 1-2 and 6 are standalone UX changes. Phases 3-4 should be coordinated with the existing `docs/reorg_plan.md` (splitting active_run_screen.dart and settings_screen.dart into smaller files). Doing the file split first would make the UX changes easier to implement and test.
