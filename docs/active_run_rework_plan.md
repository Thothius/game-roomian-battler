# Active Run Rework — 3 Display Modes + 2.5D Inventory

> **Designer-led re-imagining of the active run screen.** Same core data
> (character + items + guns + run stats), three surprising new ways to view
> it, plus a volumetric inventory feel. Plan doc — implementation follows
> after approval.

---

## Identity

| Field | Value |
|-------|-------|
| **Owner** | Coder (Design Specialist), Slot 3 |
| **Branch** | `coder/active-run-rework` |
| **Scope** | Active run screen rework — additive, no data model changes |
| **Risk** | Touches the core `active_run_screen.dart` + `player_page.dart` — must preserve all existing MP/coop/dice/emote flows |
| **Started** | 2026-08-18 |

---

## Goals (from user brief)

1. **3 interchangeable display modes**, switchable instantly via a top-level
   Preferences/Settings bar with **big labels + live visual previews** of each:
   - **Mode 1 — The Gungeon Codex Book:** asset-styled book compendium,
     parchment/cyber panels, turning-page or structured-panel layout.
   - **Mode 2 — Super-Compact Quick Run:** high-density, minimal footprint,
     max stats/items/guns packed in for fast sessions.
   - **Mode 3 — Purple Gungeon Matrix:** looped animated background with
     Matrix-style digital rain — falling "code blocks" are purple-tinted
     Gungeon glyphs (gun names, item names, stat readouts) with active run
     data overlaid. Reference: `gungeon-matrix.mp4`.
2. **Core data continuity** across all 3 modes: character portrait, items
   view, guns view, real-time run stats.
3. **2.5D inventory management** by default: volumetric feel via perspective
   scaling, layered depth shadows, floating/tilt on hover-select — using our
   existing animation libraries (`flutter_animate`).

---

## Architecture Decisions

### A1. New `RunDisplayMode` enum in `VisualPrefs`

Mirrors the existing `InventoryDisplayMode` pattern (the proven, lowest-risk
way to add a persisted visual preference). One new field on `VisualPrefs`,
one new setter, one new prefs key, one new line in `_with()` + `_persist()`.

```dart
enum RunDisplayMode {
  codex,    // Mode 1 — book compendium
  compact,  // Mode 2 — super-compact quick run
  matrix,   // Mode 3 — purple gungeon matrix
}
```

- Default: `codex` (the most "Gungeon-authentic" first impression). **Confirmed by user.**
- Persisted via `SharedPreferences` key `runDisplayMode`.
- Setter: `VisualPrefs.setRunDisplayMode(RunDisplayMode)`.
- Reactive via existing `VisualPrefs.notifier` — no new notifier needed.

**Why not a separate notifier?** `VisualPrefs.notifier` already drives every
visual toggle on the active run (dashboards, calc, effects, shrine). Adding
one more field keeps the rebuild graph single-source and matches the
established pattern. A separate notifier would double-rebuild the header.

### A2. Mode switcher = a new top-level bar in `ActiveRunScreen`

Currently the active run has: `[Windgunner banner?] → [MpHeader | PlayerSwitcher] → [PageView of PlayerPage]`.

Insert a **`RunDisplayModeBar`** between the header and the PageView — a
horizontal strip of 3 large tappable preview cards (one per mode), each
showing a tiny live thumbnail of the mode's aesthetic. Tapping switches
instantly with a spring cross-fade (no navigation, no rebuild of MP state).

- Big labels: "CODEX BOOK", "COMPACT RUN", "GUNGEON MATRIX".
- Each card has a 1-line description below the label.
- Selected card gets the theme's `primary` glow border + scale 1.04.
- Collapsible: a chevron collapses the bar to a single pill showing the
  current mode name, freeing screen real estate once the user has picked.
  Persisted collapsed state via `VisualPrefs.runDisplayModeBarCollapsed`.
  **Default: collapsed** (user-confirmed). The collapsed pill is clearly
  tappable — chevron + mode name + "TAP TO SWITCH" hint on first launch,
  fading after first interaction.

**Placement rationale:** above the PageView so it's visible on both solo
and MP/coop (the PageView is per-player; the mode is run-scope). It sits
below `MpHeader`/`PlayerSwitcher` so player switching stays primary nav.

### A3. Each mode = one widget under `lib/widgets/active_run/modes/`

```
lib/widgets/active_run/modes/
  run_display_mode_bar.dart     // the switcher strip
  codex_book_mode.dart          // Mode 1
  compact_run_mode.dart         // Mode 2
  matrix_mode.dart              // Mode 3 (background + overlay)
```

Each mode widget receives the same `PlayerSlot` + reads `RunProvider` itself
(consistent with how `PlayerPage` works today). They share a small set of
helpers extracted from `player_page.dart` (sort, transfer, tile actions) so
we don't duplicate ~300 lines of MP/transfer logic three times.

**Shared helpers extracted to `lib/widgets/active_run/mode_helpers.dart`:**
- `effectiveDps(Gun, RunProvider)` — already inline in player_page.
- `topDpsInfo(player)` — top gun name + value.
- `synergyGlowColors(p)` — wrap the existing `activeSynergyGlowColors`.
- `promptTileActions`, `promptTransferGun`, `promptTransferItem` — lifted
  verbatim from `PlayerPageState` into top-level functions taking `BuildContext`.
- `tileGrid(context, displayMode)` — already a method, becomes a function.

`PlayerPage` keeps its current body as the **fallback / "classic"** view
(used if a mode widget errors or for coop where modes can be selectively
disabled). This preserves the existing tested surface area.

### A4. 2.5D inventory = a `DepthTile` wrapper around `PeriodicTile`

Not a rewrite of `PeriodicTile` — a **wrapper** that applies the volumetric
treatment. This keeps the existing tile's data layout intact and lets us
apply 2.5D to any mode that uses the grid.

```dart
class DepthTile extends StatefulWidget {
  final Widget child;
  final bool isTopDps;
  final Color? glowColor;
  // ...
}
```

Effects (all via `flutter_animate` + a `GestureDetector` + `MouseRegion`
for hover on desktop):
- **Perspective tilt:** on tap-down / hover, the tile rotates on X and Y
  axes (max ±8°) toward the touch point — feels like picking up a card.
  Uses `Transform` with a `Matrix4.identity()..setEntry(3,2, perspective)`
  ..rotateX/rotateY. Released → springs back via `Curves.elasticOut`.
- **Layered depth shadow:** a `BoxShadow` whose blur + offset grow with tilt
  magnitude, so the tile appears to lift off the surface.
- **Top-DPS float:** the gold-crowned top gun gets a slow idle bob
  (2s `Curves.easeInOut` loop, ±3px) so it reads as "the prize".
- **Synergy glow pulse:** existing `synergyGlowColor` becomes a breathing
  outer glow (1.4s loop) instead of a static border.

Performance: tilt is driven by a single `AnimationController` per tile,
disposed in `dispose()`. No per-frame `setState` — uses
`AnimatedBuilder` + `Transform`. Hover is desktop-only (web/desktop);
on mobile, tap-down drives the tilt. This matches the existing
`_LabeledIconButton` haptic pattern.

**Default-on:** `DepthTile` wraps every grid tile in all 3 modes unless the
user disables it (new `VisualPrefs.depthInventory` bool, default `true`).
One toggle in the mode bar's "Preferences" section.

### A5. Matrix mode background = new `CustomPainter`

`lib/widgets/backgrounds/gungeon_matrix_rain.dart` — a `CustomPainter` on a
looping `AnimationController` (pattern lifted from `GungeonFallAnimation`'s
`_PortalPainter`).

- **Columns** of falling glyphs, each column a `List<_Glyph>` with its own
  y-offset, speed, and trail length.
- **Glyph pool** sourced from the live run: gun names, item names, stat
  readouts ("DPS 56.0", "COOL 12", "CURSE 4"), gungeoneer name. Falls back
  to a static Gungeon word pool if inventory is empty (starter state).
- **Color:** purple-tinted (`Color(0xFFBCA0F8)` core, `Color(0xFF9D5CDB)`
  trail) — matches the existing vortex palette from
  `gungeon_fall_animation.dart` for visual continuity with the home screen.
- **Lead glyph** of each column is brighter (white-purple) and slightly
  larger — the classic Matrix "head" effect.
- **Performance:** painter is `repaint`-bound to the controller only; glyph
  positions update in the painter's `paint()` from a precomputed seed (no
  per-frame allocations). ~24 columns, ~18 glyphs each = cheap.
- **Overlay:** the active run data (character, stats, gun/item lists) sits
  in semi-transparent panels on top with a purple backdrop blur
  (`BackdropFilter` + `ImageFilter.blur`) so the rain reads behind.

Looped via `..repeat()` on a 12s controller; respects
`VisualPrefs.particlesEnabled`? **No** — Matrix is a display *mode*, not a
particle effect. It runs whenever mode == matrix, independent of the
particle toggle (which controls the ambient particle field). This avoids
the BUG-038-style coupling between particle prefs and display mode.

---

## File Plan

### New files
| File | Purpose | LOC est. |
|------|---------|----------|
| `lib/widgets/active_run/modes/run_display_mode_bar.dart` | The 3-card switcher strip + collapse state | ~220 |
| `lib/widgets/active_run/modes/codex_book_mode.dart` | Mode 1 — book compendium layout | ~320 |
| `lib/widgets/active_run/modes/compact_run_mode.dart` | Mode 2 — high-density compact | ~260 |
| `lib/widgets/active_run/modes/matrix_mode.dart` | Mode 3 — matrix rain + overlay panels | ~300 |
| `lib/widgets/active_run/mode_helpers.dart` | Shared helpers extracted from player_page | ~180 |
| `lib/widgets/active_run/depth_tile.dart` | 2.5D tile wrapper | ~160 |
| `lib/widgets/backgrounds/gungeon_matrix_rain.dart` | Matrix rain CustomPainter | ~240 |

### Modified files
| File | Change | Risk |
|------|--------|------|
| `lib/services/app_theme.dart` | Add `RunDisplayMode` enum, `runDisplayMode` field on `VisualPrefs`, `setRunDisplayMode`, `depthInventory` field + setter, `_with()` + `_persist()` + load wiring | LOW — additive, mirrors existing pattern |
| `lib/screens/active_run_screen.dart` | Insert `RunDisplayModeBar` between header and PageView; pass selected mode into `PlayerPage` | MED — core screen, must preserve MP/coop/dice/emote flows |
| `lib/widgets/active_run/player_page.dart` | Accept `RunDisplayMode` param; route to the chosen mode widget instead of the classic scroll when a mode is set; extract shared helpers to `mode_helpers.dart` | MED — large file, extraction must be verbatim |
| `assets/data/changelog.json` | New entry under current version | LOW |
| `gungeon_mate/VERSION_HISTORY.md` | Sync (if not gitignored) | LOW |

### Untouched (explicitly)
- `lib/screens/experience_studio_screen.dart` — **user WIP, off-limits per AC4.**
- `lib/widgets/periodic_tile.dart` — wrapped, not modified.
- All MP/coop/dice/emote code in `active_run_screen.dart` — preserved as-is.
- Data models, services, providers — no changes.

---

## Mode Specifications

### Mode 1 — The Gungeon Codex Book

**Aesthetic:** A leather-and-brass compendium. The screen reads as an open
book: left page = character + stats, right page = guns/items. Page corners
have a subtle curl shadow. Section transitions use a page-turn animation
(`flutter_animate` `flip` + fade).

**Layout:**
- Top: character portrait in an oval "locket" frame (reuse
  `GungeoneerHeader`'s avatar but restyle the frame).
- Left page: stats block (coolness, curse, master rounds, robot DMG if
  applicable) in parchment cards with brass corner studs.
- Right page: guns list (compact rows, not grid) + items list below.
- "Turn page" chevrons at the bottom to flip between Guns page / Items page
  / Synergies page — or swipe horizontally (PageView inside the mode).
- Special dashboards (Robot, Junkan, etc.) appear as an "appendix" page at
  the end when present.

**2.5D:** book pages have a slight perspective skew on the outer edges;
tapping a gun row "lifts" it out of the page (DepthTile on rows too, not
just grid tiles).

**Assets:** **no new PNGs** (user-confirmed) — uses existing character
portraits + `QualityBadge` + brass borders + color gradients drawn in
code. Parchment feel comes from warm color overlays + subtle noise via
a `CustomPainter` overlay, not a raster texture.

### Mode 2 — Super-Compact Quick Run

**Aesthetic:** Tactical HUD. Everything fits in one screen-height on a
typical phone — no scroll for the core loadout. Dense, monospace, neon.

**Layout:**
- Top strip: character name + 4 inline stat chips (COOL/CURSE/HP/DPS-top).
- Middle: **2-column grid** — left column guns (icon + name + DPS, one line
  each), right column items (icon + name + recharge). ~6 rows visible.
- Overflow: a small "X more" chip at the bottom of each column opens a
  scrollable sheet (not a full screen) for the rest.
- Special dashboards collapse into a single "SPECIAL" chip that expands an
  inline mini-panel.
- No section headers, no sort pickers in the main view — sort is set via
  the mode bar's Preferences section. Maximizes density.

**2.5D:** tiles use a flatter tilt (±4°) since density is the priority;
hover/tap still lifts but less dramatically. Top-DPS gun gets a gold
left-border accent instead of a crown (saves vertical space).

**Why this is valuable:** the existing grid is great for browsing but
forces scrolling on long runs. Compact mode is the "I'm mid-fight and need
to glance at my loadout" mode.

### Mode 3 — Purple Gungeon Matrix

**Aesthetic:** `gungeon-matrix.mp4` reference. Deep purple-black background,
falling glyph columns in purple, active run data in translucent
glassmorphic panels floating over the rain.

**Layout:**
- Full-screen `GungeonMatrixRain` painter as the bottom layer.
- Character portrait in a circular "terminal" frame top-left, with a
  scanning line animation across it.
- Stats as a vertical "data readout" panel on the right edge — monospace,
  purple text, values update live (coolness, curse, top DPS, gun count,
  item count, synergies active).
- Guns + items as two horizontal "data streams" — each item/gun is a chip
  that drifts slowly left-to-right (or right-to-left alternating) with its
  name + key stat. Tapping one opens detail (same as other modes).
- A central "focus panel" shows the top-DPS gun's full stats card — the
  hero of the run — with a subtle purple glow pulse.

**2.5D:** the data stream chips have the deepest tilt (±10°) and a strong
drop shadow so they feel like cards floating in front of the rain. The
focus panel has a parallax offset driven by device tilt (via
`sensors_plus` if already a dep — check; otherwise skip, static is fine).

**Performance guardrails:**
- Rain painter capped at 24 columns × 18 glyphs.
- Data stream chips use a single `AnimationController` for the drift, not
  per-chip controllers.
- `BackdropFilter` blur is applied once to the panel container, not per
  panel.
- If `MediaQuery.devicePixelRatio` > 2.5 (retina), reduce column count to
  18 to keep fillrate sane.
- **No device-tilt parallax** (user-confirmed) — chips drift via a single
  animation controller, no `sensors_plus` dependency. Static is fine.

---

## Preferences / Settings Switcher

The mode bar has a "PREFERENCES" expandable section (or a gear icon on the
right of the bar) that opens a bottom sheet containing:

1. **Display Mode** — the 3 cards (same as the bar, for when the bar is
   collapsed).
2. **2.5D Inventory** — toggle (`VisualPrefs.depthInventory`).
3. **2.5D Tilt Intensity** — slider 0–100% (scales the max tilt degrees).
4. **Matrix Rain Speed** — slider (only enabled in matrix mode).
5. **Matrix Glyph Density** — slider (column count, only in matrix mode).
6. **Codex Page Turn Speed** — slider (only in codex mode).
7. **Compact Column Count** — 2 / 3 (only in compact mode).

Each control has a 1-line explanation below it. The sheet uses the
existing `HomeCustomizationSheet` styling pattern (dark container, purple
top border, grabber).

**Why a sheet and not a full screen?** The user said "switch to
preferences menu and settings menu — place appropriately with big label
and options explained with previews." A sheet keeps the user in the active
run context — they see the mode change live behind the sheet. A full
screen would hide the very thing they're customizing.

---

## Implementation Phases

### Phase 1 — Foundation (no visual change yet)
1. Add `RunDisplayMode` enum + `runDisplayMode` / `depthInventory` fields
   to `VisualPrefs` + setters + `_with` + `_persist` + load wiring.
2. Extract `mode_helpers.dart` from `player_page.dart` (verbatim lift,
   no behavior change). `PlayerPage` imports them.
3. Build `DepthTile` wrapper as a standalone widget with unit-testable
   tilt math.
4. `flutter analyze` clean. Commit.

### Phase 2 — Mode switcher + Mode 1 (Codex)
5. Build `RunDisplayModeBar` with the 3 preview cards + collapse state.
6. Wire it into `active_run_screen.dart` between header and PageView.
7. Build `codex_book_mode.dart`. Route `PlayerPage` to it when
   `runDisplayMode == codex`.
8. Apply `DepthTile` to the codex grid/rows.
9. Bughunt: verify MP/coop/dice/emote still work end-to-end.
10. `flutter analyze` clean. Commit.

### Phase 3 — Mode 2 (Compact)
11. Build `compact_run_mode.dart` — 2-column dense layout.
12. Wire routing.
13. Apply `DepthTile` (flatter tilt).
14. Bughunt. `flutter analyze`. Commit.

### Phase 4 — Mode 3 (Matrix)
15. Build `gungeon_matrix_rain.dart` painter.
16. Build `matrix_mode.dart` — rain + overlay panels + data streams.
17. Wire routing.
18. Apply `DepthTile` to data stream chips.
19. Performance bughunt (frame rate on a real device or web preview).
20. `flutter analyze`. Commit.

### Phase 5 — Preferences sheet + polish
21. Build the preferences bottom sheet with all 7 controls.
22. Wire each control to its `VisualPrefs` setter.
23. Changelog + VERSION_HISTORY update.
24. Full bughunt: all 3 modes, MP, coop, dice, emotes, transfer sheets,
    quick-add FAB, windgunner banner.
25. `flutter analyze` clean on full `lib/`. Commit + release slot.

---

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Breaking MP/coop/dice/emote flows in `active_run_screen.dart` | Mode bar is purely additive between header and PageView; no existing callback touched. Full MP bughunt in Phase 2. |
| `player_page.dart` extraction introduces a regression | Extract verbatim, diff-only review, keep `PlayerPage`'s classic body as fallback. |
| Matrix rain kills frame rate on low-end devices | Column cap + DPR-aware reduction + single controller. Ship with conservative defaults. |
| 2.5D tilt feels gimmicky / nauseating | Default tilt is subtle (±8°), intensity slider lets users dial to 0. `depthInventory` toggle kills it entirely. |
| Mode bar eats too much vertical space | Collapsible to a single pill; collapsed state persisted. |
| `experience_studio_screen.dart` conflict (user WIP) | I do not touch it. My `VisualPrefs` additions are in `app_theme.dart` — different file. |

---

## Out of Scope (explicitly, per Ponytail Rules)

- No new dependencies. `flutter_animate` is already in `pubspec.yaml`.
  `sensors_plus` parallax in Matrix mode is **optional** — only add if
  already a dep; otherwise ship static.
- No changes to data models, services, or providers.
- No new PNG assets in v1 (codex parchment texture is a nice-to-have, not
  required — brass borders drawn in code carry the aesthetic).
- No rewrite of `PeriodicTile` — wrapped, not forked.
- No removal of the classic `PlayerPage` view — kept as fallback.
- No changes to `experience_studio_screen.dart` (user WIP).

---

## Verification Plan (per Safety S6/S10)

- `flutter analyze` clean on every modified file after each phase.
- Grep proof for `dispose()` on every new `AnimationController` /
  `PageController` / `StreamSubscription`.
- Grep proof for `context.mounted` checks before any async-gap UI op.
- Manual verification: launch each mode, switch between them mid-run, add/
  remove items, trigger a dice challenge in MP, send an emote, transfer a
  gun to coop. All must work identically to today.
- Paste actual command outputs in the session log handoff row.
