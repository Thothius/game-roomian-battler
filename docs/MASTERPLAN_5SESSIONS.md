# Masterplan — 5 Sessions to Done

> Goal: take GungeonMate from "feature-complete ~85–90%, proof thin" to
> verified, hardened, release-ready. **APK build/release is explicitly
> OUT of scope** — this plan ends at "everything proven and polished".
> NOTE: by S5 the tree will sit ~15+ commits past v3.7.0 — when the
> user green-lights the build, bump the version FIRST per
> `.windsurf/rules/release-checklist.md` (all 5 files in lockstep),
> THEN build.
>
> Baseline at plan time: **726 tests green** (was 686 — Slot 4's
> synergy pass `7f629dd` + bug-report hardening `e45a2e3` landed since),
> analyze 0 issues, **~47.5% line coverage** (14,375/30,290 — recompute
> in S1, expect slight drift), v3.7.0 committed, **7 commits unpushed**,
> Gradle 9.3.1 / AGP 9.1.0 toolchain landed (`e4b7fba`).
> All file paths below verified on disk 2026-11-25; **state refreshed
> after Slot 4's synergy pass-3 (`7f629dd`) — U-015 closed, `any_of_min`
> + `activation` schema fields live.**

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
| S1 CI + logic tests | PARALLEL (Devin, Slot 3) | DONE | app `ddb6d4f` + `54bb84a` | S1.1–S1.5 complete: 753 tests, analyze 0, coverage baseline 48.1%, CI workflow + coverage_report.py committed. **PUSHED** after gh `workflow`-scope refresh; first CI run green (run 45093492984, 3m16s — analyze + tests + coverage gate all pass). tile_logic/dice_roll_logic/mp_handlers/run_lifecycle are widget mixins → deferred to S2. |
| **H Detective hole-hunt** | PARALLEL (Devin, Slot 3) | DONE | `docs/HOLE_REPORT_2026-11-23.md` + app `dfc7770`/`fb4b1ea`/`5e1e033`/`e342b1c`/`e988f92`+`046c3e0`/`56505a0`/`73552a8` + `gun_id_integrity_test` | All 9 lenses done across 7 slices, zero unrouted findings. All routes resolved: FIX-NOW guards `dfc7770`; S3/S4/S5-routed items landed via `56614ab` S5 sweep (L3 dead cull, L8 docs sync, L2-3 verified), `7e9b011` L6-1, L6-2 save-corruption flag; L8-1 `data_integrity.py` repoint landed in root `7cee067` doc sync. Only remaining: release cut (S5 gate / user go-ahead) |
| S2 widget coverage | PARALLEL (Devin, Slot 3) | DONE | app `1d1ae9e`..`fce513d` | 87 widget tests, all 6 priority batches. Coverage 48.1→62.3% overall (widgets 56.5%). 2 test-found bugs fixed. Residual deep-coverage gaps noted in session log |
| S3 data truth | _unclaimed_ | PENDING | — | — |
| S4 MP hardening | _unclaimed_ | PENDING | — | — |
| S5 release readiness | _unclaimed_ | PENDING | — | — |

---

## GLOBAL GROUND RULES (read once, apply everywhere)

**Toolchain** — never bare `flutter`:
```bash
cd X:/GungeonMate/gungeon_mate
/c/src/flutter/bin/flutter.bat analyze
/c/src/flutter/bin/flutter.bat test
/c/src/flutter/bin/flutter.bat test --coverage   # writes coverage/lcov.info
/c/src/flutter/bin/dart.bat format <files>
```

**Git** — two repos: app `gungeon_mate/` → `GungeonMate.git`, root
`X:/GungeonMate/` → `game-roomian-battler.git`. Foreign WIP exists in the
tree (bug-report system from Slot 2 as of 2026-11-25) — **always
`git add <explicit paths>`, never `git add -A`**. Never `git checkout --`
on dirty files. Commit per task (S7), descriptive sentence style, Devin
trailer. Push only when asked.

**Board** — claim a slot in `AGENT_STATUS.md` before code (AC1), update
Files-in-progress as you go (AC2), release + Session Log row at end
(AC3). This doc's Claims table tracks *plan-level* progress.

**Test harness pitfalls — already paid for, do not rediscover:**

1. `SharedPreferences.setMockInitialValues({})` in `setUp` for ANY test
   that builds `RunProvider` — without it you get
   `MissingPluginException` noise that passes anyway and masks failures.
2. `RunProvider` autosave debounce (~400ms timer) → every widget test
   that touches it needs a final `await t.pump(const
   Duration(milliseconds: 500))` (or `pumpAndSettle` where safe) or you
   get "pending timer" failures at teardown.
3. `compute()` isolates **never complete** under `flutter_test`. For
   screens parsing large JSON, add a `@visibleForTesting static bool
   debugParseInline` that bypasses `compute` (see
   `ammonomicon_screen.dart` — copy that pattern).
4. Asset `loadString` futures need `t.runAsync(...)` — but `runAsync` is
   flaky across consecutive tests in one file (real-async zone
   pollution). **Preferred pattern:** a `debugStartLoaded`-style static
   flag that skips data loading entirely for pure UI/nav tests (see
   `ammonomicon_screen.dart` + `ammonomicon_nav_test.dart`). Reserve
   `runAsync` polling for the ONE smoke test that verifies real loading.
5. Finders: `GoopText` renders a `Text` — `find.text` works. But
   `find.text('X')` fails if the string is built via interpolation at
   build time; prefer `find.textContaining` or widget-type finders.
6. Always end widget tests with `expect(t.takeException(), isNull)` —
   overflow/layout exceptions don't fail the test otherwise.

**Definition of "session done" (all sessions):** analyze 0 issues ·
`flutter test` all green · focused new tests pass · changelog entry if
user-facing · Claims table updated · slot released.

**Review rule:** protocol/wire changes (S4.1, S4.4, S4.5) and
persistence/schema changes (S3.1, S1.4 baseline) get a **second-slot
review before merge** — these are the changes that corrupt silently.
Everything else: self-bughunt per S6 is sufficient.

---

## Coverage Trajectory (the ratchet pulls UP, not just holds)

| Checkpoint | Line coverage target | Driver |
|---|---|---|
| Baseline (now) | 47.5% | — |
| After S1 | ~50% | 7 logic files tested |
| After S2 | ~60% | widgets 34%→60%+ |
| After S3 | ~62% | data-integrity tests |
| After S4 | ~65% | MP edge-path tests |
| After S5 | **≥65% final** | golden/a11y additions |

Rule: `test/coverage_baseline.txt` updates ONLY upward, in the same
commit that earns it. CI fails on any drop.

### Automation — `tools/coverage_report.py` (build in S1)

Don't compute coverage by hand (I did it with a throwaway python
one-liner — don't repeat that). S1.4 should ship a script that:
1. Runs `flutter test --coverage`
2. Parses `coverage/lcov.info` → per-directory + total line %
3. Prints the trajectory table above with pass/fail vs baseline
4. Optionally `--update-baseline` writes the new floor

~40 lines. Lives in `gungeon_mate/tools/` next to
`test/data_integrity_test.dart` (flutter test). CI calls it; humans call it before committing
test work. This is what makes the trajectory *enforced*, not aspirational.

## Cross-Session Conflict Matrix (who must wait for whom)

Sessions look parallel-safe but three pairs share files. Check this
before claiming — it's the difference between smooth parallelism and
a rebase nightmare.

| Pair | Shared surface | Rule |
|---|---|---|
| **S2.1/S2.2 ↔ S3.4** | `item_body_sections.dart`, `gun_stats_sections.dart`, `item_detail_screen.dart` | **ORDER MATTERS.** S3.4 adds UI (ammonomicon_entry/effect fields) → S2 tests written first will break when it lands. If parallel: S3.4 lands FIRST, then S2.1/S2.2 write tests against final UI. If S2 first: S3.4 must re-run S2's item-detail tests after merging. Never both mid-flight on the same file. |
| **S2.6 ↔ S4.6** | `paradox_player_panel.dart`, `surprise_overlay.dart` | Already flagged — first claimer writes tests, other reviews for protocol correctness. Claims table decides. |
| **S4.4/S4.5 ↔ existing mp tests** | `multiplayer_messages.dart`, `mp_sync.dart` | Wire-contract changes (toJson cleanup, spriteKey dual-write) can break existing `test/mp_*` suites. After ANY S4 wire change: run the FULL mp test suite before committing, not just focused tests. |
| **S3.1 ↔ data tests** | `assets/data/items.json` | Any JSON data change → `python test/data_integrity_test.dart` + full suite. Id fixes can silently change lookup results app-wide. |
| ~~H ↔ S4 (Slot 4 live)~~ | `synergies.json`, `synergy.dart`, `synergy_queries.dart`, `gun_synergies_tab.dart` | **RESOLVED 2026-11-25** — Slot 4 shipped pass-3 (`7f629dd`) and released. Synergy surface got 3 audit passes; H-L1 may now include `synergies.json` for a *fourth-pass verification* (spot-check Slot 4's 15 corrections against the dump) but should not re-audit from scratch — diminishing returns. Still check AGENT_STATUS.md before starting H in case new synergy work lands. |
| **H ↔ all sessions** | read-only by design | H produces a findings report, not fixes. Only trivial (<15min, obvious) fixes inline per scope-creep rule; everything else routes to USER_BUG_LIST tagged with the owning session (S3 data / S4 MP / S5 polish / new U-XXX). This is what keeps H parallel-safe with everything. |
| **S5.x ↔ everything** | cosmetic sweeps touch many files | S5 runs LAST precisely because it touches files every other session tested. If S5 finds a real bug, log it — don't fix-and-expand; it's the gate. |

**Parallel-safe pairs (verified disjoint):** S1 ∥ S3 (infra vs data),
S2-core (non-item widgets) ∥ S3, S4 ∥ S2-non-MP-widgets.

## Effort Estimates + Minimum Viable Slice

Sizes lie; here's the honest range so sessions can be planned around
real calendars. "MVS" = if you only have one focused hour, this is
the slice that still counts as progress.

| Session | Est. effort | MVS (1 hour) |
|---|---|---|
| S1 | 4–6h | S1.1 push + S1.2 CI workflow only — everything else is bonus until CI exists |
| **H** | **4–6h** | **H-L5 honesty hunt + H-L3 dead surface — highest bug-yield-per-hour lenses** |
| S2 | 8–12h | S2.4 periodic_tile + S2.5 dice_roll (most-tapped widgets) — skip the 400-line files if time is short |
| S3 | 2–4h (was 3–5h) | ~~S3.1 U-015~~ now verify-only · S3.3 mojibake proof (10 min) · S3.4 item fields is the real work |
| S4 | 4–6h | S4.4/S4.5 suspect-spot cleanup (bounded) — S4.1 race is the wildcard |
| S5 | 3–5h | S5.7 final gate + S5.2 ticker audit — the rest is polish |

**Overrun rule:** if a session exceeds estimate by >50%, STOP, update
the Claims table with what's done/not-done, and hand off. A half-done
session with an honest claims row beats a finished session that ate
the next session's slot.

## Session Handoff Template (paste into Claims table / session log)

```
Session: S<N> — <name>
Agent: <slot/agent>
Status: DONE | BLOCKED | STALE
Commit(s): <SHA(s)>
Done: <work item IDs completed>
Not done: <work item IDs remaining + why>
Found-not-fixed: <U-XXX bugs logged>
In hand: <uncommitted files / half-done sub-items, or "clean">
Next: <recommended first item for whoever picks up>
Watch out for: <anything the next agent must know>
```

## Risk Register (decisions made BEFORE they're needed)

| Risk | Likelihood | Pre-decided fallback |
|---|---|---|
| CI Flutter pin wrong → red CI day one | Medium | Pin exact local version (`flutter --version`); if pub.dev resolution differs on Linux, add `flutter-version` + `flutter-channel` explicitly and test the workflow on a throwaway branch first |
| S4 mis-pair race not reproducible | Medium | Timebox repro to 2h; if not found, add instrumentation/logging behind a debug flag, ship the flag, log U-021 as "needs device repro" — do NOT guess-fix protocol code |
| S2 balloons (484-line files are hard to test) | High | Per-file rule: smoke render test counts as done; deep interaction coverage is bonus. Never let one file block the session |
| Golden tests flaky on CI (font rendering differs Linux vs Windows) | High | Run goldens Linux-only in CI OR mark them `skip` on CI with local-run docs — decide in S5.1, don't discover it mid-session |
| Coverage gate blocks a legit refactor | Low | Baseline file is the escape hatch — lower it ONLY with a session-log note explaining why |
| Foreign WIP collides mid-session | Medium | Explicit `git add` paths always; if a conflict appears, STOP and check AGENT_STATUS.md before resolving |

## Scope-Creep Rule (every session will find bugs — here's what to do)

- **Trivial** (<15 min, obvious fix, same file you're in): fix it,
  mention it in the commit message.
- **Real but off-task**: log to `docs/USER_BUG_LIST.md` as `Reported`
  with repro notes, add to Claims table under "Found, not fixed" —
  do NOT fix inline. Sessions stay scoped; nothing is lost.
- **Critical/data-loss**: stop the session, fix it, everything else
  waits. There is no other category.

## The Missing Piece — Visual Regression Spike (folds into S5)

Widget tests prove *behavior*; they can't prove the app still *looks*
right. For a polish-driven app this is the last unguarded surface.

- [ ] **S5.0 (NEW, do FIRST in S5)** Golden-test spike: pick the 3
      highest-value screens — `main_menu_screen`, `active_run` player
      page, `experience_studio` preview. `matchesGoldenFile` on a
      fixed surface size. Expect font-rendering differences — that's
      what the risk register's golden fallback is for. If goldens
      prove too flaky in the timebox (half session), fall back to
      **screenshot-diff smoke tests**: pump screen, `takeException()`
      null + key `find.byType` anchors present — cheap, stable,
      catches blank-screen regressions (the U-001 bug class).

## "Superb" Scorecard (what done actually looks like)

- [ ] Coverage ≥65% AND ratchet enforced in CI
- [ ] Zero 0%-coverage files >200 lines
- [ ] All 5 MP suspect spots resolved or documented-accepted
- [ ] All open USER_BUG_LIST items closed or scheduled-with-owner
- [ ] Golden or screenshot-diff net exists for top-3 screens
- [ ] `docs/HOLE_REPORT_*.md` exists — every lens checked, zero
      un-routed findings
- [ ] `flutter analyze` 0 · `flutter test` green · CI green on master
- [ ] Every session left the Claims table honest

---

## SESSION 1 — "Prove the core" (test infrastructure)

**Size: M · Depends on: nothing · Blocks: everything (CI protects all later work)**

### Prep kit
- No `.github/workflows/` exists yet — you're creating it fresh.
- Coverage baseline file to create: `test/coverage_baseline.txt`
  containing `47.5`.
- Existing test style reference: `test/damage_calculator_test.dart`
  (pure unit), `test/widget/ammonomicon_nav_test.dart` (widget +
  debugStartLoaded pattern), `test/run_provider_test.dart` (provider).

### Work items
- [ ] **S1.1 Push pending commits** — `git log origin/master..HEAD` in
      app repo (**7 commits** as of 2026-11-25 — includes Slot 4's
      synergy pass + bug-report system). Push with explicit paths if
      foreign WIP is dirty. *Mistake-proofing:* run `git status` first;
      `git push` ships commits not working tree, so it's safe as long
      as you don't commit their files.
- [ ] **S1.2 CI workflow** — create `.github/workflows/test.yml`:
      ```yaml
      name: test
      on: [push, pull_request]
      jobs:
        flutter-test:
          runs-on: ubuntu-latest
          steps:
            - uses: actions/checkout@v4
            - uses: subosito/flutter-action@v2
              with: { flutter-version: '3.29.x', channel: stable,
                       cache: true }
            - run: flutter pub get
            - run: flutter analyze
            - run: flutter test --coverage
      ```
      *Pitfall:* verify the exact Flutter version (`flutter --version`
      locally) — pinning wrong breaks CI on first run. `3.29.x` is the
      documented line but confirm.
- [ ] **S1.3 Logic unit tests** — targets, in priority order:
      | File | Lines | Why first |
      |---|---|---|
      | `lib/widgets/periodic_tile/tile_logic.dart` | 217 | pure functions, most-tapped widget |
      | `lib/screens/active_run/mp_handlers.dart` | 171 | MP correctness logic |
      | `lib/widgets/active_run/dice_roll/dice_roll_logic.dart` | 158 | pure dice math |
      | `lib/services/effect_tagger.dart` | — | text→effect parsing |
      | `lib/services/run_lifecycle.dart` | — | run start/end invariants |
      | `lib/services/paired_partners_store.dart` | — | persistence round-trip |
      | `lib/services/haptics.dart` | — | small, quick win |
      For each: read the file, extract pure functions, test edge cases
      (empty input, boundaries, malformed data). Test file naming:
      `test/<name>_test.dart` for services, `test/widget/` only if it
      needs a widget harness.
- [ ] **S1.4 Coverage ratchet** — extend the workflow (or add a script
      `tools/check_coverage.py`) that parses `lcov.info`, computes
      line %, fails if < baseline in `test/coverage_baseline.txt`.
      Update baseline ONLY upward, in the same commit that raises it.
- [ ] **S1.5 Mock prefs audit** — `grep -rL setMockInitialValues test/`
      lists files that *don't* mock; cross-reference with files that
      construct `RunProvider`/`MpSession` and add the mock where missing.

**Done when:** CI green on master · all 7 logic files have tests ·
coverage gate fails on a deliberately-lowered baseline (prove it works,
then restore).

---

## SESSION 2 — "Prove the surfaces" (widget tests for 0% UI)

**Size: L · Depends on: S1.3 patterns (reuse them) · Can parallel: S3**

### Prep kit
- Widgets coverage today: **34.2%** (4,761/13,915 lines).
- Every target below is **0% or near-0%** — verified from lcov.info.
- Reference harnesses to copy:
  - `test/widget/cool_curse_screen_test.dart` — provider-heavy screen,
    timer flushing, negative-value rendering.
  - `test/widget/stats_detail_screen_test.dart` — slider/stepper/meter
    interactions.
  - `test/widget/ammonomicon_nav_test.dart` — `debugStartLoaded` for
    asset-loading screens.
  - `test/widget/paradox_widgets_test.dart` — `MpSession.placeholder()`
    + `FakeMpLink` wiring.
- For screens that load assets: prefer adding a `debugStartLoaded`-style
  hook (pattern proven in ammonomicon) over `runAsync` polling — pitfall
  #4. Only ONE smoke test per screen should exercise the real load path.

### Work items (in suggested order — biggest × most-tapped first)
- [ ] **S2.1** `item_body_sections.dart` (484 lines, 0%) — item detail
      body renderer. Test: renders each section type (stats, notes,
      synergies, LEB ghost rows), empty states, long-text overflow.
- [ ] **S2.2** `gun_stats_sections.dart` (407, 0%) — same approach.
- [ ] **S2.3** `quiz_session_screen.dart` (417, 0%) + `quiz_chest.dart`
      (130, 0%) — question flow, answer selection, chest rewards.
      *Pitfall:* quiz engine (`quiz_engine.dart`) is already tested —
      these tests should mock/feed the engine, not re-test it.
- [ ] **S2.4** `periodic_tile.dart` (261) + `tile_logic.dart` (217) —
      tile rendering, quality tiers, S-tier gold, hold-to-shake poof,
      reduced-motion dot. Coordinate with S1.3: logic unit tests there,
      widget tests here — don't duplicate.
- [ ] **S2.5** `dice_roll.dart` (225) + `dice_roll_logic.dart` (158) —
      same split: logic in S1.3, widget/animation here.
- [ ] **S2.6** `paradox_player_panel.dart` (210) + `surprise_overlay.dart`
      (186) — **OVERLAP WITH S4**: whoever claims first writes the widget
      tests; the other reviews assertions for MP-protocol correctness.
      Mark the Claims table so it's not done twice.
- [ ] **S2.7** `inventory_list_row.dart` (163),
      `ammonomicon_detail_screen.dart` (182),
      `effects_summary_screen.dart` (159),
      `emote_animations.dart` (113) — smoke + key-interaction tests.

**Done when:** every file above has ≥1 render test + key interactions
covered · widgets dir coverage ≥60% · no new `skip:` tests added.

---

## SESSION 3 — "Data truth" (correctness sweep)

**Size: M · Depends on: nothing · Can parallel: S2**

### Prep kit
- Bug tracker: `docs/USER_BUG_LIST.md` (root repo) — update statuses per
  B1–B4 when fixing.
- Data integrity tool exists: `cd gungeon_mate && C:/src/flutter/bin/flutter.bat test test/data_integrity_test.dart`
  (see `.devin/workflows/verify-data`) — run it after ANY json edit.
- Reference for id-collision test: existing integrity tests in
  `test/` (avatar file-existence, wallpaper-name coverage, splash
  bidirectional) — same pattern: assert invariant over the dataset.

### Work items
- [ ] **S3.1 ~~U-015~~ — RESOLVED by Slot 4 (`7f629dd`).** `Junk`→127,
      `Ser Junkan 1`→580. **Verify, don't redo:** confirm the integrity
      test Slot 4 added actually guards id uniqueness app-wide (their
      commit says "+8 logic tests" — check whether a *uniqueness*
      invariant test exists; if not, add one — that's the remaining
      hole). Then mark U-015 verified-closed in the bug list.
- [ ] **S3.2 U-001 — re-capture `08_char_select.png`.** Cosmetic;
      needs clean Playwright session (`.devin/workflows/` or manual).
      *Pitfall:* it's a screenshot asset, not a code bug — verify the
      file lands where the docs/site expects before closing.
- [ ] **S3.3 Mojibake proof.** `grep -rn $'\xEF\xBF\xBD' assets/data/`
      (or python scan for U+FFFD). Output the result; if clean, mark
      verified in bug list; if hits, fix JSON + add integrity test.
- [ ] **S3.4 Unsurfaced item fields** (feedback item 5): item `effect`
      and `ammonomicon_entry` JSON fields not shown in detail UI.
      *First verify* — item `effect` line may already render
      (changelog 3.3.0 says "Item detail now shows the mechanical
      effect line"). Only `ammonomicon_entry` may be missing. Read
      `item_body_sections.dart` + `item_detail_screen.dart` before
      writing code.
- [ ] **S3.5 XtG wiki-text filter** (feedback item 6) — check
      `docs/FEEDBACK_PLAN_2026-10-28.md` for the exact ask; implement
      or close with documented reason.
- [ ] **S3.6 Synergy-scan perf proof** — H13 memoization landed
      (`a69b56a`). Don't assume: write a timing test or profile a
      browse-screen build with a large inventory; record numbers in
      the session log. If it's still O(n) per build, that's a real bug
      to fix, not a doc note.

**Done when:** U-015 closed with test · U-001 re-captured · mojibake
verified · items 5–6 resolved-or-closed · perf claim has numbers.

---

## SESSION 4 — "MP hardening" (multiplayer edge cases)

**Size: M · Depends on: S2.6 overlap resolution · Context: MP protocol**

### Prep kit
- Wire protocol: `lib/models/multiplayer_messages.dart` (sealed
  `MpMessage`, `encode()` injects `'type'`; subclass `toJson()` must NOT
  include it).
- Transport test harness: `FakeMpLink` in-memory transport — see
  existing `test/mp_*` suites for the pattern.
- **Known suspect spots** (from `gungeon_mate/AGENTS.md` — all verified
  still-open at plan time):
  1. `spriteKey`/`sprite` rename is NOT forward-compatible — new build
     → old peer drops the sprite. `fromJson` reads both, but old peers
     can't read new.
  2. `MpSurprise.toJson()` emits `'type'` + always-includes empty
     fields — violates the "no type field" contract.
  3. `fx` field has NO sender — dead wire capability.
  4. Custom surprise `:icon:` hint text is never parsed into
     `spriteKey` — renders literally. (Chat parses `:key:`; nothing
     parses it for surprises.)
  5. Preset fx map lives in `_SurpriseCard._presetContent`
     (`surprise_overlay.dart`) while sender presets are a separate
     tuple list in `SurpriseSheet` (`surprise_sheet.dart`) — drift risk.

### Work items
- [ ] **S4.1 First-endpoint mis-pair race** — last open MP protocol
      bug. Repro first (two devices/emulators or FakeMpLink simulating
      rapid connect), find the race in `mp_sync.dart`/`mp_link.dart`,
      fix, regression test. *Pitfall:* this has been deferred twice —
      read git log for prior attempts before designing a fix.
- [ ] **S4.2 Host-gone hint coverage** — H16 deduped handlers
      (`257888c`). Verify "partner may have left" fires on ALL paths:
      timeout, kill, airplane-mode disconnect, app backgrounded.
      Add missing-path tests.
- [ ] **S4.3 Reconnect UX audit** — `mp_reconnect_banner.dart`,
      blank-view guards, 2-min partner-left hint: widget-test each
      state a user actually sees.
- [ ] **S4.4 Protocol version skew decision** — for suspect #1: either
      (a) accept + document as known limitation, or (b) dual-write
      both `sprite` and `spriteKey` for one release. Recommend (b) —
      cheap insurance. Test old↔new handling either way.
- [ ] **S4.5 Wire contract cleanup** — suspects #2/#3/#4/#5:
      `toJson` contract fix (remove `'type'`, omit empty fields),
      either wire an `fx` sender or remove the field, parse `:icon:` in
      surprise hints or fix the hint copy, unify the two preset lists
      into one source of truth.
- [ ] **S4.6 Paradox/surprise widget tests** — if S2.6 hasn't claimed
      them, do them here (see overlap note).

**Done when:** mis-pair race fixed + regression test · all 5 suspect
spots resolved or explicitly accepted-with-docs · reconnect states
tested.

---

## SESSION 5 — "Release readiness & polish sweep"

**Size: M · Depends on: S1–S4 · This is the gate, not a feature session**

### Prep kit
- Version lockstep: `version_lockstep_test` enforces pubspec ↔
  `kAppVersion` ↔ changelog ↔ VERSION_HISTORY — run it first; if it
  fails, that's job #1.
- Reduced-motion API: `ReduceMotion`/`disableAnimations` — grep for
  existing usage to match the established pattern before adding checks.
- Neo-Skeuo tokens: `Skeuo.inkIf`/`Skeuo.collapse` — the collapse
  pattern for semantic colors under the paper skin.

### Work items
- [ ] **S5.1 Neo-Skeuo dark-island audit** — surfaces possibly still
      hardcoded under the paper skin: `neo_skeuo_lab_screen.dart`,
      `asset_viewer_screen.dart`, `shrine_picker/`, quiz screens,
      bug-report sheet (new — check it!). For each: render under
      Neo-Skeuo, fix contrast via `Skeuo.inkIf`/`collapse`.
- [ ] **S5.2 Ticker/reduced-motion audit** — `grep -rn "\.repeat(" lib/`
      → every `AnimationController.repeat` must be gated on
      reduced-motion. We manually fixed 3 (periodic_tile pulse, header
      ambient, GungeonMeter); find the rest. Add a lint-style test if
      feasible (count active tickers under disableAnimations).
- [ ] **S5.3 Asset diet round 2** — verify H7 cull (`edf7b77`)
      left no orphan references: `grep` for deleted filenames in lib/.
      Confirm `uni_5.webp` + wallpaper decode sizes sane. Check for
      newly-dead assets from S1–S4 work.
- [ ] **S5.4 Responsive sweep** — ≤500px width pass on browse, detail,
      studio, settings. One row-overflow was fixed earlier; check
      siblings. Use `Responsive.factor` conventions.
- [ ] **S5.5 Lockstep + changelog** — `flutter test
      test/version_lockstep_test.dart`; changelog.json ↔
      VERSION_HISTORY.md honest and synced.
- [ ] **S5.6 Docs sync** — TECHNICAL_REFERENCE.md,
      REWORK_LESSONS_LEARNED.md, USER_BUG_LIST.md reflect final state.
- [ ] **S5.7 FINAL GATE** — `flutter analyze` 0 issues ·
      `flutter test` all green · `--coverage` regenerated ·
      Claims table all DONE · board released. *This is "we are done" —
      hand off to user for the actual APK build.*

**Done when:** every box checked, final gate green, user gives the
APK go-ahead.

---

## SESSION H — "Detective Hole-Hunt" (audit from different angles)

**Size: M · Depends on: S1 merged (CI exists to verify any fix) ·
Parallel-safe with S2/S3/S4 BY DESIGN — read-only audit, findings
route to the owning session. Run it EARLY so S2–S5 inherit the findings.**

### The contract (what makes H safe to run alongside everything)

H is a **read-only audit that produces a findings report**. It does NOT
fix bugs — it finds them, classifies them, and routes them. Fixes happen
in the owning session (or inline only if trivial per scope-creep rule).
This is the difference between a hole-hunt and a scope bomb.

### Prep kit
- Deliverable: `docs/HOLE_REPORT_<date>.md` (root repo) — findings table:
  `| # | Lens | Severity | File/line | Repro/evidence | Suggested fix | Route to |`
- Route codes: `S3` (data truth), `S4` (MP), `S5` (polish/gate),
  `FIX-NOW` (trivial inline), `U-XXX` (log to USER_BUG_LIST, unscheduled).
- Evidence standard: every finding needs a file:line or command output.
  "Looks suspicious" is not a finding — "grep shows X called nowhere"
  is.

### The lenses (each is a different angle of attack)

- [ ] **H-L1 Data truth vs dump** — Slot 4 owns `synergies.json`;
      you take everything else: `guns.json`, `items.json`, `shrines`,
      `bosses`, `enemies`, `gungeoneers`, `chapters` vs
      `tools/gungeon_dump.json`. Diff counts, names, ids, stats.
      *Pitfall:* dump `required=2` is NOT total-pickups; our id2name
      map is authoritative for display names — verify before "fixing".
- [ ] **H-L2 Schema/persistence backward-compat** — NEW fields landed
      2026-11-25: `any_of_min`, `activation` (Slot 4 `7f629dd`),
      plus earlier `ambienceLoad`, wallpaper names. `Synergy.fromJson`
      already defaults both (`?? 'ACTIVE'`, nullable `anyOfMin`) —
      verify by inspection + one round-trip test rather than assuming.
      For each field: does an OLD persisted JSON (prefs, preset store,
      run_state autosave) still parse? Write a migration test per new
      field — this is where silent data loss lives. Also cover the NEW
      bug-report system (`bug_report.dart`, `BugReportContext`) — its
      context JSON isn't persisted, but the mailto/clipboard paths
      deserve an error-path look under H-L6.
- [ ] **H-L3 Dead surface hunt** — (a) assets referenced nowhere:
      grep asset filenames in lib/; (b) lib functions never called:
      `dart analyze` won't catch public-but-unused — spot-check
      suspicious exports; (c) dead prefs: prefs fields with no UI
      setter or no consumer; (d) unreachable screens: routes pushed
      nowhere; (e) JSON fields written but never read (grep each key).
      Prior art: WP-2 dead-pref sweep, H7 asset cull — extend, don't
      repeat.
- [ ] **H-L4 Lifecycle/async hunt** — `grep -rn "AnimationController"
      lib/` → every one has `dispose()`; `Timer(`/`StreamSubscription`/
      `Future.delayed` → cancelled/handled; `await` followed by
      `context.` without `context.mounted` check; `setState` after
      dispose. We fixed 3 ticker bugs manually — find the rest
      systematically.
- [ ] **H-L5 Honesty hunt** — places where UI *claims* mechanics the
      code doesn't deliver (the LEB ghost-list bug class). Check:
      every displayed formula vs its computation (jam %, cooldown
      speed, DPS in damage_calculator vs displayed DPS, reward
      multiplier text); every "X% chance" label vs the actual roll;
      every explainer text vs live math. CoolCurseScreen was just
      fixed for exactly this — sweep for siblings.
- [ ] **H-L6 Error-path hunt** — what happens when: a JSON asset is
      missing/corrupt/empty array; an asset file referenced in code
      doesn't exist; first run with zero data; MP peer on old app
      version sends unknown message type; SharedPreferences returns
      garbage. For each: crash, graceful empty state, or silent wrong
      answer? Silent-wrong is the worst outcome.
- [ ] **H-L7 Perf hunt** — `build()` doing heavy work (JSON parse,
      list scan, regex); missing `const`; animated layers without
      `RepaintBoundary`; images decoded without `cacheWidth`/
      `cacheHeight`; non-lazy lists of game assets. Prior art: H13
      synergy index, H15 wallpaper _syncMotion — same pattern.
- [ ] **H-L8 Docs/changelog honesty** — do docs reference deleted
      files (`stat_sheets.dart` was deleted — grep docs for it)?
      Does changelog.json claim features that were cut or never
      shipped? Does TECHNICAL_REFERENCE match reality (file sizes,
      architecture map)? Does VERSION_HISTORY match changelog?
- [ ] **H-L9 Test-blindspot ranking** — formalize what the coverage
      audit eyeballed: rank 0%-coverage files by (lines × user
      visibility). Output feeds S2 prioritization if S2 hasn't run yet.

### Done when
- `docs/HOLE_REPORT_<date>.md` exists with every lens checked
- Every finding has evidence + route code
- Trivial fixes committed; real bugs in USER_BUG_LIST
- Claims table updated; slot released

---

## Execution order

```
S1 (CI) ──► H (hole-hunt, read-only) ──► S2 (widget tests) ──┐
         │                        └──► S3 (data truth) ──┼──► S5 (polish gate)
         │                        └──► S4 (MP) ─────────┘
         └──────────────────────────────────────────────────── (S1 also ∥ S3 data fixes that don't need CI)
```

- **S1 first, always** — CI makes every later session verifiable.
- **H right after S1** — it's read-only so it can overlap S2/S3/S4,
  but running it early means its findings *feed* those sessions
  instead of arriving after they've closed.
- **S2 ∥ S3** — tests vs data, disjoint files, safe in parallel.
- **S4** needs MP context fresh; good pair with S2's MP widget overlap.
- **S5 last** — it's the gate, and it should inherit H's polish-route
  findings.

## Session kickoff checklist (copy per session)

```
[ ] Read this doc + AGENT_STATUS.md; claim slot (AC1)
[ ] Add row to Claims table: session, name, IN_PROGRESS
[ ] git pull both repos; git status — note foreign WIP, don't touch
[ ] Work items in order; commit per item (explicit git add paths)
[ ] flutter analyze + focused tests after each item
[ ] Update Claims table per item: DONE + SHA, or BLOCKED + reason
[ ] Session end: full flutter test, changelog if user-facing,
    release slot (AC3) + Session Log row + Claims table final state
```
