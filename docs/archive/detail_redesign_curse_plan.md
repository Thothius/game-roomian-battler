# Item/Gun Detail Redesign + Special Mechanics + Curse Dashboard Plan

## Status: Research Complete — Ready for Implementation

---

## 1. Icon Removal (DONE — this session)

### What was done
- **NeckbearMedal** hidden in `item_detail_screen.dart` (_Header) and `browse_screen.dart` (tile view)
- **BugReport icons** hidden in `item_detail_screen.dart` (_Header Positioned), `active_run_screen.dart` (MP Link View + Inventory View trailing)
- All changes are comment-outs, not deletions — fully reversible

### Remaining cleanup (optional, future)
- `neckbear_medal.dart` widget file still exists, import still present in both screens
- `BugReporter` class and `bug_reporter.dart` untouched — still functional if re-enabled
- `neckbearApproved` field in `Gun` and `Item` models untouched — data integrity preserved
- If permanent: remove imports + widget file in a follow-up pass

---

## 2. Item/Gun Detail View Redesign

### Current State
- `_Header` widget: Row layout — 96px icon left, name+quality+quote right, favourite button top-right
- `_GunStats` widget: Split row (fire-type animation | DPS readout), then stat groups (Combat/Handling/Meta) as pill wraps
- `_ItemBody` widget: Effect text, recharge/duration pills, synergy list, special trackers (Junkan, Spice, Sprun, Payday)
- Title is 24px, icon is 96px — both feel small on modern devices

### Redesign Goals
1. **Bigger title + graphic** — hero-style header
2. **Top panel with metadata** — sell price, synergy count, curse/coolness, quality badge
3. **Bottom area: short gun summary string**
4. **Stats panel: firing mode, DPS, all stats neatly together**

### Proposed Layout

```
┌─────────────────────────────────────┐
│         [128px Icon/Graphic]        │  ← Bigger icon, centered or left
│                                     │
│  ITEM NAME (28px, w900)             │  ← Bigger title
│  [Quality Badge]  [Type]  [Class]   │  ← Inline metadata row
│                                     │
│  "Quote text in italics"            │
│                                     │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐    │  ← Metadata chips row
│  │Sell │ │Syns │ │Curse│ │Cool │    │
│  │ 15  │ │  3  │ │ +1  │ │  0  │    │
│  └─────┘ └─────┘ └─────┘ └─────┘    │
│                                     │
│  Short summary string               │  ← One-line gun summary
│  "Full-auto beam, 25.8 DPS, homing" │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  [Fire Animation]  │  [DPS: 25.8]   │  ← Existing split row, refined
│                    │  [Damage: 6.5] │
│                    │  [Reload: 1.1s]│
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  COMBAT                             │
│  [Damage] [Fire Rate] [Mag] [Ammo]  │  ← Existing pill groups
│  HANDLING                           │
│  [Range] [Shot Speed] [Force]       │
│  META                               │
│  [Class] [Sell] [Chest]             │
└─────────────────────────────────────┘
```

### Implementation Details

#### A. _Header Redesign
- Increase icon from 96px → 128px
- Increase title from 24px → 28px
- Add metadata chip row below quote: Sell Price, Synergy Count, Curse, Coolness
- Synergy count: query `RunProvider.synergies` for items matching this entity name
- Sell price: already available as `gun.sellPrice` / item sell price from data
- Curse/Coolness: already available as `gun.curse` / `gun.coolness` / `item.curse` / `item.coolness`
- Generate short summary string from gun stats (see below)

#### B. Short Gun Summary String
Auto-generate a one-liner like:
- `"Full-auto • 25.8 DPS • Homing • Piercing"`
- `"Semiauto • 6.5 dmg • 1.1s reload • Beam"`
- `"Charge • Explosive • 2.5 curse"`

Pattern: `{fireType} • {DPS} DPS • {notable tags from effect_tagger}`

For items:
- `"Passive • +1 Curse • Companion"`
- `"Active • 6s recharge • Charm chance"`

#### C. _GunStats Refinement
- Keep the split animation/DPS row (it works well)
- Move sell price OUT of Meta group (now in header chips)
- Add DPS to the summary string in header (redundant but quick-glance)
- Consider adding `gunClass` as a visual badge in header instead of Meta pill

### Files to Modify
- `lib/screens/item_detail_screen.dart` — `_Header`, `_GunStats`, `_ItemBody`
- Possibly `lib/widgets/` — new `_MetadataChip` widget if reusable

### Estimated Effort
- Header redesign: ~2 hours (layout + data wiring)
- Summary string generator: ~1 hour (logic + formatting)
- Stats panel cleanup: ~30 min (remove duplicates, reorganize)
- Testing & polish: ~1 hour

---

## 3. UX Assessment: Missing Effect Symbols/Tags

### Current Tag System
`effect_tagger.dart` has 30+ tags across 8 categories:
- **Mobility**: flight, speed_up, dodge_up, shoot_while_rolling
- **Damage**: damage_up, fire_rate_up, piercing, bouncing, homing, explosive, crit, freeze, poison, burn, stun, knockback
- **Ammo**: ammo_up, reload_up, free_ammo
- **Defense**: max_hp_up, armor, heal, invuln, damage_resist, revive
- **Economy**: key_drops, open_any, shop_discount, shop_steal, extra_loot, map_reveal
- **Utility**: blank_grant, charm, slow_time, companion_summon
- **Status**: coolness_up
- **Debuff**: curse_up, damage_down, ammo_down, speed_down, hp_cost, jam_risk

### Gaps Identified

#### Missing tags (effects that exist in game data but have no regex pattern):
1. **Bleed/Poison DoT** — "poison" tag exists but doesn't distinguish DoT vs on-hit chance
2. **Goop/Pool creation** — no tag for "leaves behind a pool of poison/fire" (e.g. Plague Pistol, Dragunfire)
3. **Table flip** — no tag for table-flip mechanics
4. **Beam/laser** — no tag for sustained beam weapons (only inferred from `type` field)
5. **Charge mechanics** — no tag for charge-time weapons (only inferred from `type` field)
6. **Twin shot / Multi-shot** — no tag for guns that fire multiple projectiles per shot
7. **Orbital bullets** — no tag for orbiting projectile mechanics
8. **Time dilation for enemies** — "slow_time" exists but only for player-triggered slow-mo
9. **Jammed enemy spawning** — "jam_risk" catches "jammed enemies" but not "spawns jammed"
10. **Curse scaling damage** — no tag for "damage scales with curse" (e.g. Cursed Cannon)
11. **Glass guon stones** — no specific tag
12. **Mimic avoidance** — no tag for "prevents mimics" or "reveals mimics"

#### Tags that fire too broadly:
- `companion_summon` pattern `follows? the player` could match non-companion descriptions
- `burn` pattern `\bburn(s|ing)?\b` could match "burns through ammo" type phrases

#### Missing visual symbols:
- No icon for **beam/continuous fire** type (only animation GIF covers this)
- No icon for **charge type** (only animation GIF)
- No icon for **curse-scaling** mechanics
- Effect chips show text label + icon but no **tier color coding** (all use category color)

### Recommendations
1. Add 5-8 new EffectTags for the gaps above (goop, beam, charge, multi-shot, orbital, curse_scale, table_flip)
2. Tighten `companion_summon` regex to require "companion" or specific names
3. Add `gunClass`-derived tags (BEAM, CHARGE, FULLAUTO) as visual badges in detail view
4. Consider a "mechanics" section in detail view showing effect tags with icons + excerpts

### Files to Modify
- `lib/services/effect_tagger.dart` — add new tags, tighten patterns
- `lib/screens/item_detail_screen.dart` — display effect tags in detail view

---

## 4. Special Guns/Items with Leveling Mechanics — Assessment

### Already Tracked (Dashboard Slivers in active_run_screen.dart)

| Entity | Type | Mechanic | State in RunProvider | Dashboard Widget |
|--------|------|----------|---------------------|-----------------|
| **Gunderfury** | Gun | Levels 1-60, 6 forms, XP from kills | `gunderfuryLevel` | `_GunderfuryDashboardSliver` |
| **Triple Gun** | Gun | 3 forms (shotgun/chaingun/beam), swap via reload | `tripleGunForm` | `_TripleGunDashboardSliver` |
| **Evolver** | Gun | 6 stages, evolves on unique enemy kills (25 total) | `evolverForm`, `evolverKills` | `_EvolverDashboardSliver` |
| **Ser Junkan** | Item | 8 ranks (Peasant→Angelic Knight) based on junk count | Tracked via item count | `_JunkanDashboardSliver` |
| **Spice** | Item | Stacking uses (1-5+), escalating stats + curse | `spiceUsageCount` | Inline in `_ItemBody` |
| **Sprun** | Item | Hidden trigger per run, transforms to Windgunner | `sprunTriggerIndex`, `windgunnerCountdown` | Inline in `_ItemBody` |
| **Payday** | Item | Clown Mask + Smoke Bomb tracking for heist bonus | Tracked via item presence | Inline in `_ItemBody` |

### Other Special Mechanics (NOT yet tracked)

| Entity | Type | Mechanic | Notes |
|--------|------|----------|-------|
| **Chamber Gun** | Gun | Transforms based on current chamber floor | Could add a floor selector |
| **Boxing Glove** | Gun | Stars (1-3) from kills, lost on damage/switch | Simple counter tracker |
| **Devolver** | Gun | Chance to devolve enemies | No tracking needed (passive) |
| **Betrayer's Shield** | Gun | Shield that blocks bullets while reloading | No tracking needed |
| **Cursed Cannon** | Gun | Damage scales with curse | Could show dynamic DPS from curse |
| **Heroine** | Gun | Damage increases with curse (up to 200%) | Could show dynamic DPS from curse |
| **Ray of Hope** | Gun | Heals on hit, unique mechanic | No tracking needed |
| **AKEY-47** | Gun | Opens any chest/lock without key | No tracking needed (passive) |
| **Dungeon Eagle** | Gun | Charged shot pierces walls | No tracking needed |
| **Gungine** | Gun | Speeds up with movement, full-auto at max | Could add a momentum tracker |

### Dashboard Clutter Problem

Currently the active run screen uses conditional Sliver widgets:
```dart
if (player.character?.name.toLowerCase().contains('robot') ?? false)
  const _RobotDashboardSliver(),
if (player.character?.name.toLowerCase().contains('hunter') ?? false)
  const _HuntressDashboardSliver(),
if (player.items.any((it) => it.name.toLowerCase() == 'ser junkan'))
  _JunkanDashboardSliver(slot: _slot),
if (player.guns.any((g) => g.name.toLowerCase() == 'gunderfury'))
  _GunderfuryDashboardSliver(slot: _slot),
// ... etc
```

**Problem**: A player could have Robot + Ser Junkan + Gunderfury + Triple Gun + Evolver + Spice + Sprun = 7+ dashboard panels stacked vertically. This is too much.

### Proposed Solution: Collapsible Dashboard Section

1. **Group all special-mechanic panels under a single "Special Mechanics" expandable section**
2. Each panel becomes a card inside a horizontal PageView or vertical accordion
3. Only the active/expanded panel takes screen space
4. Collapsed state shows a compact row: `[icon] Gunderfury Lvl 42  [icon] Evolver Stage 3  [icon] Junkan Knight`
5. Tapping a compact row expands that panel inline

**Alternative**: Tab bar at top of the section — swipe between special mechanic panels

**Implementation approach**:
- Create `_SpecialMechanicsHub` widget that wraps all conditional panels
- Each special entity registers a "compact summary" + "expanded detail" builder
- Hub renders compact summaries in a Wrap/Row, expands one at a time
- Reduces 7 slivers to 1 sliver

### Files to Modify
- `lib/screens/active_run_screen.dart` — replace individual slivers with hub
- New widget: `lib/widgets/special_mechanics_hub.dart` (or inline)

---

## 5. Curse Mechanics Assessment & Dashboard Plan

### All Curse Sources in Enter the Gungeon

#### A. Items that Grant Curse (while held)

| Item | Curse | Quality | Notes |
|------|-------|---------|-------|
| Cursed Cannon | +1.0 | A | Gun, damage scales with curse |
| Dueling Pistol | +1.0 | — | Gun |
| Elephant Gun | +1.0 | — | Gun |
| Gray Maiden | +1.0 | — | Gun |
| Hexagun | +1.0 | — | Gun |
| Shader | +1.0 | — | Gun |
| Betrayer's Shield | +1.0 | — | Gun, shield while reloading |
| Cursed Bullets | +1.0 | 1S | Item, projectile impacts trigger blank |
| Debug Pistol | +1.0 | 1S | Gun |
| Fatigued Cannon | +1.0 | — | Gun (if exists in data) |
| Dr. Flock's Flock | +1.0 | — | Gun |
| Heroine | +2.0 | — | Gun, damage scales with curse up to 200% |
| Machine Fist | +2.0 | — | Gun |
| Cursed Bullets | +1.5 | 1S | Item |
| Rattling Shield | +1.0 | D | Item, blank on damage + ammo refill |
| Katana Bullets | +1.0 | C | Item, slash flurry on kill |
| Knife Chair | +1.0 | D | Item, ring of knives |
| Shellraiser | +1.0 | B | Item, spawns enemies + chance for gun/item |
| C4 | +1.0 | D | Item, explosive, calls missile |
| Vampire Glasses | +1.0 | A | Item, heals after 1200 damage |
| Too Much Information | +1.0 | C | Item, shows enemy HP + damage/accuracy up |
| Master Round I-V | — | — | No curse (these are rewards) |
| Ring of Mimic Friendship | +2.0 | 1S | Item, grants 2 hearts + charm chance |
| Excommunicate | +2.0 | B | Item, activates blank |
| Blessing of Kaliber | +2.0 | A | Item, +2 coolness per curse point |
| Spicy Visor | +1.0 | C | Item, damage scales with curse |
| Cop's Revolver | +2.0 | A | Item (companion), talking to dead cop +2 curse |
| Cursed Bullet | +1.0 | 1S | Item, opens any chest/lock |

#### B. Guns that Grant Curse (while held)

| Gun | Curse | Notes |
|-----|-------|-------|
| Cursed Cannon | +1.0 | Damage scales with curse |
| Dueling Pistol | +1.0 | |
| Elephant Gun | +1.0 | |
| Gray Maiden | +1.0 | |
| Hexagun | +1.0 | |
| Shader | +1.0 | |
| Betrayer's Shield | +1.0 | Shield while reloading |
| Debug Pistol | +1.0 | |
| Machine Fist | +2.0 | |
| Heroine | +2.0 | Damage scales with curse |
| Cursed Bullet (gun?) | +2.5 | (if in guns.json) |

#### C. Shrines that Grant Curse

| Shrine | Curse | Notes |
|--------|-------|-------|
| Shell'tan (Ammo Shrine) | +3.5 | Refills all weapon ammo |
| Sacrifice Shrine | +1.5 | Removes heart, +25% damage |
| Dice Shrine | +5.0 | Random effect |
| Hero Shrine | Sets to 9 | Only after killing past |

#### D. Shrines that Remove Curse

| Shrine | Effect | Notes |
|--------|--------|-------|
| Cleanse Shrine | Sets curse to 0 | Costs 5 coins per point |

#### E. Manual/Action-Based Curse Sources

| Action | Curse | Current UI |
|--------|-------|-----------|
| Stealing from shop | +1.0 | Popup menu in active_run_screen |
| Buying from Cursula | +2.5 | Popup menu in active_run_screen |
| Spice (1st use) | +0.5 | Spice tracker in item detail |
| Spice (2nd+ use) | +1.0 each | Spice tracker in item detail |
| Talking to dead Cop (Cop's Revolver) | +2.0 | Not tracked |

#### F. Curse Effects (from stats_detail_screen.dart)

Curse table already implemented (0-10+):
- Jammed enemy chance: 0% → 50%
- Jammed boss chance: 0% → 50%
- Mimic chance: 2.25% → 23.25%
- Fuse time: unchanged → -50%
- Room rewards: unchanged → -50%
- Ammo drop multiplier: x1.00 → x1.50

### Proposed Curse Dashboard

When user taps the Curse bubble in `GungeoneerHeader`, instead of going to the generic `StatsDetailScreen`, show a dedicated **Curse Management Panel**:

```
┌─────────────────────────────────────┐
│  CURSE MANAGEMENT                   │
│  Current: 4.5                       │
│  [Slider: 0 ────●── 15]            │
│  [-1] [-0.5] [+0.5] [+1]           │
│                                     │
│  ─── CURSE SOURCES ───              │
│                                     │
│  From Items/Guns (held):            │
│  • Cursed Cannon     +1.0           │
│  • Heroine           +2.0           │
│  • Spicy Visor       +1.0           │
│  Subtotal: +4.0                     │
│                                     │
│  Manual Adjustments:                │
│  • Steal (shop)      +1.0           │
│  • Cursula buy       +2.5           │
│  Subtotal: +3.5                     │
│                                     │
│  ─── QUICK ACTIONS ───              │
│  [Steal from Shop +1]               │
│  [Buy from Cursula +2.5]            │
│  [Use Spice +0.5/+1.0]              │
│  [Cleanse Shrine → 0]               │
│                                     │
│  ─── CURSE EFFECTS ───              │
│  Jammed Enemy: 2%   Boss: 0%        │
│  Mimic Chance: 8.55%                │
│  Fuse: +15%   Rewards: -3%          │
│  Ammo: x1.15                        │
│                                     │
│  ─── CURSE-SCALING ITEMS ───        │
│  • Heroine: +200% dmg at 10 curse   │
│  • Spicy Visor: dmg scales w/curse  │
│  • Cursed Cannon: dmg scales w/curse│
│  • Blessing of Kaliber: +2 cool     │
│    per curse point                  │
└─────────────────────────────────────┘
```

### Implementation Approach

1. **New screen or expanded bottom sheet**: `CurseDashboardScreen` or transform `StatsDetailScreen` when `statType == StatType.curse`
2. **Curse source breakdown**: Query player's held items/guns, sum their curse values, show itemized list
3. **Quick action buttons**: Reuse existing `adjustCurse` calls from popup menu, but as persistent buttons
4. **Curse-scaling section**: List items in loadout that have curse-dependent mechanics
5. **Cleanse button**: Sets curse to 0 (calls `p.resetManualStats()` or new method)

### Files to Modify
- `lib/screens/stats_detail_screen.dart` — expand curse view or branch to new widget
- `lib/screens/active_run_screen.dart` — change `onTapCurse` to route to new curse dashboard
- Possibly new: `lib/screens/curse_dashboard_screen.dart` or `lib/widgets/curse_dashboard.dart`

### Data Already Available
- `RunProvider.runState.totalCurse` — current total
- `RunProvider.runState.curse` — manual base
- Each `Gun.curse` and `Item.curse` — per-entity curse
- `_curseTable` in stats_detail_screen — effects table
- `p.adjustCurse(delta)` — adjustment method
- Existing popup menu items for steal/cursula

---

## 6. Implementation Priority

| Phase | Task | Effort | Priority |
|-------|------|--------|----------|
| **Done** | Hide neckbear + bug report icons | 30 min | P0 |
| **Phase 1** | Write this plan doc | 1 hr | P0 |
| **Phase 2** | Redesign _Header (bigger icon/title, metadata chips) | 3 hrs | P1 |
| **Phase 3** | Add gun summary string generator | 1.5 hrs | P1 |
| **Phase 4** | Refine _GunStats (remove duplicates, reorganize) | 1 hr | P2 |
| **Phase 5** | Add missing effect tags (5-8 new patterns) | 2 hrs | P2 |
| **Phase 6** | Build Special Mechanics Hub (collapse dashboards) | 4 hrs | P2 |
| **Phase 7** | Build Curse Dashboard (source breakdown + actions) | 4 hrs | P1 |
| **Phase 8** | Show effect tags in detail view | 2 hrs | P3 |

### Dependencies
- Phase 2-4 are independent of each other (all touch item_detail_screen.dart but different widgets)
- Phase 6 depends on nothing (active_run_screen.dart only)
- Phase 7 depends on nothing (stats_detail_screen.dart + active_run_screen.dart routing)
- Phase 5 is independent (effect_tagger.dart only)
- Phase 8 depends on Phase 5 (needs new tags to exist first)

---

## 7. Key Files Reference

| File | Purpose |
|------|---------|
| `lib/screens/item_detail_screen.dart` | _Header, _GunStats, _ItemBody (3029 lines) |
| `lib/screens/active_run_screen.dart` | Dashboard slivers, curse popup, stat adjuster (7375 lines) |
| `lib/screens/stats_detail_screen.dart` | Curse/coolness detail with effects table (756 lines) |
| `lib/screens/browse_screen.dart` | Browse tiles with neckbear/verified (1628 lines) |
| `lib/widgets/gungeoneer_header.dart` | Curse/coolness capsules, tap handlers (857 lines) |
| `lib/services/effect_tagger.dart` | 30+ effect tags, regex patterns, scan/chip system (769 lines) |
| `lib/models/gun.dart` | Gun model with getDynamicDps, curse, sellPrice (195 lines) |
| `lib/models/item.dart` | Item model with curse, coolness |
| `lib/providers/run_provider.dart` | State: gunderfuryLevel, tripleGunForm, evolverForm, spiceUsageCount, etc. |
| `assets/data/items.json` | 15 items with curse > 0 |
| `assets/data/guns.json` | 9 guns with curse > 0 |
| `assets/data/shrines.json` | 3 shrines with curse > 0, 1 cleanse shrine |
