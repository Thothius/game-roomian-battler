# GungeonMate — Full App UX Assessment (2026)

**Author:** SUPPORT (Slot 4)
**Date:** 2026-08-27
**Scope:** Whole-app UX audit — weak points, bottlenecks, bugs.
**Method:** Static read-only audit. Mechanical greps (inline colors, deprecated APIs, shrinkWrap, designSize-scaling, template leftovers) + screen-by-screen reads against the `beautify-flutter` audit protocol and the project's own `docs/REWORK_LESSONS_LEARNED.md` standards.
**Verification:** ⚠️ **Degraded verification: static checks only.** No device run, no screenshots, no `flutter analyze`/`flutter test` execution. Findings are based on source reads and greps; visual/overflow claims should be confirmed on a device before acting.

---

## A. Verdict & Score

**Design Read:** Utility/expressive hybrid — a dark-neon Enter-the-Gungeon companion app. Curated 14 themes with splash artwork, custom-painted meters, session-based theme preview/Apply. Dials: `DESIGN_VARIANCE` 6, `MOTION_INTENSITY` 5, `VISUAL_DENSITY` 6.

**Audit score (0–4 per dimension, /20):**

| Dimension | Score | Notes |
|---|---|---|
| Theming | 2 | Tokens exist but are widely bypassed; `onSurface` hardcoded white → contrast failures on light fills (B2). |
| Typography & color | 2 | Type scale is well-built but ignored in screens (inline `fontSize`, sub-10px text). No light theme. |
| States & interaction | 3 | Skeleton loader, Retry on error, designed Browse empty state, reduced-motion + contrast utils exist. Active Run + Home empty/error states are bare. |
| Platform & adaptivity | 2 | `ScreenProfile` window-class helper is good scaffolding; `SafeArea` missing on a few screens; `MediaQuery.height * 0.x` fixed-ratio sizing; back-arrow bug on Settings tab. |
| Motion & performance | 3 | `IndexedStack` keeps all tabs alive; `shrinkWrap` in 7 spots; otherwise motion tokens + `RepaintBoundary` discipline present. |
| **Total** | **12/20** | "Significant work" band. Passes the slop test (designed, not default-generated) but theming consistency is the weakest axis. |

**Slop test:** Passes first-order (not guessable as "AI meditation/finance/AI app"). The curated themes + custom meters + Gungeon pixel-art identity give it a real signature. The failure mode is internal consistency, not template-ness.

---

## B. Bugs (confirmed, with file:line)

### B1 — Corrupted Unicode (mojibake) in user-facing strings [P0]

Encoding corruption (likely git autocrlf / PowerShell write) produced garbage glyphs in shipped strings:

| File:line | Shown | Should be |
|---|---|---|
| `lib/screens/active_run_screen.dart:69` | `'≡ƒÄ▓ Gunfortuna Challenge! ≡ƒÄ▓'` | `'🎲 Gunfortuna Challenge! 🎲'` |
| `lib/screens/active_run_screen.dart:565` | `'ADVANCED LIBRARY Γ₧ö'` | `'ADVANCED LIBRARY ➔'` |
| `lib/widgets/active_run/summary_tab.dart:73` | `'≡ƒº╜'` | `'🧽'` (tooltip confirms "Sponge") |
| `lib/widgets/active_run/summary_tab.dart:88` | `'≡ƒº╽'` | `'🧽'` |

Also in **doc-comments** (not user-visible, but should be cleaned): `lib/widgets/active_run/player_header.dart:202-207` — box-drawing chars replaced with `ΓööΓöÇ` etc.

**Why P0:** Users see literal garbage on screen. Trivial fix (replace the strings).

### B2 — White text hardcoded regardless of flair luminance [P0] *(root cause of U-002)*

`lib/services/app_theme.dart:4162-4168` — `themeFor()` always builds:
```dart
final scheme = ColorScheme.dark(
  primary: f.primary,
  secondary: f.secondary,
  surface: f.card,
  onSurface: Colors.white,                    // ← always white
  onSurfaceVariant: Colors.white.withValues(alpha: 0.7),
);
```
Any flair with a light `card`/`primary` fill (yellow PLAY AS gradient, light-theme role cards, light accent buttons) gets white text → contrast < 4.5:1. This is the systemic source of the user-reported **U-002** ("btn's maybe a bit bright to see labels on when btn is lighter colored and font inside is white").

**Fix options:** (a) derive `onSurface` from surface luminance via `ContrastUtils`; (b) guarantee all flairs use dark surfaces (clamp luminance); (c) compute a contrast-correct on-color per flair. The `ContrastUtils` helper already exists at `lib/utils/contrast.dart` — use it.

### B3 — Settings tab back arrow exits the app [P1]

`lib/screens/settings_screen.dart:27-31` — AppBar `leading` calls `Navigator.of(context).maybePop()`. But Settings is rendered as a **bottom-nav tab inside `IndexedStack`** (`lib/screens/home_screen.dart:116`), not a pushed route. The back arrow is meaningless on a tab and on Android pops the `HomeScreen` → exits the app. The `HomeScreen` already has a `PopScope` that redirects non-Inventory tabs back to Inventory (`home_screen.dart:129-139`), so the Settings back arrow is both redundant and wrong.

**Fix:** Remove the `leading` IconButton, or gate it on a `showBackButton` flag like `BrowseScreen`/`CodexScreen` do.

### B4 — Em-dashes in UI strings [P3]

`lib/screens/active_run_screen.dart:139` → `'Not connected — can't send emote'`. The project's beautify-flutter rules ban em-dashes in generated strings (restructure with a period/comma/colon). Likely other instances across the codebase — a quick grep pass when fixing.

---

## C. Weak Points (UX / design consistency)

### W1 — Widespread inline colors bypass the token system [P1]

The team built `lib/theme/tokens.dart` (`Insets`/`Radii`/`Motion`/`FontSizes`/`TypeScale`) and `ThemeFlair`, but screens ignore them. Grep counts (capped at 60 each):

- **~60+ `Color(0xFF...)` / `Color.fromARGB` / `Color.fromRGBO`** in screen/widget files.
  - `lib/widgets/gungeoneer_header.dart` (14 matches — synergy/curse glow colors, quality-tier palette)
  - `lib/screens/codex_screen.dart:70-135` (10 hardcoded hex category colors that never adapt to the active theme)
  - `lib/screens/codex_detail_screen.dart:115-124`, `lib/widgets/rich_link_text.dart` (7), `lib/widgets/item_detail/gun_stats.dart` (8), `lib/widgets/item_detail/header.dart` (6), `lib/screens/gungeoneer_detail_screen.dart` (6), `lib/widgets/active_run/player_header.dart` (3), `lib/screens/experience_studio_screen.dart:1236`, `lib/widgets/home/home_customization_sheet.dart:176`
- **~60+ `Colors.*`** matches.
  - `lib/widgets/active_run/player_page.dart` (23 — `Colors.white`, `Colors.amberAccent`, `Colors.greenAccent`, `Colors.redAccent`)
  - `lib/screens/mp_lobby_screen.dart` (21), `lib/widgets/mp_reconnect_banner.dart` (15), `lib/screens/mp_connect_screen.dart`, `lib/screens/main_menu_screen.dart`

**Why it matters:** This is *why* B2/U-002 exist and why theme switches look inconsistent. Codex category colors are the clearest example — 10 hex values baked into the screen that ignore the active flair. Fix: route through `ThemeFlair`/`ColorScheme` roles; only theme-defining files (`app_theme.dart`, `tokens.dart`) should hold raw hex.

### W2 — Inline numeric `fontSize` ignores `FontSizes` / `TypeScale` [P2]

~50+ inline numeric `fontSize` literals in screens. Highlights:
- `lib/widgets/active_run/player_page.dart` — 13, 11, 14.5, 9.5, 9
- `lib/widgets/gungeoneer_header.dart` — 8.5, 10.5, 11.5, 8, 13
- `lib/widgets/active_run/active_run_helpers.dart` — 13, 11, 15, 9, 12
- `lib/widgets/rich_link_text.dart` — 12.5, 13.5, 10.5, 13
- `lib/screens/mp_lobby_screen.dart` & `mp_connect_screen.dart` — `fontSize * sf` scaled values

**Sub-10px text** (8, 8.5, 9, 9.5) risks readability at 1.3× system text scale. The `FontSizes` constants (10–32) and `TypeScale` templates exist precisely to prevent this. Fix: replace inline literals with `FontSizes.*` / `TypeScale.*` references.

### W3 — No light theme / no `themeMode` [P2]

`lib/main.dart:102` sets only `theme:` (no `darkTheme:`/`themeMode:`). `themeFor()` always returns `ColorScheme.dark`. The app is dark-only — which is a legitimate design choice for a Gungeon companion — *but* flairs can still produce light fills (see B2). Two coherent paths:
1. **Commit to dark-only** and clamp flair surface luminance so no fill gets bright enough to break white text. Simplest.
2. **Implement a real light scheme** and respect the system theme preference.

Currently it's neither: dark-only intent, but flair-driven light fills leak through and break contrast.

### W4 — Bare / undesigned empty & error states [P2]

| Screen | File:line | State |
|---|---|---|
| Active Run (no character) | `lib/screens/active_run_screen.dart:350-353` | `Center(child: GoopText('No inventory loaded'))` — bare text, no next action, no illustration |
| Home (error) | `lib/screens/home_screen.dart:67-86` | Raw `'Error: ${runProvider.error}'` + Retry button. Functional but exposes internal error text; no illustration/next-action design |
| Home (loading) | `lib/screens/home_screen.dart:34-50` | SkeletonLoader — ✅ good |

**Model to follow:** `lib/screens/browse_screen.dart:470-496` has a properly designed empty state (themed icon, message that adapts to query vs. no-data, centered padding). Apply that pattern app-wide.

### W5 — `shrinkWrap: true` inside scrollables [P2]

7 occurrences — each needs a per-case check (short fixed lists are fine; long lists are a perf tell):
- `lib/screens/experience_studio_screen.dart:602`
- `lib/widgets/settings/settings_tab.dart:362`
- `lib/screens/stats_detail_screen.dart:821`
- `lib/widgets/settings/theme_visuals_tab.dart:324`
- `lib/widgets/home/home_customization_sheet.dart:198`
- `lib/widgets/active_run/starter_hint.dart:123`
- `lib/widgets/dashboards/dashboard_swiper.dart:239`

### W6 — `MediaQuery.size.height * 0.x` fixed-ratio sizing [P3]

Flagged fingerprint (breaks on short screens with keyboard):
- `lib/screens/item_detail_screen.dart:169` — `height: MediaQuery.of(context).size.height * 0.5`
- `lib/widgets/sheets/damage_calc_sheet.dart:44` — `maxHeight: ... * 0.75`
- `lib/screens/active_run_screen.dart:504` — quick-add sheet `height: ... * 0.55`

Prefer constraint-driven sizing (`LayoutBuilder` / `minHeight` / `maxHeight` from `ScreenProfile`).

### W7 — `Responsive.factor` width-only scaling compounds with system text scale [P3]

`lib/utils/responsive.dart:28` multiplies metrics by a width factor (clamped 0.85–1.25). `lib/main.dart:118` *also* applies `prefs.textScaleFactor`. Combined with inline `fontSize * sf` in `mp_lobby_screen`/`mp_connect_screen`, font sizes can over/under-shoot at 320dp + 1.3× text scale. Clamping makes this safer than raw `*0.x`, but the compounding is still a risk worth a test pass.

### W8 — Missing `SafeArea` on several screen bodies [P3]

- `lib/screens/character_select_screen.dart` — body `Column` has no `SafeArea` (grid can sit under the gesture-nav inset on edge-to-edge Android).
- `lib/screens/settings_screen.dart` — body relies on `SettingsTab` for its own padding.
- `lib/screens/codex_screen.dart` — body unverified in this pass.

AppBar handles the top inset only. Bottom inset (gesture nav) needs explicit `SafeArea` on bodies that fill the screen.

---

## D. Bottlenecks (perf / architecture)

### P1 — `IndexedStack` keeps all 4 tabs alive [P2]

`lib/screens/home_screen.dart:142` — `ActiveRun`, `Browse`, `Codex`, `Settings` are all built and held in memory from the moment a run starts. Codex parses 5 JSON files on mount (`codex_screen.dart:151-159`) even if the user never opens the Codex tab. Consider a lazy `IndexedStack` (build each child on first visit, then keep alive) or `PageView` + `AutomaticKeepAliveClientMixin`.

### P2 — Giant god-files [P2]

| File | Lines | Holds |
|---|---|---|
| `lib/services/app_theme.dart` | 3535+ | Themes, `VisualPrefs`, persistence, flairs, custom-theme store, `themeFor`, weight-bias — all in one |
| `lib/providers/run_provider.dart` | 1762 | All run state, shared state, restore, lifecycle |

Maintenance/review bottleneck and a merge-conflict magnet for parallel agents (the AGENTS.md AC4 file-lock system exists *because* of this). Splitting `app_theme.dart` into `theme_definitions.dart` / `visual_prefs.dart` / `custom_theme_store.dart` / `theme_builder.dart` would reduce collision surface significantly.

### P3 — Orphaned / dead code [P3]

- `_PaletteStep` in `lib/screens/experience_studio_screen.dart` — analyzer warning per tech ref; orphaned from the 5-step→4-tab redesign.
- `lib/widgets/settings/run_log_screen.dart` — no longer imported anywhere (tech ref §5 notes this).
- `RunDisplayMode` enum + related `VisualPrefs` fields may remain after all mode widgets were deleted in v2.0.2–v2.0.3 (tech ref §5: "The `RunDisplayMode` enum and related VisualPrefs fields may still exist but the mode widgets are gone").
- `lib/widgets/active_run/player_header.dart:202-207` mojibake doc-comments.

Dead code inflates analyzer noise, confuses future agents, and bloats the god-files. A `/cleanup` sweep (Slot 4's specialty) is the right tool.

---

## E. What's Working Well (keep doing)

- **Tokens file** (`lib/theme/tokens.dart`) — `Insets`/`Radii`/`Motion`/`FontSizes`/`TypeScale` is well-structured; `buildAppTextTheme` is colorless (correct pattern, prevents theme-switch color bleed).
- **Browse screen** — designed empty state, `prototypeItem` for scroll dims, `keyboardDismissBehavior` on drag, `didUpdateWidget` clears search on tab switch. Model citizen.
- **SkeletonLoader** for loading; **Retry** button on home error.
- **`ScreenProfile`** window-class helper (compact/medium/expanded/large) — real adaptivity scaffolding, height-aware.
- **Reduced-motion** (`lib/utils/reduce_motion.dart`) + **contrast utils** (`lib/utils/contrast.dart`) exist and are wired into the standards doc.
- **Session-based preview → Apply** for themes; live rendered preview (not screenshots).
- `debugShowCheckedModeBanner: false` ✅; MP reconnect banner + request listener wired.
- **105 tests passing** with CI on every push.
- **No deprecated APIs** in production code — the only `textScaleFactor` hit is a custom getter on `VisualPrefs` (legitimate), not the deprecated framework property. No `MaterialStateProperty`/`surfaceVariant`/`withOpacity`/`CardTheme(` leakage.
- **No template leftovers** — no `flutter_application`/`deepPurple` seed (the one `deepPurpleAccent` hit is a semantic curse-tier color in `periodic_tile.dart`, not a theme seed).

---

## F. Recommended Fix Order (if remediation is wanted)

| # | Item | Priority | Effort | Unblocks |
|---|---|---|---|---|
| 1 | **B1** — fix mojibake strings (4 lines) | P0 | trivial | — |
| 2 | **B2/U-002** — onSurface luminance via `ContrastUtils` | P0 | small | W1, W3 |
| 3 | **B3** — remove/gate Settings back arrow | P1 | trivial | — |
| 4 | **W1** — inline-color sweep → flair/tokens | P1 | medium | W3 |
| 5 | **W4** — empty/error states app-wide (Browse as model) | P2 | medium | — |
| 6 | **P1** — lazy `IndexedStack` / keep-alive | P2 | small | — |
| 7 | **W2** — inline `fontSize` → `FontSizes`/`TypeScale` | P2 | medium | — |
| 8 | **P3** — dead-code sweep (`_PaletteStep`, `run_log_screen`, `RunDisplayMode`) | P3 | small | P2 |
| 9 | **W5/W6/W7/W8** — shrinkWrap audit, fixed-ratio sizing, SafeArea, scaling test pass | P3 | medium | — |
| 10 | **B4** — em-dash sweep | P3 | trivial | — |

Items 1–3 are quick wins with high user-visible impact. Item 4 is the structural lift that makes W3 and future theme work tractable.

---

## G. Open Items from `docs/USER_BUG_LIST.md`

| ID | Status | This report |
|---|---|---|
| **U-001** — blank `08_char_select.png` screenshot | Reported | Not an app bug — Playwright/service-worker artifact. Re-capture in a clean session. No code action. |
| **U-002** — white labels unreadable on light buttons | Reported | Root cause found: **B2** (`app_theme.dart:4162` hardcodes `onSurface: Colors.white`). Fix B2 to close U-002. |

---

*This document is a point-in-time snapshot. Re-run the audit after the P0/P1 fixes land — the theming score (currently 2/4) should rise to 3 once B2 + W1 are addressed.*
