# Customization Hub — Design Brief

> Handoff for the **VISUAL/DESIGN agent** (claim Slot 1).
> The "Themes" system is being reworked into **Customization** — a
> single, honest customization hub for palettes, fonts, particles,
> glows and ambience. This doc = current-state diagnosis + target
> design + your scope. Commit prefix: `ui:` / `theme:`.

## A — What's wrong today (from in-app screenshots)

- **Two UIs in one screen** — `ExperienceStudioScreen` serves a
  *simple picker* (`initialTab == 0`, BACK button) AND a *studio
  chrome* (`initialTab > 0`, RESET button + SAVE THEME) depending on
  the entry point. Same screen, different shape.
- **Button inconsistency** — simple picker bottom bar: `BACK ·
  PREVIEW · APPLY`; studio tabs: `RESET · PREVIEW · APPLY`. Back vs
  Reset in the same slot is disorienting.
- **Preview semantics unclear** — does PREVIEW already change the
  app? The studio also has a small preview card with dots — two
  overlapping preview concepts.
- **51 presets, flat list** — whimsical names (catLady, mrRobot,
  unicornII-IV), no grouping or search.
- **Save flow buried** — "SAVE THEME" only exists inside the studio
  chrome; saved palettes then appear as `SAVED PALETTE` cards in the
  simple picker.

## B — Target design (user-directed)

### Naming
- Everything user-facing: **"Customization"** (not Themes/Studio).
- Presets trim to exactly **3**: `unicorn`, `moltenSteel`, `paperInk`
  (+ user's saved customs on top). `custom` pseudo-mode stays — it's
  the mechanism for saved palettes, not a preset.
- Entry labels: Settings tile + main-menu entry → "Customization".

### Layout — sticky action bar + draggable preview pane
```
┌─────────────────────────────────────────┐
│  ← BACK      👁 PREVIEW      ✓ APPLY    │  ← sticky, always on top
├─────────────────────────────────────────┤
│  PRESETS │ CUSTOM │ FONTS │ PARTICLES │ AMBIANCE │  ← tab strip
├─────────────────────────────────────────┤
│  LIVE LOOK pane — compact mini-UI       │  ← ~1/3 of screen
│  rendered with the staged picks         │
│  ──────────── ═══ (handle) ═══ ───────  │  ← drag handle
├─────────────────────────────────────────┤
│  (scrollable options — see §C)          │
└─────────────────────────────────────────┘
```
- The action bar lives **inside** the customization screen, pinned
  above the tab strip, never scrolls away.
- **BACK** — pop to caller (discard unapplied picks? see §D).
- **APPLY** — commits *all* current picks immediately (palette, font,
  particles, glow, ambience in one shot) and shows confirm feedback.
- **PREVIEW** — the tricky part, **built last**. See §E.

### The LIVE LOOK pane (user-specified, core UX)
A compact preview rendering **the app's own UI elements** with the
currently-staged picks — the user must actually *see* what each color
role does:

- Content: a mini mock of real UI — a panel card with a title row
  (prime accent), body text, a stat highlight, a button — showing
  canvas/panel/prime/second/stat colors + active font + glow tint.
- **Drag handle**: a bottom-sheet-style grab handle on the pane's
  bottom edge. Drag up/down resizes it live:
  - default ≈ **1/3 of the screen**
  - expandable up to **≈75%** (for a really good look)
  - collapsible small (≈15%?) so options get room when editing
  - animate the resize (AnimatedContainer or fractionalSizedBox
    driven by drag delta); remember the last height per session.
- It updates **live** as the user changes any pick (tap a swatch →
  pane re-renders immediately — no Apply needed for the pane).

### Option rows + color popups
- Options list below the pane: **one row per color role**
  (CANVAS · PANEL · PRIME · SECOND · STAT · GLOW + extras).
- Each row: role name + current color swatch chip → **tap opens a
  color-picker popup**. The app already has a ColorPicker widget
  (see `test/widget/color_picker_test.dart` — SV panel, hue slider,
  hex input, presets) — reuse it, don't rebuild.
- Non-color options stay as the existing tiles/sliders/chips.

### Tabs (order: importance)
1. **PRESETS** — the 3 theme cards (Unicorn, Molten Steel, Paper &
   Ink) + **SAVED PALETTES** section (user's custom saves with their
   names + default icon). Each card keeps the existing 5-swatch
   strip (CANVAS·PANEL·PRIME·SECOND·STAT).
2. **CUSTOM** — option-row list per §B: each UI color role (canvas,
   panel, prime, second, stat, glow + extras) is a name+swatch row →
   tap opens the existing ColorPicker popup. Extras below the color
   rows (border style? accent intensity?) at designer's discretion.
   The LIVE LOOK pane above shows every change instantly. Feeds the
   Save flow below.
3. **FONTS** — family tiles (existing: Enter the Gungeon, Megrim,
   Russo One, Fredoka, DM Sans, JetBrains Mono), size slider,
   weight bias, letter spacing. Keep the live sample text
   ("The Gungeon Awaits" card).
4. **PARTICLES** — enable toggle, count slider, type tiles
   (dot/square/glow orb/shell/rainbow/void/glitch), physics
   (bounce/chaos/tilt), color mode. Keep the live preview strip.
5. **AMBIANCE** — screen glow intensity, glow color swatches,
   wallpaper/bg options.

### Save flow (core ask)
- From CUSTOM (or anywhere): **"SAVE AS PRESET"** → name field →
  gets a default icon → appears in PRESETS under SAVED PALETTES
  forever after. Saved presets hold the *full* pick set (palette +
  font + particles + glow), not just colors — confirm this against
  `theme_custom_data.dart` before designing the card.

## C — Current assets to reuse

- Swatch strip + card layout from the simple picker (screenshot 1).
- Font-family tile grid + sample card (screenshot 3).
- Particle type tiles + physics chips (screenshot 4).
- Glow swatch row (screenshot 2).
- `PaletteMakerScreen` (679 lines) — existing color-pick UI; fold
  into the CUSTOM tab or repurpose its widgets.

## D — State semantics to define (decide + document)

- Does BACK discard un-applied picks or keep them staged? Recommend:
  picks are *staged locally* inside Customization; APPLY writes to
  `VisualPrefs`; BACK discards staging (confirm + warn if staged).
- RESET — if kept, it resets *the current tab's* staged picks only.

## E — PREVIEW (build last — hardest)

Today `displayedMode`/`_previewMode` re-skins the app live while
browsing. Target: PREVIEW = explicit try-on mode —
the whole app behind the sheet changes, plus a visible
"PREVIEWING — [APPLY] [DISCARD]" affordance so the user knows state
isn't committed yet. Out of scope for the first pass if it's deep;
ship the unified tabs + save flow first.

## F — Files

- `lib/screens/experience_studio_screen.dart` (1,360 ln) — the hub;
  biggest edit target. `_buildSimpleBody` vs `_buildStudioBody` dual
  UI is what gets unified.
- `lib/screens/experience_studio/` — studio_palette, studio_particles,
  studio_typography, studio_ambiance, studio_widgets (tab content,
  mostly reusable).
- `lib/screens/palette_maker_screen.dart` — fold into CUSTOM.
- `lib/services/theme/` — modes (51→3+saved), prefs, custom data.
- Entry labels: `main_menu_screen.dart`, `settings_tab.dart`,
  `active_run_helpers.dart`, `paradox_player_panel.dart`.

## G — Coordination

- **My prerequisite (CORE):** trim `AppThemeMode` to 3 + saved-mode
  migration (stale stored index → fallback), before or in parallel.
- Claim Slot 1 on `AGENT_STATUS.md`. Don't touch other agents' dirty
  files (avatar webp deletions are Slot 4 WIP).
- Conventions: flair.* tokens, GoopText, haptics, `fastRoute`,
  `BoxFit.contain`, `Responsive.factor`, dispose everything,
  maxLines on fixed-height text, `part of` splits for file size.
- Verify: `flutter analyze` clean, codex/widget tests green, full
  suite before pushing.
