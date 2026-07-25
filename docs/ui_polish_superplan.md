# GungeonMate UI Polish Super-Plan

> Consolidated from: Flutter docs review (FAQ, widget index, performance best practices),
> performance audit, UX optimization plan, detail redesign plan, comprehensive app assessment.
>
> **Goal:** Maximize user-visible polish and performance gains, ordered by impact-to-effort ratio.
> Each task is independently committable.

---

## Knowledge Base — What We Learned

### From Flutter Performance Best Practices
- **`Opacity` widget in animations triggers `saveLayer()`** — use color alpha instead
- **`RepaintBoundary` isolates repaints** — critical for animated widgets embedded in scrollable parents
- **`AnimatedBuilder` child pattern** — pass non-animated subtrees as `child`, not rebuilt inside `builder`
- **`const` constructors** — short-circuit rebuilds; use everywhere possible
- **Localize `setState()`** — only rebuild the subtree that changed
- **Lazy list builders** — `ListView.builder`/`GridView.builder` only build visible items
- **Avoid `Clip.antiAliasWithSaveLayer`** — most expensive clip mode (we have 0 — good)
- **`ShaderMask` is expensive** — acceptable with early-return guard when not animating
- **Target 16ms/frame** — 8ms build + 8ms raster for 60fps

### From Flutter Widget Index
- Confirmed available: `AnimatedOpacity`, `AnimatedScale`, `AnimatedSize`, `AnimatedPositioned`, `AnimatedSwitcher`, `TweenAnimationBuilder`, `RepaintBoundary`
- All ready for use in UI polish tasks

### From Flutter FAQ
- AOT compilation → no `dart:mirrors` (we use static JSON — correct)
- Widget composition over inheritance (we follow this)
- Platform channels for native integration (used for Nearby Connections)

### From Performance Audit (this session)
- **1 animated `Opacity` anti-pattern** in `themed_number.dart:363-374` — triggers `saveLayer()` every frame
- **`ShaderMask` in `theme_engines.dart:213`** — acceptable (has early-return guard)
- **7 static `Opacity` widgets** — not animated, low priority, but could use color alpha
- **Only 4 `RepaintBoundary` instances** — `periodic_tile.dart` and `themed_number.dart` lack isolation
- **25 `AnimatedBuilder` usages** — mostly correct child-passing pattern
- **0 `Clip.antiAliasWithSaveLayer`** — clean
- **19 lazy builder instances** — good coverage

### From UX Optimization Plan (Playwright tour)
- SynergiesOverviewScreen was orphaned (now wired up in recent commit)
- EffectsSummaryScreen hidden behind tiny icon
- Run Options is a flat ungrouped list
- Active Run screen extremely dense, no collapsible zones
- Settings Theme tab is a long scroll with duplicated controls
- No undo on destructive actions
- No first-run onboarding

### From Detail Redesign Plan
- Phase 2 done (128px icon, 28px title, metadata chips)
- Phase 3 pending: summary string for guns
- Stats panel refinement pending

### From Comprehensive Assessment
- **Dead code:** `animated_chat_bubble.dart` (317 lines), `vertical_swipe_layout.dart` (141 lines)
- **Dead assets:** `concepts.json` (33KB), `npc_dialogues.json` (36KB) — bundled but never loaded
- **Uncommitted changes:** Wallpaper asset reorganization + code cleanup in working tree
- **0 open bugs** — all 12 fixed
- **Version:** v1.6.8+69

---

## Task List — Ordered by Impact/Effort

### Tier 1: Performance Quick Wins (minutes each, immediate frame-rate impact)

| # | Task | File(s) | Effort | Impact |
|---|------|---------|--------|--------|
| P1 | **Replace animated `Opacity` with color alpha** in themed_number.dart twinkle bullets | `themed_number.dart` | 1 line | Eliminates per-frame `saveLayer()` |
| P2 | **Add `RepaintBoundary` to `periodic_tile.dart`** — isolates tile animation repaints from parent scroll | `periodic_tile.dart` | 1 wrapper | Prevents cascading repaints during scroll |
| P3 | **Add `RepaintBoundary` to `themed_number.dart`** — isolates twinkle animation | `themed_number.dart` | 1 wrapper | Prevents twinkle repaints from triggering parent rebuilds |

### Tier 2: Animation Polish (30-60 min each, visible UX improvement)

| # | Task | File(s) | Effort | Impact |
|---|------|---------|--------|--------|
| A1 | **Hero transitions for item/gun detail** — `Hero(tag: 'entity_${name}')` on browse card icon → detail header icon | `browse_screen.dart`, `item_detail_screen.dart` | ~30 min | Cinematic detail navigation |
| A2 | **`AnimatedSize` for collapsible sections** — wrap expand/collapse transitions in `AnimatedSize` for smooth height morph | `stats_detail_screen.dart`, `multiplayer_lobby_screen.dart`, `item_detail_screen.dart`, `settings_screen.dart` | ~30 min | Smooth expand/collapse instead of instant pop |
| A3 | **`AnimatedSwitcher` for tab content swaps** — cross-fade between Browse tabs instead of instant swap | `browse_screen.dart` | ~20 min | Polished tab transitions |
| A4 | **`AnimatedOpacity` for static `Opacity` widgets** — replace 7 static `Opacity` widgets with `AnimatedOpacity` or color alpha | `active_run_screen.dart`, `synergies_overview_screen.dart`, `item_detail_screen.dart` | ~30 min | Performance + smoother fade-in |
| A5 | **Spring physics for tile poof** — replace linear fade-out with `SpringSimulation` on tile removal | `periodic_tile.dart` | ~40 min | Satisfying bouncy tile removal |

### Tier 3: UX Discoverability (30-60 min each, user-facing impact)

| # | Task | File(s) | Effort | Impact |
|---|------|---------|--------|--------|
| U1 | **Surface EffectsSummaryScreen** — replace tiny icon with "View All Effects" button in section header | `active_run_screen.dart` | ~15 min | Users discover effects summary |
| U2 | **Group Run Options into categories** — Run Actions / Inventory / Reference / Session with icons | `active_run_screen.dart` | ~45 min | Cleaner menu, prevents accidental End Run |
| U3 | **Make SYN counter tappable** — opens SynergiesOverviewScreen | `active_run_screen.dart` | ~5 min | Players see active synergies |
| U4 | **Add undo snackbar after destructive actions** — Reset Items, Steal Item | `active_run_screen.dart` | ~30 min | Safety net for misclicks |

### Tier 4: Dead Code Cleanup (15 min, APK size reduction)

| # | Task | File(s) | Effort | Impact |
|---|------|---------|--------|--------|
| D1 | **Remove `animated_chat_bubble.dart`** — 317 lines, not imported anywhere | `lib/widgets/animated_chat_bubble.dart` | Delete | -317 lines, -11KB |
| D2 | **Remove `vertical_swipe_layout.dart`** — 141 lines, not imported anywhere | `lib/widgets/vertical_swipe_layout.dart` | Delete | -141 lines, -5KB |
| D3 | **Remove `concepts.json` from pubspec assets** — 33KB, never loaded in code | `pubspec.yaml`, `assets/data/concepts.json` | Delete + 1 line | -33KB APK size |
| D4 | **Remove `npc_dialogues.json` from pubspec assets** — 36KB, never loaded in code | `pubspec.yaml`, `assets/data/npc_dialogues.json` | Delete + 1 line | -36KB APK size |

### Tier 5: Detail Redesign Continuation (1-2 hours)

| # | Task | File(s) | Effort | Impact |
|---|------|---------|--------|--------|
| R1 | **Gun summary string** — one-line "Full-auto beam, 25.8 DPS, homing" under metadata chips | `item_detail_screen.dart` | ~45 min | Quick scan of gun capabilities |
| R2 | **Stats panel refinement** — align firing mode + DPS + all stats in clean grid | `item_detail_screen.dart` | ~60 min | Professional stat layout |

### Tier 6: Settings Polish (1-2 hours, from UX plan)

| # | Task | File(s) | Effort | Impact |
|---|------|---------|--------|--------|
| S1 | **Add sub-section chip navigation to Settings** — [Palette] [Wallpaper] [Typography] [Grid] [Particles] [Glow] | `settings_screen.dart` | ~60 min | No more long scroll |
| S2 | **Deduplicate Theme controls** — Settings → Theme tab becomes launcher to Theme Picker | `settings_screen.dart`, `theme_picker_screen.dart` | ~45 min | Removes confusion |

---

## Prerequisites

- **Commit current uncommitted changes first** — wallpaper asset reorganization + code cleanup in working tree
- **`flutter analyze` clean** before starting
- Each task: implement → `flutter analyze` → bughunt → commit

## Execution Strategy

1. **Commit current working tree state** (wallpaper reorg + code cleanup)
2. **Tier 1 (P1-P3)** — performance quick wins, 3 one-line changes
3. **Tier 2 (A1-A5)** — animation polish, one at a time with testing
4. **Tier 3 (U1-U4)** — UX discoverability
5. **Tier 4 (D1-D4)** — dead code cleanup
6. **Tier 5 (R1-R2)** — detail redesign continuation
7. **Tier 6 (S1-S2)** — settings polish

Each task is independently committable. We pause between tasks for testing and user feedback.
