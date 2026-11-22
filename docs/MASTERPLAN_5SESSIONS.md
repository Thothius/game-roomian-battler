# Masterplan — 5 Sessions to Done

> Goal: take GungeonMate from "feature-complete ~85–90%, proof thin" to
> verified, hardened, release-ready. **APK build/release is explicitly
> OUT of scope** — this plan ends at "everything proven and polished".
>
> Baseline at plan time: 686 tests green, analyze 0 issues, **47.5%
> line coverage** (14,375/30,290), v3.7.0 committed, ~4 commits unpushed,
> Gradle 9.3.1 / AGP 9.1.0 toolchain landed (`e4b7fba`).
> All file paths below verified on disk 2026-11-25.

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
      app repo; push with explicit paths if foreign WIP is dirty.
      *Mistake-proofing:* run `git status` first; if Slot 2's
      bug-report files are modified, do NOT sweep them — push only
      commits already made (`git push` pushes commits, not working tree,
      so this is safe as long as you don't commit their files).
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
- Data integrity tool exists: `python gungeon_mate/tools/data_integrity.py`
  (see `.devin/workflows/verify-data`) — run it after ANY json edit.
- Reference for id-collision test: existing integrity tests in
  `test/` (avatar file-existence, wallpaper-name coverage, splash
  bidirectional) — same pattern: assert invariant over the dataset.

### Work items
- [ ] **S3.1 U-015 — items.json id collision.** `Junk` claims id 580
      (dump says SackKnightBoon); `Ser Junkan 1` id is null.
      Steps: (a) dump `tools/gungeon_dump.json` is authoritative for
      game ids — check what id 580 actually is; (b) fix `items.json`
      provenance; (c) add integrity test asserting unique non-null ids
      (allow the known-null exception ONLY if the schema requires it —
      check how `id` is consumed first via grep). *Pitfall:* AGENTS.md
      warns dump `required=2` is NOT total-pickups and our id2name map
      is authoritative for display names — don't "fix" names to match
      dump internals.
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

## Execution order

```
S1 (CI) ──► S2 (widget tests) ──┐
         └─► S3 (data truth) ──┼──► S5 (polish gate)
              S4 (MP) ─────────┘
```

- **S1 first, always** — CI makes every later session verifiable.
- **S2 ∥ S3** — tests vs data, disjoint files, safe in parallel (two
  agents: one takes S2, other takes S3).
- **S4** needs MP context fresh; good pair with S2's MP widget overlap
  or a dedicated session.
- **S5 last** — it's the gate.

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
