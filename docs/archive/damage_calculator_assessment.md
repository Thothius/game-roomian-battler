# Damage Calculator Assessment & Redesign Plan

## Current State

### What Exists
- **`lib/services/damage_calculator.dart`** (82 lines) — Scans guns+items for `damage_up`/`damage_down` effect tags via `EffectTagger`, extracts numeric percentages from wiki text, sums them into a flat multiplier (e.g. 1.23 = +23%).
- **`_UniversalDamageCalculatorSliver`** in `active_run_screen.dart` (lines 3750–4018) — Terminal-style UI showing the multiplier, per-source contributions, and per-gun base→modified DPS.

### Problems Identified

1. **Flat multiplier applied to ALL guns equally** — A +15% damage item buffs every gun the same way. In-game, some synergies only affect specific guns or gun types. The calculator can't model gun-specific modifiers.

2. **Only scans `damage_up`/`damage_down` tags** — Misses:
   - Fire rate increases (which effectively raise DPS)
   - Crit chance/multiplier effects
   - Character-specific passives (Robot's junk/lies, Marine's reload, etc.)
   - Active item damage buffs (temporary)
   - Synergy bonuses (the biggest gap — synergies like "Double Down" double damage but aren't scanned)

3. **No synergy damage modeling** — Active synergies can dramatically change DPS (doubling damage, adding projectiles, etc.). The calculator ignores them entirely. `RunProvider.getActiveSynergiesCombined()` exists but isn't consulted.

4. **Additive-only stacking** — All percentages are summed additively. Some in-game effects stack multiplicatively. The current `1 + sum(pct)/100` model is wrong for multiplicative buffs.

5. **Regex extraction is fragile** — `EffectTagger.extractStat()` pulls the first number from effect text. Items like "Doubles damage" extract `2` and get treated as `+2%`, not `+100%`. The regex `(\d+(?:\.\d+)?)` grabs raw numbers without context.

6. **No per-gun breakdown** — Can't show "Gun X: base 50 → +15% from Item A → +100% from Synergy B → 172.5 effective DPS". Just shows flat base × multiplier.

7. **No character passive integration** — Each Gungeoneer has unique mechanics (Marine's reload speed, Hunter's dog, Pilot's discounts, Robot's junk tiers, Convict's damage after damage taken, Cultist's... nothing). None are modeled.

### Root Cause
The calculator was built as a quick "sum damage tags" utility, not a full DPS simulation. It's character-agnostic by design (comment says so), which means it intentionally skips the richest sources of damage variation.

## Redesign Plan

### Phase 1: Fix the regex parser (quick win)
- Fix "Doubles damage" → parse as ×2 multiplier, not +2%
- Handle "Increases damage by X%" vs "Doubles damage" vs "X% more damage"
- Add test cases for known item effect text patterns

### Phase 2: Integrate synergy bonuses
- Query `RunProvider.getActiveSynergies()` / `getActiveSynergiesCombined()`
- Parse synergy `effect` text for damage modifiers (same regex approach)
- Add synergy contributions as separate line items in the breakdown
- This is the biggest impact — synergies are where the real damage multipliers live

### Phase 3: Per-gun DPS with modifiers
- Instead of one flat multiplier, compute per-gun effective DPS:
  - Start with base DPS from gun data
  - Apply global damage modifiers (items, character passives)
  - Apply gun-specific synergy modifiers (some synergies name specific guns)
  - Apply fire rate modifiers (convert to DPS multiplier)
- Show a per-gun breakdown: base → +modifiers → effective

### Phase 4: Character passive modeling
- Add a `CharacterPassive` system:
  - Marine: reload speed bonus (affects sustained DPS)
  - Robot: junk/lies/gold-junk damage tiers (already has dedicated HUD)
  - Convict: damage up after taking damage (situational)
  - Hunter: trusty sidearm, dog companions
  - Pilot: active item charge rate
  - Cultist: teamwork bonus in co-op
  - Paradox: random gun generation
  - Gunslinger: dual-wield mechanics
- Each passive contributes to the damage calculation

### Phase 5: Interactive "what-if" mode
- Let the user tap a gun to see its full damage breakdown
- Show which items/synergies/character passives affect THIS gun specifically
- Allow simulating "if I add item X, how does my DPS change?"
- This is the "interactively calculate" part the user wants

### Architecture
```
DamageCalculator (static)
  ├── contributions(guns, items, synergies, character) → List<DamageContribution>
  ├── gunEffectiveDps(gun, guns, items, synergies, character) → double
  ├── multiplier(guns, items, synergies, character) → double  (global)
  └── breakdown(gun, guns, items, synergies, character) → DamageBreakdown

DamageBreakdown
  ├── baseDps: double
  ├── globalMultiplier: double
  ├── gunSpecificMultiplier: double
  ├── effectiveDps: double
  └── contributions: List<DamageContribution>  (filtered to this gun)
```

### Priority
1. **Phase 1** (fix regex) — 1 hour, immediate accuracy improvement
2. **Phase 2** (synergy integration) — 2 hours, biggest impact
3. **Phase 3** (per-gun breakdown) — 3 hours, UX improvement
4. **Phase 4** (character passives) — 4 hours, depth
5. **Phase 5** (interactive what-if) — 4 hours, polish
