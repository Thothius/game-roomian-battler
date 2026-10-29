# Optimization Plan — Lean Codebase Push

> Created 2026-10-29 after the relocation + cleanup session.
> Companion doc: `docs/BIG_FILES.md` (file-split plan).
> Verified baseline this session: `flutter analyze` = **zero issues**
> (was 21 test-side lints); `flutter test` = all green; lib tree free of
> unreferenced files.

---

## Done this session (fluff purge)

- 12 unreachable files deleted (~2,900 lines): `favourites_screen`,
  `gunslinger_codex_screen`, `paradox_codex_screen`, `mode_helpers`,
  `summary_tab` (orphaned `SpongeButton`), `animated_wallpaper`,
  `gungeon_fall_animation`, `cat_throne`, `home_customization_sheet`,
  `junk_particle_field`, `rotating_gungeoneer`, `vortex_lightning`.
- `MpHeader` dead class cut from `player_header.dart` (~335 lines,
  superseded by `ParadoxBar`).
- Vestigial native Android scaffold removed: `app/`, root
  `build.gradle.kts`, `settings.gradle.kts`, `gradlew*`, `gradle/`,
  `gradle.properties` (real module is self-contained under `android/`).
- All 21 test-file lints fixed (unused imports, underscore locals,
  deprecated `.blue` → `.b`).
- `dart format` tall-style pass: 155 files — one mechanical commit,
  ends mixed reflow-diffs in every future change.
- Deleted: `coverage/`, local `dev` branch, 6 stashes, `X:\tmp_flutter`.

## Perf targets (ranked by impact)

### P1 — Synergy predictor recompute-per-build
`browse_screen.dart:818,872` calls `RunProvider.synergiesCompletedBy(name,
slot:)` inside row `build()`. That's a 395-synergy `matchesItems` scan per
visible row per rebuild — the known scroll jank source.
Plan: memoize in RunProvider keyed by `(name, slot, inventoryVersion)`;
bump `inventoryVersion` on any inventory mutation. Rows then hit a Map
lookup. Est. small diff, big win on long lists.

### P2 — `matchesItems` per-build in row filters
`browse_screen.dart:541,578` run full synergy scans during list
filtering/sorting too. Same memoization layer fixes both.

### P3 — JSON mojibake sweep
`�` replacement chars noted in `assets/data/*.json` (AGENTS.md deferred
list). One-off `tools/` script to scan + fix encoding, add a data-integrity
test case so it can't regress.

### P4 — RepaintBoundary audit on remaining CustomPaint widgets
GAP-1 wrapped 8 in Aug; particle_engine + dashboards grew since.
Sweep for `CustomPaint` not wrapped in `RepaintBoundary`.

### P5 — `run_provider.dart` persistence batching
`_scheduleSave()` autosave — verify debounce interval still makes sense
post-unification; encode already off-thread via `compute()`.

## Known open bugs (from AGENTS.md + UI_HEALTH, still open)

| Bug | Where | Severity |
|---|---|---|
| Browse rows overflow ~15px at ≤500px width | `browse_screen` rows | High (primary audience) |
| TIERS mode test regression | `browse_synergies_test` (test-side) | Medium |
| MP first-endpoint mis-pair race | mp_link handshake | Medium |
| Host-gone hint missing | mp_session | Low |
| Item `effect`/`ammonomicon_entry` unsurfaced in detail UI | item_body | Low (data loaded, UI gap) |

## File splits — schedule per `docs/BIG_FILES.md`

Suggested order for next sessions (one per session, green at every step):
1. `app_theme.dart` (4.7k) — palettes first, then flair, then maker
2. `run_provider.dart` (2.0k) — special-trackers extraction
3. `experience_studio_screen.dart` (3.2k) — tab-per-file
4. `compact_dashboards.dart` (1.6k) — dashboard-per-family
5. `particle_engine.dart` (2.0k) — emitter/painter/preset split

## House rules
- One concern per commit; `analyze` + `test` green at every commit.
- No semantic changes inside format/refactor commits.
- Claim a board slot per AGENTS.md before multi-file work.
