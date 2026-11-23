---
description: Verify guns/items/synergies data against cached wiki.gg source before trusting or shipping data changes
---

# Data Verification Pipeline

Run this whenever guns.json, items.json, or synergies.json have been hand-edited,
or before any release, to catch drift from the wiki source of truth.

> **Agent coordination:** Update your slot in `AGENT_STATUS.md` with the files
> you're verifying (AC2). If verification takes long, update **Last board update**
> so stale detection doesn't fire on you.

All commands run from the repo root `x:\GungeonMate`.

## 1. Structural integrity sweep
// turbo
```
cd gungeon_mate && C:/src/flutter/bin/flutter.bat test test/data_integrity_test.dart
```
Checks: JSON parses, unique names, synergy refs resolve, back_refs resolve,
icon files exist, required fields present, rich-token refs resolve.
**Must exit 0 (no hard errors) before continuing.**

## 2. Completeness audit
> **REMOVED** — `tools/audit_stats.py` no longer exists. Empty-field and
> icon checks are covered by `test/data_integrity_test.dart` (step 1);
> manual review of `assets/data/*.json` covers the rest.

## 3. Diff guns.json / items.json against game data
> **REMOVED** — `scripts/validate_db.py` and the `cache_wikigg/` pipeline
> no longer exist. Ground truth is now `tools/gungeon_dump.json` (raw game
> data) + the official wiki. Compare fields manually or via ad-hoc python.
Compares dps, damage, fire_rate, magazine_size, ammo_capacity, reload_time,
shot_speed, range, force, spread, class, quality (guns) and quality, type,
recharge_time (items) against `cache_wikigg/*.html`.

## 4. Diff synergies.json against game data
> **REMOVED** — the wiki-scrape pipeline (`scripts/validate_synergies.py`,
> `cache_wikigg/`) is gone. Ground truth: `tools/gungeon_dump.json`
> synergy records (matched via `game_name_key`) + official wiki. The last
> full pass is documented in `docs/SYNERGY_AUDIT_2026.md`.

## 5. Review and decide
- If mismatches are found in steps 3/4, read each one — confirm the wiki
  cache is actually current/correct before overwriting hand-tuned data.
- Elemental/status tags (`ElementalTagger`, `EffectTagger` in
  `lib/services/`) are regex-inferred from `effect`/`notes` text and have
  no structured wiki field to diff against for items — these can only be
  spot-checked manually, not auto-validated.

## 6. Re-run structural sweep after any repair
// turbo
```
cd gungeon_mate && C:/src/flutter/bin/flutter.bat test test/data_integrity_test.dart
```
Confirms no repair introduced a broken reference or duplicate.
