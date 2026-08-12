# 🔥 Bullet Hell Edition — Release Plan

> **Persistent reference for the next major release.** All agents working on
> bugs/features tagged for this edition should read this doc first and keep
> it in sync as items land. The edition is a branded milestone, not a single
> patch — fixes accumulate under one banner until we ship the APK.

---

## Identity

| Field | Value |
|-------|-------|
| **Edition name** | Bullet Hell Edition |
| **Version** | `v2.0.0` (build `+79`) |
| **Title (changelog/main menu)** | `🔥 BULLET HELL EDITION` |
| **Status** | IN PROGRESS — accumulating fixes |
| **Started** | 2026-08-12 |
| **Folds in** | The v1.8.39 hotfix batch (BUG-017/019/020) — no separate v1.8.39 ship |

---

## Scope — Bug Lineup

### Landed (done, committed)
| Bug | Sev | Summary | Commit |
|-----|-----|---------|--------|
| BUG-017 | HIGH | Max Pane synergy: added `Glass Guon Stone` to items array so it flags active when both are owned | `e0f928b` |
| BUG-019 | HIGH | MP reconnect: floating "Connection restored — sync resumed" snackbar + `Haptics.success()` on real reconnect (not teardown) | `e0f928b` |
| BUG-020 | MED | Quality `1S` → `S` across 36 data entries (guns 19 + items 17); browse sort simplified | `e0f928b` |

### Pending (in the Task Queue, ready for Coder pickup)
| Bug | Sev | Summary | Notes |
|-----|-----|---------|-------|
| BUG-035 | UX | PeriodicTile gun panel: gun type below title (centered addon-panel) + RANGE on the periodic grid alongside DPS | Touches `periodic_tile.dart` — coordinate with pre-existing uncommitted UI tweaks in that file (see AGENT_STATUS handoff) |
| BUG-036 | UX | Active run HeaderMenu: quick "Reset Player Items" action + move Settings to bottom section | Lift `_confirmClearInventory` from `run_tab.dart` to share |
| BUG-037 | UX | Remove MP Summary panel/tab (SummaryTab + MpSummaryPage) | Leave `summary_tab.dart` on disk (Safety S4) — just unwire it |
| BUG-038 | HIGH | Unicorn theme: particles don't show + palette selector scrolls + no per-palette particle previews | Largest scope — theme+particle system. Prefer overlay-side preset override over clobbering global pref |
| BUG-039 | MED | S-tier chest/quality colors unreadable — revert to documented black pill + white text + gold glow across `QualityBadge` + `_ChestChip` + `PeriodicTile` | Touches `item_detail/header.dart` — coordinate with pre-existing uncommitted UI tweaks (see AGENT_STATUS handoff) |

### Optional / consider folding in (open bugs, lower priority)
| Bug | Sev | Summary |
|-----|-----|---------|
| BUG-018 | MED | Browse screen has no empty-search state |
| BUG-021 | MED | 46 active items missing `recharge_time` |
| BUG-022 | MED | 289 synergies missing local icon assets |
| BUG-023 | LOW | 3 guns missing wiki notes content |
| BUG-024 | LOW | 2 items missing wiki content |
| BUG-026 | MED | Browse grid add-button tap target too small |
| BUG-027 | LOW | Item detail buttons lack haptic feedback |
| BUG-028 | LOW | Collapsible sections pop instead of animate height |
| BUG-029 | LOW | Quick Add sheet search results limited to 6 |
| BUG-032 | LOW | `catch (_) {}` silently swallows SharedPreferences errors |
| BUG-033 | LOW | Browse filter chips use emoji instead of Material icons |
| BUG-034 | LOW | Favourites heart toggle clears all snackbars |

> The optional list is the "and things" of the edition — fold in as many as
> time allows before the APK build. The UX polish group (BUG-018/026/027/028/
> 029/033/034) is the natural second batch after BUG-035–039.

---

## Styling & Branding Direction

- **Changelog entry** (`assets/data/changelog.json`): single entry, version
  `v2.0.0`, title `🔥 BULLET HELL EDITION`, date `August 2026`. Each fix is a
  punchy headline item with a leading emoji (💥/🔗/✨/🎯…). As pending bugs
  land, append their headline items to the same `items` array — do NOT create
  a second v2.0.0 entry.
- **Main menu** (`main_menu_screen.dart`): version string `v2.0.0`, changelog
  button `Changelog (v2.0.0)`, subtitle line `v2.0.0 — BULLET HELL EDITION`.
- **VERSION_HISTORY.md**: one `## v2.0.0 — 🔥 BULLET HELL EDITION` section with
  "Landed so far" + "Coming in the edition" subsections; move pending items to
  "Landed" as they commit.
- **APK filename** (when shipped): `gungeon-mate-v2.0.0-bullet-hell-edition.apk`
  — include the edition slug for discoverability.
- **Aesthetic**: keep the dark neon Gungeon look. The edition is a branding
  moment, not a reskin — no new color system. Particle/haptic polish from
  BUG-038/039 should feel like the "bullet hell" energy: snappy, bright, alive.

---

## Ship Checklist (when ready to release)

1. All targeted bugs fixed + bughunted + committed.
2. `flutter analyze` clean on all modified files.
3. Changelog `items` array finalized — no "coming soon" placeholders left.
4. VERSION_HISTORY "Coming in the edition" section emptied into "Landed".
5. `pubspec.yaml` version confirmed `2.0.0+79`.
6. Build release APK → `app-releases/gungeon-mate-v2.0.0-bullet-hell-edition.apk`.
7. Tag `v2.0.0` + GitHub Release with APK asset.
8. Update AGENT_STATUS Session Log with the edition ship row.

---

## Coordination Notes

- **Maintainer** logged BUG-035–039 with implementation-ready detail (commit
  `73569c9`, outer repo). Coder picks them up from the Task Queue.
- **Pre-existing uncommitted UI tweaks** in `lib/widgets/item_detail/header.dart`
  and `lib/widgets/periodic_tile.dart` (from the prior Coder session) overlap
  with BUG-035 and BUG-039. The Coder must coordinate/stash before starting
  those two to avoid clobbering (see AGENT_STATUS Session Log note).
- `gungeon_mate/` is a nested git repo — code commits land there; the outer
  repo holds docs + AGENT_STATUS. Keep both in sync on edition progress.

---

## Feature: Stat-Group Tag Upgrade (bigger + theme-tied colors)

> **Status:** PLANNED — not yet implemented. This is a Bullet Hell Edition
> visual upgrade. Folds in naturally alongside BUG-035 (PeriodicTile rework)
> and BUG-039 (S-tier color revert) since all three touch the stat/quality
> visual language. Track as a feature, not a bug — no BUG-NNN ID.

### What the user asked for

1. **Make the Combat / Handling / Meta group tags bigger** — they're currently
   11.5px and easy to miss. Make them clearly readable.
2. **Style them with different colors**, tied into the active theme + its
   palette, so the groups are color-coded and visually grouped/interesting.
3. Plan it as a **theme upgrade** — the colors should come from (or derive
   from) the active `ThemeFlair`, not be hardcoded.

### Where the tags live today

- **File:** `lib/widgets/item_detail/gun_stats.dart`
- **Widget:** `StatGroup` (class at lines 27–75) — renders the group label
  (e.g. "COMBAT") as a small `Row(icon + GoopText)` header above a `Wrap` of
  `StatPill`s.
- **Current label style** (lines 53–61): `fontSize: 11.5`, `fontWeight: w700`,
  `letterSpacing: 1.2`, `color: Colors.white.withValues(alpha: 0.65)` —
  **hardcoded grey-white**, no theme tie-in, no per-group color.
- **Current icon** (lines 47–51): `size: 14`, `color: Colors.white.withValues(alpha: 0.6)` —
  also hardcoded grey.
- **Call sites** (3, all in `gun_stats.dart` build method 1085–1325):
  - `StatGroup(label: 'Combat', icon: Icons.local_fire_department, stats: combat)` (1304)
  - `StatGroup(label: 'Handling', icon: Icons.tune, stats: handling)` (1311)
  - `StatGroup(label: 'Meta', icon: Icons.info_outline, stats: meta)` (1320)
- **Stat group contents** (assembled at 1087–1102):
  - Combat: Damage, Fire rate, Magazine, Max ammo, Reload
  - Handling: Range, Shot speed, Force, Spread
  - Meta: Class
- **`StatPill`** (class at 77–210) is the individual stat chip inside each
  group. It already reads `AppTheme.flair` for `chipFilled`/`chipRadius`
  (108–109) and has per-stat accent colors for Charge/Duration (110–114).
  Items also use `StatPill` directly in a flat `Wrap` (`item_body.dart:1110`) —
  no group labels there, so the group-tag change is gun-only.

### Design direction

The goal: each stat group gets a **signature accent color** that (a) is bright
enough to read at the new bigger size, (b) derives from the active theme so it
feels palette-coherent, and (c) is distinct per group so Combat/Handling/Meta
read as three color-coded clusters.

**Two-layer color strategy:**

1. **Base group identity color** (per-group, theme-independent fallback):
   - Combat → red/orrange family (fire/damage energy)
   - Handling → cyan/blue family (precision/control)
   - Meta → amber/gold family (info/meta knowledge)
   These are the "semantic" colors that match the icon glyphs already chosen
   (`local_fire_department` / `tune` / `info_outline`).

2. **Theme palette tie-in** (per-theme override of the base):
   Each `ThemeFlair` can optionally override the three group colors so they
   harmonize with the theme's palette. When a theme doesn't define overrides,
   fall back to the base identity colors. This keeps it lazy: only themes that
   want a custom look opt in.

### Implementation plan

#### Phase 1 — `ThemeFlair` extension (app_theme.dart)

Add three optional fields to `ThemeFlair` (around line 1781, after
`glowSecondary`):

```dart
/// Optional per-stat-group accent colors. When null, [StatGroup] falls
/// back to its semantic defaults (Combat=red, Handling=cyan, Meta=amber).
/// Themes opt in to palette-tied group colors by setting these.
final Color? statGroupCombat;
final Color? statGroupHandling;
final Color? statGroupMeta;
```

Add them to the constructor (with `this.statGroupCombat,` etc., default null)
and to the `_hueShift` copy in the remix path (around 1867–1875) so remixes
inherit + hue-shift them.

Then opt in **per theme** in the flair definitions (the `staticFlair`/`flair`
blocks, lines ~40–760). Examples:
- **Unicorn palettes** (cottonCandy/neon/dreamy/sunset/bubblegum/mulberry):
  - Combat → `flair.primary` (pink/magenta family)
  - Handling → `flair.headlineStat` (violet/light-blue family)
  - Meta → `flair.secondary`
  This makes the groups read as three shades of the unicorn palette.
- **Forge Master**: Combat → forge ember orange, Handling → steel blue, Meta → gold.
- **Frostbite**: Combat → ice cyan, Handling → deep blue, Meta → white-blue.
- **Curseblaster**: Combat → curse purple, Handling → green, Meta → red.
- **Default/Gungeon Classic**: leave null → semantic defaults (red/cyan/amber).
- **Minimalist Paper**: leave null (the paper theme is intentionally muted).

This is the "tie in with themes and their palettes" part — each themed look
gets a coherent three-color group identity.

#### Phase 2 — `StatGroup` widget upgrade (gun_stats.dart)

Rework the `StatGroup` build (lines 39–74):

1. **Bigger label.** Bump `fontSize` from `11.5` → `15` (or `16`). Bump icon
   from `14` → `18`. Bump the letter spacing slightly (`1.2` → `1.5`) to keep
   the caps-spaced look proportional. Bump font weight to `w800`.

2. **Color resolution.** Add a helper that picks the group color:
   ```dart
   Color _groupColor(BuildContext context) {
     final f = AppTheme.flair;
     switch (label.toLowerCase()) {
       case 'combat':  return f.statGroupCombat  ?? const Color(0xFFFF5252); // red
       case 'handling': return f.statGroupHandling ?? const Color(0xFF40C4FF); // cyan
       case 'meta':    return f.statGroupMeta    ?? const Color(0xFFFFD54F); // amber
       default:        return f.primary;
     }
   }
   ```
   Apply this color to both the icon and the label text (replacing the
   hardcoded `Colors.white.withValues(alpha: 0.6/0.65)`).

3. **Group header treatment.** Upgrade the header from a plain `Row` to a
   more "grouped" visual — a small filled pill or a left accent bar so the
   color grouping reads as a panel boundary, not just colored text. Two
   options:
   - **(a) Accent bar:** a 3px vertical bar in the group color to the left of
     the label, like a section divider. Minimal, clean.
   - **(b) Filled pill:** the label sits inside a translucent pill
     (`color.withValues(alpha: 0.12)` bg, `color.withValues(alpha: 0.5)`
     border) — matches the existing `StatPill` filled-chip aesthetic.
   - Prefer **(b)** for themes with `chipFilled: true`, **(a)** for
     `chipFilled: false` (Minimalist Paper) — read `flair.chipFilled` to
     decide. This keeps the group header in the theme's visual language.

4. **Optional: tint the `StatPill`s in the group.** Subtle — give each
   `StatPill` in the group a faint border or label tint in the group color
   (e.g. label color shifts from `Colors.white.withValues(alpha: 0.6)` to
   `groupColor.withValues(alpha: 0.75)`). This makes the whole cluster read
   as color-coordinated. Keep the value text white for readability. Pass the
   group color down via a new `groupColor` param on `StatPill` (optional,
   default null = current behavior). **Items** (`item_body.dart`) pass null
   so item stats stay neutral — only gun stat groups get the color coding.

#### Phase 3 — Verification & edge cases

- **Readability:** at `fontSize: 15–16` with the group color (e.g. red on dark
  bg), confirm contrast ≥ 4.5:1. The semantic defaults (red `0xFFFF5252`,
  cyan `0xFF40C4FF`, amber `0xFFFFD54F`) are all bright enough on the
  `0xFF1E1E22` scaffold. For theme overrides, pick palette colors that are
  bright enough — avoid using a dark palette `primary` for the group color.
- **Minimalist Paper** (`chipFilled: false`): uses the accent-bar treatment,
  group colors stay muted (the semantic defaults are fine; don't opt this
  theme into palette overrides).
- **Unicorn Bubblegum**: `primary` is `0xFFFF80AB` (bubblegum pink) — fine for
  Combat. `headlineStat` is `0xFFB388FF` (light violet) — fine for Handling.
  `secondary` is `0xFFE040FB` (magenta) — fine for Meta. All bright on the
  `0xFF1A0F1E` scaffold.
- **Items** (`item_body.dart`): no group labels, so no change. `StatPill`
  gains an optional `groupColor` param that items don't pass — item stats
  stay as-is.
- **`flutter analyze`** on `app_theme.dart`, `gun_stats.dart`, `item_body.dart`.
- **Visual check:** open a gun with all three groups populated (e.g. a
  full-stat gun) in 3 themes (Gungeon Classic, Unicorn Bubblegum, Forge
  Master) — confirm the group headers are bigger, color-coded, and the colors
  shift with the theme.

### Files touched

| File | Change |
|------|--------|
| `lib/services/app_theme.dart` | Add `statGroupCombat`/`statGroupHandling`/`statGroupMeta` to `ThemeFlair` + constructor + remix copy. Opt in per-theme in flair definitions. |
| `lib/widgets/item_detail/gun_stats.dart` | `StatGroup`: bigger label/icon, group-color resolution, filled-pill vs accent-bar header. `StatPill`: optional `groupColor` param for subtle cluster tinting. |
| `lib/widgets/item_detail/item_body.dart` | No change (items don't use `StatGroup`; `StatPill` call stays null for `groupColor`). |

### Coordination with other edition work

- **BUG-035** (PeriodicTile rework) touches the *inventory grid tile*, not the
  detail screen — no file overlap with this feature. Safe to do in parallel.
- **BUG-039** (S-tier colors) touches `quality_badge.dart` + `item_detail/header.dart`
  + `periodic_tile.dart` — no overlap with `gun_stats.dart`. Safe in parallel.
- **BUG-038** (Unicorn particles) touches `app_theme.dart` (the same file as
  Phase 1 of this feature). If both land in the same session, coordinate the
  `ThemeFlair` edits — one agent should own `app_theme.dart` at a time (AC4).
  Recommend: do this feature's `ThemeFlair` field addition + BUG-038's
  `UnicornPalette.particleConfig` getter in the same pass to avoid a conflict.
- This feature does **not** need a BUG-NNN ID — it's a planned visual upgrade,
  not a defect. Track it via this doc + the Task Queue.

### Suggested Task Queue entry

```
| 6 | Stat-group tag upgrade: bigger Combat/Handling/Meta labels + theme-tied per-group colors (ThemeFlair extension + StatGroup rework) | — | TODO | BUG-038 (both touch app_theme.dart) |
```
