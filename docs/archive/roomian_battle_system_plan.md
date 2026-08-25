# Roomian Battle System — Concept Design Document

> **Status:** Brainstorm / Big Picture Framing  
> **Date:** Jul 25, 2026  
> **Scope:** Pokemon-like creature collection + PvP battle mechanics for GungeonMate

---

## 1. Core Concept

Players find or earn **Room Balls** (3 per run, active-use items). When used, a Room Ball summons a **Roomian** — a creature from the Gungeon's depths. At launch, every Room Ball summons a **Blob** (template creature): RNG-colored, Level 0, no category yet. As the system grows, Roomians will be categorized into types with unique stats, abilities, and evolution paths.

**The loop:** Summon → Battle → Earn XP/Scars → Evolve/Upgrade → Battle again (or quest)

---

## 2. Room Balls

| Property | Value |
|----------|-------|
| Quantity per run | 3 |
| Item type | Active use item (consumed on use) |
| Summon result | RNG-colored Blob, Level 0 |
| Acquisition | Found in chests, shop, or shrine rewards (TBD) |
| Storage | Roomian is stored in player's "Roomian Belt" (separate from gun/item inventory) |

**Design note:** Room Balls are the *entry point* to the system. Limited to 3 per run so players make strategic choices about when to summon. The Ball is consumed on use — the Roomian persists.

---

## 3. Roomian Creature Model (Template Blob)

### 3.1 Core Stats

Inspired by Pokemon's 6-stat system but distilled for GungeonMate's companion-app context:

| Stat | Abbrev | Description |
|------|--------|-------------|
| **Vitality** (HP) | VIT | How much damage before downed |
| **Power** (ATK) | PWR | Physical attack damage |
| **Grit** (DEF) | GRT | Damage reduction from physical |
| **Focus** (SPD) | FOC | Turn order + dodge chance |
| **Luck** (CRIT) | LCK | Critical hit chance + item find rate |

> **Why 5 not 6:** GungeonMate is a companion app, not a full RPG. 5 stats keep team-building decisions meaningful without overwhelming. Special attack/defense merged into Power/Grit — we can split later if categories demand it.

### 3.2 Blob Baseline (Level 0 Template)

```
VIT: 20    PWR: 5     GRT: 5     FOC: 5     LCK: 5
Type: Neutral (no category yet)
Color: RNG from Gungeon palette (Amber, Cyan, Green, Pink, Purple, White)
Abilities: [Tackle] — basic PWR-based attack
```

### 3.3 Leveling & Growth

- **XP sources:** Battles (win/lose), Quests (success/fail), Training (wait-based)
- **Level cap:** 20 (keeps numbers manageable for a companion app)
- **Stat growth per level:** +2 VIT, +1 to two random stats (RNG, weighted by category once defined)
- **Evolution:** At certain level thresholds (e.g. L5, L10, L15), Roomian can evolve — changes appearance, unlocks new ability, stat boost. Evolution is optional (player chooses) — some strategies may prefer lower-level with better scar management.

### 3.4 Persistence

Roomians survive across runs (they're companions, not consumables). Stored in SharedPreferences as JSON:
```json
{
  "id": "roomian_001",
  "name": "Blobby",
  "species": "Blob",
  "level": 0,
  "xp": 0,
  "color": "#FF00E5FF",
  "stats": {"vit": 20, "pwr": 5, "grt": 5, "foc": 5, "lck": 5},
  "abilities": ["tackle"],
  "scars": [],
  "status": "active",
  "cooldownUntil": null,
  "deathSaves": {"successes": 0, "failures": 0},
  "isDowned": false
}
```

---

## 4. Battle System

### 4.1 Design Philosophy

**Turn-based, streamlined.** Pokemon's formula is proven but too heavy for a companion app. We distill to:

- **1v1 Roomian battles** (expand to 2v2 later)
- **3 action slots** per turn (not 4 moves like Pokemon — less menu clutter)
- **Type effectiveness** (once categories are defined — Blob vs Blob is neutral)
- **Speed-based turn order** (FOC stat determines who goes first)
- **STAB equivalent:** If Roomian's category matches ability category, +50% damage

### 4.2 Damage Formula (Simplified Pokemon)

```
Damage = floor(((2 * Level / 5 + 2) * Power * PWR / GRT) / 50 + 2) * TypeMod * STAB * Random(0.85–1.0)
```

- **Power** = ability base power (Tackle = 35)
- **PWR** = attacker's Power stat
- **GRT** = defender's Grit stat
- **TypeMod** = 0.5 / 1.0 / 2.0 (once categories exist)
- **STAB** = 1.5 if category match, else 1.0
- **Random** = 85%–100% damage roll (the RNG spice)
- **Critical** = LCK% chance for 1.5x damage (ignores GRT boosts)

### 4.3 Battle Flow

```
1. Both players select their Roomian (from Belt)
2. Battle screen shows both Roomians with HP bars
3. Each turn:
   a. Both players pick an action (attack / ability / swap / flee)
   b. Higher FOC acts first
   c. Damage calculated, HP reduced, animations play
   d. Check for downed (HP <= 0)
4. When a Roomian is downed → Death Saving Throw sequence
5. Battle ends when one Roomian is dead or fled
```

### 4.4 Action Types

| Action | Description |
|--------|-------------|
| **Attack** | Use one of 3 equipped abilities |
| **Defend** | Halve incoming damage next turn, +1 FOC temporarily |
| **Swap** | Switch to another Roomian in Belt (costs full turn) |
| **Flee** | Escape battle — high risk (see below) |

### 4.5 Status Effects (Gungeon-Themed)

Inspired by Pokemon status conditions + Gungeon's elemental system:

| Status | Effect | Source |
|--------|--------|--------|
| **Jammed** | -25% PWR, visual purple tint | Curse-type abilities |
| **Chilled** | -50% FOC (slowed) | Ice-type abilities |
| **Burning** | Lose 1/16 VIT per turn, -50% PWR | Fire-type abilities |
| **Poisoned** | Lose 1/8 VIT per turn | Poison-type abilities |
| **Charmed** | 25% chance to skip turn | Charm-type abilities |
| **Blanked** | Cannot use abilities (attack only) | Blank-type abilities |

---

## 5. Death Saving Throws

### 5.1 When It Triggers

When a Roomian's VIT reaches 0 in battle, it enters the **Downed** state. The player must roll a **d20 death saving throw** — animated using the existing dice roll system from `dice_roll.dart`.

### 5.2 Mechanics (D&D 5e Inspired, Simplified)

| Roll (d20) | Result |
|------------|--------|
| **Natural 1** | 2 failures (catastrophic) |
| **2–9** | 1 failure |
| **10–19** | 1 success — **Roomian survives but gains a Scar** |
| **Natural 20** | 1 success + revive at 1 VIT (miracle) |

**Rules:**
- **3 failures = Roomian perishes permanently** (removed from Belt, memorialized)
- **1 success = Roomian survives** (simplified from D&D's 3-success stabilize)
- Need only **1 success** to survive (per user spec — high stakes, quick resolution)
- After surviving, Roomian enters **cooldown** (cannot battle for a wait period)

### 5.3 Scar System

On a successful death save (10–19), the Roomian gains a **Scar** — a permanent negative debuff. Scars are cumulative.

### Scar Table (d6 roll after survival)

| d6 | Scar | Effect |
|----|------|--------|
| 1 | **Weakened** | -2 PWR permanently |
| 2 | **Brittle** | -2 GRT permanently |
| 3 | **Sluggish** | -2 FOC permanently |
| 4 | **Cursed** | -2 LCK permanently |
| 5 | **Lobotomized** | 25% chance any action fails (does nothing) |
| 6 | **Fractured** | -1 to ALL stats permanently |

**Design intent:** Scars make death saves feel consequential even when you survive. A Roomian that barely survives 3 battles might be so debuffed it's practically useless — creating the strategic tension of "do I keep pushing this Roomian or retire it?"

### 5.4 Death Animation

When a Roomian perishes (3 failures):
- Screen darkens, Roomian sprite desaturates and dissolves
- Brief memorial screen: name, level, battles fought, scars survived
- Roomian slot in Belt becomes empty (Ball is gone too)
- Player must find/earn a new Room Ball

### 5.5 Fleeing — High Risk

Fleeing from battle is not free:
- **50% chance to fail** (must take incoming hit, no defense)
- If flee fails, opponent gets a free turn
- Successful flee = no XP, no scar, but Roomian is **shaken** (cannot battle for 10 min cooldown)

---

## 6. Quests & Training

### 6.1 Roomian Quests

Roomians can be sent on quests (solo, no player input needed). This is the "idle game" layer.

| Quest Type | Duration | Risk | Reward |
|------------|----------|------|--------|
| **Forage** | 5 min | None | Small XP + chance of item find |
| **Scout** | 15 min | Low | Medium XP + map info |
| **Hunt** | 30 min | Medium | High XP + rare item chance |
| **Deep Dive** | 60 min | High | Massive XP + evolution material, but Roomian can be downed (triggers death save on return) |

### 6.2 Quest Success Rates

Success chance = base 50% + (LCK * 2%) + (Level * 1%) - (Scar count * 5%)

- **Success:** Full XP + rewards
- **Partial success:** Half XP, minor reward
- **Failure:** No XP, Roomian enters cooldown (shaken, 5 min)
- **Critical failure (Deep Dive only):** Roomian downed, must death save on return

### 6.3 Training (Wait-Based Upgrade)

- Send Roomian to Training → cannot be used for X minutes
- Returns with +1 to a random stat
- Cost: increasing per training session (gold/resources TBD)
- Diminishing returns: each training session is 10% less effective than the last for that stat

---

## 7. Cooldown System

| Activity | Cooldown |
|-----------|----------|
| Battle (win) | 2 min |
| Battle (loss + survived) | 5 min |
| Battle (loss + fled) | 10 min |
| Quest (Forage) | None |
| Quest (Scout/Hunt) | 5 min |
| Quest (Deep Dive) | 15 min |
| Training | None (but Roomian unavailable during) |
| Death save survived | 10 min |
| Revived (nat 20) | 1 min (quick recovery) |

During cooldown, Roomian cannot battle or quest. Player can still view stats, manage abilities, or swap to another Roomian in their Belt.

---

## 8. Multiplayer Integration

### 8.1 Battle Requests

Leverages existing `MultiplayerSession` infrastructure (Nearby Connections):

- **Roomian Challenge:** Player A sends battle request to Player B
- Player B sees incoming challenge dialog (reuse pattern from dice challenge)
- Both players select their Roomian → battle screen opens on both devices
- Turn actions sent via `MpMessage` (new message types)
- Battle state synced via snapshot system

### 8.2 New MP Message Types

```
MpRoomianChallenge    — "Player A wants to battle Roomians!"
MpRoomianAccept       — Accept challenge
MpRoomianDecline      — Decline challenge
MpRoomianAction       — {action: attack/defend/swap/flee, abilityId, target}
MpRoomianState        — Full battle state sync (HP, status, positions)
MpRoomianResult       — Battle outcome + XP/scars/death
```

### 8.3 Spectator Mode (Future)

Other connected players can watch active battles via the MP snapshot stream.

---

## 9. Evolution System

### 9.1 Evolution Tiers

| Tier | Level | Changes |
|------|-------|---------|
| **Base** (Blob) | 0–4 | Template form, 1 ability |
| **Tier 1** | 5+ | New appearance, +1 ability slot, stat boost, category emerges |
| **Tier 2** | 10+ | New appearance, +1 ability slot, category deepens |
| **Tier 3** | 15+ | Final form, 3 ability slots, signature ability unlocked |

### 9.2 Evolution Cost

- Requires XP threshold + **Evolution Material** (from Deep Dive quests or battle rewards)
- Player chooses when to evolve (not automatic)
- **Risk:** Evolving resets scar count to 0 BUT also resets all stat training bonuses
- **Strategic tension:** Evolve early for power, or stay low-level to preserve training investment

---

## 10. Categories (Placeholder — To Be Defined)

The user will define Roomian categories later. The system is designed to support:

- **Type effectiveness chart** (like Pokemon's 18-type matrix, but smaller — maybe 6-8 Gungeon-themed categories)
- **Category-based abilities** (each category has signature moves)
- **STAB bonus** (1.5x when ability category matches Roomian category)
- **Dual-category Roomians** (possible at Tier 2+)

**Potential Gungeon-themed categories (brainstorm seed):**
- 🔥 Ember (fire, burn, AoE)
- ❄️ Frost (ice, chill, control)
- ☠️ Toxic (poison, DoT, debuff)
- ⚡ Spark (electric, speed, crit)
- 💀 Necrotic (death, sacrifice, high-risk)
- 🛡️ Steel (defense, tank, counter)
- ✦ Prismatic (rainbow, versatile, wild card)

---

## 11. UI/UX Vision

### 11.1 Roomian Belt Screen

Accessible from the Active Run screen (new tab or icon in header):
- Shows up to 3 Roomian slots (one per Room Ball)
- Each slot: Roomian sprite, level, HP bar, status icons, scar count
- Tap a Roomian → detail view (stats, abilities, scars, quest/train buttons)
- Empty slots show "No Roomian — find a Room Ball!"

### 11.2 Battle Screen

- Split-screen: your Roomian (left) vs opponent (right)
- HP bars at top, action menu at bottom
- Animated attacks (reuse particle system from `dice_roll.dart`)
- Death save sequence: full-screen d20 roll animation (reuse `DiceWidget`)
- Result screen: XP gained, scars received, items found

### 11.3 Aesthetic

- Roomian sprites: pixel-art blobs with category-colored auras
- Battle background: Gungeon chamber aesthetic (dark stone, torches)
- HP bars: Gungeon loot-tier colors (green → amber → pink → purple → cyan)
- Death save: red vignette, dramatic lighting, dice roll with screen shake

---

## 12. Technical Architecture (Preliminary)

### 12.1 New Files

```
lib/models/roomian.dart              — Roomian data model + JSON ser/de
lib/models/roomian_battle.dart       — Battle state, action queue, damage calc
lib/models/roomian_scar.dart         — Scar definitions + effects
lib/providers/roomian_provider.dart  — Belt management, XP, cooldowns, persistence
lib/screens/roomian_belt_screen.dart  — Belt overview UI
lib/screens/roomian_battle_screen.dart — Battle UI (turn-based)
lib/screens/roomian_detail_screen.dart — Single Roomian stats/abilities/scars
lib/widgets/roomian_sprite.dart      — Animated pixel-art creature display
lib/widgets/roomian_hp_bar.dart      — Tier-colored HP bar
```

### 12.2 Reusable Existing Systems

| System | Reuse |
|--------|-------|
| `dice_roll.dart` | D20 animation for death saves |
| `MultiplayerSession` | Battle challenge/response messaging |
| `Haptics` | Battle impact, death save tension |
| `AppTheme` | Battle UI theming |
| `particle_engine.dart` | Attack VFX |
| `SharedPreferences` | Roomian persistence |
| `RunProvider` | Integration with active run (Room Ball as active item) |

### 12.3 Data Files

```
assets/data/roomians_base.json    — Base species definitions (Blob template)
assets/data/roomian_abilities.json — Ability definitions (power, type, effects)
assets/data/roomian_quests.json    — Quest definitions
assets/data/roomian_evolution.json — Evolution paths + requirements
```

---

## 13. Implementation Phases (High-Level)

### Phase 1: Foundation (MVP)
- Roomian data model + persistence
- Room Ball active item (summons RNG Blob)
- Roomian Belt screen (view only)
- Basic 1v1 battle (local, both players on same device — hot-seat)
- Death save with d20 animation
- Scar system
- Basic XP/leveling

### Phase 2: Multiplayer Battles
- MP battle challenge/accept/decline
- Synchronized battle state via MP messages
- Battle result + XP/scar sync

### Phase 3: Quests & Training
- Quest system (send Roomian, wait, get results)
- Training system
- Cooldown tracking
- Deep Dive death save on return

### Phase 4: Categories & Evolution
- Define category type chart
- Category-based abilities
- Evolution system
- Tier-based sprites

### Phase 5: Polish & Depth
- Spectator mode
- Roomian trading between players
- Rare/shiny Roomians
- Seasonal events
- Leaderboards

---

## 14. Key Design Decisions & Rationale

| Decision | Rationale |
|----------|-----------|
| 5 stats not 6 | Companion app context — simpler team building |
| 1 success to survive (not 3) | Faster resolution, higher tension per roll |
| Scars on survival | Makes "surviving" still feel costly — not a free pass |
| Lobotomize at 25% | Strong enough to matter, not so high it's unusable |
| 3 Room Balls per run | Forces strategic choices, prevents spamming |
| Roomians persist across runs | They're companions, not consumables — emotional investment |
| Evolution resets training | Creates strategic tension: power vs investment |
| Fleeing has risk | No free escape — commitment to battle matters |
| Quests have death save risk (Deep Dive) | High risk high reward for endgame content |

---

## 15. Open Questions (To Resolve Later)

1. **Categories:** What are the final type names and effectiveness chart?
2. **Room Ball acquisition:** Chests only? Shop? Shrine? All three?
3. **Belt size:** Fixed at 3 (one per Ball) or expandable?
4. **Trading:** Can players trade Roomians via MP?
5. **Shiny/rare Roomians:** RNG variant with stat boost?
6. **Roomian death penalty:** Should losing a Roomian also curse the player?
7. **Balance:** How do we prevent veteran players from stomping new players?
8. **Art assets:** Who draws the Roomian sprites? Procedural color tinting for now?
9. **Story integration:** Are Roomians canon to Enter the Gungeon lore, or a meta-game layer?
10. **Single-player battles:** Can you battle wild Roomians (AI-controlled) or only other players?

---

*This document is a living blueprint. Categories, abilities, and balance numbers are placeholders until the user defines them.*
