# Color System Expansion — Plan (C1 research)

> Task: NEXT_ROUND_MASTERPLAN #31 / C1–C3. User directive: "more colorpicker
> palette variety from darks to lights… specials group of 64 amazing special
> colors that glow/pulse."
> Status: C1 research complete — awaiting GO for C2 implementation.

## 1. Current-state audit — where colors live today

### Live color entry points (all funnel through one sheet)

| Surface | Data | Persistence |
|---|---|---|
| `_PaletteColorSheet` (`experience_studio_screen.dart:4089`) | ~200 curated ARGB swatches in 5 tabs: GENERAL (60), METALLIC (~30), PINK & PURPLE (~30), BLUE & CYAN (30), GREEN & MINTY (30) | Returns `Color` to caller |
| `ColorFavorites` (`services/color_favorites.dart`) | 6 ARGB slots | `vp.color_favorites_v1` SharedPreferences — survives preset switches, app-level |
| `VisualPrefs.glowColors` (`theme_flair_prefs.dart:496`) | 48 curated glow colors + `glowColorIndex` + `glowCustomColor` ARGB | `vp.glow_v1` |
| `CustomThemeData` (`theme_custom_data.dart:80`) | 6 fields: scaffold, card, primary, secondary, headlineStat, bulletColor | Embedded in `SavedCustomTheme` JSON (`custom.themes.v1`) |
| Built-in themes | 9 palettes + Palette Maker in `theme_data_tables.dart` / `app_theme.dart` | Theme selection only |

Every picker call site uses `_PaletteColorSheet.show(context, current)` →
`Color?`. There is **no free-form HSV entry point in the live UI**.

### Findings

1. **Dead HSV picker** — `lib/widgets/color_picker_dialog.dart` is a complete
   saturation/value panel + hue slider + hex input, and has **zero call sites**
   (grep: only its own file). Either wire it in or delete it.
2. **`glowColors` duplicates** — comment claims "36 deep" but the list has 48
   entries with repeats: `0xFF6A1B9A` ×2, `0xFFAD1457` ×2, `0xFF1A237E` ×2
   (Magenta Pulse/Royal Plum, Wine/Raspberry, Shadow Indigo/Midnight).
3. **Tab overlap** — GENERAL's 60 swatches already contain red/orange/green/
   blue/purple families that the four hue tabs repeat. The hue tabs are
   subsets of the same Tailwind-ish palette, not distinct ramps.
4. **No light-end coverage** — curated lists skew dark/saturated; there is no
   systematic dark→light ramp per hue, which is exactly the user's ask.
5. **Selection is color-only** — nothing carries "this color behaves
   specially". Any behavior feature must be resolvable from the stored ARGB
   value alone (prefs/presets store plain ints).

## 2. Proposed data model

New file `lib/theme/color_ramps.dart` (code, not JSON — see rationale):

```dart
class ColorRamp {
  final String id;      // 'crimson', 'ocean', ...
  final String label;   // 'CRIMSON'
  final double hue;     // HSL hue anchor
  final List<Color> shades; // 32 entries, index 0 = darkest → 31 = lightest
}
```

- **12 hue groups × 32 shades = 384 swatches.** Canonical groups:
  CRIMSON, EMBER, AMBER, LIME, FOREST, MINT, CYAN, AZURE, COBALT, VIOLET,
  MAGENTA, ROSE. (GOLD folds into AMBER; PINK splits into ROSE + MAGENTA;
  slate/gray neutrals stay in the CURATED tab.)
- Shade generation: deterministic HSL interpolation — index `i` maps
  lightness ~8%→92% with saturation eased (deep→vivid→soft). Generated once
  in a `static final` (not `const` — HSVColor isn't const); tests pin count,
  uniqueness, and monotonic lightness.
- **Why code, not JSON:** zero asset payload, type-safe, unit-testable,
  versioned by git. JSON buys nothing here — the data is formulaic.
  (If hand-tuned exceptions are wanted later, a `Map<int, Color>` override
  per ramp is a 5-line addition.)

New file `lib/theme/special_colors.dart`:

```dart
class SwatchEffect { static const none=0, glow=1, pulse=2, shimmer=3, aurora=4; }

class SpecialColor {
  final Color color;
  final String label;    // 'NOVA PULSE'
  final int effect;      // SwatchEffect.*
}
```

- **64 specials = 8 families × 8 variants.** Families: NOVA (blue-cyan),
  PYRE (orange-red), VERDANT (green), LILAC (purple-pink), GOLDEN, ROSE,
  FROST (pale cyan-white), UMBRA (near-black with colored rim — the
  "invisible until glow" trick). Each family gets the 4 core effects ×
  2 intensities.
- `static final Map<int, SpecialColor> byArgb` — O(1) lookup so any
  consumer resolves behavior from a stored color.

## 3. Behavior plumbing (the "glow/pulse" part)

Persistence stays **plain ARGB everywhere** — presets, prefs, wire format,
and MP snapshots need zero changes. Behavior is derived:

```
stored ARGB → SpecialColorRegistry.byArgb[argb] → SwatchEffect?
```

- **Phase-1 render scope (recommended):** the ambient glow
  (`VisualPrefs.glowColor` consumers — `AmbientGlow`/theme overlay) and
  custom-theme `primary`/`secondary` accents. These are the surfaces where
  an animated color is actually visible app-wide.
- `SwatchEffect` rendering: reuse existing motion tokens — pulse =
  `Curves.easeInOut` alpha/scale loop at `Durations.base`, shimmer =
  moving gradient sweep, glow = static colored BoxShadow bloom (cheap),
  aurora = slow hue drift (most expensive — cap at 1 instance).
- **ReduceMotion:** all effects render as the static color — mandatory,
  matches existing `ReduceMotion.of(context)` convention.
- Degradation: unknown/legacy ARGB → `none`. Old peers/presets unaffected.

## 4. Picker UI (C2 scope preview)

`_PaletteColorSheet` gains two tabs, becoming 7 total — but the tab strip
already wraps 5 across 2.5 rows; **recommend replacing the tab strip with a
segmented group row**: `CURATED | RAMPS | SPECIAL` (3 groups), where RAMPS
adds a second row of 12 hue chips + a 32-swatch horizontal strip, SPECIAL
shows the 64 animated swatches in the existing 10-col grid.

- Ramp swatch: plain circle, selected = white ring (existing `_swatch`
  pattern). Long-press could preview the full ramp — optional, skip for MVP.
- Special swatch: same circle but **animates its own effect at low
  intensity** so users see what they're picking. One shared
  `AnimationController` (vsync: sheet state) drives all 64 via
  `AnimatedBuilder` — NOT 64 controllers. Static under ReduceMotion.
- Favorites row unchanged — special colors favorite like any ARGB.

## 5. Perf budget

- 384+64 new swatches are data-only until the sheet opens; sheet builds
  lazily per tab (current `GridView.count` already lazy).
- Animated specials: 1 controller + 64 `AnimatedBuilder`s repainting only
  their own `CustomPaint`/decoration — cheap. Cap `cacheWidth` N/A (no
  images). RepaintBoundary per swatch unnecessary at 22px.
- Ramp generation: 384 `Color` objects built once at first access
  (~microseconds); no per-frame cost.

## 6. Tests (C3)

- `color_ramps_test.dart`: 12 ramps × 32 shades; all argb unique across the
  set; lightness monotonic per ramp; endpoints differ from mid.
- `special_colors_test.dart`: exactly 64; unique argb; every entry has
  label + valid effect; `byArgb` round-trips a stored int.
- Widget: sheet renders RAMPS group chips + SPECIAL grid without overflow
  at 360px and 800px widths; selecting a special swatch pops its ARGB and
  `ColorFavorites.setSlot` round-trips it.
- Pref round-trip: `glowCustomColor = special.argb` → `glowColor` resolves
  → registry returns the effect (proves behavior survives restart).

## 7. Open questions (recommendations inline)

1. **Hue group list** — proposed 12 above; user may want fewer/more
   (e.g. add SLATE/NEUTRAL ramp for grays). **Rec:** ship 12, neutrals stay
   in CURATED.
2. **Effect set** — proposed none/glow/pulse/shimmer/aurora. **Rec:** ship
   all 5; aurora reserved for ≤8 swatches to bound GPU cost.
3. **Where specials apply** — glow + theme accents only (phase 1) vs
   every colored surface. **Rec:** phase 1 — effects on text/badges would
   be noise.
4. **Dead HSV dialog** — wire into sheet as "CUSTOM" tab or delete.
   **Rec:** wire it — it's already built and tested-looking; gives true
   free-form picking the curated grids can't.
5. **`glowColors` dedupe** — fold into C2 (regenerate the 48-list from
   ramp mid-shades + keep the named labels).

## 8. File map (C2 estimate)

| File | Change |
|---|---|
| `lib/theme/color_ramps.dart` | NEW — ramps + generation |
| `lib/theme/special_colors.dart` | NEW — 64 specials + registry |
| `lib/screens/experience_studio_screen.dart` | `_PaletteColorSheet` group strip + RAMPS/SPECIAL tabs; wire dead HSV dialog as CUSTOM |
| `lib/services/theme/theme_flair_prefs.dart` | dedupe `glowColors` (optional) |
| `lib/widgets/ambient_glow*.dart` / theme overlay | effect rendering for glowColor |
| `test/color_ramps_test.dart`, `test/special_colors_test.dart` | NEW |

Effort: C2 ≈ M–L (picker rework is the bulk; effects rendering is small).
C3 ≈ S.
