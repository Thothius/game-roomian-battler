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
| Bug/Feature | Sev | Summary | Commit |
|-----|-----|---------|--------|
| **Bullet Hell codex page** | FEATURE | Themed special page under Codex (6th tab) — header graphic + lore/mechanics for Chamber 6. `bullet_hell_codex_screen.dart` + tab wiring + `assets/images/codex/Bullethell_header.png` | `42be72c` |
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

---

## Feature: Quick Theme Selection + Compact Settings (Special Mission)

> **Status:** PLANNED — not yet implemented. Two-part UX upgrade for the
> Bullet Hell Edition. Folds in naturally with BUG-038 (Unicorn theme/particles)
> since both touch the theme picker. Track as features, not bugs.

### User intent

> "make sure themes and theme selection process is quick, interactive and fun.
> combine run and app options in Settings and make them very compact to use
> and select please. we are too cluttered."

Two deliverables:
1. **Quick + interactive + fun theme selection** — the current picker is
   immersive but slow (one full-screen swipe per theme, 3 levels deep to
   reach, apply kicks you to the home screen).
2. **Combine Run + App settings tabs** into one compact, decluttered tab.

### Design decisions (user-approved)

- **Theme picker:** Hybrid — keep the full-screen immersive pager, add a
  quick-access theme strip at the top (jump to any theme), add a main-menu
  quick-launch entry.
- **Settings merge:** Two-column grid of compact action tiles (icon + label,
  no subtitles). Denser, less scrolling.

---

### Part 1 — Quick Theme Selection

#### Current state

- **Entry point:** Only from Settings → VISUALS tab → "CHOOSE THEME PALETTE"
  button (`theme_visuals_tab.dart:144-148`). 3 levels deep.
- **Picker** (`theme_picker_screen.dart`): Full-screen `PageView.builder` with
  `viewportFraction: 1.0` — one theme per full screen. 5 visible themes
  (`kVisibleThemes`: minimalist, unicorn, forgeMaster, robotsCore, custom).
  Swipe to preview, tap "Use This Palette" to apply.
- **Apply flow** (`_select`, line 41-49): calls `Navigator.popUntil((route) =>
  route.isFirst)` — kicks user all the way back to home, losing their place.
- **Palette selector** (`_PaletteSelector`, line 1090-1195): horizontal
  `ListView.separated`, height 64 — already flagged in BUG-038 as needing
  a no-scroll layout.

#### Changes

**(1a) Quick-access theme strip at the top of the picker.**

Add a horizontal row of 5 mini palette-swatch buttons at the top of
`ThemePickerScreen`, between the back button row and the `PageView`. Each
button is a small circle or pill showing the theme's `flair.primary` color
with the theme's icon. Tapping one jumps the `PageView` to that theme
(`_pc.animateToPage(i)`). The active theme's button gets a ring/border.

```dart
// In _ThemePickerScreenState.build, after the top bar Row, before Expanded(PageView):
Padding(
  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
  child: Row(
    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
    children: List.generate(modes.length, (i) {
      final m = modes[i];
      final f = AppTheme.flairFor(m);
      final isActive = m == _activeMode;
      final isCurrent = i == _index;
      return GestureDetector(
        onTap: () {
          _pc.animateToPage(i, duration: 350.ms, curve: Curves.easeOutCubic);
        },
        child: AnimatedContainer(
          duration: 250.ms,
          width: 44, height: 44,
          decoration: BoxDecoration(
            color: f.scaffold,
            shape: BoxShape.circle,
            border: Border.all(
              color: isCurrent ? f.primary : Colors.white24,
              width: isCurrent ? 2.5 : 1.0,
            ),
            boxShadow: isCurrent
                ? [BoxShadow(color: f.primary.withValues(alpha: 0.4), blurRadius: 8)]
                : null,
          ),
          child: Icon(_themeIcon(m), size: 20, color: f.primary),
        ),
      );
    }),
  ),
),
```

Add a `_themeIcon(AppThemeMode)` helper mapping each mode to an icon:
- minimalist → `Icons.minimize_rounded`
- unicorn → `Icons.auto_awesome_rounded`
- forgeMaster → `Icons.local_fire_department_rounded`
- robotsCore → `Icons.precision_manufacturing_rounded`
- custom → `Icons.palette_rounded`

This gives instant jump-to-theme without swiping through all 5 pages.

**(1b) Main-menu quick-launch entry.**

Add a theme-picker launch button to the main menu
(`main_menu_screen.dart`). The main menu already has a settings/gear button —
add a small palette icon button next to it that goes directly to
`ThemePickerScreen`. This makes theme switching 1 tap from the home screen
instead of 3 levels deep.

Look at the main menu's existing action buttons (gear/settings, favourites,
etc.) and add a palette-swatch icon button in the same row. Use
`Icons.palette_rounded` with `AppTheme.flair.primary` color. On tap:
`Navigator.push(context, fastRoute(const ThemePickerScreen()))`.

**(1c) Fix the apply flow — don't pop to home.**

Change `_select` (line 41-49) to pop just the picker screen, not all the way
to home:

```dart
void _select(AppThemeMode m) {
  AppTheme.previewNotifier.value = null;
  AppTheme.setMode(m);
  setState(() => _activeMode = m);
  Haptics.success();
  if (Navigator.of(context).canPop()) {
    Navigator.of(context).pop(); // just pop the picker, not popUntil first
  }
}
```

This way, if you launched from Settings, you land back in Settings. If you
launched from the main menu, you land back at the main menu. The theme is
applied live via `AppTheme.setMode` + the `ThemeOverlay` notifier, so the
background changes instantly — the user sees the new theme as they land.

**Exception:** If launched from the main menu quick-launch (1b), popping
back to the main menu is correct — the main menu will already show the new
theme. No special-casing needed; `pop()` handles both entry points.

**(1d) Add a haptic + visual "applied" confirmation.**

When the user taps "Use This Palette", add a brief success animation on the
button before popping — a scale pulse + color flash — so the apply feels
tactile and fun, not abrupt. Use `flutter_animate` (already imported):

```dart
// In _ImmersiveThemePage, wrap the Apply FilledButton:
.animate(
  onComplete: (controller) {
    if (isActive) controller.reverse();
  },
)
```

Actually simpler: in `_select`, before `pop()`, show a 400ms overlay flash
or just rely on `Haptics.success()` (already there) + the instant theme
change. The instant background color shift IS the confirmation. Keep it
simple — don't over-engineer the animation. The haptic + instant theme
swap is enough feedback.

**(1e) Palette selector no-scroll fix (coordinate with BUG-038).**

BUG-038 already plans to replace the `_PaletteSelector` horizontal
`ListView` with a `Wrap`. This feature's theme-strip (1a) handles
theme-level quick jump; BUG-038 handles palette-level no-scroll. They're
complementary. If both land in the same session, one agent should own
`theme_picker_screen.dart` to avoid conflicts (AC4).

#### Files touched (Part 1)

| File | Change |
|------|--------|
| `lib/screens/theme_picker_screen.dart` | Add quick-access theme strip (1a), fix apply flow to `pop()` not `popUntil` (1c), add `_themeIcon` helper |
| `lib/screens/main_menu_screen.dart` | Add palette quick-launch button next to settings gear (1b) |

#### Edge cases (Part 1)

- **5 themes on a 360px screen:** 5 × 44px circles + 4 × ~12px gaps = ~268px.
  Fits with `spaceEvenly`. On 320px: 5 × 44 = 220 + gaps ≈ 268, still fits.
- **Custom theme has no `flairFor` until configured:** `AppTheme.flairFor(custom)`
  returns the custom flair (or a default). Verify it doesn't crash if the user
  hasn't customized yet — the strip button should still render with a fallback
  color.
- **`popUntil` was there for a reason?** Check if any flow expects to land on
  home after applying a theme. Grep for `ThemePickerScreen` callers — there's
  only one (the VISUALS tab button). After this change, applying from VISUALS
  lands back in VISUALS, which is correct (user can see the theme card update).
  The new main-menu entry (1b) lands back at the main menu, also correct.
- **`previewNotifier` cleanup:** `_select` already sets
  `AppTheme.previewNotifier.value = null` before `setMode` — keep this so the
  overlay switches from preview to active mode cleanly.

---

### Part 2 — Combine Run + App Settings Tabs

#### Current state

- **3 tabs** in `settings_screen.dart`: VISUALS, RUN, APP.
- **RUN tab** (`run_tab.dart`, 368 lines): 4 section headers + 6 tiles.
  Sections: Multiplayer & Co-op (1 card + MP tiles), Inventory Maintenance
  (1-2 tiles), Gameplay Actions (1 tile), Run Data (1 tile), Core Actions
  (1 tile).
- **APP tab** (`app_tab.dart`, 469 lines): 4 section headers + 4 tiles + 1
  card. Sections: Dialogue (1 card with haptics toggle + text speed slider),
  About (1 tile), Dev Tools (1 tile), Data Management (1 tile).
- Both tabs duplicate `_sectionHeader` + `_utilTile` (identical code).

#### Changes

**(2a) Merge into 2 tabs: VISUALS + RUN & APP.**

Change `settings_screen.dart`:
- `DefaultTabController(length: 3)` → `length: 2`
- Tabs: `Tab(text: 'VISUALS')`, `Tab(text: 'RUN & APP')`
- `TabBarView` children: `ThemeVisualsTab()`, `CombinedRunAppTab()`

Create a new widget `lib/widgets/settings/combined_run_app_tab.dart` that
replaces both `RunTab` and `AppTab`. Don't delete the old files yet (Safety
S4) — leave them on disk as dormant, mark with a TODO comment. Once the
combined tab is verified, they can be removed in a follow-up.

**Wait — Safety S4 says don't delete files you didn't create.** The old
`run_tab.dart` and `app_tab.dart` were created by a previous Coder session.
So: leave them on disk, just remove the imports from `settings_screen.dart`
and add `// TODO: remove after CombinedRunAppTab is verified` at the top of
each. The combined tab will lift the logic (confirm dialogs, reset methods)
from both.

**Actually — better approach:** Don't create a new file. **Refactor
`run_tab.dart` into the combined tab** (rename `RunTab` →
`CombinedRunAppTab`, merge App tab's content into it). This avoids leaving
dormant files and keeps the diff smaller. Delete `app_tab.dart` only if the
user confirms (Safety S4 — ask first). For the plan, assume we refactor
`run_tab.dart` in place and leave `app_tab.dart` dormant (remove its import
from settings_screen, add TODO).

**Hmm — Ponytail rule: deletion over addition.** The cleanest path:
- Refactor `run_tab.dart` to become the combined tab (rename class, merge
  app content).
- Remove `app_tab.dart` import from `settings_screen.dart`.
- Leave `app_tab.dart` on disk with a TODO (don't delete without user OK).

**(2b) Two-column grid of compact action tiles.**

Replace the `_sectionHeader` + `_utilTile` (vertical list) pattern with a
responsive 2-column grid. Each tile is a compact card: icon + label only
(no subtitle), ~80px tall, tappable.

Group the tiles into 3 visual clusters with small group labels above each
grid section (not full section headers — just a tiny label):

```
RUN SESSION
[Co-op P2]  [Use Shrine]
[Event Log] [Save MP]

INVENTORY & DATA
[Reset P1]  [Reset P2]
[Changelog] [Dev Tools]

DANGER ZONE
[End Run]   [Reset All Data]
```

The Dialogue card (haptics toggle + text speed slider) stays as a full-width
card above or below the grid — it has interactive controls, not just a tap
action, so it doesn't fit the grid tile pattern.

Layout:
```dart
SliverGrid(
  gridDelegate: SliverGridDelegateWithMaxCrossAxisExtent(
    maxCrossAxisExtent: 180,
    mainAxisSpacing: 8,
    crossAxisSpacing: 8,
    childAspectRatio: 1.8,
  ),
  delegate: SliverChildBuilderDelegate(
    (context, i) => _CompactActionTile(...),
    childCount: tiles.length,
  ),
)
```

Use `SliverGrid` with `maxCrossAxisExtent: 180` so it's 2 columns on phones,
3+ on tablets. Each tile:

```dart
class _CompactActionTile extends StatelessWidget {
  final IconData icon;
  final String label;
  final Color color;
  final VoidCallback onTap;
  // ...
  Widget build(BuildContext context) {
    return Material(
      color: Colors.white.withValues(alpha: 0.06),
      borderRadius: BorderRadius.circular(10),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(10),
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 12),
          decoration: BoxDecoration(
            border: Border.all(color: color.withValues(alpha: 0.2)),
            borderRadius: BorderRadius.circular(10),
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(icon, color: color, size: 22),
              const SizedBox(height: 6),
              GoopText(label, style: TextStyle(
                fontSize: 11, fontWeight: FontWeight.w800,
                color: Colors.white70, letterSpacing: 0.4,
              ), textAlign: TextAlign.center, maxLines: 2),
            ],
          ),
        ),
      ),
    );
  }
}
```

**Danger Zone tiles** (End Run, Reset All Data) get a red-tinted border +
icon to signal destructive action.

**Conditional tiles:**
- "Reset P2" only when `p.runState.hasCoop` (same gate as today).
- "Save MP" only when `mpSession.isActive` (same gate as today).
- "Remove P2" / "Add Co-op" — this is currently a full-width card with a
  button, not a tile. Convert to a grid tile ("Co-op: Add/Remove") that
  opens the existing confirm dialog. The status (SOLO vs P2 ACTIVE) can
  show as a tiny badge on the tile.

**Group labels:** tiny, like the current `_sectionHeader` but smaller:
```dart
GoopText('RUN SESSION', style: TextStyle(
  fontSize: 10, fontWeight: FontWeight.w900,
  color: Colors.white38, letterSpacing: 0.8,
))
```

**Dialogue card:** stays full-width, above the grid:
```dart
// Full-width card with haptics toggle + text speed slider
_buildDialogueCard(flair),
const SizedBox(height: 12),
// Then the grid sections
```

**Multiplayer status card:** the current MP & Co-op card (lines 187-229)
has a status display + button. Convert to a compact full-width status bar
(1 line: "SOLO" or "P2 ACTIVE: Cultist") + the co-op action moves to a grid
tile. Or keep it as a slim full-width card. Decide during implementation —
keep it simple, prefer the slim card.

**Confirm dialogs:** lift `_confirmClearInventory`, `_confirmEndRun`,
`_confirmLeaveMp`, `_confirmRemoveCoop`, `_confirmResetAppData` into the
combined tab. They're all private methods — just copy them in. The
`_confirmClearInventory` lift is also needed by BUG-036 (HeaderMenu reset
action) — coordinate so the dialog ends up in a shared location if both
land in the same session.

**(2c) Remove the duplicated code.**

Both `run_tab.dart` and `app_tab.dart` have identical `_sectionHeader` and
`_utilTile`. The combined tab uses `_CompactActionTile` (new) + tiny group
labels, so the old helpers aren't needed. The confirm dialogs are the only
logic to lift.

#### Files touched (Part 2)

| File | Change |
|------|--------|
| `lib/screens/settings_screen.dart` | 3 tabs → 2 tabs (VISUALS + RUN & APP), update imports |
| `lib/widgets/settings/run_tab.dart` | Refactor into `CombinedRunAppTab` — merge app content, replace list with 2-col grid, lift confirm dialogs |
| `lib/widgets/settings/app_tab.dart` | Remove import from settings_screen, add TODO comment. Leave on disk (Safety S4). |

#### Edge cases (Part 2)

- **`RunTabState` is referenced externally?** BUG-036 plans to lift
  `_confirmClearInventory` from `RunTabState`. Check if anything else
  references `RunTabState` or `AppTabState` — grep before renaming. If
  BUG-036 lands first and extracts the dialog to a shared helper, the
  combined tab just calls the shared helper.
- **Dialogue card height:** the card has a toggle + slider — ~100px tall.
  Full-width above the grid is fine.
- **MP active + coop:** when both MP and coop are active, there are 2 extra
  tiles (Save MP, Leave MP). The grid handles variable tile counts via
  `SliverChildBuilderDelegate`. Verify the grid reflows when tiles
  appear/disappear.
- **Danger Zone:** End Run and Reset All Data are destructive — keep the
  confirm dialogs. The tile just opens the dialog; the dialog does the
  safety check.
- **Dev Tools "Special Items & Guns":** requires a run to be active (checks
  `p.runState.main.character != null`). The tile should still show but
  show the "start a run first" snackbar if tapped without a run. Same
  behavior as today.
- **Tab width:** "RUN & APP" is wider than "RUN" — verify it fits in the
  TabBar on narrow screens. May need `labelPadding` adjustment or shorter
  label like "RUN & APP" → "RUN&APP" if cramped. Test on 360px.
- **`flutter analyze`:** after removing the `app_tab.dart` import, verify
  no unused-import warnings. The `run_tab.dart` refactor must keep all
  imports it still needs (provider, multiplayer_session, etc.).

---

### Coordination with other edition work

| Item | Overlap | Coordination |
|------|---------|--------------|
| **BUG-036** (HeaderMenu reset) | Both lift `_confirmClearInventory` from `RunTabState` | If BUG-036 lands first, it extracts the dialog to a shared helper — the combined tab calls the helper. If this feature lands first, the combined tab owns the dialog and BUG-036 calls into it. One agent should own `run_tab.dart` at a time. |
| **BUG-038** (Unicorn particles) | Both touch `theme_picker_screen.dart` (this feature adds the strip; BUG-038 fixes the palette selector) | One agent should own `theme_picker_screen.dart` at a time (AC4). Recommend doing both in the same session. |
| **Stat-group tag upgrade** (task 6) | Touches `app_theme.dart`, not settings or theme picker | No overlap. Safe in parallel. |
| **BUG-035/037/039** | Different files entirely | No overlap. Safe in parallel. |

### Suggested Task Queue entries

```
| 7 | Feature: Quick theme selection — theme strip in picker + main-menu quick-launch + fix apply flow (pop not popUntil) | — | TODO | BUG-038 (both touch theme_picker_screen.dart) |
| 8 | Feature: Combine Run + App settings tabs into compact 2-column grid (CombinedRunAppTab) | — | TODO | BUG-036 (both lift _confirmClearInventory from run_tab.dart) |
```

### Verification

**Part 1 (theme selection):**
- Open theme picker from Settings → VISUALS: confirm the 5-circle strip
  appears at the top, tapping any circle jumps to that theme instantly.
- Open theme picker from main menu quick-launch: confirm it opens directly.
- Apply a theme: confirm you land back where you launched from (not home).
- Confirm the theme changes live as you swipe (preview notifier works).
- `flutter analyze` on `theme_picker_screen.dart`, `main_menu_screen.dart`.

**Part 2 (settings merge):**
- Open Settings: confirm 2 tabs (VISUALS, RUN & APP), no APP tab.
- RUN & APP tab: confirm 2-column grid of compact tiles, all actions work
  (co-op add/remove, reset P1/P2, shrine, event log, end run, changelog,
  dev tools, reset all data).
- Confirm Dialogue card (haptics + text speed) is present and functional.
- Confirm Danger Zone tiles (End Run, Reset All Data) have red tint + confirm
  dialogs.
- Add coop player: confirm "Reset P2" tile appears in the grid.
- Start MP session: confirm "Save MP" tile appears.
- `flutter analyze` on `settings_screen.dart`, `run_tab.dart`.
- Test on 360px screen: confirm 2-column grid fits, tab label fits.
