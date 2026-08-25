# GungeonMate — Theme UX Assessment (2026 Designer Lens)

**Assessor:** XEENU-ANIMATOR (Slot 1)
**Date:** 2026-08-25
**Audited commit:** `fe1a16c` (master HEAD — "Fix experience_studio_screen compile error v1.9.62")
**Method:** Code-grounded audit of the full theme/visual system. Build attempted; screenshots reviewed from `docs/screenshots/` (2026-08-17/18 capture set).

---

## 0. Executive Summary

GungeonMate has an **ambitious, lore-rich theme system** — 32 enum themes (15 visible), 17 `AvatarAuraStyle` variants, 37 particle presets, 12 glow effects, 68 Google Fonts, 4 active-run display modes, ambient GLSL fragment shaders, a 12-layer composited `ThemeOverlay`, and a `ThemeLore` registry that re-skins stat labels per theme. This is genuinely **2026-grade in ambition**.

**But master HEAD does not compile.** The theme picker (Experience Studio) and the display-mode switcher are both broken. The last "fix" commit addressed one compile error and left seven more. No screenshot can be captured from a clean build today. This is the headline finding.

Below: the full assessment, ranked by severity.

---

## 1. CRITICAL — Build is broken (blocks all UX)

### 1.1 `splashSlug` getter is referenced but never defined
- **Files:** `lib/screens/experience_studio_screen.dart` lines 518, 521, 994, 996
- **Symptom:** `error G4127D1E8: The getter 'splashSlug' isn't defined for the type 'AppThemeMode'` (×4)
- **Root cause:** The v1.9.61 changelog/VERSION_HISTORY *claim* `AppThemeMode.splashSlug` was added as a getter mapping themes to asset slugs, and 14 splash JPGs exist in the working tree (`assets/images/themes/splash/*.jpg`, 1.7–8.6 MB each). But the getter was **never committed to `app_theme.dart`**. The `themeSplashPath()` helper in `asset_paths.dart` exists, but the enum getter that feeds it does not.
- **UX impact:** The Experience Studio — the primary theme-selection surface — will not build. Users cannot pick themes. This is the single most damaging UX defect: the entire theme system is unreachable.
- **Fix:** Add `String get splashSlug` to `AppThemeMode` (extension or in the enum), mapping each visible theme to its splash filename slug (`unicorn`, `forge_master`, `robots_core`, `cat_lady`, `moonlit_chamber`, `storm_caller`, `mr_robot`, `valor_of_marines`, `the_bullet`, `the_paradox`, `gunpowder`, `dragunfire`, `lichs_domain`, `custom`). Return `''` for hidden themes. Then commit the 14 splash JPGs (currently untracked in main WD).

### 1.2 `RunDisplayMode.matrix` — half-removed enum value
- **Files:** `lib/widgets/active_run/modes/run_display_mode_bar.dart` lines 187, 357, 429; `lib/services/app_theme.dart` line 1964
- **Symptom:** `error G42E56F65: The type 'RunDisplayMode' is not exhaustively matched by the switch cases since it doesn't match 'RunDisplayMode.matrix'` (×3)
- **Root cause:** `TECHNICAL_REFERENCE.md` §5 states "Matrix mode was removed in v1.9.62. `matrix_mode.dart` and `gungeon_matrix_rain.dart` deleted." The *files* were deleted (confirmed in `git status`), but the **enum value `matrix` was left in `RunDisplayMode`** (line 1964). Three switches in the mode bar don't handle it → non-exhaustive.
- **UX impact:** The display-mode switcher — the user's entry point to Classic/Codex/Compact/Signature modes — won't build. Even after fixing 1.1, this blocks the active-run screen.
- **Fix:** Remove `matrix` from the `RunDisplayMode` enum (line 1964) AND from the `RunDisplayModeX` extension's `label`/`description` switches (lines 1987–1988). Also bump the persisted pref key `_kRunDisplayMode` to `v3` since the index shifts again, or add a migration that clamps any persisted `matrix` index back to `classic`.

---

## 2. HIGH — Architectural / consistency issues

### 2.1 Dead code: `_PaletteStep` orphan
- **File:** `lib/screens/experience_studio_screen.dart` (~line 1089)
- **Issue:** The v1.9.62 "fix" commit message explicitly notes "`_PaletteStep` warning remains as user's dead code to clean up." This is the old 5-step wizard's palette step, left behind after the 4-tab redesign. It's a `flutter analyze` warning and a maintenance trap.
- **Fix:** Delete `_PaletteStep` and its call site in `_ThemeStep`.

### 2.2 `RunDisplayMode` enum vs. docs vs. code drift
- The enum has 5 values (`classic, codex, compact, matrix, signature`). The docs say 4. The mode bar handles 4. `player_page.dart` routing may also not handle `matrix`. This is a **three-way drift** between enum, docs, and consumers.
- **Fix:** Single source of truth. Remove `matrix` everywhere (enum + extension + docs already say 4). Run `grep -rn "RunDisplayMode.matrix"` to catch any remaining references.

### 2.3 17 hidden themes carry full `ThemeFlair` weight
- 17 of 32 enum values are not in `kVisibleThemes` (the legacy lore themes: `ammonomicon`, `hollowChill`, `lordJammed`, `theBreach`, `bulletHell`, `resourcefulRat`, `gungeonProper`, `theOubliette`, `pastParadox`, `highPriestVoid`, `cultOfGundead`, `synergySurge`, `glitchedChest`, `lichsTomb`, `winchestersGame`, `unicornII/III/IV`).
- Each has a complete hand-tuned `ThemeFlair` with ~25 color fields. They're unreachable from the picker but still consume enum space, appear in `kThemeParticleDefaults`, and complicate the `splashSlug` mapping.
- **UX impact:** No direct user impact (they're hidden), but it's cognitive debt for any future agent and bloats the splash mapping.
- **Recommendation:** Keep them (they're lore-rich and could be re-released), but document clearly that `kVisibleThemes` is the only list the picker reads. Add a `// HIDDEN — not in kVisibleThemes` comment block above the first hidden enum value.

### 2.4 Splash images untracked / uncommitted
- 14 JPGs (1.7–8.6 MB each, total ~44 MB) sit in `assets/images/themes/splash/` in the main working directory but are **untracked in git**. The `pubspec.yaml` declares the directory (line 124), so if they're not committed, a fresh clone or CI build has broken image references.
- **Fix:** `git add assets/images/themes/splash/*.jpg` and commit. Consider git-LFS given the size (44 MB of JPGs in a regular repo is heavy).

---

## 3. MEDIUM — UX polish gaps (2026 lens)

### 3.1 Experience Studio: Ambiance tab is a placeholder
- The 4-tab picker (Theme / Particles / Typography / Ambiance) has Ambiance falling through to a placeholder. Three of four tabs are functional; the fourth is empty.
- **UX verdict:** A 4-tab UI with one empty tab feels unfinished. Either implement Ambiance (glow intensity, glow color, dialogue haptics, text speed, shader toggle) or remove the tab and make it a 3-tab picker. Three complete tabs > four with a hole.

### 3.2 No live theme preview on the home screen
- The fullscreen preview in Experience Studio shows a sample scene (item card, stat chips, buttons, synergy glow, palette strip). Good. But there's no "apply and see on real home screen" — the user must Apply, exit, and judge. 2026 UX expectation: live preview that reflects the actual app shell, not just a mock scene.
- **Recommendation:** The `previewNotifier`/`displayedMode` mechanism already exists for live preview. Consider a "Preview on home" toggle that temporarily applies the theme to the real home screen for 5 seconds, then reverts.

### 3.3 Theme splash images: 2048×2048 JPGs at 55% opacity
- Each splash is a 2048×2048 Gemini-generated portrait shown at 55% opacity behind the preview. At 55% opacity over a dark scaffold, fine detail is lost. The splash is the **single most expressive asset** for selling a theme — it should be more prominent.
- **Recommendation:** In the fullscreen preview, show the splash at 70–85% opacity with a gradient scrim only at the bottom (for label readability), not a uniform dim. Let the art breathe.

### 3.4 68 fonts with no categorization in the picker
- `AppFont` has 68 values (pixel, sci-fi, serif, script, gothic, modern sans…). The settings Appearance tab exposes them as a "swipe font picker." 68 fonts in a flat swipe list is overwhelming.
- **Recommendation:** Group fonts by category (Pixel / Sci-Fi / Serif / Script / Gothic / Modern) with a category chip row. The descriptions already exist (`_googleFontDescriptions`) — use them as subtitles. A 2026 font picker is a categorized grid, not a 68-item swipe.

### 3.5 Particle preset count: 37 — no search/filter
- 37 `ParticlePreset` values is a lot to scroll. The Particles tab presumably lists them flat.
- **Recommendation:** Group by element (Fire / Ice / Cosmic / Tech / Cute / Glitch) or add a "themed" filter that shows only the current theme's default + related presets.

### 3.6 `ThemePreviewData` exists but is only for hidden themes
- `kThemePreviewData` (lines 1740–1939) has entries for `ammonomicon`, `theBreach`, `unicorn`, `unicornII/III/IV`, `forgeMaster`, `hollowChill`, `lordJammed`, `bulletHell`, `resourcefulRat`, `gungeonProper`, `theOubliette`, `pastParadox`, `highPriestVoid`, `robotsCore`, `cultOfGundead`, `synergySurge`, `glitchedChest`, `lichsTomb`, `winchestersGame`, `custom`.
- **Missing:** `minimalist`, `catLady`, `moonlitChamber`, `stormCaller`, `mrRobot`, `valorOfMarines`, `theBullet`, `theParadox`, `gunpowder`, `dragunfire`, `lichsDomain` — i.e. most of the *visible* themes. The preview data is keyed to the old theme set.
- **UX impact:** The Experience Studio preview scene for visible themes falls back to whatever default the preview widget uses, not the curated `ThemePreviewData`. Inconsistent preview quality across themes.
- **Fix:** Add `ThemePreviewData` entries for all 15 visible themes.

---

## 4. LOW — Refinements

### 4.1 `ThemeOverlay` lacks `RepaintBoundary` on the main particle field
- The touch-particle layer is wrapped in `RepaintBoundary` (line 363), but the main `ParticleField` (line 276) is not. Every particle frame repaints the full stack below it. On a 120Hz display with 16+ particles, this is avoidable GPU work.
- **Fix:** Wrap `particleBackdropBg` in a `RepaintBoundary` so the particle animation doesn't force the content layer to repaint.

### 4.2 `ThemeFlair` is a 25-field immutable record with no `copyWith`
- Adding a new flair knob requires updating `_hueShiftFlair` (lines 2399–2437) by hand — easy to forget a field, which silently breaks hue-shifted remixes.
- **Recommendation:** Add a `copyWith` to `ThemeFlair` and have `_hueShiftFlair` use it. Or generate the hue-shift via reflection/macro.

### 4.3 `kThemeParticleDefaults` includes hidden themes
- The map (lines 1487–1522) has entries for all 32 themes including hidden ones. Not harmful, but it implies a coupling that doesn't exist for hidden themes.
- **Recommendation:** Trim to visible themes only, or document that hidden entries are intentional for forward-compat.

### 4.4 Glow color palette: 12 fixed colors
- `VisualPrefs.glowColors` (lines 2785–2798) is a fixed 12-color list. The user can't pick a custom glow color. With a `custom` theme that lets users pick any palette, the glow being limited to 12 presets is a mismatch.
- **Recommendation:** Add a 13th "Custom" option that opens a color picker, or tie the glow color to the active theme's `glowPrimary` automatically.

### 4.5 `depthTiltIntensity` default 0.6 — no onboarding
- 2.5D inventory tilt is on by default at 0.6 intensity. New users see tiles tilt on tap with no explanation. 2026 UX: a one-time coach mark ("Tap and hold a tile — it tilts in 3D") would aid discoverability.

---

## 5. STRENGTHS (what's genuinely 2026-grade)

These deserve recognition — the system does a lot right:

1. **`ThemeOverlay` 12-layer composited stack** — base color → video vortex → shader → particles → ambient glow → content → vignette → readability scrim → page frame → edge drip → touch sparkles. This is a sophisticated scene-graph approach. Each layer is `IgnorePointer` where appropriate. The auto-glow (themes with `glowPrimary.a > 0.01` get 0.15 baseline glow) is smart — every theme "feels alive" out of the box.

2. **Theme-auto-binding of particles** — `kThemeParticleDefaults` + the overlay's `userOnDefault` check means selecting a theme auto-applies its signature particles without clobbering an explicit user choice. This is the correct precedence chain: explicit user > theme default > gungeonDust fallback.

3. **`ThemeLore` registry** — re-skinning stat labels (COOLNESS→TEMPER for Forge, →SPARKLE for Unicorn, →CHILL for Lich) is a delightful detail that makes Theme Signature mode feel like a *different app* per theme, not just a recolor. 14 entries with title/tagline/quote/element/decor/glyph.

4. **`_ThemeDecorPainter`** — 14 custom painters (embers, frost, sparkles, circuits, paws, moonlight, lightning, brass, blade, rift, powder, bone, tactical, custom) driving the Theme Signature background. Each is a `CustomPaint` on a `RepaintBoundary` with an 8-second repeating `AnimationController`. Performant and themed.

5. **Unicorn megapack** — 6 palettes in one theme (`cottonCandy/neon/dreamy/sunset/bubblegum/mulberry`) with per-palette particle colors. This is a clean way to offer variety without enum bloat. The migration logic (unicornII→unicorn+neon palette) preserves user prefs across versions.

6. **`AvatarAuraStyle` (17 styles)** — animated avatar borders (goldShimmerRing, pastelPulse, oxbloodBreath, frostRing, voidPulse, toxicOoze, forgeGlow, lichPurple, cosmicTemporal, catPawTrail, moonGlow, lightningArc, paradoxRift, dragunScale, tacticalRing, brassConic, none). Each theme has a recognizable aura "from across the room."

7. **Persistence & migration** — `VisualPrefs` has 30+ persisted fields with versioned keys (`_v1`, `_v2`), legacy key migration (`_kScaleLegacy` → `_kFontSize`), enum-index clamping on load, and the `RunDisplayMode` v2 index-shift migration. This is production-grade state hygiene.

8. **`RefreshableValueNotifier`** — solves the `ValueNotifier` no-op-on-equal-value problem (BUG-002) cleanly. Custom theme edits now trigger rebuilds via `refresh()`.

9. **Hue-shift remixes** — `kThemeRemixes` lets Forge Master have Ember/Magma/Inferno variants, Robot's Core have Rust/Arc Flash/Voltage, Minimalist have Graphite/Platinum/Charcoal/Obsidian — all via HSL hue shift or explicit flair. This is a cheap way to 4× the perceived theme count.

10. **`CustomThemeData.random()`** — 20 curated Gungeon-authentic color schemas + a lore name generator ("Angry Bulletkin", "Jammed Beholster"). The random custom theme is *on-brand*, not a random rainbow. Thoughtful.

---

## 6. Recommended Action Priority

| # | Action | Severity | Effort |
|---|--------|----------|--------|
| 1 | Define `splashSlug` getter on `AppThemeMode` + commit 14 splash JPGs | CRITICAL | Low |
| 2 | Remove `RunDisplayMode.matrix` from enum + extension; migrate pref key | CRITICAL | Low |
| 3 | Delete orphaned `_PaletteStep` | HIGH | Trivial |
| 4 | Implement or remove the Ambiance tab | MEDIUM | Med |
| 5 | Add `ThemePreviewData` for the 11 missing visible themes | MEDIUM | Med |
| 6 | Wrap main `ParticleField` in `RepaintBoundary` | LOW | Trivial |
| 7 | Categorize the 68-font picker | LOW | Med |
| 8 | Add `copyWith` to `ThemeFlair` | LOW | Low |
| 9 | Raise splash opacity in fullscreen preview to 75%+ | LOW | Trivial |

**Items 1 and 2 are blocking.** No screenshot can be captured, no theme can be picked, and no active-run display mode can be switched until they're fixed. Everything else is polish on a system that is architecturally sound.

---

## 7. Screenshot Status

- **Existing screenshots:** 28 PNGs in `docs/screenshots/` (captured 2026-08-17/18, v1.9.55-era) + 21 ad-hoc PNGs in repo root. These reflect an *older* build state and may not represent current master.
- **Fresh capture:** **Not possible.** Master HEAD (`fe1a16c`) fails to compile with 7 errors (see §1). A Windows debug build was attempted in an isolated worktree (`.worktrees/slot1-xeenu/gungeon_mate`) and failed at the `flutter_assemble` step.
- **Recommendation:** Fix §1.1 and §1.2, rebuild, then capture a fresh screenshot set covering: home (3 themes), Experience Studio (theme grid + fullscreen preview), each of the 4 display modes, settings Appearance tab, and the particle studio. The 2026-08-17 set is stale.

---

## 8. Files Audited

| File | Lines | Role |
|------|-------|------|
| `lib/services/app_theme.dart` | 3548 | Themes, ThemeFlair, VisualPrefs, AppTheme runtime, UnicornPalette, AppFont, RunDisplayMode, CustomThemeData |
| `lib/widgets/theme_overlay.dart` | 380 | 12-layer visual stack |
| `lib/widgets/active_run/modes/theme_lore.dart` | 286 | ThemeLore registry (14 entries) + ThemeDecor enum |
| `lib/widgets/active_run/modes/theme_signature_mode.dart` | 806 | Theme-adaptive run display + 14 decor painters |
| `lib/widgets/active_run/modes/run_display_mode_bar.dart` | 492 | Display mode switcher (BROKEN — §1.2) |
| `lib/screens/experience_studio_screen.dart` | ~1150 | 4-tab theme picker (BROKEN — §1.1) |
| `lib/widgets/particle_engine.dart` | — | 37 presets, 12 glow effects |
| `lib/widgets/settings/theme_visuals_tab.dart` | 468 | Settings Appearance tab |
| `lib/utils/asset_paths.dart` | 74 | `themeSplashPath()` helper |
| `pubspec.yaml` | — | shaders + splash asset declarations |

---

*End of assessment. Items 1–2 are the gate. Fix those, rebuild, and the theme system becomes assessable by screenshot again.*
