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

## Claims trace

- Slot 3 ACTIVE on this slice → release on commit of this report.
- No `lib/` files touched. Zero collision risk with any slot.
