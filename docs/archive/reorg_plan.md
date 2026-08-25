# GungeonMate Codebase Reorganization Plan

## Status: ALL PHASES COMPLETE
Created: 2026-07-21
Last assessed: 2026-07-23

## Completed Phases
- ✅ Phase 1: `active_run_screen.dart` 9520→566 lines → 15 files (commit 05dc81d)
- ✅ Phase 2: `theme_overlay.dart` 951→312 lines → 8 files (commit 7c8012b)
- ✅ Phase 3: `item_detail_screen.dart` 3582→332 lines → 6 files (commit 84fd11f)
- ✅ Phase 4: `browse_screen.dart` 1638→1130 lines → 4 files (commit 54d69dc)
- ✅ Phase 5: `settings_screen.dart` 2390→64 lines → 6 files (commit dcf6891)

## Current Architecture Assessment

### File Size Heatmap (Top 10)

| File | Size | Lines | Classes | Verdict |
|------|------|-------|---------|---------|
| `screens/active_run_screen.dart` | 391KB | 9953 | 20+ | 🔴 CRITICAL — megafile (grew 40% since plan was written) |
| `screens/item_detail_screen.dart` | 134KB | 3582 | 15+ | 🔴 CRITICAL — megafile (grew 17%) |
| `services/app_theme.dart` | 101KB | 2462 | 1 enum | 🟡 BORDERLINE — single enum, hard to split cleanly |
| `screens/settings_screen.dart` | 102KB | ~2400 | 7+ | 🟡 BORDERLINE (grew 82% — was 56KB) |
| `screens/multiplayer_lobby_screen.dart` | 66KB | ~1600 | — | 🟡 BORDERLINE (grew 38%) |
| `providers/run_provider.dart` | 57KB | ~1400 | 1 | 🟢 OK — central state |
| `screens/browse_screen.dart` | 58KB | 1639 | 7+ | � BORDERLINE |
| `widgets/theme_overlay.dart` | 34KB | 1065 | 5+ | 🟢 OK — already split down from 105KB |
| `widgets/periodic_tile.dart` | 40KB | 999 | — | 🟢 OK — single complex widget |
| `services/multiplayer_session.dart` | 56KB | 1406 | 1 | 🟢 OK — single complex class |

### What's Already Good
- `models/` — 8 files, all <10KB, focused data classes
- `providers/run_provider.dart` — single class, central state, well-organized
- `services/` — 8 focused service files
- `utils/` — 3 tiny utility files
- Small screens: `character_select`, `effects_summary`, `favourites`, `home`, `main_menu`, `synergies_overview`

---

## Reorganization Plan

### Phase 1: Split `active_run_screen.dart` (285KB → ~15 files)

**Current contents (20+ classes in one file):**

| Class | Lines | Target File |
|-------|-------|-------------|
| `ActiveRunScreen` + `_ActiveRunScreenState` | ~600 | `screens/active_run_screen.dart` (slimmed) |
| `_PlayerSwitcher` | ~45 | `widgets/active_run/player_switcher.dart` |
| `_BigPlayerTab` | ~115 | `widgets/active_run/player_switcher.dart` (same file) |
| `_MpHeader` | ~600 | `widgets/active_run/mp_header.dart` |
| `_PlayerPage` + `_PlayerPageState` | ~800 | `widgets/active_run/player_page.dart` |
| `_TransferSheet` | ~55 | `widgets/sheets/transfer_sheet.dart` |
| `_RobotDashboardSliver` + State | ~483 | `widgets/dashboards/robot_dashboard.dart` |
| `_JunkanDashboardSliver` + State | ~337 | `widgets/dashboards/junkan_dashboard.dart` |
| `_GunderfuryDashboardSliver` + State | ~231 | `widgets/dashboards/gunderfury_dashboard.dart` |
| `_TripleGunDashboardSliver` + State | ~203 | `widgets/dashboards/triple_gun_dashboard.dart` |
| `_EvolverDashboardSliver` + State | ~208 | `widgets/dashboards/evolver_dashboard.dart` |
| `_EvolverStageSpec` | ~15 | `widgets/dashboards/evolver_dashboard.dart` (same file) |
| `_UniversalDamageCalculatorSliver` + State | ~260 | `widgets/dashboards/universal_damage_calculator.dart` |
| `_HuntressDashboardSliver` + State | ~545 | `widgets/dashboards/huntress_dashboard.dart` |
| `_BreakpointItem` | ~5 | `widgets/dashboards/huntress_dashboard.dart` (same file) |
| `_EffectsTile` + State | ~152 | `widgets/active_run/effects_tile.dart` |
| `_HeaderMenu` | ~509 | `widgets/active_run/header_menu.dart` |
| `_SectionHeaderSliver` | ~75 | `widgets/active_run/section_header_sliver.dart` |
| `_StatAdjusterSheet` | ~300 | `widgets/sheets/stat_adjuster_sheet.dart` |
| `_SortPickerSheet` | ~90 | `widgets/sheets/sort_picker_sheet.dart` |
| `_TileActionsSheet` | ~80 | `widgets/sheets/tile_actions_sheet.dart` |

**Key decisions:**
- Private classes (`_Foo`) must become public (`Foo`) when moved to separate files, OR use Dart's `part` directive to keep them private
- **Recommendation: Make them public.** Dart's `part` directive creates implicit coupling and makes navigation harder. Public classes with clear names are more maintainable.
- Naming convention: drop the underscore prefix, keep the descriptive name (e.g., `_RobotDashboardSliver` → `RobotDashboardSliver`)
- Each extracted file needs its own imports (flutter, provider, models, services, widgets)

**Import updates needed:**
- `active_run_screen.dart` will import all extracted files
- Any other file that imports `active_run_screen.dart` (only `home_screen.dart`) needs no change — it imports the screen, not the internal classes

### Phase 2: Split `theme_overlay.dart` (105KB → ~18 files)

**Current contents (20+ classes in one file):**

| Class | Lines | Target File |
|-------|-------|-------------|
| `ThemeOverlay` + State | ~380 | `widgets/theme_overlay.dart` (slimmed — wrapper + dispatch only) |
| `_TouchParticle` | ~7 | `widgets/particles/touch_particle.dart` |
| `_AmbientGlow` | ~95 | `widgets/particles/ambient_glow.dart` |
| `_GoldDust` | ~150 | `widgets/particles/gold_dust.dart` |
| `_Sparkles` | ~215 | `widgets/particles/sparkles.dart` |
| `_RedBreathDrip` | ~15 | `widgets/particles/red_breath_drip.dart` |
| `_CurseFog` + Painter | ~90 | `widgets/particles/curse_fog.dart` |
| `_CurseBreath` | ~50 | `widgets/particles/curse_breath.dart` |
| `_CrimsonDrip` | ~115 | `widgets/particles/crimson_drip.dart` |
| `_BrassMotes` | ~140 | `widgets/particles/brass_motes.dart` |
| `_IceCrystals` | ~175 | `widgets/particles/ice_crystals.dart` |
| `_WhiteDust` | ~140 | `widgets/particles/white_dust.dart` |
| `_ToxicBubbles` | ~135 | `widgets/particles/toxic_bubbles.dart` |
| `_PageFrame` | ~20 | `widgets/backgrounds/page_frame.dart` |
| `_ForgeEmbers` | ~155 | `widgets/particles/forge_embers.dart` |
| `_Hellfire` | ~130 | `widgets/particles/hellfire.dart` |
| `_CosmicRift` | ~145 | `widgets/particles/cosmic_rift.dart` |
| `_CustomParticleBackdrop` + Painter | ~300 | `widgets/particles/custom_particle_backdrop.dart` |
| `_HypnoticBg` + Painter | ~390 | `widgets/backgrounds/hypnotic_bg.dart` |
| `_SecretCatThroneOverlay` | ~20 | `widgets/easter_eggs/cat_throne.dart` |
| `_CuriousCatStareWidget` | ~90 | `widgets/easter_eggs/curious_cat.dart` |
| `_StillWallpaperBackground` | ~75 | `widgets/backgrounds/still_wallpaper.dart` |
| `_AnimatedWallpaperBackground` | ~130 | `widgets/backgrounds/animated_wallpaper.dart` |

**Key decisions:**
- `ThemeOverlay` stays in `theme_overlay.dart` — it's the dispatch hub that selects which particle system to render based on the active theme
- Each particle system is self-contained: it takes colors/params and renders. No cross-references between particle files.
- The `_TouchParticle` data class is shared by the custom particle backdrop — move with it or to a shared file.
- Many of these are `StatefulWidget`s with `TickerProviderStateMixin` — each needs its own imports for flutter, sensors, etc.

### Phase 3: Split `item_detail_screen.dart` (114KB → ~7 files)

**Current contents (15+ classes in one file):**

| Class | Lines | Target File |
|-------|-------|-------------|
| `ItemDetailScreen` + State | ~300 | `screens/item_detail_screen.dart` (slimmed) |
| `_Header` | ~190 | `widgets/item_detail/header.dart` |
| `_GunStats` | ~930 | `widgets/item_detail/gun_stats.dart` |
| `_EvolverStageSpec` | ~15 | `widgets/item_detail/gun_stats.dart` (same file) |
| `_StatGroup` | ~45 | `widgets/item_detail/gun_stats.dart` (same file) |
| `_StatPill` | ~140 | `widgets/item_detail/gun_stats.dart` (same file) |
| `_ItemBody` | ~897 | `widgets/item_detail/item_body.dart` |
| `_SynergiesSection` | ~45 | `widgets/item_detail/synergies_section.dart` |
| `_SynergyCard` | ~165 | `widgets/item_detail/synergies_section.dart` (same file) |
| `_SynergyChip` | ~120 | `widgets/item_detail/synergies_section.dart` (same file) |
| `_DestroyBanner` | ~75 | `widgets/item_detail/destroy_banner.dart` |
| `_QuickJumpButton` | ~40 | `widgets/item_detail/quick_jump_button.dart` |

### Phase 4 (Optional): Split `browse_screen.dart` (58KB → ~5 files)

| Class | Target File |
|-------|-------------|
| `BrowseScreen` + State | `screens/browse_screen.dart` (slimmed) |
| `_AnyEntry` | `widgets/browse/any_entry.dart` |
| `_Row` | `widgets/browse/browse_row.dart` |
| `_GunMeta` | `widgets/browse/gun_meta.dart` |
| `_ItemMeta` | `widgets/browse/item_meta.dart` |
| `_ToolbarButton` | `widgets/browse/toolbar_button.dart` |
| `FlipPageRoute` | `widgets/browse/flip_page_route.dart` |

### Phase 5 (Optional): Split `settings_screen.dart` (56KB → ~5 files)

| Class | Target File |
|-------|-------------|
| `SettingsScreen` + State | `screens/settings_screen.dart` (slimmed) |
| `_ThemeVisualsTab` | `widgets/settings/theme_visuals_tab.dart` |
| `_RunUtilitiesTab` + State | `widgets/settings/run_utilities_tab.dart` |
| `_SwipePicker` + State | `widgets/settings/swipe_picker.dart` |
| `_DangerTile` | `widgets/settings/danger_tile.dart` |

---

## Execution Strategy

### Approach: Part Files vs Public Classes

**Option A: Dart `part` directive**
```dart
// active_run_screen.dart
part 'active_run_screen/player_switcher.dart';
part 'active_run_screen/robot_dashboard.dart';
```
- Pros: Classes stay private (`_Foo`), no import changes needed
- Cons: Part files can't have their own imports — all imports must be in the main file. Creates a giant import block. IDE navigation is worse with parts.

**Option B: Public classes in separate files**
```dart
// widgets/dashboards/robot_dashboard.dart
class RobotDashboardSliver extends StatefulWidget { ... }
```
- Pros: Clean separation, each file has its own imports, IDE navigation works perfectly
- Cons: Classes become public (but they're only used by the parent screen, so the exposure is minimal), need to update imports in the parent screen

**Recommendation: Option B (public classes).** The import cleanliness and IDE navigation benefits outweigh the minor exposure concern. Dart doesn't have package-private visibility, so "public" just means "importable" — and nobody will import these outside the screen they serve.

### Execution Order

1. **Phase 1 first** (active_run_screen) — it's the biggest pain point and will immediately improve development velocity
2. **Phase 2** (theme_overlay) — second biggest, and particle systems are self-contained (low coupling risk)
3. **Phase 3** (item_detail_screen) — third priority
4. **Phase 4 & 5** (browse, settings) — optional, do when touching those screens for other reasons

### Safety Protocol

For each phase:
1. `git stash` before starting (safety net)
2. Extract classes one at a time: cut class from source, paste into new file, add imports, make public
3. Update imports in the source file
4. Run `flutter analyze` after each extraction
5. Run `flutter build web --release` + `/playwright-smoke` after completing each phase
6. Commit with `[Coder] refactor: extract [class name] from [source file]`
7. If anything breaks: `git stash pop` to restore

### Risk Assessment

- **Low risk**: Particle systems in theme_overlay are self-contained — they take params and render. No cross-references.
- **Low risk**: Dashboards in active_run are self-contained slivers — they read from RunProvider and render. Minimal cross-references.
- **Medium risk**: `_PlayerPage` and `_MpHeader` in active_run are tightly coupled to the parent screen's state (page controller, callbacks). May need callback props adjustments.
- **Medium risk**: `_ItemBody` in item_detail is 897 lines and may reference private methods from the parent state.
- **Mitigation**: Extract one class at a time, run `flutter analyze` after each, commit frequently.

---

## Target Directory Structure (After All Phases)

```
lib/
├── main.dart
├── models/                          # ✅ Unchanged (8 files)
├── providers/
│   └── run_provider.dart            # ✅ Unchanged
├── services/                        # ✅ Unchanged (8 files)
├── utils/                           # ✅ Unchanged (3 files)
├── screens/
│   ├── active_run_screen.dart       # ~600 lines (was 7059)
│   ├── browse_screen.dart           # ~900 lines (was 1554) [Phase 4]
│   ├── character_select_screen.dart # ✅ Unchanged
│   ├── effects_summary_screen.dart  # ✅ Unchanged
│   ├── favourites_screen.dart       # ✅ Unchanged
│   ├── home_screen.dart             # ✅ Unchanged
│   ├── item_detail_screen.dart      # ~300 lines (was 2942)
│   ├── main_menu_screen.dart        # ✅ Unchanged
│   ├── multiplayer_lobby_screen.dart# ✅ Unchanged
│   ├── settings_screen.dart         # ~100 lines (was 1282) [Phase 5]
│   ├── settings_sheet.dart          # ✅ Unchanged
│   ├── shrine_picker_screen.dart    # ✅ Unchanged
│   ├── stats_detail_screen.dart     # ✅ Unchanged
│   ├── synergies_overview_screen.dart # ✅ Unchanged
│   └── theme_picker_screen.dart     # ✅ Unchanged
├── widgets/
│   ├── active_run/                  # ← NEW (Phase 1)
│   │   ├── player_switcher.dart
│   │   ├── player_page.dart
│   │   ├── mp_header.dart
│   │   ├── effects_tile.dart
│   │   ├── header_menu.dart
│   │   └── section_header_sliver.dart
│   ├── dashboards/                  # ← NEW (Phase 1)
│   │   ├── robot_dashboard.dart
│   │   ├── junkan_dashboard.dart
│   │   ├── gunderfury_dashboard.dart
│   │   ├── triple_gun_dashboard.dart
│   │   ├── evolver_dashboard.dart
│   │   ├── huntress_dashboard.dart
│   │   └── universal_damage_calculator.dart
│   ├── sheets/                      # ← NEW (Phase 1)
│   │   ├── transfer_sheet.dart
│   │   ├── stat_adjuster_sheet.dart
│   │   ├── sort_picker_sheet.dart
│   │   └── tile_actions_sheet.dart
│   ├── particles/                   # ← NEW (Phase 2)
│   │   ├── touch_particle.dart
│   │   ├── ambient_glow.dart
│   │   ├── gold_dust.dart
│   │   ├── sparkles.dart
│   │   ├── red_breath_drip.dart
│   │   ├── curse_fog.dart
│   │   ├── curse_breath.dart
│   │   ├── crimson_drip.dart
│   │   ├── brass_motes.dart
│   │   ├── ice_crystals.dart
│   │   ├── white_dust.dart
│   │   ├── toxic_bubbles.dart
│   │   ├── forge_embers.dart
│   │   ├── hellfire.dart
│   │   ├── cosmic_rift.dart
│   │   └── custom_particle_backdrop.dart
│   ├── backgrounds/                 # ← NEW (Phase 2)
│   │   ├── hypnotic_bg.dart
│   │   ├── still_wallpaper.dart
│   │   ├── animated_wallpaper.dart
│   │   └── page_frame.dart
│   ├── easter_eggs/                 # ← NEW (Phase 2)
│   │   ├── cat_throne.dart
│   │   └── curious_cat.dart
│   ├── item_detail/                 # ← NEW (Phase 3)
│   │   ├── header.dart
│   │   ├── gun_stats.dart
│   │   ├── item_body.dart
│   │   ├── synergies_section.dart
│   │   ├── destroy_banner.dart
│   │   └── quick_jump_button.dart
│   ├── browse/                      # ← NEW (Phase 4, optional)
│   │   ├── any_entry.dart
│   │   ├── browse_row.dart
│   │   ├── gun_meta.dart
│   │   ├── item_meta.dart
│   │   ├── toolbar_button.dart
│   │   └── flip_page_route.dart
│   ├── settings/                    # ← NEW (Phase 5, optional)
│   │   ├── theme_visuals_tab.dart
│   │   ├── run_utilities_tab.dart
│   │   ├── swipe_picker.dart
│   │   └── danger_tile.dart
│   ├── theme_overlay.dart           # ~380 lines (was 2890)
│   ├── theme_engines.dart           # ✅ Unchanged
│   ├── animated_chat_bubble.dart    # ✅ Unchanged
│   ├── avatar_aura.dart             # ✅ Unchanged
│   ├── game_icon.dart               # ✅ Unchanged
│   ├── glass_container.dart         # ✅ Unchanged
│   ├── gungeoneer_header.dart       # ✅ Unchanged
│   ├── inventory_list_row.dart      # ✅ Unchanged
│   ├── mp_request_listener.dart     # ✅ Unchanged
│   ├── neckbear_medal.dart          # ✅ Unchanged
│   ├── periodic_tile.dart           # ✅ Unchanged
│   ├── quality_badge.dart           # ✅ Unchanged
│   ├── rich_link_text.dart          # ✅ Unchanged
│   ├── scale_button.dart            # ✅ Unchanged
│   ├── synergy_glow.dart            # ✅ Unchanged
│   ├── themed_number.dart           # ✅ Unchanged
│   ├── themed_section_title.dart    # ✅ Unchanged
│   ├── vertical_swipe_layout.dart   # ✅ Unchanged
│   └── wiki_sections.dart           # ✅ Unchanged
```

### File Count Impact

| Metric | Before | After |
|--------|--------|-------|
| `lib/` total files | 57 | ~90 |
| Largest file | 285KB (7059 lines) | ~600 lines |
| Files >50KB | 7 | 3 (app_theme, multiplayer_session, multiplayer_lobby) |
| Files >20KB | 15 | ~12 |
| Average file size | ~18KB | ~12KB |

---

## When to Execute

- **Phase 1** (active_run_screen): Execute when next touching active run features. The 285KB file is actively painful for any active run work.
- **Phase 2** (theme_overlay): Execute when next touching theme/particle systems. Self-contained, low risk.
- **Phase 3** (item_detail_screen): Execute when next touching item detail. Medium risk due to `_ItemBody` coupling.
- **Phase 4 & 5** (browse, settings): Execute opportunistically when already working on those screens.

**Do NOT execute all phases in one session.** Each phase is a full commit. Run `/playwright-smoke` after each phase to verify no regressions.
