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
python gungeon_mate/tools/data_integrity.py
```
Checks: JSON parses, unique names, synergy refs resolve, back_refs resolve,
icon files exist, required fields present, rich-token refs resolve.
**Must exit 0 (no hard errors) before continuing.**

## 2. Completeness audit
// turbo
```
python gungeon_mate/tools/audit_stats.py
```
Reports empty critical fields (damage/dps/etc on guns, effect/recharge on items),
missing icons, synergies with only 1 required item (possibly incomplete).

## 3. Diff guns.json / items.json against cached wiki infobox data
```
python scripts/validate_db.py --verbose
```
Compares dps, damage, fire_rate, magazine_size, ammo_capacity, reload_time,
shot_speed, range, force, spread, class, quality (guns) and quality, type,
recharge_time (items) against `cache_wikigg/*.html`.

Review the mismatch report manually first. Only add `--repair` once you've
confirmed the reported wiki values are correct (not vice versa) — repair
overwrites `guns.json`/`items.json` in place:
```
python scripts/validate_db.py --repair
```

## 4. Diff synergies.json against the wiki's master Synergies.html table
If `scripts/validate_synergies.py` does not exist yet, it needs to be built
first (see `docs/SYNERGIES_FIX_PLAN.md` for context) — it should reuse
`parse_wiki_data.py::parse_synergies()` to re-parse `cache_wikigg/Synergies.html`
into ground truth, then diff each synergy's `items` + `any_of` sets against
the current `assets/data/synergies.json` by matching `name`.
```
python scripts/validate_synergies.py --verbose
```

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
python gungeon_mate/tools/data_integrity.py
```
Confirms no repair introduced a broken reference or duplicate.
