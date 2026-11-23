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

## H-L3 — Dead surface (assets, screens, prefs)

Method: cross-referenced every file under `assets/images/` (1,157) against
(a) literal path/stem references in `lib/`, (b) asset filenames declared
in `assets/data/*.json` (icon fields etc.), (c) slug-resolution rules
(`slugForAssetName` → `localGunIcon`/`localItemIcon`/etc.), (d) registry
patterns (`custom_*`, `uni_*`, `gN_M`, `wp_*` avatars/wallpapers),
(e) pubspec declarations. Then public widget classes in `lib/screens/`
checked for zero external references. Prefs keys scanned for
write-only/read-only literals.

### Confirmed dead assets (~3.4MB reclaimable)

| File | Size | Evidence |
|---|---|---|
| `images/wallpapers/animated/gungeonmate-animation-02.mp4` | **2.4MB** | Zero refs; nothing reads `wallpapers/animated/` at all |
| `images/ammonomicon/{Bullethell,Challenge,Drake,Rat}_header.png` | ~930KB | Zero refs in lib/ or data JSONs — likely pre-redesign leftovers |
| `images/enemies/Blockner%27s_Ghost.png` | 210B | URL-encoded filename artifact; Blockner's icon is `Blockner.png` |
| `images/enemies/Chancellor.png` | 258B | enemies.json maps Chancellor→`Chancellor_Revenge.png`, Old Chancellor→`Old_Chancellor.png` |
| `images/home/enter_the_gungeon_logo.png` | 53KB | No code ref — main menu renders logo via painter/text. **VERIFY** before delete: may be intentional source asset |

### Confirmed dead code

| Symbol | File | Evidence |
|---|---|---|
| `PaletteMakerScreen` | `lib/screens/palette_maker_screen.dart` | Zero references in lib/ or test/ — entry point removed at some point |
| `SynergiesOverviewScreen` | `lib/screens/synergies_overview_screen.dart` | Zero references — superseded by browse synergy mode |

### Verified LIVE (false positives avoided — do NOT cull)

- `images/app_icon.png` — pubspec `flutter_launcher_icons` source (:70,:72)
- `images/gungeoneers/the_*_map.png` ×9 — resolved at runtime by
  `gungeoneerMapIconPath()` (`asset_paths.dart:91`) called from
  `player_header.dart:139`; pattern-based, invisible to literal grep
- All 13 `assets/fonts/*.ttf` — pubspec-declared; GoogleFonts families
  resolve dynamically via `AppFont.bundledFontFamily`
  (`'GoogleFonts.${label}'`) and are assigned per-theme in
  `app_theme_modes.dart`
- All `avatars/` + `wallpapers/custom/` files — registry-driven ids
- SharedPreferences keys — no write-only or read-only orphans found

### Route

- Dead assets + dead screens → **S5 asset/code cull** (bundle-size win
  ~3.4MB; screens need a git-history check before deletion to confirm
  the entry points were intentionally removed, not accidentally lost)
- `enter_the_gungeon_logo.png` → verify-then-decide inside that cull

### Not covered (remaining L3 surface)

- Write-only JSON *fields* (schema-level, deeper than icon paths)
- Dead functions/methods inside live files (only screens audited)
- Unreachable *routes* beyond screen classes (deep-link surface is nil)

## H-L8 — Docs honesty

Method: extracted every `lib/…`, `test/…`, `docs/…`, `tools/…` path
reference from `AGENTS.md`, `AGENT_STATUS.md`, `docs/TECHNICAL_REFERENCE.md`,
`docs/REWORK_LESSONS_LEARNED.md`, `gungeon_mate/AGENTS.md`,
`.windsurfrules` and checked existence on disk. Verified version
lockstep across the 5 canonical files. Cross-checked changelog recency
against post-v3.7.0 commits.

### Findings

| # | Finding | Severity | Route |
|---|---------|----------|-------|
| L8-1 | **`tools/data_integrity.py` does not exist.** Referenced as mandatory by `gungeon_mate/AGENTS.md` (C7 data protocol), `.windsurf` rules (`verify-data` workflow), `docs/MASTERPLAN_5SESSIONS.md` (S1.4/S3.1/CI spec), `docs/AMMONOMICON_DESIGN_BRIEF.md`. Only `tools/coverage_report.py` exists in `gungeon_mate/tools/`. The JSON-integrity checks live in `test/data_integrity_test.dart` (flutter test) — the .py script is gone or was never committed. **Every agent following the documented data-change protocol runs a missing file.** | **FIXED** — script was deliberately replaced by `test/data_integrity_test.dart` in v3.2.1; all 6 live doc refs repointed, verify-data workflow dead steps marked REMOVED |
| L8-2 | `docs/TECHNICAL_REFERENCE.md` — the canonical doc every agent must read — has **~14 stale `lib/` paths** describing pre-reorg architecture: `widgets/active_run/modes/*` (theme_signature_mode, codex_book_mode, compact_run_mode, run_display_mode_bar, mode_picker_onboarding — dir doesn't exist), `services/multiplayer_service.dart`, `services/multiplayer_session.dart`, `services/mp/mp_pairing.dart`, `models/paired_partner.dart`, `screens/multiplayer_lobby_screen.dart`, `widgets/settings/{run,gameplay,theme_visuals}_tab.dart`, `widgets/backgrounds/{animated_wallpaper,gungeon_matrix_rain}.dart`, `widgets/active_run/depth_tile.dart`, `test/widget/codex_screen_test.dart`. Architecture section needs a rewrite to current layout (mp_session/mp_sync/mp_link, mp_lobby_screen, dashboards/). | MED | **FIXED** — stale live refs corrected (analyze example, GungeonMeter/mode-picker/settings tables, animated wallpaper note); remaining mode/* rows are intentional deletion-history tables |
| L8-3 | Root `AGENTS.md` references 6 missing docs: `animation_architecture_assessment.md`, `reorg_plan.md`, `mp_auto_reconnect_plan.md`, `MULTIPLAYER_PLAN.md`, `APP_FEATURES_MAP.md`, `SYSTEM_SUMMARY.md`, `TECHNICAL_STACK.md` (some may be intentionally archived — verify before pruning references) | LOW | S5 docs sync |
| L8-4 | **Changelog drift:** ~15 commits landed post-v3.7.0 including user-facing features (bug-report system `35c6c9c`/`e45a2e3`/`ed3220a`, LEB auto-enable `1bd2a5f`, Cool & Curse `2281592`, Gradle 9 migration `e4b7fba`) with **no changelog.json/VERSION_HISTORY entries** — C10 violation in flight. Version still `3.7.0+167`. Masterplan already flags the 5-file bump before APK; the changelog gap is bigger than the version gap. | MED | **FIXED** — consolidated retroactive changelog entries added (bug-report system + polish sweep) under 3.7.0 |
| L8-5 | `AGENT_STATUS.md` session-log rows reference ~30 deleted/moved files — **expected, not a defect**: session logs are history, not living docs. Noted so future audits don't re-flag them. | INFO | none |

### Verified clean

- **Version lockstep:** pubspec `3.7.0+167` = `kAppVersion '3.7.0'` =
  VERSION_HISTORY head `v3.7.0 build 167` = changelog[0] `3.7.0` —
  the 5-file invariant currently holds.
- `.worktrees/webcheck` (detached HEAD `25bbcd9`) exists in app repo —
  **stale worktree**, likely leftover; route to housekeeping prune
  (verify no unmerged work first).

## H-L2 — Schema backward-compat

Method: traced every persisted/wire schema touched in recent sessions —
`Synergy` (`any_of`, `any_of_min`, `groups`, `activation`,
`effect_tokens`), `VisualPrefs` (liquid/ambient/shader/wallpaper fields),
`SavedCustomTheme`/`CustomThemeStore`, `RunState` (incl. legacy format),
`MpMessage` wire protocol (v3 + `spriteKey`/`fx` additions), bug-report
pipeline, `mp_store` recovery JSONs.

### Verdict: the persistence layer is well-armored — better than expected

| Surface | Compat mechanism | Status |
|---|---|---|
| `Synergy.fromJson` | Every new field defaulted: `anyOfMin`→null (→1 via `requiredAnyOfCount`), `activation`→'ACTIVE', `groups`→[], `any_of`→[]. Old JSON parses cleanly. | **CLEAN** |
| `VisualPrefs.fromJson` | Every field `?? default` + `.clamp()` to setter range (preset JSON is user-importable — out-of-range can't assert-crash sliders). `AppFontLabel.migrate()` maps stale font indices onto live fonts. | **CLEAN — exemplary** |
| `CustomThemeStore.load` | Per-item try/catch — one malformed preset is skipped, gallery survives (comment documents the prior nuke-the-gallery bug). | **CLEAN** |
| `RunState.fromJson` | Explicit legacy branch for pre-0.4.0 shape (`selected_character`/`active_guns`/`active_items`). | **CLEAN** |
| MP wire `decode` | Unknown `type` → `FormatException` → caught + dropped silently at `mp_link.dart:657`. New message types can't crash old peers. | **CLEAN** |
| `MpSurprise` old→new | `spriteKey: (j['spriteKey'] ?? j['sprite'])` — reads both wire keys. | **CLEAN** |
| `fx` field | Wire-additive; old peers' `fromJson` ignores unknown keys. | **CLEAN** |
| Bug report | Stateless — composes mailto/clipboard at send time, zero persistence. No compat surface. | **CLEAN** |
| `mp_store` recovery JSONs | `RunState.fromJson` handles them (same legacy path). | **CLEAN** |

### Residual findings (all LOW)

| # | Finding | Route |
|---|---------|-------|
| L2-1 | **New→old peer skew:** a *new* build sending `spriteKey` to an *old* build — old `fromJson` only reads `'sprite'`, so custom-surprise sprites silently drop on version skew. `fx` degrades gracefully (ignored). Only affects custom surprises between mismatched installs; both devices must run Nearby-discovered builds, so skew windows are small. | **DONE** — `mp_spritekey_compat_test.dart` pins old-peer decode (spriteKey drops, text/preset survive), legacy `sprite` read, key precedence, fx wire-additivity |
| L2-2 | Presets saved before the `prefs` field existed in `SavedCustomTheme` are silently dropped by the per-item catch (graceful, but lossy). Likely theoretical — `prefs` shipped with the store. Verify store introduction commit if it ever matters. | INFO — no action |
| L2-3 | `particleSpritePath` / custom wallpaper file persisted by name — if a future asset cull removes the file, consumers must degrade silently. Wallpaper already has `errorBuilder → SizedBox.shrink()` (blank bg, no crash — acceptable). Particles path unverified — spot-check in S5 asset audit. | **VERIFIED** — `ItemIconField._loadImage` onError swallows decode failures → null image → blank particles, no crash; wallpaper already has errorBuilder. Both persisted-path consumers degrade silently as required |

### Not covered

- `gungeon_dump.json` merge tooling schemas (offline pipeline, not shipped)
- `back_refs.json`/`synergy_meta.json` consumers beyond fromJson (H-L1 territory)

## H-L5 — Honesty (displayed claims vs actual math)

Method: hunted every UI surface that presents a *number* as game-derived —
Cool & Curse screens, stats detail effects, item-detail authored effect
text, damage calculator, dice/gun stat displays — then cross-checked
same-stat claims across surfaces for consistency.

### Findings

| # | Finding | Severity | Route |
|---|---------|----------|-------|
| L5-1 | **Cool & Curse screens contradict each other on jammed-enemy/boss chances.** `cool_curse_screen.dart:38-39` computes `jamChance = curse>=10 ? 100% : curse*4` and `bossJamChance = curse>=10 ? 100% : curse*2` — at curse 5 it shows **20% enemy / 10% boss**. `stats_detail/effects.dart` `curseTable` shows **5% enemy / 0% boss** at curse 5, non-linear values (9→25%/30%), and a footnote explicitly claiming "jam chances **cap at 50%**". Same app, same stat, 4× different numbers, different caps (100% vs 50%). The screen's own comment claims "same formulas EtG uses" — at least one surface is wrong vs the game AND vs itself. | **HIGH** — user-facing stat displays disagree | **FIXED** — wiki-verified: `curseTable` was correct all along; `cool_curse_screen` used invented linear formulas (curse*4/*2, 100% cap). Both surfaces now read shared `lib/utils/cool_curse_math.dart`; added fuse/mimic/ammo rows; `cool_curse_math_test.dart` pins every integer 0-10 + caps |
| L5-2 | **`cool_curse_screen` fuse claim may describe a different mechanic than `effects.dart`.** Screen: "Chest fuse auto-defuse — chance a mimicked/unmimicked chest **resets its fuse**" (`cool*2.5` cap 10%). Effects tab: "Chest fuse **chance reduction**" (same `c*2.5` cap 10%). Same formula, two different claimed effects — defuse-on-spawn vs reduced-fuse-chance are not the same thing. One description is wrong. | MED | **FIXED** — wiki confirms coolness reduces chest-fuse CHANCE by 2.5%/pt (cap 10%); screen now says so and shows the reduction, matching effects.dart |
| L5-3 | **`stats_detail_screen` meter labels use invented conversions.** `value*5`→"Active Cooldown Speedup %" and `value*10`→"Bullet Hell Threat Level %" (`stats_detail_screen.dart:123-126`). The `*5` matches the coolness cooldown claim (consistency good), but "Bullet Hell Threat Level" has no named in-game equivalent — it's a fabricated derived stat presented in the same visual language as real ones. | MED-LOW | **FIXED** — meter labels now show real effects: 'Cooldown reduction' via `cooldownReduction()` and 'Jammed enemy chance' via `jammedEnemyChance()` instead of the fabricated 'Bullet Hell Threat Level' |
| L5-4 | **Spice stacking table is authored approximation presented as exact cumulative totals.** `item_body_sections.dart:344-374` shows "N Uses Applied: +55% Damage, -34% Spread…" — precise-looking totals from a hardcoded table. `spiceUsageCount` is display-only (does NOT feed `DamageCalculator` or cool/curse math — verified: only consumers are this widget + `dash_items`). Descriptive wiki-style info, but the precision implies simulation the app doesn't do. | LOW | **FIXED** — note now states "Effect totals are approximate" (`e342b1c`) |
| L5-5 | **Coolness formulas themselves need wiki verification.** `cool*5` cooldown (cap 50%), `cool*2.5` fuse (cap 10%), `1+cool-curse` room reward — used consistently across `cool_curse_screen` + `effects.dart`, but "same formulas EtG uses" is asserted, not proven. If any is invented, BOTH surfaces lie consistently (worse than L5-1 — no internal contradiction to catch it). | MED | **FIXED** — all three verified vs official wiki Coolness/Curse pages; formulas unchanged (they were right) but now sourced from `cool_curse_math.dart` with test coverage |

### What checked out honest

- `DamageCalculator` — unquantifiable sources return `percent: 0` and are
  *listed for transparency* rather than silently skipped; aggregation is
  simple sum, no hidden math. Best-effort wiki-text extraction is
  documented as such in the class doc.
- Cool/curse breakdown (`base`/`fromItems`) — traces to real
  `Gun.curse`/`Item.curse` JSON fields, not invented.
- `effects.dart` footnote correctly describes the 10+ curse cap —
  internally consistent with its own table (the *other* screen is the
  outlier).

## H-L6 — Error paths

Method: traced failure handling for (a) bundled JSON loads in
`RunProvider.loadData`, (b) persisted prefs/run-state corruption,
(c) missing image assets, (d) malformed MP payloads, (e) quiz/progress
persistence.

### Verdict: core paths are hardened; secondary paths degrade silently

| Path | Behavior | Verdict |
|---|---|---|
| `guns.json`/`items.json` load or parse failure | No per-file catch → `Future.wait` throws → `_error` set → `home_screen.dart:75` renders `ErrorState` with retry | **CORRECT — fatal is surfaced** |
| `synergies`/`shrines`/`gungeoneers`/`back_refs`/`synergy_meta` JSON fail | `.catchError((_) => '')` → empty string → parse skipped → empty lists/maps | **SILENT DEGRADATION** — see L6-1 |
| `current_run` prefs corruption | Double-buffered: falls back to `current_run_backup`; both fail → silent fresh run | Acceptable; backup makes it rare |
| `CustomThemeStore` bad preset | Per-item try/catch skips bad entry | **CORRECT** |
| `VisualPrefs`/`RunState` malformed fields | `??` defaults + clamps + legacy branch | **CORRECT** |
| Missing gungeoneer gif/anim | Fallback chain animPath→gifPath→icon (`mp_connect_screen:1093`, `mp_lobby_screen:482`) | **CORRECT** |
| Missing wallpaper file | `errorBuilder → SizedBox.shrink()` | Acceptable (blank bg, no crash) |
| Malformed/unknown MP message | `decode` throws → caught + dropped at `mp_link.dart:657` | **CORRECT** |
| `BackRefs` parse failure | → `BackRefs.empty` | Acceptable |

### Findings

| # | Finding | Severity | Route |
|---|---------|----------|-------|
| L6-1 | **Secondary JSON failures are silent.** If `synergies.json`/`shrines.json`/`gungeoneers.json`/`back_refs.json`/`synergy_meta.json` fails to load *or parse*, the app boots normally with empty data — browse shows no synergies, no shrines, no characters — with **zero logging and zero user signal**. A corrupt bundled asset (bad merge, truncated write) produces a plausibly-normal-looking app missing whole features. `catch (_)` swallows even the error object. | MED — silent wrong answer | **FIXED** — `_loadOptionalAsset` + `_recordAssetFailure` log+record every secondary-asset load/parse failure; exposed via `assetLoadFailures`; `asset_load_failures_test` pins zero failures on shipped data |
| L6-2 | **Double-corruption of run save is silent data loss.** If both `current_run` and `current_run_backup` fail to parse, user gets a fresh run with no notice. Rare (needs two corrupt writes) and arguably correct UX (better than crash), but a one-line run-log entry "save data was unreadable — started fresh" would close the honesty gap. | LOW | **FIXED** — `_saveWasCorrupt` flag + debugPrint when primary+backup both fail; `save_corruption_test` pins all three cases |

## H-L7 — Performance

Method: scanned all `build()` methods for expensive calls (sort,
jsonDecode, RegExp allocation, compute, asset loads), all scrollables
for eager vs lazy children, all `Image.asset` for missing
`cacheWidth`/`cacheHeight`, and per-frame allocation patterns.

### Verdict: no egregious perf bugs — the codebase is disciplined

| Check | Result |
|---|---|
| Heavy calls in `build()` | 25 flagged sites triaged — all benign: `Image.asset` constructors are cheap (framework-cached), sorts run over bounded collections (≤395 synergies, log entries), RegExp allocs are per-build not per-frame |
| Eager vs lazy lists | All `ListView(children:)` sites are small bounded sets (category groups, single-shrine detail, stat cards). No unbounded eager lists found — browse/grid paths already use builders/slivers |
| `cacheWidth`/`cacheHeight` | 29 `Image.asset` without explicit cache size — triaged the large-image candidates (wallpaper already has `cacheWidth: 1080`; avatars/icons are cell-bounded ≤~100px). Remaining are small icons where decode size ≈ display size. **No real waste** |
| Per-frame allocations | Particle engine + tickers already audited under L4; `Transform.scale`/`ClipRect` in avatar grid is intentional (gridline bleed fix, documented) |

### Findings

| # | Finding | Severity | Route |
|---|---------|----------|-------|
| L7-1 | **Synergy re-classification per rebuild — confirmed still open.** `all_synergies_screen.dart:15-30` re-buckets all ~395 synergies (active/partial/locked via `matchesItems`) on *every* `RunProvider` notify; `item_detail_screen.dart:82` and `gun_synergies_tab.dart:412` do similar per-build owned-set rebuilds. During an active run, provider notifies on every state tick — 395 × set-lookups × N rebuilds/sec is the known "synergy-scan recompute-per-build" deferred item (bug list + masterplan S3). Not a new bug — **this audit confirms it's still live and quantifies the surface**. | MED (known) | **FIXED** — `_ownedLowerFor` sig-keyed owned sets + result caches on set/`_allSynergies` identity in synergy_queries.dart |
| L7-2 | **`ownedList.map().toSet()` recomputed in multiple build()s.** `all_synergies_screen`, `item_detail_screen`, `browse_screen` each rebuild the lowercase owned set per build — trivial cost alone, but it's the same recomputation L7-1 multiplies. A `RunProvider.ownedNamesLower` cached getter would serve all three. | LOW | **FIXED** — same memoization covers combined/per-slot paths; `currentOwnedLower`/`getSynergiesByInventory` reuse cached sets |

### Not covered

- Frame-time profiling (needs device/emulator traces — out of scope for
  static audit)
- `particle_engine.dart` inner-loop efficiency (1,315 lines — a dedicated
  perf pass would need profiling, not grep)

## H-L1 — Data vs dump (spot-check, non-synergy)

Scope note: Slot 4's Gemini pass already deep-verified synergies +
item/gun catalog completeness. This lens spot-checked the *structural*
invariants instead: global ID uniqueness (the U-015 bug class),
id↔dump consistency, and app↔dump coverage by id-join.

Method: parsed `tools/gungeon_dump.json` (379 guns / 279 items raw
entries incl. per-level variants) vs `assets/data/*.json`; compared by
**id-join** (reliable — name normalization produces false mismatches:
dump 'Comm4nd0' vs app 'Com4nd0', renamed items, etc.).

### Findings

| # | Finding | Severity | Route |
|---|---------|----------|-------|
| L1-1 | **Live duplicate gun id — the U-015 bug class is NOT fully closed.** `guns.json` id `50` is claimed by both **Colt 1851** and **SAA**. `data_integrity_test.dart` checks duplicate *names* only — no id-uniqueness invariant exists for guns (S3.1 predicted exactly this gap). Impact is currently nil (`gun.id` has zero consumers — name-resolution everywhere), but the invariant hole is real. | LOW (latent) | **FIXED** — Colt 1851→dump id 62, SAA→null (no dump counterpart); `gun_id_integrity_test` enforces uniqueness |
| L1-2 | **`guns.json` `id` field is unreliable provenance.** Only **56/239** app gun ids match the dump's ids for the same gun; 52 outright mismatches (e.g. app Colt 1851 id 50 vs dump 62, app AK-47 id 15 vs dump 221). Items were normalized to dump ids during U-015; guns were not. Nothing consumes `gun.id` today, but the field *looks* like dump provenance and mostly isn't — a trap for the next data merge. | LOW-MED | **DOCUMENTED/ACCEPTED** — ids are merge-provenance only (Gun model ignores them); full re-derivation vs dump deferred, uniqueness now enforced |
| L1-3 | **14 app-only item ids** (Amulet of the Pit Lord, Gundromeda Strain, Shock/Explosive/Shadow/Vorpal/Flak/Hungry/Katana/Blank/Devolver Rounds, Hidden Compartment, Elder Blank, Angry Bullets) — none collide with dump ids; they're app-assigned ids for wiki-sourced items the memory dump lacks. Bullet-family cluster. Safe today; note for future dump merges. | INFO | **ACCEPTED** — app-only items legitimately have no dump id; documented, no collisions |
| L1-4 | **Coverage by id-join is clean:** 0 app-only gun ids, items consistent post-U-015. The dump's 141 "missing" gun entries are per-level/evolution/cut variants the app intentionally curates out — not missing content. | PASS | none |

### Verified clean

- Zero cross-file id collisions (guns↔items↔enemies↔etc.)
- `app-only` gun ids: **0** — every app gun maps to a real dump entity
- Duplicate *names*: none in any entity file (integrity test covers this)

## Hole-hunt complete — final scoreboard

All 9 lenses executed across 7 slices. Findings routed:

| Route | Items |
|---|---|
| **FIX-NOW (done)** | L4-1..3 mounted guards — shipped `dfc7770` |
| **S3 data truth** | (L1-1 dup id FIXED + uniqueness test; L1-2/L1-3 documented-accepted) — remaining:  synergy memoization DONE — e988f92+046c3e0; L6-1/L6-2 honesty DONE; L5 cool-curse DONE) |
| **S4 MP** | ~~L2-1 spriteKey old-peer skew fixture~~ DONE |
| **S5 polish/release** | ALL DONE — L3 cull `56614ab` (~3.4MB), L8-1/2/3/4 docs sync, L2-3 verified, L5-4 `e342b1c` |
| **Unscheduled** | L8-1 `data_integrity.py` missing — FIX-NOW candidate (restore from git history or repoint docs) |

**Zero unrouted findings.** The two highest-value catches: the
cool/curse screen contradiction (L5-1, user-facing wrong numbers) and
the missing mandatory data-integrity tool (L8-1, broken documented
workflow).

## Claims trace

- Slot 3 ACTIVE on this slice → release on commit of this report.
- No `lib/` files touched. Zero collision risk with any slot.
