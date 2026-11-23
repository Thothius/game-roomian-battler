# Hole Report — 2026-11-23

**Session:** H (detective hole-hunt) — **L4 slice only** (lifecycle/async).
**Agent:** PARALLEL (Devin, Slot 3) — read-only audit, no code changes.
**Scope:** undisposed `AnimationController`/`Timer`/subscriptions, missing
`context.mounted` after `await`, unguarded `setState` in async callbacks.

## Method

1. Enumerated all `AnimationController(` sites (51), `Timer(` (34),
   `Timer.periodic` (8), `.listen(` (1) under `lib/`.
2. Cross-checked every controller/timer/subscription field for a
   `.dispose()`/`.cancel()` call — automated scan + manual verification.
3. Scanned every `await` in UI-layer files (`screens/`, `widgets/`) for
   subsequent `context.`/`Navigator.`/`setState` use without a `mounted`
   guard in the same callback — 33 candidates, manually triaged.

## Verdict: lifecycle hygiene is GOOD

The codebase is noticeably cleaner than the bug history suggests. The
three ticker bugs fixed earlier this week appear to have been the last
of their kind — no systematic leak remains.

- **Controllers:** all 51 `AnimationController` sites dispose correctly.
  The 4 flagged by the automated scan (`_demo`, `_glow` ×2, `_pulse`)
  all use the nullable `_x?.dispose()` lazy-create pattern — verified
  each disposes on state exit AND on feature toggle-off.
- **Timers:** all 34 `Timer(` + 8 `Timer.periodic` sites cancel properly.
- **Subscriptions:** the single `.listen(` (`theme_overlay.dart:76`
  accelerometer stream → `_sensorSub`) is cancelled in `dispose()` (:99);
  its callback writes to a static notifier, not `setState` — safe.
- **Async guards:** every `await Navigator.push/pushReplacement` site
  checked (`browse_screen` ×2, `mp_lobby_screen` ×3, `quiz_home_screen`)
  has an explicit `if (!mounted) return;` or `if (mounted && ...)`.
  `mp_connect_screen`'s delayed auto-pop is double-guarded.
  `mp_recovery`'s delayed radio restart checks `_active`.

## Findings (all LOW severity — narrow crash windows)

All three are the same pattern: `await` on a fast persistence/theme call
(SharedPreferences / `AppTheme.*` — microseconds-to-ms) followed by
`setState`/`_closeAfterCommit` with no `mounted` check. Crash requires
the user to pop the screen inside that tiny window. Real but unlikely.

| # | File:line | Pattern | Route |
|---|-----------|---------|-------|
| L4-1 | `lib/screens/experience_studio_screen.dart` ~2671–2705 (`_seedFromEntry`) | `await VisualPrefs.replaceAndPersist(...)` / `saveCustomThemeData` → `setState` ×2, no mounted guard | **FIX-NOW** |
| L4-2 | `lib/screens/experience_studio_screen.dart` ~4095 (unicorn palette dot `onTap`) | `await AppTheme.setUnicornPalette(p)` → `setState(() {})`, no mounted guard | **FIX-NOW** |
| L4-3 | `lib/screens/experience_studio_screen.dart` `_closeAfterCommit` (:222–230) called after awaits in `_applyEntry`/`_saveAndApply` | `setState(() => _allowPop = true)` unguarded; only the post-frame pop checks `mounted` | **FIX-NOW** |

**Fix shape:** add `if (!mounted) return;` after each await (L4-1, L4-2)
and guard the `setState` in `_closeAfterCommit` (L4-3). ~4 lines total,
zero behavior change. Trivial enough to fold into any session's
scope-creep allowance, or a 5-minute FIX-NOW pass.

## Not covered (deferred to remaining H lenses)

- L1 data-vs-dump, L2 schema backward-compat, L3 dead surfaces,
  L5 honesty, L6 error paths, L7 perf, L8 docs, L9 test blindspots —
  each is its own slice. L4 found the codebase clean; the remaining
  lenses hunt different bug classes.

## H-L9 — Test blindspots (formalized from fresh lcov, post-S1)

Parsed `coverage/lcov.info` from the S1 coverage run (753 tests, 48.1%
baseline). Ranked by **uncovered lines** — this is S2's priority queue.

### Tier A — 0–1% coverage, biggest absolute holes

| Uncovered | File | Note |
|---|---|---|
| 528 | `screens/neo_skeuo_lab_screen.dart` | Dev tool — arguably *should* stay untested; flag for S5 decision (exclude from widget targets or smoke-only) |
| 484 | `widgets/item_detail/item_body_sections.dart` | Largest real UI hole — **S2.1 top priority** |
| 417 | `screens/quiz/quiz_session_screen.dart` | **S2 quiz batch** |
| 407 | `widgets/item_detail/gun_stats_sections.dart` | **S2.1** — pairs with body_sections, same detail screen |
| 353 | `widgets/dashboards/compact/dash_items.dart` | **NEW — not on old list**; compact dashboard cluster |
| 342 | `widgets/dashboards/compact/dash_forms.dart` | same cluster |
| 324 | `widgets/dashboards/special_gun/gun_evo_dashboards.dart` | same cluster |
| 312 | `widgets/dashboards/compact/dash_counters.dart` | same cluster — **~1330 lines at ~1% combined** |
| 265 | `screens/shrine_picker/shrine_sheet.dart` | shrine picker untested |
| 261 | `widgets/periodic_tile.dart` | **S2** |
| 232 | `widgets/active_run/dice_roll.dart` | **S2** |
| 221 | `screens/shrine_picker_screen.dart` | pairs with shrine_sheet |
| 217 | `widgets/periodic_tile/tile_logic.dart` | mixin — widget test via tile |
| 210 | `widgets/paradox/paradox_player_panel.dart` | **S2.6 / S4 overlap** |
| 194 | `screens/quiz/quiz_home_screen.dart` | quiz batch |
| 186 | `widgets/paradox/surprise_overlay.dart` | **S2.6 / S4 overlap** |
| 186 | `screens/ammonomicon_detail_screen.dart` | **S2** |
| 171 | `screens/active_run/mp_handlers.dart` | mixin — S4 territory |

### Tier B — partial coverage, big absolute gaps

| Uncovered | File | cov% |
|---|---|---|
| 448 | `widgets/particle_engine.dart` | 35% — visual core, only ambient tests touch it |
| 445 | `widgets/avatar_aura.dart` | 18% — **NEW finding**, aura widget nearly untested |
| 375 | `screens/experience_studio_screen.dart` | 81% of 1945 — absolute biggest file, decent % |
| 314 | `widgets/active_run/active_run_helpers.dart` | 7% — **NEW finding** |
| 284 | `widgets/theme_overlay.dart` | 12% — tilt/liquid core |
| 283 | `providers/run_provider.dart` | 54% — core, watch for S3 |
| 268 | `screens/ammonomicon_screen.dart` | 40% |
| 264 | `widgets/active_run/player_page.dart` | 25% — **active-run core UI** |
| 216 | `services/mp/mp_link.dart` | 25% — transport, S4 |

### S2 re-prioritization (supersedes old file list)

1. **item_detail pair** (`item_body_sections` + `gun_stats_sections`, ~890 uncovered) — one screen, one harness
2. **compact dashboards cluster** (~1330 uncovered across 4 files) — NEW, biggest single win available
3. **quiz batch** (`quiz_session_screen` + `quiz_home_screen` + `quiz_chest`, ~740)
4. **shrine picker pair** (~486)
5. **active-run trio** (`periodic_tile`+`tile_logic`, `dice_roll`, `player_page`, `active_run_helpers` — ~1240)
6. **paradox pair** (`paradox_player_panel` + `surprise_overlay`, ~396) — coordinate with S4
7. `ammonomicon_detail_screen` (186), `neo_skeuo_lab` decision (528 — recommend smoke-only or exclusion)

**Route:** feeds S2 session scope directly. `neo_skeuo_lab` is a dev-only
screen — recommend documenting it as intentionally untested rather than
spending S2 hours on it.

## Claims trace

- Slot 3 ACTIVE on this slice → release on commit of this report.
- No `lib/` files touched. Zero collision risk with any slot.
