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
| ~~H1~~ | **any_of multi-pick pools** — DONE: `groups` AND-of-OR schema added; Smart Bombs/Unbelievably Charming/Super Serum regrouped, Tea for Two pool completed, `Resourceful Indeed` typo fixed, `360 Yes Scope` verified correct | U-011 | M |
| ~~H2~~ | **TIERS test** — already fixed (`bfd8c36`/`df06981` stale expectations); test green in full suite | deferred | S |
| ~~H3~~ | **Browse row overflow ≤500px** — fixed `5cbf7c6` (pill ellipsis + drop prototypeItem); 500px test green | deferred | S |
| ~~H4~~ | **MP mis-pair race** — fixed `7be7537` (`_initiatedIds` handshake guard in mp_link.dart, verified present) | deferred | M |
| ~~H5~~ | **Host-gone hint** — shipped `7be7537` (`onDisconnectElapsed` → banner/paradox bar, mp_recovery.dart) | deferred | S |
| H6 | **12 missing theme splash JPGs** — generate/source art for the_cultist, gunslinger, convict, hunter, pilot, rat, breach, lead_lord_keep, oubliette, black_powder_mine, bullet_hell, rg_department — or trim slug map | U-013 | M |

## Tier 2 — Data & asset hygiene

| # | Task | Ref | Effort |
|---|------|-----|--------|
| ~~H7~~ | ~~`images/game/` dead weight~~ — **DONE `edf7b77`**: 602 PNGs deleted, 12 live icons kept, pubspec trimmed | U-012 | S |
| ~~H8~~ | **Wallpaper re-encode** — DONE `968fe55`: dims already ≤1200px; uniform q80/method=6 → 12.1→10.1 MB (~2 MB APK saved). q75 would save ~5 MB but risks banding on dark art — held at safe quality | U-014 | M |
| ~~H9~~ | ~~`synergy_meta.json` coverage~~ — **DONE `5604432`**: all 395 classified (coop+fx via batched Gemini pass; TEAM candidates wiki-checked → all BOTH) | audit F5 | L |
| ~~H10~~ | **Expand `kLebExcludedSynergies`** — DONE `9e48e86`: +The Submachinist (dual-wield) +Detective Mode (needs Badge) per official LEB wiki exception list | audit | S |
| ~~H21~~ | **Synergy pool audit vs game dump** — all 343 keyed synergies cross-validated vs `tools/gungeon_dump.json`; 17 pool corrections shipped `9e48e86` | audit addendum | M |
| ~~H11~~ | **JSON mojibake** — sweep found zero `�` in assets/data/*.json | deferred | S |
| ~~H12~~ | ~~U-001 screenshot recapture~~ — **CLOSED obsolete**: artifact not in repo; char-select covered by `ref-02-character-select.png` | U-001 | S |

## Tier 3 — Performance

| # | Task | Ref | Effort |
|---|------|-----|--------|
| ~~H13~~ | ~~Synergy-scan recompute-per-build~~ — **DONE `a69b56a`**: piece→synergy index + identity-guarded caches, `matchesOwnedSet` everywhere, group-aware count/partial caches | deferred | M |
| H14 | **Ambience-mud guidance** — atmosphere + liquid + shader + particles can stack into visual mud; add intensity hint or mutual-exclusion nudge in studio | board | S |
| ~~H15~~ | **`CustomWallpaper._syncMotion` in build** — DONE `257888c`: prefs/MediaQuery listener + didChangeDependencies drive the gate; build is side-effect free | QA obs | S |
| ~~H16~~ | **Consolidate `onStartRun` wiring** — DONE `257888c`: shared `_onPeerStartRun`/`_onPeerSurprise`/`_onRecoveryElapsed` handlers; also fixed latent bug — `updateRunProvider` was dropping `onDisconnectElapsed` (host-gone hint lost after provider swap) | QA obs | S |

## Tier 4 — Infra & release

| # | Task | Ref | Effort |
|---|------|-----|--------|
| ~~H17~~ | ~~Android toolchain migration~~ — **DONE `e4b7fba`**: Gradle 9.3.1 + AGP 9.1.0 + built-in Kotlin; debug APK green. KGP 2.2.20 kept declared (apply false) for plugins; Kotlin 2.3.x N/A under built-in Kotlin | build warnings | L |
| H18 | **Push backlog** — app repo ~65+ commits ahead of origin/master; push when remote reachable | git | S |
| H19 | **Release decision** — v3.7.0 shipped menu+ambiance; protocol v4 + synergy fixes argue for v3.7.1 or fold into next feature release; run full release checklist (5 lockstep files) if bumping | release rule | S |
| ~~H20~~ | ~~Font swap fallout check~~ — **VERIFIED**: swap landed `5618722`; all 13 declared font assets exist on disk, picker/TYPE tab/tests green | tree state | S |

## Tier 5 — Nice-to-have / polish backlog

| # | Task | Ref |
|---|------|-----|
| ~~H21~~ | **Wallpaper display names** — VERIFIED DONE: `kWallpaperNames` map (30 mood-matched names) + `wallpaperDisplayName()` already wired as `_WallpaperTile.label` in the studio picker | Session A verify |
| ~~H22~~ | **`uni_5` grid verify** — `9unis.jpg` source no longer on disk (was untracked, gone). Asset itself verified healthy: uni_5.webp 320×320, 22k unique colors, non-blank | Session A verify |
| ~~H23~~ | **Preview session-seed label** — DONE: `_startSession` re-seeds `_rng` per session (`_sessionSeed`), tiny `#seed` label beside LIVE PREVIEW header; reroll gets a fresh seed | Session A |
| H24 | S7 LIVE LOOK mini-slice (optional) | masterplan deferred |
| ~~H25~~ | **Browse LEB discoverability** — DONE: browse chip keeps its compact form; added "Browse LEB badges" toggle row to Settings → SYNERGY READOUT panel so the browse-local pref is discoverable + controllable outside the filter bar | Session A |

---

## Suggested sequencing

1. **H1** (synergy data correctness — highest user-facing impact)
2. **H6 + H12** (cheap cosmetic wins)
3. **H7 + H8 + H11** (one asset-hygiene session: delete dead sprites, re-encode wallpapers, mojibake sweep)
4. **H2–H5** (test/bug sweep batch)
5. **H13–H16** (perf/cleanup batch)
6. **H17** (toolchain — schedule alone, it's disruptive)
7. **H18/H19** (push + release whenever user wants)
