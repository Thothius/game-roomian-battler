# UI & Settings Masterplan — GungeonMate v3.7.x

Audit date: 2026-11-20 · Auditor: CORE (Slot 2)
Scope: every user-facing view/surface, the Settings/Preferences IA, and whether
Experience Studio + VisualPrefs customization actually reaches each surface.

Companion docs: `docs/USER_BUG_LIST.md` (U-012/U-013/U-014 asset findings),
`DESIGN.md` (design contract), `docs/REWORK_LESSONS_LEARNED.md`.

---

## 0. TL;DR verdict

Theming pipeline is **sound**: `ThemeOverlay` + `ThemeData` + `GoopText` +
`AppTheme.flair` cover every normal surface. The real problems are **IA and
coverage gaps**, not missing hooks:

1. **Settings/prefs are unreachable without an active run** — biggest UX hole.
2. **Two parallel menus** (gear sheet vs SettingsScreen) duplicate ~6 actions
   with confusing naming ("Customize" vs "Preferences" vs Studio).
3. **One dead pref** (`periodicGridColumnCount`) — saved, read, never set.
4. **One unthemed screen** (`cool_curse_screen.dart`) — hardcoded purple.
5. **Stale/dead theme code** in `theme_overlay.dart` (`kHomeGalaxyAsset`,
   hardcoded menu base, "theme-locked" comments).
6. **Skeuo coverage is opportunistic** — `Skeuo.inkIf` is applied per call
   site; dark-island screens (MP, quiz, cool_curse) aren't audited.
7. Asset findings U-012/U-013/U-014 are real but orthogonal — deferred.

---

## 1. View-by-view inventory

### 1.1 Main menu (no active run)
Files: `lib/screens/main_menu_screen.dart`, `lib/widgets/home/home_backdrop.dart`,
`lib/widgets/skeuo/skeuo_backdrop.dart`, `lib/widgets/skeuo/skeuo_surface.dart`.

| Element | State | Notes |
|---|---|---|
| Backdrop | DONE (v3.7.0) | Theme-derived gradient + flock/rise sprite drift. Reduced-motion safe. |
| Menu buttons | DONE | Hero = `flair.primary`, ghosts = accent wash/border, luminance-checked labels. |
| Neo-Skeuo toggle | DONE | Top-right chip, `kNeoSkeuoEnabled` re-enabled (`38f39a7`). |
| Logo/glow | DONE | secondary/headlineStat/primary driven. |
| Entry points | GAP | Local Run / Multiplayer / Customization / Ammonomicon. **No Settings door.** |

**Risk:** ghost buttons rely on accent border at α.55 — on themes with dark or
grey primaries (paperInk `0xFF90A4AE`, minimalist `0xFFE0E0E0` is fine) the
button can read faint. Watch on-device; tune wash alpha if needed.

### 1.2 Home shell (active run)
File: `lib/screens/home_screen.dart`.

| Element | State | Notes |
|---|---|---|
| Nav: Inventory / Browse / Ammonomicon | DONE | `IndexedStack`, lazy Ammonomicon JSON load, `SkeuoNavBar` under skeuo. |
| PopScope back policy | DONE | Non-inventory tabs redirect to Inventory first. |
| MP banners | DONE | `MpReconnectBanner` + `MpRequestListener` wrap. |

### 1.3 Active-run header + run-tools sheet
Files: `lib/widgets/active_run/active_run_helpers.dart`,
`lib/widgets/active_run/player_page.dart`,
`lib/widgets/paradox/paradox_player_panel.dart`.

| Element | State | Notes |
|---|---|---|
| Gear → `_RunToolsSheet` | WORKS, OVERLOADED | 7 rows: Ammonomicon, Shrines, Dice, Surprise, Neo-Skeuo, Customize, Quiz, **Preferences**, End Run. Titled "run tools" but is really a misc drawer. |
| 4 toggle icons (Calc/Effects/Shrine/Panels) | DONE | BUG-041 labels shipped. |
| Paradox panel → SettingsScreen | DUPLICATE | Second door to same Settings; fine, but see §2. |
| Customize row | INCONSISTENT | Disabled under skeuo with no explanation; label says "Customize" but pushes Experience Studio. |

### 1.4 Browse / Ammonomicon / detail screens
Files: `lib/screens/browse_screen.dart`, `lib/screens/ammonomicon_*.dart`,
`lib/screens/item_detail_screen.dart`, `lib/widgets/item_detail/*`.

| Element | State | Notes |
|---|---|---|
| `CodexColors` category colors | INTENTIONAL | Fixed game identity per DESIGN.md — immune to theme by design. |
| LEB browse toggle | DONE | `browseShowLichEyeBullets` pref, set inline in browse. |
| Item detail tabs (synergies etc.) | DONE | Uses `LebViewScope`, co-op tags, completes-pill. |
| Raw `Colors.*` usage | AUDITED, FINE | Mostly white-alpha neutrals + `Skeuo.inkIf(Colors.amber)` semantics. |

### 1.5 Settings screen (the prefs hub)
Files: `lib/screens/settings_screen.dart` (thin wrapper),
`lib/widgets/settings/settings_tab.dart`, `settings_sections.dart`,
`settings_widgets.dart`.

| Section | Contents | Reachability |
|---|---|---|
| RUN TOOLS | Shrine picker, add/remove co-op, save run | run-only (correct — needs run state) |
| GAMEPLAY → SYNERGIES | LEB bullets, co-op scope tags | run-only |
| GAMEPLAY → DICE | Dice type | run-only |
| GAMEPLAY → PANELS | Special-panels toggle | run-only |
| MULTIPLAYER | MP prefs (conditional) | run-only |
| DATA & STORAGE | Reset players | anywhere-safe, but unreachable |
| CUSTOMIZATION | Studio link tile | duplicates gear sheet |
| DEV TOOLS | Dev toggles | run-only |
| DANGER ZONE | Reset data, End Run | run-only |

**Verdict:** the *contents* are fine; the *placement* is wrong. Half the screen
is run-scoped actions that duplicate the gear sheet; the other half (dice type,
panel toggles, font-adjacent prefs) are app-level prefs trapped behind a run.

### 1.6 Experience Studio (visual customization)
Files: `lib/screens/experience_studio_screen.dart`, `studio_flow.dart`,
`studio_ambiance.dart`, `studio_particles.dart`, `studio_typography.dart`,
`studio_widgets.dart`.

| Surface | State | Notes |
|---|---|---|
| Preset gallery / wizard / dashboard | DONE | v3.6-era rework; live `displayedMode` preview. |
| Ambiance tab | DONE | Glow, vignette, grain, cinematic bars, ambient kind, shader, liquid tank, tap fx. |
| Particles tab | DONE | Type, sprite, count/speed/size/opacity, bounce/chaos/touch/links. |
| Typography tab | DONE | Font, sizes, weight bias, letter spacing → `GoopText` global. |
| Canvas tab | DONE | Wallpaper (custom themes), panel chrome. |
| Neo-Skeuo lock | DONE | Fixed-identity message; intentional. |
| Entry points | 3 doors | Main-menu "Customization", gear sheet "Customize", Settings "CUSTOMIZATION" tile — three labels for one screen. |

### 1.7 Pushed/standalone screens

| Screen | Theming | Action needed |
|---|---|---|
| `character_select_screen.dart` | flair + `Skeuo.inkIf` — OK | polish pass already delegated/landed (queue row: Agent 2 items) |
| `mp_connect_screen.dart` / `mp_lobby_screen.dart` | `MpColors` identity palette | intentional; verify skeuo readability only |
| `quiz/*` | white-alpha + amber streak on themed backdrop | acceptable; optional accent pass |
| **`cool_curse_screen.dart`** | **HARDCODED purple island** | re-skin to flair/skeuo tokens — only real offender |
| `shrine_picker_screen.dart` | `Skeuo.inkIf` semantics — OK | none |
| `stats_detail_screen.dart` / `effects_summary_screen.dart` | semantic cool/curse colors | OK |
| `avatar_picker_screen.dart` | flair-driven | OK |
| `main.dart` error screen | hardcoded | fine (error path) |

### 1.8 ThemeOverlay internals
File: `lib/widgets/theme_overlay.dart`.

- Layer order verified: wallpaper → gradient → liquid tank → ambient field →
  shader → particles → glow → page frame → vignette/scrim.
- Menu suppression via `menuOnTop` — correct, no double-ambient.
- **Dead/stale:** `kHomeGalaxyAsset` (unused since galaxy video removal),
  menu base still paints `0xFF0A0710` under `MainMenuBackdrop` (covered but
  misleading), "theme-locked" comments predate the re-skin.
- `currentScreenIndex` still used for sparkle gating — keep.

---

## 2. The IA problem (core of this plan)

Today there are **two settings surfaces with overlapping scope**:

```
Main menu ──Customization──► ExperienceStudio (visual prefs: theme, particles,
                             ambiance, typography, wallpaper)

Active run ──gear sheet──► RunToolsSheet ──Preferences──► SettingsScreen
                │                                    └─► dice/panels/LEB/co-op
                └──Customize──► ExperienceStudio (same screen, 3rd door)
```

Problems:
- No Settings door on the home menu → gameplay prefs (dice type, special
  panels, LEB, co-op tags) unreachable until a run starts.
- "Preferences" (gear sheet) and "CUSTOMIZATION" (Settings tile) and
  "Customize" (gear sheet) and "Customization" (main menu) = 4 labels, 2
  destinations.
- Settings mixes app-level prefs with run-scoped actions (shrine picker,
  reset items, save run, end run) that already live in the gear sheet.

### Proposed target IA (Option A — recommended)

Split by scope, not by screen count:

```
Main menu
 ├── Local Run / Multiplayer / Ammonomicon   (unchanged)
 ├── Studio        → ExperienceStudio        (visual customization)
 └── Settings      → SettingsScreen          (gameplay + app prefs)

Active-run gear sheet  → slimmed to run actions only:
   Ammonomicon · Shrines · Dice roll · Surprise (MP) · Quiz · End Run
   (+ "Settings" row → SettingsScreen)
```

- SettingsScreen keeps GAMEPLAY/DATA/DEV/DANGER sections; **RUN TOOLS and
  MULTIPLAYER sections move back to the gear sheet** (they're run-scoped) or
  stay but are clearly labeled "Run" — decide at implementation; lean toward
  moving them out so Settings = prefs only.
- Rename gear-sheet "Preferences" → "Settings" for consistency; keep one
  label everywhere.
- Keep the Customize→Studio row in the gear sheet (in-run theme tweaking is a
  feature), but it should deep-link to the Studio dashboard, not a generic
  push.

### Option B (lighter)

Keep both screens; just (a) add a Settings entry to the main menu, (b) rename
all four labels to two consistent ones ("Studio" / "Settings"), (c) remove the
CUSTOMIZATION tile from Settings (Studio already has 2 doors). Less restructure,
leaves the run-scoped sections inside Settings.

**Recommendation: Option A.** The duplication is the actual UX debt; Option B
leaves it.

---

## 3. Customization coverage matrix

Legend: ✅ wired end-to-end · ⚠️ partial/conditional · ❌ gap · — n/a

| Pref / flair field | Studio control | Persisted | Consumer(s) | Status |
|---|---|---|---|---|
| `appThemeMode` + palette/remix/custom | ✅ gallery+wizard | ✅ | ThemeData, flair, ThemeOverlay | ✅ |
| `font`, `fontSize`, `inventoryFontSize` | ✅ typography | ✅ | GoopText (global), MediaQuery scaler | ✅ |
| `fontWeightBias`, `letterSpacing` | ✅ typography | ✅ | GoopText | ✅ |
| `glowIntensity/Color/Index/Style` | ✅ ambiance | ✅ | ThemeOverlay glow layer | ✅ |
| `vignetteIntensity`, `grainIntensity` | ✅ ambiance | ✅ | ThemeOverlay scrim | ✅ |
| `cinematicBars` | ✅ ambiance | ✅ | ThemeOverlay page frame | ✅ |
| `ambientKind`, `shaderEnabled/Preset` | ✅ ambiance | ✅ | ThemeOverlay layers | ✅ |
| `liquidTankKind` | ✅ ambiance | ✅ | ThemeOverlay liquid layer | ✅ |
| `wallpaperImmersive` | ✅ canvas | ✅ | CustomWallpaper | ✅ |
| `wallpaper` (per custom theme) | ✅ canvas | ✅ | ThemeOverlay layer 0 | ✅ (custom themes only — by design) |
| `bgMode` solid/gradient/none | ⚠️ data model supports, **no picker UI** | ✅ | ThemeOverlay gradient layer | ⚠️ preset-flow spec called for picker; MVP shipped wallpaper+solid only |
| `particleEnabled`, type, sprite, count, speed, size, opacity, bounce, chaos, touch, links, color schema, glow | ✅ particles | ✅ | ParticleField / ItemIconField | ✅ |
| `panelColor/Opacity/BorderColor/BorderWidth/Radius` | ✅ canvas | ✅ | `AppTheme.flairFor()` | ✅ |
| `inventoryDisplayMode` | ❌ **no control found** — set inline in player_page? | ✅ | player_page renderers | ⚠️ verify — may only be settable via run UI |
| `periodicGridColumnCount` | ❌ none | ✅ | player_page:567 | **❌ DEAD — wire a picker or delete** |
| `customDiceType` | ✅ settings DICE section | ✅ | dice_roll | ✅ (but Settings unreachable w/o run → see §2) |
| `showLichEyeBullets` (global) | ✅ settings + browse inline | ✅ | gun_synergies_tab, browse | ✅ |
| `browseShowLichEyeBullets` | ✅ browse inline | ✅ | browse rows | ✅ |
| `showSynergyCoopTags` | ✅ settings | ✅ | synergy surfaces | ✅ |
| `showDashboard` / dashboard visibility | ✅ settings + paradox panel | ✅ | MP panels | ✅ |
| Tap sparkles / ripple fx | ✅ ambiance | ✅ | ThemeOverlay gestures | ✅ |
| Avatar + frame | ✅ avatar picker | ✅ | FramedAvatar (MP/lobby) | ✅ (lobby-scoped — fine) |

**Net:** every *visual* pref reaches its consumer. The gaps are: one dead
pref, `bgMode` picker never shipped, and gameplay prefs gated behind a run.

---

## 4. Work packages (proposed order)

Each package = one commit-sized unit; all on `master` (sole-agent rule unless
board says otherwise). Version bump + release checklist only on the last
package or per user request.

### WP-1 — Settings IA restructure ✅ SHIPPED `48bf8fd`
Files: `main_menu_screen.dart`, `settings_tab.dart`, `settings_sections.dart`,
`active_run_helpers.dart`, `settings_screen.dart`.
- Add "Settings" gear chip to main menu — small chip top-left mirroring the
  skeuo toggle chip (user decision).
- Rename gear-sheet "Preferences" → "Settings".
- Decide RUN TOOLS/MULTIPLAYER-in-Settings disposition per §2 Option A.
- Update tests touching settings nav.

### WP-2 — Dead pref removal + bgMode picker ✅ SHIPPED `4fe215a` (bgMode picker already existed — verified all 4 chips live)
- `periodicGridColumnCount`: **delete** pref + `setPeriodicGridColumnCount`;
  simplify `player_page.dart:567` to auto column count (`w<360?3 : w<600?4 : 6`).
- `bgMode`: add Wallpaper/Solid/Gradient/None segmented picker to Studio
  CANVAS tab. Data model supports all 4 (`theme_custom_data.dart` `bgMode`
  0–3). Gradient needs stop colors — reuse canvas color fields or add two
  stop pickers; check what CANVAS already edits before designing.

### WP-3 — cool_curse_screen re-skin ✅ SHIPPED `bc9ff19`
- Replace hardcoded `0xFF0D0716/0xFF140B22/B388FF/4DD0E1/BA68C8` with
  `AppTheme.flair` tokens + `Skeuo.inkIf` semantics; transparent scaffold so
  ThemeOverlay shows through (match other pushed screens).

### WP-4 — ThemeOverlay cleanup ✅ SHIPPED `54a6596`
- Remove `kHomeGalaxyAsset`, delete/neutralize the dead menu base layer +
  stale comments, keep `currentScreenIndex` sparkle gating.

### WP-5 — Skeuo coverage pass — ASSESSED, deferred
MP/quiz/char-select screens are already flair-driven (`flair.scaffold` scrims,
`flair.primary` buttons, GoopText ink-collapse). Remaining gap: raw accent
`Icon`/`Color()` literals aren't `Skeuo.inkIf`-wrapped — cosmetic polish debt,
not breakage. Revisit if skeuo-on-MP screenshots look off.
- Enumerate pushed screens with own dark surfaces: mp_connect, mp_lobby,
  quiz/*, cool_curse (fixed by WP-3), character_select.
- For each: confirm `GoopText` ink-collapse covers text; wrap accent colors
  in `Skeuo.inkIf`; ensure scaffold is transparent or skeuo paper.
- Output: short list of per-screen fixes, implement the cheap ones.

### WP-6 — Asset findings (defer unless user asks)
- U-012: 614 raw PNGs ~97% dead weight — needs reference audit before any
  deletion (S4: don't delete without approval + verification).
- U-013: 12 theme splash slugs → missing art — art task, not code.
- U-014: wallpaper payload ~12MB/46 files — re-encode to webp/resolution
  pass; measurable APK win, do as separate chore.

---

## 5. Decisions (user, 2026-11-20)

1. **Settings entry:** small gear chip on home menu (mirrors skeuo toggle).
2. **Settings scope:** Option A — move RUN TOOLS / MULTIPLAYER / run-scoped
   DATA actions to the gear sheet; SettingsScreen becomes prefs-only
   (GAMEPLAY prefs + DEV TOOLS + app-level reset).
3. **bgMode:** ship all 4 modes (wallpaper/solid/gradient/none) in Studio
   CANVAS — data model already supports it.
4. **periodicGridColumnCount:** DELETE the pref + setter; simplify
   player_page:567 to the existing auto column-count logic.
5. **Neo-Skeuo toggle:** keep in both home menu and gear sheet (user decision).
6. **U-012/013/014:** leave open in USER_BUG_LIST — not scheduled.

## 6. Verification plan (per WP)

- `C:/src/flutter/bin/flutter.bat analyze` — 0 issues on touched files.
- `flutter test` — full suite green (baseline 627 pass / 9 skip).
- New widget tests: settings entry point on menu, renamed labels, bgMode
  picker round-trip, cool_curse token usage (golden-free smoke test).
- Manual: theme-switch sweep over every pushed screen; skeuo on/off sweep.
