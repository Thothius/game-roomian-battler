# Synergies Data Fix Plan

## The bug

Synergies whose `effect` field begins with **"One of the following:"** show up
in the app as a jumbled list of item names with no description, no separators,
and no information about what the combination actually *does*.

Example (`assets/data/synergies.json`):

```json
{
  "name": "BEES",
  "items": ["Bee Hive"],
  "effect": "One of the following: Honeycomb Bumbullets Jar of Bees",
  "any_of": ["Honeycomb", "Bumbullets", "Jar of Bees"]
}
```

The `any_of` array is correct. The `effect` text is what's broken.

## Root cause

`parse_wiki_data.py:parse_synergies` does:

```python
# 1. Pulls the alternatives out of a nested <table> inside the effect <td>.
nested_table_m = re.search(r'<table[^>]*>(.*?)</table>', effect_cell, ...)
if nested_table_m:
    any_of = _extract_titles(nested_table_m.group(1))

# 2. Flattens the WHOLE cell (still containing the nested table) to text.
effect = strip_html(effect_cell)
```

Because the nested table is *not* removed from `effect_cell` before the flatten,
its `<td>` contents (just the item names) end up concatenated into `effect`
with no separators.

Worse: the wiki's "one of the following" rows generally don't carry a
human-readable description in the synergy *table* — the per-combination
description lives on each individual item's wiki page in their Synergies
section. So even with a clean parser, `effect` would just be the bare
prefix `"One of the following:"`.

## Fix — Phase 1 (in-app, shipping now)

**Status: implemented.**

`Synergy.prettyEffect` rewrites the cell on the fly when `effect` starts with
`one of the following` / `any of the following` and `any_of` is populated:

```
Activates with one of: Honeycomb, Bumbullets or Jar of Bees.
```

Used by `synergies_overview_screen.dart` and `item_detail_screen.dart` so the
synergy panel reads cleanly without re-parsing the wiki.

## Fix — Phase 2 (parser, next data refresh)

1. **Strip the nested alternatives table from the effect cell** *before*
   flattening, so any prose surrounding the alternatives is preserved when
   the wiki bothered to write any:

   ```python
   nested = re.search(r'<table[^>]*>.*?</table>', effect_cell, re.DOTALL)
   if nested:
       any_of = _extract_titles(nested.group(0))
       effect_html_no_alt = effect_cell[:nested.start()] + effect_cell[nested.end():]
   else:
       effect_html_no_alt = effect_cell
   effect = strip_html(effect_html_no_alt).strip()
   ```

2. **Backfill per-combination descriptions from the partner item pages.**
   Each item's wiki page already has a Synergies section parsed by
   `parse_wiki_rich.py`. For every synergy `S` with non-empty `any_of`,
   look up each `partner ∈ items + any_of` and search their wiki bullets
   for a token chain that mentions `S.name` — the surrounding bullet text
   *is* the per-combination effect.

   Persist as a new `effect_variants` field on the synergy:

   ```json
   {
     "name": "BEES",
     "any_of": ["Honeycomb", "Bumbullets", "Jar of Bees"],
     "effect_variants": {
       "Honeycomb":   "Bee Hive shoots additional bees per shot.",
       "Bumbullets":  "Bees do extra damage and pierce.",
       "Jar of Bees": "Bee Hive periodically launches a jar swarm."
     }
   }
   ```

3. **Render variants in the app.** When `effect_variants` is present the
   synergy panel switches from the single `prettyEffect` line to a small
   variant list (one row per alternative, "Honeycomb → ...").

## Fix — Phase 3 (data quality sweeps)

- Audit other patterns that lose info: rows that begin with `"and one of"`,
  rows with deeply nested `<dl>`/`<ul>` markers, rows with `<br>`-separated
  variants instead of nested tables.
- Add a parser test: feed `synergies.json` through a validator that flags any
  effect that's just a prefix + concatenated `any_of` member names. Should
  drop to zero after Phase 2.
- Re-run `parse_wiki_rich.py` after the parser changes; verify
  `effect_tokens` no longer contain duplicate name fragments.
