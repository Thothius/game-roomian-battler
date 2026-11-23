# Masterplan — 3 Final Sessions (post-bug-list drain)

> Authored 2026-11-25. Bug list is EMPTY; S1–S5 masterplan DONE.
> This is the runway to "everything proven and polished" + a release
> decision. Each session has a green gate: analyze 0, full suite green,
> board released, docs synced.

---

## Session A — Hygiene & docs consolidation (SUPPORT-flavored)

Goal: zero uncommitted limbo, one source of truth per concern.

1. **Foreign WIP disposition** — ~9 dirty files in app WD
   (item_detail/mp_connect/stats_detail/theme/codex/gun_synergies/
   bug_report/paradox tests). Identify owner intent → commit, stash
   with label, or archive. Nothing stays dirty >48h after this.
2. **Doc archival** — `MASTERPLAN_5SESSIONS.md` (DONE) → `docs/archive/`;
   verify `CUSTOMIZATION_MASTERPLAN.md` + `QA_REMEDIATION_PLAN.md`
   complete → archive or mark superseded.
3. **`GUNGEONMATE.md` refresh** — still claims v3.3.0+162 and references
   removed `changelog.json`; update version/features or fold into
   TECHNICAL_REFERENCE and archive.
4. **`.windsurfrules` dedup** — make it a thin pointer to `AGENTS.md`
   (two sources of truth for coordination rules will drift).
5. **Small housekeeping tail** — H21 wallpaper display names,
   H22 `uni_5` grid verify, H23 preview seed label, H25 LEB toggle
   discoverability pass.

Gate: clean `git status` on both repos (excluding intentional
untracked), docs cross-referenced, analyze 0.

## Session B — Depth pass: coverage, seams, polish leftovers

Goal: close the known test/behavior gaps, not new features.

1. **Quick-add MP seam** — `sendAddToPeer` path is untested
   (`MpSession.placeholder()` is inactive). Add a mockable seam or
   fake session → test peer-add routing + error toast.
2. **Coverage ratchet** — target the next uncovered clusters
   (dashboards detail paths, quiz_session, browse rows) toward ~68%;
   bump `coverage_baseline.txt`.
3. **H6 theme splash audit** — 12 themes missing splash JPGs: either
   source/generate art (user step) or trim `splashSlug` map so the app
   never requests missing assets.
4. **H14 ambience-mud nudge** — studio warning when atmosphere +
   liquid + shader + particles stack heavy.
5. **H24 S7 LIVE LOOK mini-slice** (optional — only if user wants it).

Gate: new tests green, coverage baseline raised honestly, analyze 0.

## Session C — Release cut: v3.7.1 (or v3.8.0)

Goal: ship ~50 commits of user-facing work since v3.7.0+167.

Since v3.7.0: dice rework, cool/curse quick-manage sheet, quick-add
random view + lifecycle fix, MP social layer disabled, +33 avatars,
studio swiper removal + pills/a11y, dashboard swiper dedup, Huntress
slot fix, full U-0xx bug drain, settings control-deck, Neo-Skeuo
excision aftermath.

1. **Version decision** — recommend **v3.8.0** (feature-heavy: dice
   rework + sheets + avatars justify minor bump over patch).
2. **Release checklist lockstep** — pubspec version, kAppVersion,
   VERSION_HISTORY top heading, main_menu v-literals (3+ spots);
   `version_lockstep_test` enforces.
3. **Full gate** — analyze 0, full suite green, coverage regen.
4. **APK build** — `flutter build apk --release` →
   `app-releases\gungeon-mate-v3.8.0.apk`.
5. **Push + tag** — push both repos, `git tag -a v3.8.0` (AC5c;
   tags NOT pushed unless user asks).
6. **GitHub release asset** — update stable `GungeonMate.apk` asset +
   OG image already uploaded manually (verify).

Gate: version_lockstep green, APK builds clean, release notes =
VERSION_HISTORY Unreleased section promoted to versioned heading.

---

## Ordering rationale

A before B (clean tree makes B's diffs reviewable), B before C (don't
cut a release on top of known test gaps). C is gated on user go-ahead
— APK + version bump are explicit-request items per standing rules.
