# Housekeeping Masterplan — 2026-11-25

Consolidated list of every open/deferred cleanup, correctness, and
maintenance item across the project. Sources: `USER_BUG_LIST.md` (U-*),
AGENT_STATUS deferred notes, QA_REMEDIATION_PLAN P3, asset audit.

Legend: **[bug]** correctness · **[perf]** performance ·
**[size]** APK weight · **[data]** dataset quality · **[infra]** toolchain ·
**[docs]** hygiene

---

## Tier 1 — Correctness bugs (user-facing)

| # | Task | Ref | Effort |
|---|------|-----|--------|
| H1 | **any_of multi-pick pools** — JSON can't express `NumberObjectsRequired`; fix schema or add curated overrides. Start with confirmed-bad: `360 Yes Scope` (inverted anchor/pool), `Smart Bombs`, `Unbelievably Charming`, `Tea for Two`; fix `Resourceful Indeed,` name typo | U-011 | M |
| H2 | **TIERS test regression** — `browse_synergies` test-side failure noted since v3.2.x | deferred | S |
| H3 | **Browse row overflow ≤500px** — narrow-width layout overflow in browse rows | deferred | S |
| H4 | **MP first-endpoint mis-pair race** — edge case in endpoint pairing | deferred | M |
| H5 | **Host-gone hint/watchdog polish** — beyond current implementation | deferred | S |
| H6 | **12 missing theme splash JPGs** — generate/source art for the_cultist, gunslinger, convict, hunter, pilot, rat, breach, lead_lord_keep, oubliette, black_powder_mine, bullet_hell, rg_department — or trim slug map | U-013 | M |

## Tier 2 — Data & asset hygiene

| # | Task | Ref | Effort |
|---|------|-----|--------|
| H7 | **`images/game/` dead weight** — delete ~600 unused PNGs, keep the 13 referenced by `home_backdrop.dart`/`neo_skeuo_lab_screen.dart` (or document as intentional sprite source) | U-012 | S |
| H8 | **Wallpaper re-encode** — normalize 46 custom webps (≥1200px, consistent crop, recompress); ~12 MB → est. large savings | U-014 | M |
| H9 | **`synergy_meta.json` coverage** — only 110/395 synergies classified; second pass would make CO-OP/TEAM/ONE-PLAYER tags + fx chips honest for the rest | audit F5 | L |
| H10 | **Expand `kLebExcludedSynergies`** — add confirmed `IgnoreLichEyeBullets` cases (unlock/quest-gated synergies) as verified | audit | S |
| H11 | **JSON mojibake sweep** — `�` characters in data JSONs | deferred | S |
| H12 | **U-001 screenshot recapture** — `08_char_select.png` white/blank | U-001 | S |

## Tier 3 — Performance

| # | Task | Ref | Effort |
|---|------|-----|--------|
| H13 | **Synergy-scan recompute-per-build** — `getSynergiesFor`/`synergyCountFor` caches exist but scan still runs on inventory change paths; profile and memoize harder if needed | deferred | M |
| H14 | **Ambience-mud guidance** — atmosphere + liquid + shader + particles can stack into visual mud; add intensity hint or mutual-exclusion nudge in studio | board | S |
| H15 | **`CustomWallpaper._syncMotion` in build** — move side-effecting controller sync out of `build` | QA obs | S |
| H16 | **Consolidate `onStartRun` wiring** — duplicated identically in `mp_session.updateRunProvider` + `mp_handlers` (last-writer-wins, harmless but fragile) | QA obs | S |

## Tier 4 — Infra & release

| # | Task | Ref | Effort |
|---|------|-----|--------|
| H17 | **Android toolchain migration** — Gradle 8.14→9.1, AGP 8.13→9.0.1, Kotlin 2.2.20→2.3.20 (all now warn); needs dedicated session + release-build verify, plugin compat check (nearby_connections, media_kit, permission_handler) | build warnings | L |
| H18 | **Push backlog** — app repo ~59 commits ahead of origin/master; push when remote reachable | git | S |
| H19 | **Release decision** — v3.7.0 shipped menu+ambiance; protocol v4 + synergy fixes argue for v3.7.1 or fold into next feature release; run full release checklist (5 lockstep files) if bumping | release rule | S |
| H20 | **Font swap fallout check** — in-flight font TTF swap (26 deleted / 6 added uncommitted) needs pubspec family audit + font-picker verify once landed | tree state | S |

## Tier 5 — Nice-to-have / polish backlog

| # | Task | Ref |
|---|------|-----|
| H21 | Wallpaper display names (picker shows raw `wp_07.webp`-style labels?) | board deferred |
| H22 | `uni_5` grid cell verify vs `9unis.jpg` source | board deferred |
| H23 | Preview session-seed diagnostic label | summary deferred |
| H24 | S7 LIVE LOOK mini-slice (optional) | masterplan deferred |
| H25 | Browse LEB toggle discoverability pass (prefs/settings/browse all work — verify UX coherence) | this audit |

---

## Suggested sequencing

1. **H1** (synergy data correctness — highest user-facing impact)
2. **H6 + H12** (cheap cosmetic wins)
3. **H7 + H8 + H11** (one asset-hygiene session: delete dead sprites, re-encode wallpapers, mojibake sweep)
4. **H2–H5** (test/bug sweep batch)
5. **H13–H16** (perf/cleanup batch)
6. **H17** (toolchain — schedule alone, it's disruptive)
7. **H18/H19** (push + release whenever user wants)
