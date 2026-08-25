# GungeonMate — Mega Critical UX/UI Unification Assessment

**Date:** August 2026  
**Author:** XEENU-ANIMATOR (Slot 1)  
**Scope:** Full app UX/UI audit across all 24 screens, 4 active-run modes, theme system, Experience Studio, and shared widget library.

---

## Executive Summary

GungeonMate has grown organically across multiple agent sessions. The core architecture is sound — `AppTheme.flair` drives theming, `VisualPrefs` persists user choices, `DepthTile` and `GameIcon` provide reusable 2.5D inventory rendering. But the UI layer has accumulated **inconsistencies in button patterns, container styling, text usage, and layout philosophy** that make the app feel like it was built by 4 different developers (because it was).

**Top 5 critical issues:**
1. Experience Studio is a 5-step wizard that fights the user — needs to be a tabbed picker with slide-in preview
2. 65 `GestureDetector` vs 19 `ScaleButton` — no consistent tap-feedback pattern
3. 522 hardcoded `Colors.white/black.withValues()` vs 337 `flair.*` references — theming is half-baked
4. Active-run modes (Classic/Codex/Compact/Signature) have no shared layout scaffold — each reinvents the wheel
5. No periodic-table-style grid system for inventory — layouts are ad-hoc per mode

---

## 1. Screen Inventory (24 screens)

| Screen | File | Purpose | State |
|--------|------|---------|-------|
| Home | `home_screen.dart` | Bottom-nav shell | OK |
| Main Menu | `main_menu_screen.dart` | Landing page with vortex, gungeoneer, menu | OK |
| Active Run | `active_run_screen.dart` | Run tracking with mode switching | Needs work |
| Character Select | `character_select_screen.dart` | Pick gungeoneer for new run | OK |
| Browse | `browse_screen.dart` | Browse guns/items/enemies/etc | OK |
| Codex | `codex_screen.dart` | Tabbed codex browser | OK |
| Codex Detail | `codex_detail_screen.dart` | Single entity detail | OK |
| Item Detail | `item_detail_screen.dart` | Item stats and synergies | OK |
| Gungeoneer Detail | `gungeoneer_detail_screen.dart` | Character detail | OK |
| Experience Studio | `experience_studio_screen.dart` | Theme/particle/font picker | **BROKEN UX** |
| Settings | `settings_screen.dart` | 2-tab settings | OK (recently unified) |
| Shrine Picker | `shrine_picker_screen.dart` | Track shrines used | OK |
| Stats Detail | `stats_detail_screen.dart` | Run stats breakdown | OK |
| Favourites | `favourites_screen.dart` | Saved items | OK |
| All Synergies | `all_synergies_screen.dart` | Synergy browser | OK |
| Synergies Overview | `synergies_overview_screen.dart` | Synergy summary | OK |
| Effects Summary | `effects_summary_screen.dart` | Active effects | OK |
| Multiplayer Lobby | `multiplayer_lobby_screen.dart` | MP connect/host | OK |
| Bullet Hell Codex | `bullet_hell_codex_screen.dart` | Codex sub-tab | OK |
| Challenge Mode Codex | `challenge_mode_codex_screen.dart` | Codex sub-tab | OK |
| Drake Codex | `drake_codex_screen.dart` | Codex sub-tab | OK |
| Gunslinger Codex | `gunslinger_codex_screen.dart` | Codex sub-tab | OK |
| Paradox Codex | `paradox_codex_screen.dart` | Codex sub-tab | OK |
| Rat Codex | `rat_codex_screen.dart` | Codex sub-tab | OK |

**Observation:** 7 codex sub-tab screens are near-identical StatelessWidget shells. Could be unified into a single parameterized widget.

---

## 2. Active-Run Display Modes

Current enum (after Matrix removal):
```
RunDisplayMode.classic    — Mode 0: original scroll view (default)
RunDisplayMode.codex      — Mode 1: leather-and-brass book
RunDisplayMode.compact    — Mode 2: tactical HUD
RunDisplayMode.signature  — Mode 3: theme-aware layout
```

**Critical issue:** Each mode is a completely independent widget with no shared scaffold:
- `player_page.dart` (1460 lines) — Classic mode
- `codex_book_mode.dart` (22K) — Codex mode
- `compact_run_mode.dart` (13K) — Compact mode
- `theme_signature_mode.dart` (25K) — Signature mode

**No shared layout contract.** Each mode reinvents:
- Character header rendering
- Gun/item list rendering
- Sort picker integration
- Synergy glow handling
- MP transfer sheet triggering
- Shrine panel integration

**Recommendation:** Extract a `RunModeScaffold` that provides the shared chrome (character header, sort pickers, shrine panel, MP transfer) and lets each mode only implement the inventory layout. This would cut ~40% of the code in each mode file.

---

## 3. Experience Studio — Current State (BROKEN)

**File:** `experience_studio_screen.dart` (2530 lines)

**Current layout:**
1. Top bar (back + title + reset)
2. Live preview (160px fixed height, always visible)
3. Step header (step number, description, progress bar, tappable chips)
4. Step content (AnimatedSwitcher between 5 steps)
5. Navigation bar (Back + Next/Apply)

**5 wizard steps:**
0. Theme — grid of 14 theme cards with splash images
1. Palette — variant picker (skipped if no variants)
2. Particles — preset, color schema, speed, glow
3. Typography — font family, size, weight
4. Ambiance — glow color, haptics, text speed

**Problems:**
- **Wizard pattern is wrong for this use case.** Users want to pick a theme and see it, not walk through 5 steps.
- **Live preview is always visible but tiny** (160px) — can't see the full effect.
- **Step navigation is confusing** — Palette step is conditionally skipped, breaking the mental model.
- **No way to quickly compare themes side-by-side.**
- **The preview shows a fake mini-scene** — not the actual app.
- **2530 lines in one file** — the step widgets should be separate files.

**User's requested redesign:**
- Picker area on top (tabs, not wizard steps)
- Preview as a side bookmark button
- Tapping the bookmark slides in a fullscreen preview
- Tap anywhere to go back to picker
- No scroll — fit the screen

---

## 4. Theme System

**`AppThemeMode` enum:** 14 visible themes + hidden variants (unicornII/III/IV, etc.)

**Flair system:** `ThemeFlair` provides scaffold, card, primary, secondary, headlineStat, glowPrimary, glowSecondary, bulletColor, bulletGlyph, chipRadius, cardRadius, dividerColor, auraStyle, headerGlyph, statGroupCombat/Handling/Meta.

**Theme switching:** `AppTheme.setMode()` + `AppTheme.previewNotifier` (ValueNotifier) for live preview in Experience Studio.

**Splash images:** 14 Gemini-generated splash portraits in `assets/images/themes/splash/`, wired via `AppThemeMode.splashSlug` getter.

**Assessment:** The theme system is well-architected. The flair pattern is correct — the problem is that **half the codebase ignores it** and uses hardcoded `Colors.white/black` instead.

---

## 5. Visual Pattern Inconsistencies

### 5.1 Button Patterns (CRITICAL)

| Pattern | Count | Where |
|---------|-------|-------|
| `GestureDetector` | 65 | Everywhere — no tap feedback, no haptics, no scale |
| `ScaleButton` | 19 | Experience Studio, main menu — has scale animation + haptics |
| `InkWell` | ~5 | Scattered |
| `TextButton`/`FilledButton` | ~10 | Dialogs, settings |

**Problem:** `GestureDetector` is the dominant tap pattern but provides zero visual feedback. `ScaleButton` exists and is better — but it's only used in 19 places.

**Recommendation:** Replace all tappable `GestureDetector` containers with `ScaleButton` (or a new `GoopTap` widget that wraps ScaleButton with default styling). This is the single biggest UX improvement available.

### 5.2 Container/Border Patterns

| Pattern | Count |
|---------|-------|
| `BorderRadius.circular` | ~400 |
| `BorderRadius.all` | ~5 |
| `BorderRadius.only` | ~30 |
| `BorderRadius.vertical/horizontal` | ~20 |

**Problem:** Radius values are hardcoded per-use (8, 10, 12, 14, 16, 20...). The `flair.chipRadius` and `flair.cardRadius` fields exist but are rarely used.

**Recommendation:** Use `flair.cardRadius` for all card containers and `flair.chipRadius` for all chip/badge containers. Define a `GoopRadius` constants class for non-themed radii.

### 5.3 Text Patterns

| Pattern | Count |
|---------|-------|
| `GoopText` | ~600 |
| `Text(` | ~400 |

**Problem:** `GoopText` is the themed text widget but `Text` is still used 400 times. Many `Text` usages have hardcoded styles that should use `flair.*` colors.

**Recommendation:** Audit all `Text(` usages and convert to `GoopText` where the text is user-visible. `Text` should only be used for debug/placeholder text.

### 5.4 Color Usage

| Pattern | Count |
|---------|-------|
| `flair.primary/secondary/headlineStat/scaffold/card` | 337 |
| `Colors.white.withValues()` | ~350 |
| `Colors.black.withValues()` | ~170 |
| Hardcoded `Color(0xFF...)` | ~2600 |

**Problem:** 522 `Colors.white/black.withValues()` calls are hardcoded alpha overlays that should use `flair.scaffold` or `flair.card` with alpha. The 2600 `Color(0xFF...)` literals include both theme flairs (correct — they're defining the palette) and hardcoded UI colors (incorrect — should use flair).

**Recommendation:** Replace `Colors.white.withValues(alpha: 0.X)` with `flair.scaffold.withValues(alpha: 0.X)` or a `flair.overlay` helper. This makes dark themes look correct instead of washing out to grey-white.

---

## 6. Navigation Patterns

| Pattern | Count |
|---------|-------|
| `fastRoute` | ~60 |
| `Navigator.push` | ~30 |
| `Navigator.of(context)` | ~25 |

**Assessment:** `fastRoute` is the standard and is used consistently. Navigation is fine.

---

## 7. Animation & Performance

| Pattern | Count |
|---------|-------|
| `flutter_animate` (`.animate()`) | 34 |
| `RepaintBoundary` | 19 |
| `AnimationController` | ~15 |
| `Haptics.*` | 186 |

**Assessment:** 
- `RepaintBoundary` usage is low (19) for an app with this much custom painting. Particle fields, vortex animations, and scrolling lists should all have `RepaintBoundary` wrappers.
- `flutter_animate` is used sparingly (34) — most transitions are manual `AnimatedContainer`/`AnimatedSwitcher`.
- Haptics usage is good (186) — well-distributed.

**Recommendation:** Add `RepaintBoundary` around every `ParticleField`, `CustomPainter`, and scrolling list. Use `flutter_animate` for entrance/exit transitions instead of manual `AnimationController` where possible.

---

## 8. Periodic-Table-Style Layouts (User Request)

The user wants "periodic table like layouts with solid style and CSS magic to show depth and textured panels in 2.5D."

**Current state:** `DepthTile` (17 references) provides 2.5D tilt + shadow for inventory tiles. It's used in all 4 active-run modes but with different grid configurations:

- **Classic:** `SliverGrid` with `SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 4)`
- **Codex:** `ListView` inside `PageView` — no grid
- **Compact:** 2-column `Row` with `Column` — manual layout
- **Signature:** `ListView` with `DepthTile` rows

**Recommendation:** Create a `PeriodicTableGrid` widget that:
- Uses `SliverGridDelegateWithMaxCrossAxisExtent` for responsive column counts
- Applies `DepthTile` 2.5D tilt to every cell
- Supports category-grouped sections (like periodic table blocks: s-block, p-block, etc.)
- Has textured panel backgrounds (gradient + noise + border)
- Shows quality-tier color coding on cell borders
- Animates cells in with staggered entrance
- Uses `RepaintBoundary` per cell

This would unify the inventory layout across all modes and give the "periodic table" feel.

---

## 9. Experience Studio Redesign Plan

### Current (broken):
```
┌─────────────────────────┐
│ TopBar (back, reset)    │
│ LivePreview (160px)     │ ← always visible, too small
│ StepHeader (progress)   │ ← wizard chrome
│ StepContent (scroll)    │ ← one step at a time
│ NavBar (back/next/apply)│ ← wizard navigation
└─────────────────────────┘
```

### Redesigned:
```
┌─────────────────────────┐
│ TopBar (back, apply)    │
│ TabBar                  │ ← Theme | Particles | Type | Ambiance
│ ┌─────────────────────┐ │
│ │ TabContent          │ │ ← fills available space, no scroll
│ │ (theme grid,        │ │
│ │  particle controls, │ │
│ │  font picker, etc.) │ │
│ │                     │ │
│ └─────────────────────┘ │
│                    [▶]  │ ← side bookmark button (right edge)
└─────────────────────────┘
        │
        │ tap [▶]
        ▼
┌─────────────────────────┐
│                         │
│   FULLSCREEN PREVIEW    │ ← slides in from right
│   (theme splash +       │
│    sample UI scene      │
│    in full glory)       │
│                         │
│   tap anywhere to close │
│                         │
└─────────────────────────┘
```

**Key changes:**
1. **Tabs replace wizard steps** — no Next/Back, no progress bar. User jumps to any section instantly.
2. **Palette tab removed** — fold palette variants into the Theme tab (tap a theme to expand its variants inline).
3. **Live preview removed from main layout** — replaced with a side bookmark button on the right edge.
4. **Fullscreen slide-in preview** — tapping the bookmark slides in a full-screen preview showing the theme splash + a rich sample UI scene. Tap anywhere to dismiss.
5. **No scroll** — each tab's content fits the screen. Use compact grids and sliders.
6. **Apply always visible** in the top bar — no need to walk to the end.

---

## 10. Action Items (Priority Order)

### P0 — Critical (do now)
1. **Experience Studio redesign** — tabs + slide-in preview (user explicitly requested)
2. **Fix borderRadius + non-uniform border crashes** — DONE this session
3. **Remove Matrix mode** — DONE this session
4. **Fix shrine button** — DONE this session

### P1 — High (next session)
5. **Unify button patterns** — replace GestureDetector with ScaleButton/GoopTap
6. **Create `PeriodicTableGrid` widget** — shared 2.5D inventory grid for all modes
7. **Extract `RunModeScaffold`** — shared chrome for all 4 active-run modes
8. **Add RepaintBoundary** around all ParticleField and CustomPainter usages

### P2 — Medium (future)
9. **Replace `Colors.white/black.withValues()` with flair-based overlays**
10. **Convert remaining `Text` to `GoopText`**
11. **Use `flair.cardRadius/chipRadius` consistently**
12. **Unify 7 codex sub-tab screens into a single parameterized widget**

### P3 — Low (polish)
13. **Define `GoopRadius` constants for non-themed radii**
14. **Increase `flutter_animate` usage for entrance transitions**
15. **Add textured panel backgrounds (gradient + noise) to cards**

---

## 11. File Size Hotspots

| File | Lines | Concern |
|------|-------|---------|
| `app_theme.dart` | 3563 | Theme system + VisualPrefs + all enums. Should split. |
| `experience_studio_screen.dart` | 2530 | All 5 steps + preview in one file. Should split. |
| `player_page.dart` | 1460 | Classic mode + all shared logic. Should extract scaffold. |
| `theme_signature_mode.dart` | ~700 | Single mode. OK but large. |
| `codex_book_mode.dart` | ~650 | Single mode. OK but large. |

---

## Conclusion

The app's bones are strong — the theme flair system, VisualPrefs persistence, DepthTile 2.5D rendering, and fastRoute navigation are all correct patterns. The problems are in the **execution layer**: inconsistent button feedback, hardcoded colors ignoring the theme system, no shared layout scaffold for active-run modes, and an Experience Studio that uses a wizard pattern when tabs would be 10x better.

The Experience Studio redesign is the highest-impact single change. The PeriodicTableGrid widget is the second. Together they would transform the app from "4 agents built this" to "one cohesive product."
