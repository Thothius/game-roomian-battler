# GungeonMate — Rework Lessons Learned & Design Standards

**Author:** XEENU-ANIMATOR (Slot 1)
**Date:** 2026-08-26
**Scope:** Consolidated learnings from the full Theme UX rework (Phases 1–6, A, B, B Fix, B Polish, B Fix 2) and Codex/Ammonomicon rework.
**Purpose:** Prevent repeating the same mistakes. Enforce what worked. Guide future UI/UX work.

---

## 0. The Big Picture — What We Did

This rework took the app from a broken, inconsistent, inaccessible state to a polished, contemporary companion app. The phases were:

1. **Phase 1:** Accessibility foundations (Semantics, reduced-motion, contrast utils)
2. **Phase 2:** Design tokens and typography system
3. **Phase 3:** Customization surface (VisualPrefs → UI controls)
4. **Phase 4:** Motion design (spring physics, staggered animations)
5. **Phase 5:** State design (loading/empty/error states)
6. **Phase 6:** Code health (dead code removal, analyzer clean)
7. **Phase A:** Home/Settings/navigation structural rework (4-tab bottom nav, Settings simplified)
8. **Phase B:** Themes screen rework (live preview, session-based Reset/Apply)
9. **Phase B Fix:** Themes UX rework with live preview and compact controls
10. **Phase B Polish:** Compact swipable grids, font scoping, glow boost, home polish
11. **Phase B Fix 2:** UI bug fixes (grid sizing, font uniformity) + Codex/Ammonomicon rework

---

## 1. MISTAKES WE MADE — Don't Repeat These

### 1.1 GridView inside PageView = broken sizing + gesture conflicts
**What happened:** The 2x4 swipable grids used `GridView.builder` inside `PageView.builder`. The GridView's internal sizing fought with the PageView's viewport, causing cards to be half-visible or clipped. The `GestureDetector` on taps competed with the PageView's swipe gesture, making items unpickable.

**Fix:** Replaced with `Wrap` of fixed-size containers (for color swatches) or explicit `Row` + `Expanded` layouts (for tile grids). No nested scrollable widgets inside PageView pages.

**Rule:** **Never nest `GridView` or `ListView` inside `PageView`.** Use `Wrap`, `Row`+`Expanded`, or `Column` with fixed-size children instead. If you need paging, build each page as a non-scrollable layout.

### 1.2 FittedBox with BoxFit.scaleDown = inconsistent visual sizes
**What happened:** Font preview and font pills used `FittedBox(fit: BoxFit.scaleDown)`. Different fonts have different x-heights, ascenders, and descenders. `scaleDown` only shrinks if text overflows the box — it never grows small-font-metric text to match large-font-metric text. Result: fonts appeared different sizes despite "same" fontSize.

**Fix:** Use `FittedBox(fit: BoxFit.contain)` inside a `SizedBox` with explicit height. `contain` scales both up and down to fill the box, normalizing visual size.

**Rule:** **Use `BoxFit.contain` in fixed-height containers for uniform visual sizing across variable-metric content.** `scaleDown` is for "shrink if too big" — not for "make everything the same size."

### 1.3 Font scoping was an afterthought
**What happened:** `AppTheme.setMode()` calls `VisualPrefs.setFont(themeFont)`, which globally applies the theme's curated font to the entire app — including Home, Settings, and NavigationBar. The user wanted fonts to only affect game content (ActiveRun, Browse, Codex). We had to retrofit `Theme(data:.copyWith(textTheme: GoogleFonts.montserratTextTheme(...)))` wrappers around Home, Settings, and Nav.

**Rule:** **Decide font scope BEFORE implementing font selection.** System chrome (home, nav, settings, menus) should always use a fixed system font. Game content surfaces use the user-selected font. Wrap chrome surfaces in a default-font `Theme` widget from the start.

### 1.4 Theme persistence used enum index — fragile to reordering
**What happened:** `AppTheme.setMode()` persists `AppThemeMode.values[m.index]`. When we reduced the visible theme list from 28 to 16, any persisted index pointing to a removed theme would load the wrong theme or crash. The migration code in `AppTheme.init()` had to handle this.

**Rule:** **Persist theme identity by name/string, not enum index.** If you must use index, always validate membership in the current visible list and migrate invalid values. Never assume enum order is stable across versions.

### 1.5 `_applyAndClose` was sync but `setMode` was async
**What happened:** The Apply button called `AppTheme.setMode(_previewMode)` without awaiting. The theme was set in memory but the SharedPreferences write might not complete before the screen popped, causing the theme to revert on next launch.

**Fix:** Made `_applyAndClose` async and awaited `setMode`.

**Rule:** **Always await persistence operations before navigation transitions.** A `pop()` that fires before `SharedPreferences.setInt` completes can lose data.

### 1.6 Long vertical walls of controls — the original sin
**What happened:** Every iteration of the Themes/Customization screen started as a long vertical scroll of categorized controls. Particle presets were 37 items in a grid. Color schemas were 16 chips in a Wrap. Glow effects were 11 items. The user repeatedly asked for compact, horizontal, swipable layouts.

**Rule:** **Compact first.** If a control list has more than 8 items, use paged/swipable grids (2x4 or 5x2) from the start. Don't build a long scroll and then fix it later. The user's default mental model is "swipe to see more," not "scroll forever."

### 1.7 Descriptions on picker items wasted space
**What happened:** Glow effect chips showed both a label and a blurb/description. This made each chip tall and the grid sprawling. The user explicitly wanted "only visual and title."

**Rule:** **Picker items show visual + label only.** Descriptions, blurbs, and help text go in a separate info/help affordance (tooltip, info icon, or dedicated help screen), not on every picker chip.

### 1.8 Settings duplicated the Themes/Customization surface
**What happened:** Settings had a reduced Themes tab that duplicated the Experience Studio's theme picker but with fewer controls. The user found this confusing — "no middle ground options in settings."

**Fix:** Removed the duplicate. Settings has Core only. Themes/Customization is a separate destination from Home.

**Rule:** **One control surface per feature.** If a feature has a rich customizer (Themes/Customization), don't duplicate a reduced version in Settings. Settings is for core app preferences, not feature subsets.

### 1.9 The home screen had unexplained empty space
**What happened:** The home screen used `Spacer(flex: 1)` + content + `Spacer(flex: 4)` + buttons + `Spacer(flex: 1)`. The 4-flex spacer created a huge empty gap between the logo and the menu buttons, making the screen feel broken.

**Fix:** Removed all spacers. Used `MainAxisAlignment.center` with consistent `SizedBox` spacing.

**Rule:** **Use explicit spacing, not flex spacers, for vertical layout.** Spacers are for keyboard-adaptive layouts, not for "pushing things apart on a static screen." If the screen looks like it has a hole, it does.

---

## 2. WHAT WORKED WELL — Keep Doing These

### 2.1 Session-based Reset/Apply model
The Themes/Customization screen uses a session model: changes are preview-only until Apply. Reset restores the original state. This is the correct pattern for any destructive or multi-field customization surface.

**Keep:** Session-based preview → Apply pattern for all customizers.

### 2.2 Live preview with all effects rendered
The live preview at the top of the Themes screen renders the actual `ThemeOverlay` + `ParticleField` + glow, so users see exactly what they'll get. The full-screen preview modal is swipeable between themes.

**Keep:** Always show a live, rendered preview — not a static screenshot or description. The preview must reflect all toggled settings.

### 2.3 Sticky headers for preview + controls
The Particles tab has a sticky header with the enable toggle + live particle preview. The Typography tab has a sticky font preview. These stay visible while scrolling controls.

**Keep:** Sticky preview + primary toggle at the top of any customization tab.

### 2.4 Page indicator dots for swipable grids
Small dots at the bottom of each swipable grid show which page you're on and how many pages exist. Simple, clear, non-intrusive.

**Keep:** Page indicators for any paged/swipable content.

### 2.5 Glowing CTA buttons
PREVIEW and APPLY buttons have `boxShadow` glow + text shadows. This makes them visually discoverable and emphasizes their importance.

**Keep:** Primary CTAs should glow. Secondary actions should be flat.

### 2.6 16 themes with graphics only
Reducing from 28 to 16 themes (all with splash artwork) made the picker feel curated and complete. No broken/empty theme tiles.

**Keep:** Only show themes that have complete visual assets. Incomplete themes stay in the enum for backwards compat but aren't picker-visible.

### 2.7 Glow boost with clamp
Glow intensity was boosted 3x by changing the multiplier from 0.6 to 1.8 with a `.clamp(0.0, 1.8)`. Low values stay usable, 100% is clearly visible, and the clamp prevents total washout.

**Keep:** Use `clamp()` on any intensity/opacity boost to preserve low-value usability while making max values meaningful.

### 2.8 Bottom navigation with 4 tabs + Themes separate
Inventory, Browse, Ammonomicon (Codex), Settings in the bottom nav. Themes/Customization is a separate destination from Home. This keeps the nav clean and gives Customization its own focused space.

**Keep:** 4-tab bottom nav. Customization is a destination, not a tab.

### 2.9 Custom 2-row tab layout for Gungeoneer detail
The standard `TabBar` with `isScrollable: true` created an inconsistent, horizontally-scrolling tab strip. The custom 2-row layout (Row 1: Loadout, Tips, Playstyle. Row 2: Lore, Spoilers) is uniform, premium, and all tabs are visible at once.

**Keep:** When you have 4-5 tabs, consider a fixed 2-row grid layout instead of a scrollable TabBar.

---

## 3. DESIGN STANDARDS — Enforce Going Forward

### 3.1 Layout
- **No nested scrollables inside PageView.** Use Wrap, Row+Expanded, or Column.
- **Compact first.** >8 items = paged/swipable grid (2x4 or 5x2).
- **Explicit spacing, not flex spacers** for static screens.
- **Sticky preview + primary toggle** at the top of customization tabs.
- **Page indicator dots** for all paged content.

### 3.2 Typography
- **System chrome uses Montserrat always.** Home, Settings, Nav, menus.
- **Game content uses user-selected font.** ActiveRun, Browse, Codex/Ammonomicon.
- **Uniform visual sizing:** `FittedBox(fit: BoxFit.contain)` in fixed-height `SizedBox`.
- **Font pills:** Fixed height (36px), `BoxFit.contain`, font name rendered in its own font.
- **Font preview:** Sticky header, 2 lines (primary + secondary), both in `FittedBox` + `SizedBox`.

### 3.3 Picker/Control Patterns
- **Picker items:** Visual + label only. No descriptions on chips.
- **Selected state:** Border + background tint + glow (for primary CTAs).
- **Touch targets:** Minimum 48dp where practical.
- **Icon-only controls:** Must have tooltips/semantics.

### 3.4 Theming
- **Use `flair.*` tokens**, not raw `Colors.white/black.withValues()`.
- **Glow intensity:** 1.8x multiplier with `.clamp(0.0, 1.8)`.
- **Theme persistence:** Validate membership in visible list, migrate invalid values.
- **One control surface per feature.** No duplicates in Settings.

### 3.5 State Management
- **Session-based preview → Apply** for customizers.
- **Await persistence before navigation transitions.**
- **Reset restores original state** without persisting.

### 3.6 Accessibility
- **Reduced motion:** Check `ReduceMotion.isEnabled(context)` before animations.
- **Contrast:** Use `ContrastUtils` for WCAG validation on text.
- **Semantics:** Label all icon-only controls.
- **Text scaling:** Respect system text scale, test at 1.3x.

### 3.7 Naming
- **Home menu:** Local Run, Multiplayer Run, Customization, Ammonomicon.
- **Bottom nav:** Inventory, Browse, Ammonomicon, Settings.
- **Codex left panels:** Gungeoneers, NPCs, Enemies, Bosses, Pickups, Objects, Rat, Dragun, Bullet Hell, Challenge.
- **Gungeoneer tabs:** Row 1: Loadout, Tips, Playstyle. Row 2: Lore, Spoilers.
- **Paradox and Gunslinger** are in the Gungeoneers view, not separate special pages.

---

## 4. REMAINING REWORK NOTES — Future Polish

### 4.1 Codex/Ammonomicon panels
The content panels (search bar, entry list, detail screens) still use the pre-rework styling. A deeper visual polish pass should:
- Make panels look crisp, premium, and easy to read.
- Ensure consistent card styling across all category lists.
- Polish the Ammonomicon tab strip (left edge bookmarks).
- Review the Gungeoneer grid tiles for visual consistency.

### 4.2 Active Run screen
The active run screen was touched in early phases but hasn't had a full 2026 polish pass. It should:
- Use the design tokens established in Phase 2.
- Apply the user-selected font (it's a game content surface).
- Get consistent card/panel styling with the rest of the app.

### 4.3 Browse screen
The Browse screen needs:
- Font scoping review (should use user-selected font).
- Consistent card styling.
- Empty/loading state polish.

### 4.4 Settings screen
Settings was simplified in Phase A but the card/section styling could be more premium. Consider:
- Collapsible section cards with smooth expand/collapse animation.
- Consistent icon + label + control layout per row.

### 4.5 Particle preset visuals
The `_PresetVisual` widget shows a color swatch strip + shape icon. It could be more representative — showing a mini particle preview or a more distinct visual per preset.

### 4.6 Theme overlay glow
The 3x glow boost is applied but the glow rendering itself (RadialGradient in ThemeOverlay) could be more sophisticated — consider animated drift, multi-color gradients, or per-theme glow shapes.

---

## 5. VERIFICATION CHECKLIST — Run After Every UI Change

1. `flutter analyze lib` — zero issues
2. `flutter test` — all tests pass
3. `flutter build web --release` — builds successfully
4. Browser preview at 390x844 (mobile) — check:
   - No overflows
   - Touch targets ≥48dp
   - Text readable at small sizes
   - Swipable grids work (swipe + tap)
   - Sticky headers stay pinned
   - Page indicator dots update
5. Check font scoping: change font in Customization → Home/Settings/Nav should NOT change
6. Check theme persistence: Apply theme → restart app → theme should persist
7. Check glow: set to 100% → should be clearly visible (3x)
8. Check reduced motion: enable reduced motion → animations should be disabled

---

## 6. FILE MAP — Key Files for UI/UX Work

| File | Purpose |
|------|---------|
| `lib/screens/experience_studio_screen.dart` | Themes/Customization screen (all tabs) |
| `lib/services/app_theme.dart` | Theme definitions, VisualPrefs, persistence |
| `lib/widgets/theme_overlay.dart` | Theme background + glow rendering |
| `lib/widgets/particle_engine.dart` | Particle presets, color schemas, glow effects |
| `lib/widgets/particles/ambient_glow.dart` | Ambient glow rendering |
| `lib/screens/main_menu_screen.dart` | Home screen (logo, menu buttons) |
| `lib/screens/home_screen.dart` | Bottom nav + tab container |
| `lib/screens/settings_screen.dart` | Settings (Core only) |
| `lib/screens/codex_screen.dart` | Ammonomicon (left panels + content) |
| `lib/screens/gungeoneer_detail_screen.dart` | Gungeoneer detail (2-row tabs) |
| `lib/screens/active_run_screen.dart` | Active run (game content surface) |
| `lib/screens/browse_screen.dart` | Browse (game content surface) |
| `lib/theme/tokens.dart` | Design tokens (colors, spacing, radii) |
| `lib/utils/contrast.dart` | WCAG contrast utilities |
| `lib/utils/reduce_motion.dart` | Reduced motion utilities |
| `lib/utils/fast_route.dart` | Page transition utilities |

---

## 7. COMMIT HISTORY — Rework Timeline

| Commit | Phase | Summary |
|--------|-------|---------|
| (various) | 1–6 | Accessibility, tokens, motion, states, code health |
| (various) | A | Home/Settings/nav structural rework |
| (various) | B | Themes screen rework (session model, live preview) |
| `778c09c` | B Fix | Themes UX rework — live preview, swipe, compact grids |
| `d709dba` | B Polish | Compact swipable grids, font scoping, glow 3x, home polish |
| `74b33c4` | B Fix 2 | UI bug fixes (grid sizing, font uniformity) + Codex rework |

---

*This document is the canonical reference for UI/UX decisions in GungeonMate. Update it when new patterns are established or new lessons are learned.*
