# Masterplan — 5 Sessions to Done

> Goal: take GungeonMate from "feature-complete ~85–90%, proof thin" to
> verified, hardened, release-ready. **APK build/release is explicitly
> OUT of scope** — this plan ends at "everything proven and polished".
>
> Baseline at plan time: 686 tests green, analyze 0 issues, **47.5%
> line coverage** (14,375/30,290), v3.7.0 committed, ~4 commits unpushed,
> Gradle 9.3.1 / AGP 9.1.0 toolchain landed (`e4b7fba`).

## RULE — claims leave a trace

**Whomever picks up a session or task MUST record who has what at hand
right now.** Before starting: add your name/slot + the task IDs you're
taking to the **Claims** table below (status `IN_PROGRESS`). When you
finish or hand off: update status (`DONE` / `BLOCKED`), note the commit
SHA, and list anything still in your hand (uncommitted files, half-done
sub-items). If you abandon mid-task, mark `STALE` with a one-line note —
do not silently drop it. This table is the coordination log for this
plan; `AGENT_STATUS.md` remains the live agent board.

| Session / Task | Claimed by | Status | Commit | In hand right now |
|---|---|---|---|---|
| S1 CI + logic tests | _unclaimed_ | PENDING | — | — |
| S2 widget coverage | _unclaimed_ | PENDING | — | — |
| S3 data truth | _unclaimed_ | PENDING | — | — |
| S4 MP hardening | _unclaimed_ | PENDING | — | — |
| S5 release readiness | _unclaimed_ | PENDING | — | — |

---

## Session 1 — "Prove the core" (test infrastructure)

Everything else depends on regressions being caught automatically.

- [ ] **Push pending commits** — ~4 commits ahead of origin (incl.
      `bb75fc3` test batch); do this first so CI has something to run.
- [ ] **CI workflow** — `.github/workflows/test.yml`: on push/PR to
      master → `flutter analyze` + `flutter test`. Pin Flutter version
      to match local (`3.29.x` line). ~30 lines of YAML.
- [ ] **Unit tests for pure logic** (0% coverage today):
  - `lib/widgets/periodic_tile/tile_logic.dart` (217 lines)
  - `lib/widgets/active_run/dice_roll/dice_roll_logic.dart` (158)
  - `lib/screens/active_run/mp_handlers.dart` (171)
  - `lib/services/effect_tagger.dart`, `run_lifecycle.dart`,
    `paired_partners_store.dart`, `haptics.dart`
- [ ] **Coverage ratchet** — generate `coverage/lcov.info` in CI;
      fail if line coverage drops below the recorded baseline (47.5%).
      Store baseline in repo (e.g. `test/coverage_baseline.txt`).
- [ ] **`MissingPluginException` hygiene** — audit test files lacking
      `SharedPreferences.setMockInitialValues`; the noise masks real
      failures (seen in `_smoke_detail_test` output).

**Done when:** CI green on master, logic files >70% covered, coverage
gate active.

## Session 2 — "Prove the surfaces" (widget tests for 0% UI)

Widgets dir is at **34.2% coverage** — the biggest proof gap. Prioritize
by size × user visibility.

- [ ] `lib/widgets/item_detail/item_body_sections.dart` — **484 lines,
      0%** — largest single hole; detail-screen body renderer.
- [ ] `lib/widgets/item_detail/gun_stats_sections.dart` — 407 lines, 0%.
- [ ] `lib/screens/quiz/quiz_session_screen.dart` — 417 lines, 0%;
      plus `lib/widgets/quiz/quiz_chest.dart` (130).
- [ ] `lib/widgets/periodic_tile.dart` (261) + `dice_roll.dart` (225) —
      the two most-tapped run widgets.
- [ ] `lib/widgets/paradox/paradox_player_panel.dart` (210) +
      `surprise_overlay.dart` (186) — MP presentation (may delegate to
      S4 if that session runs first — see overlap note).
- [ ] `lib/widgets/inventory_list_row.dart` (163),
      `lib/screens/ammonomicon_detail_screen.dart` (182),
      `lib/screens/effects_summary_screen.dart` (159),
      `lib/widgets/active_run/emote_animations.dart` (113).

**Overlap note:** paradox/surprise widgets serve both S2 (coverage) and
S4 (MP hardening). Whoever claims first does the widget tests; the other
reviews the assertions for protocol correctness.

**Done when:** widgets coverage ≥60%, every file above has at least a
render smoke test.

## Session 3 — "Data truth" (correctness sweep)

- [ ] **U-015** — `items.json` id collision: `Junk` claims id 580 (dump
      says SackKnightBoon); `Ser Junkan 1` id is null. Fix provenance,
      add integrity test so id collisions can't recur.
- [ ] **U-001** — re-capture `08_char_select.png` (white/blank
      screenshot, cosmetic). Needs a clean Playwright/browser session.
- [ ] **Mojibake final proof** — grep sweep for `�` across
      `assets/data/*.json`; mark verified with output or fix stragglers.
- [ ] **Unsurfaced item fields** — feedback item 5: item `effect` and
      `ammonomicon_entry` fields exist in JSON but aren't shown in item
      detail UI. Wire them in (effect line may already render — verify
      first, then add ammonomicon_entry if missing).
- [ ] **XtG wiki-text filter** — feedback item 6; confirm status and
      implement or close with reason.
- [ ] **Synergy-scan perf proof** — H13 memoization landed; verify with
      an actual measurement (timing test or profile), don't assume.

**Done when:** U-015 fixed + regression test, U-001 re-captured, all
feedback items 5–6 resolved or explicitly closed, perf claim proven.

## Session 4 — "MP hardening" (multiplayer edge cases)

- [ ] **First-endpoint mis-pair race** — last open MP protocol bug
      (deferred list). Repro, fix, regression test.
- [ ] **Host-gone hint coverage** — H16 deduped handlers; verify the
      "partner may have left" hint fires on ALL disconnect paths
      (timeout, kill, airplane mode). Add missing-path test.
- [ ] **Reconnect UX audit** — `mp_reconnect_banner`, blank-view guards,
      2-min partner-left hint: widget-test the states users see.
- [ ] **Protocol version skew** — old-peer compat: the `spriteKey`/
      `sprite` rename in surprise messages is NOT forward-compatible
      (new build → old peer drops sprite). Decide: accept + document,
      or add dual-write. Test old↔new message handling either way.
- [ ] **`toJson` contract cleanup** — `MpSurprise.toJson()` emits
      `'type'` + always-includes empty fields, violating the documented
      "no type field" contract (suspect spot #2 in gungeon_mate/AGENTS.md).
      `fx` field has no sender yet — wire one or remove.
- [ ] Custom surprise `:icon:` hint parses nothing — chat parses
      `:key:` tokens, surprise card doesn't (suspect spot #4). Fix or
      fix the hint text.

**Done when:** mis-pair race fixed + tested, all suspect spots from
AGENTS.md resolved, reconnect states widget-tested.

## Session 5 — "Release readiness & polish sweep"

The pre-release gate — everything proven above gets a final polish pass.

- [ ] **Neo-Skeuo dark-island audit** — remaining hardcoded surfaces
      under the paper skin: `neo_skeuo_lab`, asset viewer, shrine
      picker, quiz screens, bug-report sheet.
- [ ] **Reduced-motion + ticker audit** — systematic grep for
      `AnimationController` + `.repeat(`; every one must respect
      `ReduceMotion`/`disableAnimations`. We fixed 3 manually; find the rest.
- [ ] **Asset diet round 2** — verify H7 cull left no orphan
      references; confirm `uni_5` + wallpaper decode sizes in the APK
      manifest; check for newly-dead assets from this session's work.
- [ ] **Responsive sweep** — ≤500px overflow pass across browse, detail,
      studio, settings (one row-overflow was fixed; check siblings).
- [ ] **Changelog/version lockstep** — `changelog.json` ↔
      `VERSION_HISTORY.md` ↔ `pubspec.yaml` ↔ `kAppVersion` all in sync
      (`version_lockstep_test` enforces — verify it passes).
- [ ] **Docs sync** — TECHNICAL_REFERENCE, REWORK_LESSONS_LEARNED,
      USER_BUG_LIST final state honest.
- [ ] **Final gate** — `flutter analyze` 0 issues + `flutter test` all
      green + coverage report regenerated. THIS is "we are done".

**Done when:** all boxes checked, final gate green, hand off to user for
the actual APK build (out of scope here).

---

## Suggested order & parallelism

```
S1 (CI) ──► S2 (widget tests) ──┐
         └─► S3 (data truth) ──┼──► S5 (polish gate)
              S4 (MP) ─────────┘
```

- **S1 first, always** — CI makes every later session verifiable.
- **S2 ∥ S3** — tests vs data, disjoint files, safe in parallel.
- **S4** needs MP context fresh; good solo session or pair with S2's
  MP widget overlap.
- **S5 last** — it's the gate, not a feature session.
