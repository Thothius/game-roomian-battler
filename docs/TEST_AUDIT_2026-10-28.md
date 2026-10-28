# Test Coverage Audit — 2026-10-28

## Current state

**363 tests passing, 1 skipped** (`_smoke_codex_test` — `compute()` can't finish under `flutter_test`; kept for CI/device).

Suite was broken twice recently, both found and fixed during this audit:
- `quiz_session_screen.dart` WIP — missing imports (`fastRoute`, `ItemDetailScreen`, `PlayerSlot`) failed the *entire* test compile (every test loads all of `lib/`). Fixed.
- `mp_lobby_screen_test` — 5/8 tests assumed the pre-staged single-page form. Rewritten for the role → gungeoneer → identity flow; added back-navigation coverage (9 tests now).

## Coverage map

| Area | Tests | Quality |
|---|---|---|
| MP messages/link/flow/integration/protocol/reconnect/recovery/reliability/session | ~157 across 9 files | Strong — best-covered area |
| Quiz engine | 14 | Good |
| RunProvider | 28 | Good |
| Themes (system/validation/migration) | 40 | Good |
| Widgets (13 files: screens, codex, lobby, settings, paradox) | ~120 | Surface-level mostly |
| Browse (synergies, tiers) | 2 | Thin |
| Detail views (smoke) | 2 | Minimal — height-only |

## Gaps — prioritized

### P0 — Structural, high-value

1. **Data integrity tests** — `guns.json`/`items.json`/`synergies.json` coherence. No test validates: every synergy `items`/`anyOf` name resolves to a real gun/item; every `icon` path exists on disk; no duplicate names; `sellPrice`/`quality`/`chestColor` well-formed. A typo'd piece name silently breaks a synergy forever. *Effort: low — pure JSON validation.*

2. **Version lockstep test** — `pubspec.yaml` version == `kAppVersion` == top `changelog.json` entry == top `VERSION_HISTORY.md` entry. Drift has happened before; a 20-line test ends it. *Effort: trivial.*

3. **Gun detail tabs** — the redesign ships with smoke-only coverage. Add: tab row renders, STATS shows hero stats (DPS/Range/Spread/Force), NOTES shows effect+ammonomicon, SYNERGIES groups COMPLETE/PARTIAL with owner pills, item path unchanged. *Effort: medium.*

### P1 — Feature logic with zero coverage

4. **`ElementalTagger`** — keyword→element mapping powers header/notes status icons. Zero tests. Verify fire/electric/poison/curse keywords map; gun with no elements → empty set. *Effort: low.*

5. **Synergy match edge cases** — `matchesItems` with `anyOf` alternatives, prefix-only effects, partial ownership; `_completesFor`/`_completedSynergies` owner attribution (P1/P2/P1+P2) — only 2 browse tests exist. *Effort: medium.*

6. **Special gun dashboards** — Gunderfury level tracker, Payday heister toggles, Junkan tracking, Ser Junkan name match. All built by hand, all untested. *Effort: medium — needs RunProvider wiring.*

7. **Avatar identity** — `id:frame` encode/decode round-trip, `FramedAvatar` fallback for unknown ids, picker selection persists. *Effort: low.*

8. **`RunNameGenerator`** — Paradox naming: output non-empty, adjective+noun shape, no crash across many rolls. *Effort: trivial.*

### P2 — Flow-level

9. **Dice roller** — message round-trips exist; no widget test for challenge→accept→result or cancel overlay dismissal. *Effort: medium.*

10. **Active run interactions** — item transfer request/approve/deny, shrine use, destroy-on-use banner, gift rollback on disconnect. MP reliability covers transport, not UI-level flows. *Effort: high.*

11. **Codex two-level nav** — grid renders 10 categories → tap opens category → back returns to grid (loading-state tests exist; nav tests don't). *Effort: low — needs data stub.*

## Process findings

- **WIP broke the suite silently** — missing imports failed all test compiles, not just the edited file. A pre-commit `flutter analyze` (or CI gate) catches this class instantly.
- **`pumpAndSettle` traps** — screens with continuous animations (particles, glows) never settle; tests need bounded `pump()`s (used in the new lobby tests).
- **Test-env limits** — `compute()` and `SharedPreferences` don't work under `flutter_test`; data-loading paths need fakes or marked-skip tests.
- **`Center`/`Align` without `heightFactor` in `bottomNavigationBar`** — the blank-body landmine is documented in UI_HEALTH but only guarded by the smoke test on one screen. A lint-style guard test could scan widgets, though the pattern is now closed everywhere.

## Recommended next batch (effort: ~half a session)

1. `data_integrity_test.dart` — JSON coherence (P0.1) — **DONE `1ed9b21`** (6 tests; data verified clean — no dupes, all synergy pieces resolve, all icons exist)
2. `version_lockstep_test.dart` — release consistency (P0.2) — **DONE `1ed9b21`** (3 tests)
3. Extend `_smoke_detail_test.dart` → gun tab assertions (P0.3) — **DONE `1ed9b21`** (+4 tests)
4. `elemental_tagger_test.dart` (P1.4) — **DONE `1ed9b21`** (6 tests)
5. `run_name_generator_test.dart` (P1.8) — **DONE `1ed9b21`** (2 tests)

**Suite total: 386+ tests green.** Remaining open items: P1.5–P1.7
(synergy edge cases, special dashboards, avatar identity) and P2
(dice flow, active-run transfers, codex nav).
