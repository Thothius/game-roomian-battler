# Roomian Systems Assessment & Dev Readiness

> **Purpose:** Distilled audit of all Roomian game systems. No new features — just refinement, gap identification, and a dev readiness verdict.  
> **Source docs:** `roomian_visual_pictation.md` (game design), `roomian_races_art_direction.md` (art pipeline)  
> **Date:** Jul 25, 2026

---

## 1. System Status Board

| # | System | Status | Complexity | Dev-Ready? | Notes |
|---|--------|--------|------------|------------|-------|
| 1 | **Stat System** (6 stats, 2 resources) | ✅ Complete | Low | ✅ Yes | Formulas are clean, derived values are explicit |
| 2 | **Evolution Tree** (6×3×2 = 36 forms) | ✅ Complete | Medium | ✅ Yes | All branching paths defined, stat bonuses listed for L1/L5. **L8 stat bonuses missing** — see §3.1 |
| 3 | **Ability System** (4 active, 3 passive slots) | ✅ Complete | Medium | ✅ Yes | Progression table is explicit, slot fill order is clear |
| 4 | **Battle Mechanics** (3v3 simultaneous) | ✅ Complete | High | ⚠️ Mostly | Core loop is solid. **Flee mechanic has a contradiction** — see §3.2 |
| 5 | **Damage Formula** (two-roll + crit) | ✅ Complete | Low | ✅ Yes | `(abilityPower + PWR) × rand(0.8–1.2) − GRT`, crit ×1.5 post-GRT. Clean. |
| 6 | **Death Save System** (d20, 3 failures) | ✅ Complete | Low | ✅ Yes | Reset per battle, scars on success, permanent death at 3 failures |
| 7 | **Scar System** (d6, permanent, stacks) | ✅ Complete | Low | ✅ Yes | 6 scar types, stacking rules clear, "Battle-Scarred" badge at 3+ |
| 8 | **XP & Leveling Curve** | ✅ Complete | Low | ✅ Yes | Every level has a specific reward, no dead levels |
| 9 | **Level Progression** (per-level rewards) | ✅ Complete | Low | ✅ Yes | L0-L10 table is explicit, no skill points to bank |
| 10 | **Room Ball Catch System** | ✅ Complete | Low | ✅ Yes | Throw-and-reveal, 75/85/100% rates, identity hidden until caught |
| 11 | **Status Effects** (7 types, stacking) | ✅ Complete | Medium | ⚠️ Mostly | Stacking rules are clear. **Cure mechanism contradicts "no items" pillar** — see §3.3 |
| 12 | **Quest System** (4 types, risk tiers) | ✅ Complete | Low | ✅ Yes | Forage/Scout/Hunt/Deep Dive. **Quest death undefined** — see §3.4 |
| 13 | **Training System** (stat drip) | ✅ Complete | Low | ✅ Yes | 10 min, +5 XP + small stat bump. Clear. |
| 14 | **Rest & Recovery** | ✅ Complete | Low | ✅ Yes | 5 min rest = full HP, 10 min for downed, 50% auto-heal after battle |
| 15 | **Wild AI** (PvE decision tree) | ✅ Complete | Low | ✅ Yes | Simple HP-threshold-based logic. Sufficient for MVP. |
| 16 | **Battle Formats** (1v1/2v2/3v3 + Raid) | ✅ Complete | Low | ✅ Yes | Timer rules per format are clear |
| 17 | **Flee Mechanics** | ⚠️ Underspecified | Low | ⚠️ Needs clarification | See §3.2 |
| 18 | **Team Synergy** | 📋 Future | Medium | 🔜 Phase 2 | Marked as future. Correct — not needed for MVP. |
| 19 | **Data Model** (JSON) | ✅ Complete | Low | ⚠️ Minor | Structure is solid. **Color format inconsistency** — see §3.5 |
| 20 | **Art Pipeline** (Midjourney prompts) | ✅ Complete | High | ✅ Yes | L1 prompts ready, L0 prompts added, asset audit done |
| 21 | **World/Exploration** | ❌ Undefined | High | ❌ No | How wild Roomians appear is not defined — see §3.6 |
| 22 | **Economy/Shop** | ⚠️ Underspecified | Low | ⚠️ Needs definition | Gold has no defined spend beyond "future Tutor" — see §3.7 |
| 23 | **Onboarding/Starter** | ⚠️ Underspecified | Low | ⚠️ Needs definition | Do you start with a Roomian or just balls? — see §3.8 |

---

## 2. What's Solid (No Changes Needed)

These systems are mechanically complete and internally consistent:

### Core Math
- **HP formula**: `VIT × 2 + 10 + Level × 3` — clean linear scaling
- **EN formula**: `(GRT + INT) × 2 + 15 + Level × 3` — dual-stat dependency rewards hybrid builds
- **EN regen**: `3 + floor((GRT + INT) / 5)` per turn — creates resource tension without starvation
- **Damage**: two-roll system with variance + post-GRT crits — feels organic, math is transparent
- **Dodge/Crit caps**: 30% / 25% — prevents degenerate builds

### Progression
- **Every level delivers a reward** — no dead levels, no banked skill points
- **Evolution at L1/L5/L8** — branching is permanent, creates build identity
- **Ability slot fill order** is explicit: L0 base → L1 evolution → L3 choice → L5 evolution (4 active); L1 → L4 → L8 (3 passive)
- **Evolution abilities stack** — Roomian keeps all tier abilities, creating build depth
- **XP curve** escalates smoothly: 50 → 80 → 120 → 170 → 230 → 300 → 380 → 470 → 570 → 680

### Risk Systems
- **Death save** (d20: 10+ survive with scar, nat 20 revive, 2-9 failure, nat 1 double failure, 3 failures = death) — brutal but fair
- **Scars permanent and stacking** — creates real attachment and loss aversion
- **Death save counter resets per battle** — prevents snowballing failure across sessions
- **Flee punishment** (+50% damage on failed flee) — discourages rage-quitting

### Game Loop
- **Explore → Catch → Train → Battle** loop is clean and well-defined
- **No consumable clutter** in battle — just abilities and EN management
- **3v3 simultaneous** (no swap) — unique mechanic, simplifies UI, all Roomians relevant
- **Catch is throw-and-reveal** — no battle needed, identity hidden until caught, exciting reveal

---

## 3. Issues & Gaps (Need Resolution Before Dev)

### 3.1 L8 Mastery Stat Bonuses Missing

**Problem:** L1 and L5 evolution choices list explicit stat bonuses (e.g., Fire L1: +3 PWR, +1 VIT). L8 masteries only describe the passive/ultimate ability but don't list stat bonuses.

**Impact:** The evolution card mockup (§2.6) shows L8 cards with "+5 PWR, +2 INT" — but these values aren't defined in the mastery section (§2.4). A developer won't know what stats each mastery grants.

**Fix:** Add stat bonuses to all 36 L8 masteries. Pattern: each mastery grants +5 to primary stat + +2 to secondary, matching the refinement's identity (DPS gets PWR/SPD, tank gets GRT/VIT, mage gets INT/EN regen).

### 3.2 Flee Mechanic Contradiction

**Problem:** Two conflicting rules:
- §5.2: "Flee costs 6 EN" per Roomian — implies individual Roomians flee
- §10.3: "PvP battles: Both players must agree to draw (mutual flee)" — implies team-level flee

**Impact:** Unclear whether flee is per-Roomian or per-team. If per-Roomian, what happens when one flees but others stay? Does the battle continue 2v3?

**Fix:** Clarify:
- **PvE:** Flee is per-Roomian. A Roomian that flees leaves the battle (downed but not dead). Battle continues with remaining Roomians. If all flee = loss.
- **PvP:** Flee is a team-level action. All 3 Roomians must flee together. Both players must agree to a draw. This replaces individual flee in PvP.

### 3.3 Status Cure Contradicts "No Items" Pillar

**Problem:** §8.1 lists "Burn Cure", "Freeze Cure", "Shock Cure", "Charm Cure" as cures for status effects. But Design Pillar 4 states "No consumable clutter — No potions, no items in battle."

**Impact:** Developer won't know if cures are items or abilities.

**Fix:** Cures are **abilities**, not items. Specifically:
- Light element has cleanse-type abilities (e.g., Solar Lance path mentions "cleanse all allies")
- Some passives may grant immunity (e.g., Forge Master's stun immunity)
- "Natural" cure = expires after duration without being cleansed
- Remove "Burn Cure / Freeze Cure / Shock Cure / Charm Cure" item references — replace with "Cleansed by: [ability name]" or "Natural (expires)"

### 3.4 Quest Death Undefined

**Problem:** Deep Dive quest has "Guaranteed boss battle" with "High" risk. But if the Roomian is downed in that battle, does the death save system apply? Can a Roomian permanently die on a quest?

**Impact:** Player sends a beloved Roomian on a Deep Dive and it permanently dies — this could feel terrible if unexpected. Needs to be explicit.

**Fix:** Define quest battle rules:
- **Quest battles use the same death save system** — risk is real
- **Deep Dive explicitly warns:** "WARNING: Your Roomian can permanently die on this quest"
- **Quest battle is auto-resolved** (no player input) — uses AI logic from §10.1, Roomian plays itself
- **If downed on quest:** Roomian returns with 1 HP and a scar (if death save succeeds), or dies (if 3 failures)
- **Mitigation:** Higher GRT = safer, quest success chance reduces encounter difficulty

### 3.5 Data Model Color Format Inconsistency

**Problem:** Data model uses `"color": "#FFFF4500"` (ARGB 8-digit hex), but color palette table uses `#FF6B35` (6-digit RGB hex).

**Fix:** Standardize on 6-digit RGB hex (`#FF6B35`) for all color values in data model. Alpha is handled by Flutter's `Color(0xFF...)` constructor, not stored in JSON.

### 3.6 World/Exploration System Undefined

**Problem:** The game loop shows "EXPLORE world find wild" but there's no definition of:
- How wild Roomians appear (random encounters? map locations? spawn timer?)
- Where battles happen (is there a world map? rooms? hub?)
- How players find each other for PvP (matchmaking? proximity? challenge code?)

**Impact:** This is the **largest gap**. Battle/catch/evolution systems are all well-defined, but the context in which they happen is missing.

**Assessment:** This is intentionally left open — it's the "how does the player engage with the systems" layer. The core mechanics (battle, evolution, stats) are dev-ready without it. For MVP, a simple hub-based structure would suffice:
- **Hub screen** → Tap "Explore" → Random wild Roomian encounter (catch opportunity)
- **Hub screen** → Tap "Battle" → PvP matchmaking or PvE raid selection
- **Hub screen** → Tap "Quest" → Send Roomian on quest
- **Hub screen** → Tap "Belt" → Manage Roomians

This doesn't need to be a full world map. A menu-driven hub is sufficient for MVP and can be expanded later.

### 3.7 Economy Has No Gold Sink

**Problem:** Gold is listed as a core resource, but the only defined spend is "Tutor (future)". Room Balls are "starter pack, shop" — implying a shop exists, but it's not defined.

**Fix:** Define the shop minimally:
- **Room Balls:** Standard 50g, Quality 150g (unlocks at player level 5), Master 500g (unlocks at player level 10)
- **Ability Scrolls:** Random scroll 100g, Element-specific scroll 300g
- **Rest:** Free (just time-gated)
- **Training:** Free (just time-gated)
- **Tutor:** Future — teach specific abilities for gold

This gives gold immediate value without adding new systems.

### 3.8 Onboarding/Starter Package Undefined

**Problem:** Wild Roomians are always L0 Blobs. You need Room Balls to catch them. But do you start with a Roomian or just balls?

**Fix:** Define starter package:
- **Player starts with:** 3 Standard Room Balls + 1 pre-caught L0 Blob (random element on first catch — actually no, wild are L0 neutral Blobs, element revealed at L1 evolution)
- **Tutorial flow:** 
  1. Start with 1 Blob (L0, neutral) + 3 Standard Balls
  2. First battle: guided 1v1 vs AI Blob (teaches battle basics)
  3. First evolution: guided L1 choice (teaches evolution)
  4. First catch: throw ball at wild Blob (teaches catch mechanic)
  5. Free play unlocked

This gives the player immediate engagement without a dead-start.

---

## 4. Cross-System Consistency Checks

### 4.1 Ability Slot Math ✅
```
L0: 1 active (Tackle), 0 passive
L1: 2 active (+1 evolution), 1 passive (+1 evolution)
L3: 3 active (+1 choice)
L4: 3 active, 2 passive (+1 choice)
L5: 4 active (+1 evolution), 2 passive
L8: 4 active, 3 passive (+1 evolution)
→ Max: 4 active, 3 passive. No overflow. ✅
```

### 4.2 EN Economy ✅
```
L0 Blob: EN regen = 3 + floor(10/5) = 5/turn
  Tackle costs 3 EN → can always attack. ✅
  Defend costs 4 EN → can always defend. ✅
  Flee costs 6 EN → need 2 turns to save up. Creates tension. ✅

L8 Master (GRT 20, INT 18): EN regen = 3 + floor(38/5) = 10/turn
  Heavy attack costs 8 EN → sustainable every turn. ✅
  Field ability costs 15 EN → need 2 turns. Good for ultimates. ✅
```

### 4. HP Scaling ✅
```
L0 Blob (VIT 5): HP = 10 + 10 + 0 = 20
  Tackle (abilityPower ~10, PWR 5) vs GRT 5: (10+5)×1.0 - 5 = 10 dmg
  → 2 hits to down. Fast but fair for L0. ✅

L8 Tank (VIT 20, Level 8): HP = 40 + 10 + 24 = 74
  Heavy attack (abilityPower 30, PWR 25) vs GRT 15: (30+25)×1.0 - 15 = 40 dmg
  → 2 hits to down. Consistent TTK across levels. ✅

L8 DPS (VIT 12, Level 8): HP = 24 + 10 + 24 = 58
  Same attack: 40 dmg → 2 hits to down. Glass cannon dies faster. ✅
```

### 4.4 Evolution Path Count ✅
```
L0: 1 form (Blob)
L1: 6 forms (6 elements)
L5: 18 forms (6 × 3 refinements)
L8: 36 forms (18 × 2 masteries)
Total unique final forms: 36 ✅
Total sprites needed: 1 + 6 + 18 + 36 = 61 (per race)
3 races: 183 sprites + poses + avatars ✅ (matches asset audit)
```

### 4.5 Death Save Probability ✅
```
Per death save:
  Success (10-19): 50% → survive + scar
  Nat 20: 5% → revive at 1 HP
  Failure (2-9): 40% → 1 failure mark
  Nat 1: 5% → 2 failure marks

Expected failures per save: 0.4 + 0.1 = 0.5
Expected saves until death (3 failures): ~6 saves
  → A Roomian survives ~6 near-death experiences on average before permanent death.
  → Each survival adds a scar. 6 scars = severely weakened but alive.
  → Feels brutal but fair. ✅
```

---

## 5. Dev Readiness Verdict

### ✅ Ready to Dev (Core Systems)
- Stat system + derived values
- Evolution tree (all 36 paths defined)
- Ability system (slots, progression, stacking)
- Battle mechanics (planning → execution → resolution)
- Damage formula
- Death save + scar system
- XP curve + level progression
- Room Ball catch mechanic
- Status effects + stacking
- Quest + training + rest systems
- Wild AI
- Data model (JSON structure)
- Art pipeline (Midjourney prompts + asset audit)

### ⚠️ Needs Definition Before Dev (8 items — all are clarifications, not new features)
1. **L8 stat bonuses** — add +5/+2 stats to all 36 masteries
2. **Flee mechanic** — clarify PvE (per-Roomian) vs PvP (team-level draw)
3. **Status cures** — replace item references with ability-based cures
4. **Quest death rules** — define what happens when downed on a quest
5. **Color format** — standardize on 6-digit RGB hex
6. **World/hub structure** — define minimal hub menu for MVP
7. **Shop/economy** — define Room Ball prices + gold sink
8. **Starter package** — define what player starts with + tutorial flow

### 📋 Deferred to Phase 2+ (Already Marked as Future)
- Team synergy bonuses
- Tutor NPC
- Breeding
- Prestige mechanics (L10 is cosmetic only — fine)
- World map / exploration expansion

### Verdict: **Yes, solid to dev soonish.**

The 8 items above are all **clarifications of existing systems**, not new features. They're decisions, not inventions. The core game loop (explore → catch → train → battle) is fully designed. The math is consistent. The evolution tree is complete. The art pipeline is ready.

**Recommended next step:** Resolve the 8 clarification items (30-min design session), then start with the data model + battle system as the first dev vertical slice.

---

## 6. Recommended Dev Order (MVP Vertical Slice)

```
Phase 0 — Data Layer (1-2 days)
├── Roomian data model (Dart classes from JSON schema)
├── Evolution tree data (all 36 paths as JSON)
├── Ability database (all abilities with EN cost, power, type)
├── Status effect definitions
└── Scar definitions

Phase 1 — Core Battle (3-5 days)
├── Battle state machine (planning → execution → win/loss)
├── Damage calculation (two-roll formula)
├── EN regen + resource management
├── Status effect application + stacking
├── Death save system (d20 roll)
├── Scar application
└── Wild AI (PvE decision tree)

Phase 2 — Progression (2-3 days)
├── XP tracking + level-up logic
├── Stat increase choice (3 random options)
├── Evolution choice screens (L1/L5/L8)
├── Ability slot management
└── Ability scroll learning

Phase 3 — Meta Systems (2-3 days)
├── Room Ball catch mechanic (throw + reveal)
├── Quest system (send + timer + resolve)
├── Training system
├── Rest + cooldown timers
└── Shop (Room Balls + scrolls for gold)

Phase 4 — UI (3-5 days)
├── Hub screen
├── Belt/inventory screen
├── Roomian detail screen
├── Battle screen (planning + execution)
├── Evolution choice screen
├── Death save screen
└── Level-up screens

Total MVP: ~12-18 days for a playable vertical slice
```

---

*This document is the executive summary. Full design details live in `roomian_visual_pictation.md`. Art pipeline details live in `roomian_races_art_direction.md`.*
