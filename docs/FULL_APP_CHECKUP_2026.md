# GungeonMate — Full App Checkup (2026 Standards, Skill-Augmented)

**Assessor:** XEENU-ANIMATOR (Slot 1)
**Date:** 2026-08-25
**Audited commit:** `fe1a16c` (master HEAD)
**Skills applied:** `motion-design`, `beautify-flutter`, `flutter-animations`
**Method:** 4 parallel codebase audits + manual inspection + `flutter analyze`

---

## 0. Scorecard

| Dimension | Score (0–4) | Verdict |
|-----------|:-----------:|---------|
| **Theming** | 2 | Rich custom theme system, but no token extraction — 2,478 magic numbers, 929 inline TextStyles, zero TextTheme usage |
| **Typography & color** | 2 | 68 fonts well-categorized in Studio, flat in Settings. No WCAG contrast validation. Colors inline in 71 files |
| **States & interaction** | 2 | Good empty states, decent error states, but bare spinners (no skeletons), 66 helper-method widgets |
| **Platform & adaptivity** | 2 | Excellent responsive system + SafeArea (41 uses), but zero platform adaptation, zero keyboard support |
| **Motion & performance** | 3 | Excellent disposal, 187 haptics, 21 RepaintBoundaries, good easing. No reduced-motion. fastRoute is minimal |
| **Accessibility** | 0 | **1 Semantics widget in entire app.** No screen reader support. No reduced motion. No contrast checks |
| **Build health** | 0 | **7 compile errors on master HEAD. App does not build.** |
| **Total** | **11/28** | Significant work — strong foundation, blocked by build + accessibility |

---

## 1. CRITICAL — Build is broken (P0, blocks everything)

### 1.1 `splashSlug` getter missing (4 errors)
- **Files:** `experience_studio_screen.dart:518, 521, 994, 996`
- **Root cause:** v1.9.61 changelog claims the getter was added; it was never committed to `app_theme.dart`
- **Fix:** Add `String get splashSlug` to `AppThemeMode` extension, mapping 14 visible themes to splash slugs

### 1.2 `RunDisplayMode.matrix` zombie enum (3 errors)
- **Files:** `run_display_mode_bar.dart:187, 357, 429`; enum at `app_theme.dart:1964`
- **Root cause:** `matrix_mode.dart` was deleted but the enum value was left behind
- **Fix:** Remove `matrix` from enum + extension. Migrate persisted pref key to v3

### 1.3 Splash JPGs untracked
- 14 JPGs (~44 MB) in `assets/images/themes/splash/` are untracked in git
- **Fix:** `git add` them (consider git-LFS for size)

---

## 2. CRITICAL — Accessibility is essentially absent (P0)

| Issue | Count | Standard |
|-------|-------|----------|
| **Semantics widgets** | 1 (entire app) | Every interactive element needs a label |
| **Screen reader support** | 0 | TalkBack/VoiceOver users can't navigate |
| **Reduced motion** | 0 | `MediaQuery.disableAnimationsOf` not checked anywhere |
| **Keyboard navigation** | 0 | No Shortcuts/Actions, no tab navigation, no focus management |
| **WCAG contrast validation** | 0 | No contrast checks on any of the 15 theme palettes |
| **Tooltip coverage** | 12 | Hundreds of interactive elements lack tooltips |

**This is the biggest 2026 gap.** A companion app with 129 Dart files and 60,702 lines has 1 Semantics widget. The motion-design skill's quality checklist flags "missing reduced-motion alternative" as HIGH severity. The beautify-flutter skill's accessibility reference requires contrast ≥4.5:1 for body text.

**Plan:**
1. Add `Semantics` labels to all interactive elements (IconButton, InkWell, GestureDetector, ScaleButton)
2. Implement reduced-motion: check `MediaQuery.disableAnimationsOf(context)` in ThemeOverlay and collapse particles/ambient animations to static or instant
3. Add WCAG contrast validation to the theme system (compute contrast ratios in `app_theme.dart`)
4. Add keyboard support: `Shortcuts` + `Actions` for tab navigation, search focus, back navigation
5. Increase tooltip coverage on all icon-only buttons

---

## 3. HIGH — No design token system (P1)

### 3.1 Magic numbers everywhere
- **2,478 instances** of hardcoded `fontSize:`, `BorderRadius.circular()`, `EdgeInsets.all()`, `SizedBox(height/width:)`
- **Top offenders:** `compact_dashboards.dart` (71 fontSize), `multiplayer_lobby_screen.dart` (76 fontSize)
- **No `Insets`, `Radii`, `Motion` token classes exist**

### 3.2 Zero TextTheme usage
- **929 inline `TextStyle(` constructions** across the codebase
- **0 uses of `Theme.of(context).textTheme`**
- The app has a rich `ThemeFlair` color system but no typography scale
- Font sizes are scattered: 6, 7, 8, 9, 10, 10.5, 11, 12, 13, 14, 15, 16, 18, 20, 24, 28, 32, 56

### 3.3 Inline colors in 71 files
- 500+ `Colors.` references (excluding transparent/white/black) across 71 files
- 100+ `Color(0x...)` literals in widget code (excluding theme files)
- Particle engine (39 instances) is acceptable — it's a palette system

**Plan:**
1. Create `lib/theme/tokens.dart` with `Insets` (4/8/12/16/24/32/48/64), `Radii` (8/12/16), `Motion` (150/250/400ms) classes
2. Build a `TextTheme` in `app_theme.dart` with a deliberate type scale (body 14, label 12, title 18, headline 24, display 32)
3. Migrate inline colors to theme roles — `Theme.of(context).colorScheme.*` or `AppTheme.flair.*`
4. This is a large refactor — do it incrementally, file by file, starting with the worst offenders

---

## 4. HIGH — Motion: no reduced-motion, minimal transitions (P1)

### 4.1 Strengths (already 2026-grade)
- **107 AnimationControllers, all properly disposed** — excellent
- **187 haptic calls** with appropriate intensity mapping — excellent
- **21 RepaintBoundary** usages around all heavy animation — excellent
- **Easing: 98% easeOut/easeInOut** — only 1 `Curves.linear` on spatial movement (mode_picker_onboarding.dart:423)
- **Staggered animations** present in codex screens, character select, shrine picker (30-60ms delays)
- **Durations:** 70% in 100-300ms range — good discipline

### 4.2 Gaps
- **No reduced-motion support** — `MediaQuery.disableAnimationsOf` never checked. Particles, ambient shaders, touch sparkles, avatar auras all run unconditionally
- **`fastRoute` is a 150ms pure fade** — the minimum viable transition. The beautify-flutter skill recommends `SharedAxisTransition` for parent→child navigation and `FadeThroughTransition` for tab switches. A pure fade doesn't communicate spatial hierarchy
- **No spring physics** — only `BouncingScrollPhysics` in 10 scroll views. No `SpringDescription`/`SpringSimulation` for draggable/interruptible animations
- **No `PageTransitionsTheme`** configured in MaterialApp — platform defaults for non-fastRoute routes

**Plan:**
1. Add reduced-motion gate in `ThemeOverlay`: when `disableAnimations` is true, skip particle field, shader layer, touch sparkles, and collapse entrance animations to instant
2. Upgrade `fastRoute` to include a subtle slide (4-8px Y offset) + fade, or adopt `SharedAxisTransition` from the `animations` package
3. Add `PageTransitionsTheme` to MaterialApp for consistent platform transitions
4. Consider spring physics for depth-tile release and modal dismissals

---

## 5. HIGH — State design: skeletons missing, helper methods (P1)

### 5.1 Loading states
- **7 `CircularProgressIndicator` instances** — all bare centered spinners
- **Zero skeleton loaders** — the beautify-flutter skill says "skeletons make waits feel ~2× shorter than spinners; nothing at all under 300ms"
- `home_screen.dart:33` shows a bare spinner during initial data load — first impression is a spinner

### 5.2 Empty states (good)
- Consistent pattern: icon + descriptive text across browse, run log, codex modes, player page
- Context-aware messages ("No results for '$query'" vs "No guns or items to show")
- **Well done** — just needs a shared `EmptyState` widget to standardize

### 5.3 Error states (decent)
- Centralized in `RunProvider` with retry button
- MP session has detailed, context-specific error messages
- `home_screen.dart:53-72` uses `Icons.error_outline` + red color + retry button — functional but not designed
- No global error boundary for unhandled exceptions

### 5.4 Helper-method widget factories (anti-pattern #28)
- **66 `Widget _build` methods** across 30 files
- Top: `item_body.dart` (8), `experience_studio_screen.dart` (7), `gun_stats.dart` (6)
- These should be extracted to standalone widget classes for const support, independent rebuilds, and testability

**Plan:**
1. Add skeleton loaders for list/grid content (browse screen, codex screens, item detail)
2. Create a shared `EmptyState` widget (icon + title + subtitle + optional action)
3. Create a shared `ErrorState` widget with themed styling (not `Colors.red`)
4. Extract the top 10 helper-method offenders to widget classes (incremental)

---

## 6. MEDIUM — Customization surface gaps (P2)

From the prior `CUSTOMIZATION_AUDIT_2026.md`:

| Issue | Severity |
|-------|----------|
| 20 of 37 particle presets hidden from picker | HIGH |
| No live particle preview in Particles tab | HIGH |
| Glow blurbs + particle descriptions exist but aren't shown | HIGH |
| 6 orphaned VisualPrefs fields (shaders, dice, dashboards) | HIGH |
| Font picker divergent between Studio (categorized) and Settings (flat) | MED |
| Custom theme editor missing aura/font/name | MED |

---

## 7. MEDIUM — Platform adaptivity (P2)

- **Zero platform-specific code** — no `Platform.is*` checks, no `defaultTargetPlatform`
- The app is mobile-first but runs on Windows (video_player_media_kit is initialized)
- No iOS-specific back-swipe handling, no Android predictive back
- No desktop adaptations (mouse hover, keyboard navigation, dense layouts)
- **Responsive system is good** — Material 3 breakpoints, `ScreenProfile`, adaptive grid columns, 41 SafeArea uses

**Plan:**
1. Add `PageTransitionsTheme` with platform-aware builders (Cupertino for iOS, Material for Android)
2. Add hover states for web/desktop (the beautify-flutter skill requires this)
3. Add keyboard shortcuts for desktop (search, back, tab navigation)
4. Consider desktop-specific layouts for wide screens (the responsive system already supports this)

---

## 8. LOW — Code health (P3)

| Issue | Count | Notes |
|-------|-------|-------|
| `shrinkWrap: true` | 9 | Review for scrollable parent contexts |
| Static `Opacity` widgets | 6 | Replace with `Color.withValues(alpha:)` |
| `Widget _build` helper methods | 66 | Extract to widget classes (incremental) |
| `ElevatedButton` usage | 17 | Replace with `FilledButton` for M3 consistency |
| `WidgetStateProperty` usage | 2 | Add state-based styling to component themes |
| Large files | 6 files >1000 lines | `app_theme.dart` (3337), `mp_lobby_screen` (2753), `mp_session` (2493), `experience_studio` (2363), `particle_engine` (1815), `run_provider` (1568) |

---

## 9. WHAT WENT RIGHT (celebrate these)

The audit isn't all bad news. These are genuinely 2026-grade:

| Strength | Evidence |
|----------|---------|
| **AnimationController disposal** | 107 controllers, all properly disposed — zero leaks |
| **Haptic feedback** | 187 calls with appropriate intensity mapping (selection/light/medium/success) |
| **RepaintBoundary discipline** | 21 strategic usages around all heavy animation |
| **Easing choices** | 98% easeOut/easeInOut, only 1 linear-on-spatial (fixable) |
| **const usage** | 4,059 occurrences — strong const discipline |
| **Modern button vocabulary** | FilledButton/OutlinedButton/TextButton, zero deprecated buttons |
| **Modern APIs** | `WidgetStateProperty` (not MaterialStateProperty), `withValues(alpha:)` (not withOpacity), `TextScaler` (not textScaleFactor) |
| **Responsive system** | Material 3 breakpoints, ScreenProfile, adaptive grids, 41 SafeArea uses |
| **Staggered animations** | Well-tuned cascades (30-60ms) in codex/character/shrine screens |
| **Empty states** | Consistent icon + text pattern across all screens |
| **Theme system depth** | 15 visible themes, 37 particle presets, 68 fonts, 12 glow effects, ambient shaders, 4 display modes |
| **No ScreenUtil / designSize scaling** | Uses constraint-driven layout + Responsive.factor() |

---

## 10. PRIORITIZED PLAN

### Phase 0 — Unblock the build (P0, ~1 hour)
1. Add `splashSlug` getter to `AppThemeMode` in `app_theme.dart`
2. Remove `matrix` from `RunDisplayMode` enum + extension
3. Migrate persisted pref key for run display mode
4. Commit the 14 splash JPGs
5. `flutter analyze` clean → `flutter build windows` → `flutter build apk`
6. **Gate:** No other work proceeds until the app builds

### Phase 1 — Accessibility foundation (P0, ~1 session)
1. Add reduced-motion gate in `ThemeOverlay` (check `MediaQuery.disableAnimationsOf`)
2. Add `Semantics` labels to all `IconButton`, `InkWell`, `ScaleButton` widgets
3. Add `Semantics` to `GameIcon` and `PeriodicTile` (inventory items)
4. Add header semantics to section titles
5. Add WCAG contrast validation to theme system (compute ratios, warn if <4.5:1)
6. **Gate:** `flutter analyze` clean + manual screen-reader test

### Phase 2 — Design tokens (P1, ~2 sessions)
1. Create `lib/theme/tokens.dart` — `Insets`, `Radii`, `Motion` classes
2. Build a complete `TextTheme` in `app_theme.dart` with deliberate type scale
3. Migrate the worst-offender files first: `compact_dashboards.dart`, `multiplayer_lobby_screen.dart`, `item_body.dart`, `gun_stats.dart`
4. Replace inline `Color(0x...)` in widget code with `AppTheme.flair.*` or `ColorScheme.*` roles
5. **Gate:** `flutter analyze` clean + visual regression check

### Phase 3 — Motion upgrades (P1, ~1 session)
1. Upgrade `fastRoute` to fade + subtle slide (or adopt `animations` package transitions)
2. Add `PageTransitionsTheme` to MaterialApp
3. Fix the 1 `Curves.linear` on spatial movement
4. Replace 6 static `Opacity` widgets with `Color.withValues(alpha:)`
5. Add spring physics to `DepthTile` release
6. **Gate:** `flutter analyze` clean + motion review at `timeDilation = 5.0`

### Phase 4 — State design (P1, ~1 session)
1. Create `SkeletonLoader` widget for list/grid content
2. Create shared `EmptyState` widget (icon + title + subtitle + action)
3. Create shared `ErrorState` widget (themed, not `Colors.red`)
4. Replace bare spinners in `home_screen.dart`, `codex_screen.dart`, `experience_studio_screen.dart`
5. **Gate:** `flutter analyze` clean

### Phase 5 — Customization surface (P2, ~1 session)
1. Show all 37 particle presets, grouped by category
2. Add live `ParticleField` preview to Particles tab
3. Surface glow blurbs + particle descriptions in chips
4. Add shader toggle + preset picker to Ambiance tab
5. Replace Settings flat font picker with categorized grid
6. Add aura/font/name to custom theme editor
7. **Gate:** `flutter analyze` clean + visual check

### Phase 6 — Platform adaptivity (P2, ~1 session)
1. Add platform-aware `PageTransitionsTheme`
2. Add hover states for web/desktop
3. Add keyboard shortcuts for desktop (search, back, tab)
4. **Gate:** `flutter analyze` clean

### Phase 7 — Code health (P3, ongoing)
1. Extract top 10 helper-method offenders to widget classes
2. Review 9 `shrinkWrap: true` instances
3. Replace 17 `ElevatedButton` with `FilledButton`
4. Add `WidgetStateProperty` to component themes
5. **Gate:** `flutter analyze` clean

---

## 11. SKILL-DRIVEN RECOMMENDATIONS

### From `motion-design` (LottieFiles)
- **Motion Personality:** GungeonMate is "Energetic" (100-250ms, ease-out-expo, 15-30% overshoot) for gameplay moments and "Premium" (350-600ms, cubic-bezier(0.4,0,0.2,1), 0% overshoot) for chrome. Define this explicitly.
- **Brand Motion Identity:** Define 3 constants — signature easing, duration palette (150/250/400ms), entrance pattern
- **1/3 Rule:** Verify no motion travels >1/3 screen without a keyframe
- **Three motion layers:** Ensure every animated scene has primary + secondary + ambient layers

### From `beautify-flutter`
- **The Three Dials:** GungeonMate reads as VARIANCE=7 (art-directed per-theme), MOTION=7 (choreographed), DENSITY=5 (balanced). Define these explicitly.
- **Expressive register:** The app is "design IS the product" — permissions include committed color, display typography, custom painted moments. Run the slop test: would a design-literate user guess "Gungeon companion app → dark + neon + pixel font"? If yes, push further.
- **DESIGN.md:** Create a `DESIGN.md` at project root to persist design decisions across sessions

### From `flutter-animations`
- **Implicit vs explicit:** The app is 78% explicit (107 controllers) vs 22% implicit (30 widgets). This is appropriate for the rich animation system. Consider more implicit widgets for simple state changes (toggles, chip selections).
- **Hero animations:** Only 2 Hero tags (shrine_picker). Consider Hero transitions for item tiles → item detail (shared element transition = instant premium).
- **Physics-based:** Add `SpringSimulation` for draggable elements (depth tile, swipe cards)

---

*End of full app checkup. Pairs with `docs/THEME_UX_ASSESSMENT_2026.md` and `docs/CUSTOMIZATION_AUDIT_2026.md`.*
