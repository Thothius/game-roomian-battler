# Roomian Battle System — Visual Pictation & Full Game Design

> **Status:** Comprehensive Design Document with Visual Mockups  
> **Date:** Jul 25, 2026  
> **Scope:** Full game system — stats, evolution tree (36 forms), all screen layouts, battle mechanics, skills

---

## GRAND FRAMEWORK — The Roomian Game Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                    ROOMIAN GAME LOOP                            │
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│  │  EXPLORE │───→│  CATCH   │───→│  TRAIN   │───→│  BATTLE  │ │
│  │  world   │    │  throw   │    │  level   │    │  PvP/PvE │ │
│  │  find    │    │  ball    │    │  evolve  │    │  3v3     │ │
│  │  wild    │    │  75%     │    │  choose  │    │  fight   │ │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│       ↑               │               │               │        │
│       │          ┌───────┐       ┌───────┐      ┌───────┐     │
│       │          │ STORAGE│      │ SCARS │      │ XP +  │     │
│       │          │ grow   │      │ perman│      │ loot  │     │
│       │          │ team   │      │ ent   │      │       │     │
│       │          └───────┘       └───────┘      └───────┘     │
│       └─────────────────────────────────────────────┘         │
│                                                                 │
│  CORE RESOURCES:  HP (survival)  EN (all abilities)            │
│  CORE STATS:      VIT PWR GRT SPD LCK INT                      │
│  PROGRESSION:     L0 Blob → L1 Element → L5 Refine → L8 Master │
│  RISK:            Death saves (reset/battle) → Scars (perm)    │
│  ECONOMY:         Room Balls, Ability Scrolls, Gold            │
│  SOCIAL:          PvP battles, Scroll-for-scroll trading       │
└─────────────────────────────────────────────────────────────────┘
```

### Design Pillars

1. **Simple to learn, deep to master** — 6 stats, 2 resources, 4 action types. But 36 evolution paths, ability stacking, and synergy combos create endless team-building depth.
2. **Every choice is permanent** — Evolution branching, stat allocation, and scars are all permanent. No respecs. Your Roomian is uniquely yours.
3. **Risk vs reward at every layer** — Death saves reset per battle, but scars are forever. Fleeing is punished. Catching is a 75% gamble. Deep Dive quests offer the best loot but guaranteed boss battles.
4. **No consumable clutter** — No potions, no items in battle. Just your Roomians and their abilities. The only consumables are Room Balls (for catching) and Ability Scrolls (for learning).
5. **Social but not dependent** — PvP is the primary endgame, but scroll-for-scroll trading is the only player-to-player economy. No pay-to-win, no marketplace.

---

## TABLE OF CONTENTS

1. Stat System (6 stats + 2 battle resources: HP, Energy)
2. Evolution System (6×3×2 = 36 final forms)
3. Screen Mockups
   - 3A. Versus Splash / Battle Intro
   - 3B. Battle Screen (3v3)
   - 3C. Roomian Inventory / Belt Screen
   - 3D. Roomian Detail / Actions Screen
   - 3E. Evolution Choice Screen
   - 3F. Skill Learning Screen
   - 3G. Death Save Screen
4. Skill / Ability System
5. Battle Mechanics (3v3 Team)
6. XP & Leveling Curve
7. Room Ball Catch System
8. Status Effects System
9. Scar System
10. Wild AI & Battle Formats
11. Quest & Training System
12. Roomian Data Model
13. Summary of Additions

---

## 1. STAT SYSTEM (Updated)

### 1.1 Core Stats — 6 Attributes

| Stat | Abbr | Description | Battle Effect |
|------|------|-------------|---------------|
| **Vitality** | VIT | Health pool | VIT × 2 + 10 + Level × 3 = Max HP |
| **Power** | PWR | Physical attack | Scales physical ability damage |
| **Grit** | GRT | Defense + energy | Reduces incoming damage; (GRT + INT) × 2 + 15 + Lvl × 3 = Max Energy |
| **Speed** | SPD | Initiative + dodge | Determines round action order; SPD × 0.5% = dodge chance |
| **Luck** | LCK | Crit + item find | LCK × 1% = crit chance; affects quest rewards |
| **Intelligence** | INT | Energy + learning | Contributes to Max Energy; affects ability learn speed |

### 1.1b Battle Resources (Derived from Stats)

| Resource | Abbr | Color | Derived From | Regen/turn | Used For |
|----------|------|-------|-------------|------------|----------|
| **Health** | HP | Red | VIT × 2 + 10 + Lvl × 3 | 0 (abilities only) | Survival — 0 = downed |
| **Energy** | EN | Cyan | (GRT + INT) × 2 + 15 + Lvl × 3 | 3 + floor((GRT + INT) / 5) | All abilities (attacks, magic, defend, flee) |

### 1.2 Derived Values

```
Max HP     = VIT × 2 + 10 + Level × 3
Max Energy = (GRT + INT) × 2 + 15 + Level × 3
HP Regen   = 0 (only via abilities)
EN Regen   = 3 + floor((GRT + INT) / 5) per turn
Dodge   = floor(SPD × 0.5)%  (cap 30%)
Crit    = LCK × 1%  (cap 25%)
Carry   = 3 (max Roomians in active team)
```

### 1.3 Blob Baseline (Level 0)

```
VIT: 5    PWR: 5    GRT: 5    SPD: 5    LCK: 5    INT: 5
Max HP: 20         Max Energy: 37
Abilities: [Tackle] (PWR-based, 3 EN)
                  [Pulse]   (INT-based, 3 EN — weak magic)
```

### 1.4 Level-Up Stat Growth

On each level-up, the player gets **+2 to one stat** (chosen from 3 random options presented). This means stat growth is partially player-directed, creating build variety even within the same evolution path.

```
Level Up → Present 3 random stat options:
  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │   +2     │  │   +2     │  │   +2     │
  │   PWR    │  │   INT    │  │   LCK    │
  └──────────┘  └──────────┘  └──────────┘
       Pick one → stat increases permanently
```

At evolution levels (1, 5, 8), the evolution choice ALSO grants stat bonuses — see Section 2.

---

## 2. EVOLUTION SYSTEM

### 2.1 Evolution Overview

```
Level 0          Level 1              Level 5                  Level 8              Level 10
  │                │                    │                       │                     │
  ▼                ▼                    ▼                       ▼                     ▼
 BLOB     →   6 PRIMAL ELEMENTS →  18 ELEMENT REFINEMENTS →  36 MASTERY FORMS  →   PRESTIGE
(1 form)      (6 forms)           (18 forms)               (36 forms)              (cosmetic)
```

**Evolution Levels:** 1, 5, 8  
**Max Level:** 10  
**Total Unique Final Forms:** 36

### 2.2 Level 1 — Six Primal Elements

At Level 1, the Blob chooses its primal element. This determines its color, aura, and base ability set.

```
                            ┌─── 🔥 FIRE
                            │    Red-orange aura
                            │    +3 PWR, +1 VIT
                            │    Active: Ember Strike | Passive: Burn Touch
                            │
                            ├─── 💧 WATER
                            │    Blue aura
                            │    +3 GRT, +1 INT
                            │    Active: Water Jet | Passive: Flow State
                            │
              ┌─── 🌍 EARTH
              │    Brown-green aura
              │    +3 GRT, +1 VIT
              │    Active: Stone Throw | Passive: Stone Skin
              │
  LEVEL 0 ────┼─── 💨 AIR
  BLOB        │    White-grey aura
  (neutral)   │    +3 SPD, +1 LCK
              │    Active: Gust | Passive: Wind Step
              │
              ├─── ☀️ LIGHT
              │    Golden aura
              │    +3 INT, +1 LCK
              │    Active: Flash Beam | Passive: Radiance
              │
              └─── 🌙 DARK
                   Purple aura
                   +3 PWR, +1 INT
                   Active: Shadow Claw | Passive: Night Veil
```

### 2.3 Level 5 — Element Refinement (3 Options Per Element)

At Level 5, each primal element branches into 3 refined elements. These are elemental refinements that build on the base element's identity, not generic roles.

```
  FIRE ───────────┬── 🔥 BLAZE ──────── +4 PWR, +2 SPD
  (L1)            │   "Emberblade"        Pure fire DPS, burn stacking
                   │   Active: Flame Slash, Inferno Strike
                   │
                   ├── 🌋 MAGMA ──────── +4 GRT, +2 VIT
                   │   "Magma Wall"       Lava tank, eruption counter
                   │   Active: Molten Shell, Eruption
                   │
                   └── 💨 SMOKE ──────── +4 INT, +2 EN regen
                       "Smoke Veil"         Smoke clouds, blind + burn DoT
                       Active: Smoke Veil, Ash Storm


  WATER ──────────┬── ❄️ FROST ──────── +4 PWR, +2 LCK
  (L1)            │   "Frostfang"          Ice DPS, freeze + crit
                   │   Active: Ice Shard, Glacial Pierce
                   │
                   ├── 🌊 TIDE ──────── +4 GRT, +2 VIT
                   │   "Tidewall"           Water tank, flow + absorb
                   │   Active: Tidal Shield, Whirlpool
                   │
                   └── 🧊 GLACIER ────── +4 INT, +2 EN regen
                       "Frostweaver"         Ice mage, freeze + slow control
                       Active: Blizzard, Deep Freeze


  EARTH ──────────┬── ⚙️ STEEL ──────── +4 GRT, +2 VIT
  (L1)            │   "Ironclad"           Metal tank, armor + reflect
                   │   Active: Steel Wall, Blade Storm
                   │
                   ├── 🪨 STONE ──────── +4 PWR, +2 GRT
                   │   "Bulwark"            Stone bruiser, quake + stun
                   │   Active: Rock Slide, Earthquake
                   │
                   └── 💎 CRYSTAL ────── +4 INT, +2 EN regen
                       "Prismancer"          Crystal mage, refract + amplify
                       Active: Prism Beam, Refraction


  AIR ────────────┬── ⚡ ELECTRICITY ── +4 PWR, +2 SPD
  (L1)            │   "Voltfang"           Lightning DPS, chain + stun
                   │   Active: Spark Chain, Thunderbolt
                   │
                   ├── 🌪️ STORM ──────── +4 INT, +2 EN regen
                   │   "Stormcaller"        Wind + lightning AoE, paralyze
                   │   Active: Thunderstorm, Cyclone
                   │
                   └── 🌬️ GALE ──────── +4 SPD, +2 LCK
                       "Windblade"           Speed demon, dodge + multi-hit
                       Active: Gale Slash, Tempest


  LIGHT ──────────┬── ☀️ SOLAR ──────── +4 PWR, +2 VIT
  (L1)            │   "Dawnbreaker"        Holy DPS, smite + cleanse
                   │   Active: Solar Lance, Radiant Strike
                   │
                   ├── ✨ PRISM ──────── +4 INT, +2 EN regen
                   │   "Prismweaver"        Rainbow mage, random element spells
                   │   Active: Prismatic Spray, Spectrum
                   │
                   └── 🌟 LUNAR ──────── +4 SPD, +2 LCK
                       "Moonlit"             Moon crits, sleep + dream
                       Active: Moonlit Shard, Lunar Veil


  DARK ───────────┬── 💀 DEATH ──────── +4 PWR, +2 INT
  (L1)            │   "Reaper"             Execute mechanic, lifesteal
                   │   Active: Reaper's Claw, Soul Drain
                   │
                   ├── 🌑 SHADOW ──────── +4 SPD, +2 LCK
                   │   "Nightblade"         Stealth + dodge, shadow strike
                   │   Active: Shadow Step, Eclipse
                   │
                   └── 🔮 VOID ──────── +4 INT, +2 EN regen
                       "Voidcaller"          Void mage, drain + banish
                       Active: Void Bolt, Annihilation
```

### 2.4 Level 8 — Mastery Grade (2 Options Per Refinement)

At Level 8, each of the 18 refined elements reaches its **mastery grade** — a final binary choice between two mastery paths. Each mastery has a unique name, passive, and aesthetic.

**Mastery naming convention:** [Refinement] + [Mastery title] — e.g., "Blaze, the Inferno" vs "Blaze, the Phoenix"

**L8 Stat Bonus Pattern:** Every mastery grants **+5 to primary stat + +2 to secondary stat**, matching the refinement's combat identity:

| Refinement Type | Primary (+5) | Secondary (+2) | Example Masteries |
|-----------------|-------------|----------------|-------------------|
| DPS (Blaze, Frost, Stone, Electricity, Solar, Death) | PWR | SPD | Inferno, Phoenix, Diamond Edge, Aurora |
| Tank (Magma, Tide, Steel, Storm, Lunar, Shadow) | GRT | VIT | Caldera, Obsidian, Maelstrom, Permafrost |
| Mage (Smoke, Glacier, Crystal, Gale, Prism, Void) | INT | LCK | Ashen Veil, Wildfire, Tundra, Hypothermia |

**Note:** Some masteries break pattern for thematic reasons (e.g., Phoenix gets +5 VIT +2 SPD for survivability since it's a revive tank, Galvanic gets +5 INT +2 PWR for the overcharge mage-playstyle). The table above is the default — individual entries below show exact stats.

```
═══════════════════════════════════════════════════════════════════════════════
 FIRE → BLAZE (Emberblade)
═══════════════════════════════════════════════════════════════════════════════
  ┌── 🔥 INFERNAL MASTER → "Inferno"
  │   Ultimate burn: DoT ticks twice, +50% burn damage.
  │   Passive: "Eternal Flame" — burn cannot be cleansed
  │   Color: Deep crimson with black smoke aura
  │
  └── 🔥 PHOENIX MASTER → "Phoenix"
      Rebirth: on death, revive once at 30% HP with full burn aura.
      Passive: "Rebirth Flame" — first KO auto-revives at 30% HP
      Color: Bright orange-red with feathered fire wings

═══════════════════════════════════════════════════════════════════════════════
 FIRE → MAGMA (Magma Wall)
═══════════════════════════════════════════════════════════════════════════════
  ┌── 🌋 CALDERA MASTER → "Caldera"
  │   Eruption tank: 15 damage to all enemies when hit.
  │   Passive: "Magma Core" — +2 GRT per turn at <50% HP
  │   Color: Lava red with glowing cracks
  │
  └── 🌋 OBSIDIAN MASTER → "Obsidian"
      Volcanic glass armor: absorbs 3 hits, reflects 50% as burn.
      Passive: "Glass Armor" — 3-hit shield, reflect 50% as burn
      Color: Black volcanic glass with orange veins

═══════════════════════════════════════════════════════════════════════════════
 FIRE → SMOKE (Smoke Veil)
═══════════════════════════════════════════════════════════════════════════════
  ┌── 💨 ASHEN MASTER → "Ashen Veil"
  │   Total blind: 40% miss chance to all enemies for 2 turns.
  │   Passive: "Choking Cloud" — enemies lose 2 EN/turn
  │   Color: Grey-black smoke with ember motes
  │
  └── 💨 PYRE MASTER → "Wildfire"
      Spreading flames: burn jumps to adjacent enemies.
      Passive: "Contagion Burn" — burn spreads to adjacent enemy each turn
      Color: Orange-grey with spreading fire tendrils

═══════════════════════════════════════════════════════════════════════════════
 WATER → FROST (Frostfang)
═══════════════════════════════════════════════════════════════════════════════
  ┌── ❄️ DIAMOND MASTER → "Diamond Edge"
  │   Shatter: 3x damage vs frozen targets, unfreezes after.
  │   Passive: "Brittle Edge" — frozen targets take +50% damage from all sources
  │   Color: Brilliant white with crystal facets
  │
  └── ❄️ AURORA MASTER → "Aurora"
      Light-infused ice: confuse + dazzle on freeze.
      Passive: "Aurora Borealis" — freeze also confuses for 1 turn
      Color: Green-purple shimmer with ice crystals

═══════════════════════════════════════════════════════════════════════════════
 WATER → TIDE (Tidewall)
═══════════════════════════════════════════════════════════════════════════════
  ┌── 🌊 MAELSTROM MASTER → "Maelstrom"
  │   Whirlpool: pulls all enemies, deals 8 damage + slow.
  │   Passive: "Riptide" — enemies hit lose 2 SPD for 2 turns
  │   Color: Deep blue with swirling vortex
  │
  └── 🌊 FROSTBITE MASTER → "Permafrost"
      Frozen armor: absorbs 3 hits, reflects ice damage, freezes on contact.
      Passive: "Eternal Winter" — GRT +50% for 3 turns, freeze on contact
      Color: Steel-blue with frost coating

═══════════════════════════════════════════════════════════════════════════════
 WATER → GLACIER (Frostweaver)
═══════════════════════════════════════════════════════════════════════════════
  ┌── 🧊 TUNDRA MASTER → "Tundra"
  │   Battlefield freeze: all enemies -2 SPD, 30% freeze chance.
  │   Passive: "Deep Freeze" — frozen enemies skip their turn
  │   Color: Deep ocean blue with white peaks
  │
  └── 🧊 HYPOTHERMIA MASTER → "Hypothermia"
      Sleep + decay: sleep target, stats decay while asleep.
      Passive: "Deep Slumber" — sleep 2 turns + -1 all stats/turn
      Color: Dark indigo with starry void

═══════════════════════════════════════════════════════════════════════════════
 EARTH → STEEL (Ironclad)
═══════════════════════════════════════════════════════════════════════════════
  ┌── ⚙️ FORGE MASTER → "Forgeguard"
  │   Heat-tempered: GRT scales with HP lost, +2 GRT/turn below 50% HP.
  │   Passive: "Forged in Battle" — +2 GRT per turn at <50% HP
  │   Color: Molten orange with metallic sheen
  │
  └── ⚙️ BULWARK MASTER → "Aegis"
      Immovable: immune to knockback, stun immunity, +50% GRT.
      Passive: "Unbreakable" — immune to stun and knockback, +50% GRT
      Color: Polished silver with golden engravings

═══════════════════════════════════════════════════════════════════════════════
 EARTH → STONE (Bulwark)
═══════════════════════════════════════════════════════════════════════════════
  ┌── 🪨 AVALANCHE MASTER → "Avalanche"
  │   Crash + stun: 20% stun chance on hit, 18 damage AoE slam.
  │   Passive: "Tremor" — all attacks have 20% stun chance
  │   Color: White-grey with rock fragments
  │
  └── 🪨 TITAN MASTER → "Titan"
      Colossal: +50% max HP, but -2 SPD. Unstoppable force.
      Passive: "Colossal Form" — +50% max HP, -2 SPD, immune to push
      Color: Dark stone with glowing green veins

═══════════════════════════════════════════════════════════════════════════════
 EARTH → CRYSTAL (Prismancer)
═══════════════════════════════════════════════════════════════════════════════
  ┌── 💎 REFRACT MASTER → "Refractor"
  │   Beam split: single-target spells hit 2 enemies.
  │   Passive: "Prism Split" — single-target spells auto-target 2nd enemy at 50%
  │   Color: Rainbow crystal with light refractions
  │
  └── 💎 GEODE MASTER → "Geode"
      Crystal growth: +1 INT per turn (cap +5), spells grow stronger over time.
      Passive: "Growing Crystal" — +1 INT/turn (cap +5) in battle
      Color: Purple amethyst with inner glow

═══════════════════════════════════════════════════════════════════════════════
 AIR → ELECTRICITY (Voltfang)
═══════════════════════════════════════════════════════════════════════════════
  ┌── ⚡ TEMPEST MASTER → "Tempest"
  │   Triple strike: 25% chance to hit 3 times, +2 SPD per consecutive hit.
  │   Passive: "Storm Rush" — +2 SPD per consecutive hit (cap +6)
  │   Color: Bright yellow with white wind streaks
  │
  └── ⚡ GALVANIC MASTER → "Galvanic"
      Overcharge: abilities cost 50% EN, but 10% self-damage per cast.
  │   Passive: "Overcharge" — abilities cost 50% EN, 10% max HP as recoil
      Color: Electric blue with crackling arcs

═══════════════════════════════════════════════════════════════════════════════
 AIR → STORM (Stormcaller)
═══════════════════════════════════════════════════════════════════════════════
  ┌── 🌪️ HURRICANE MASTER → "Hurricane"
  │   Wind zone: all enemies -2 SPD, 15% dodge for all allies.
  │   Passive: "Eye of the Storm" — team gains +15% dodge, enemies -2 SPD
  │   Color: Swirling grey-white with lightning arcs
  │
  └── 🌪️ THUNDER MASTER → "Thunderlord"
      Chain lightning: spells jump to 3 targets, each jump -25% damage.
  │   Passive: "Chain Lightning" — all electric spells chain to 3 targets
      Color: Dark storm cloud with constant crackling

═══════════════════════════════════════════════════════════════════════════════
 AIR → GALE (Windblade)
═══════════════════════════════════════════════════════════════════════════════
  ┌── 🌬️ CYCLONE MASTER → "Cyclone"
  │   Multi-hit: 3 hits per attack at 60% damage each (180% total).
  │   Passive: "Whirling Blades" — all attacks hit 3x at 60% damage
  │   Color: White-green with visible wind blades
  │
  └── 🌬️ ZEPHYR MASTER → "Zephyr"
      Untouchable: +20% dodge, +3 SPD, counterattack on dodge.
  │   Passive: "Wind Step" — +20% dodge, counterattack for 50% damage on dodge
      Color: Pale white with trailing wind streams

═══════════════════════════════════════════════════════════════════════════════
 LIGHT → SOLAR (Dawnbreaker)
═══════════════════════════════════════════════════════════════════════════════
  ┌── ☀️ RADIANT MASTER → "Radiant Lance"
  │   Holy smite: +50% PWR for 3 turns, cleanse all allies on entry.
  │   Passive: "Solar Blessing" — +50% PWR for 3 turns, team cleanse
  │   Color: Golden-white with sunburst aura
  │
  └── ☀️ DAWN MASTER → "Dawnbringer"
      Illumination: reveals all enemy HP/EN, +25% crit to all allies.
  │   Passive: "Light of Truth" — enemy stats always visible, team +25% crit
      Color: Warm gold with dawn light rays

═══════════════════════════════════════════════════════════════════════════════
 LIGHT → PRISM (Prismweaver)
═══════════════════════════════════════════════════════════════════════════════
  ┌── ✨ SPECTRUM MASTER → "Spectrum"
  │   Full spectrum: spells cycle through all 6 elements randomly.
  │   Passive: "Prismatic Surge" — each cast uses a random element, 20-35 dmg
  │   Color: Rainbow shimmer with constant color shifting
  │
  └── ✨ LUMEN MASTER → "Lumen"
      Light amplifier: +30% damage to all Light abilities, blinds on crit.
  │   Passive: "Brilliance" — +30% Light damage, crits blind for 1 turn
      Color: Pure white with golden sparkles

═══════════════════════════════════════════════════════════════════════════════
 LIGHT → LUNAR (Moonlit)
═══════════════════════════════════════════════════════════════════════════════
  ┌── 🌙 ECLIPSE MASTER → "Eclipse"
  │   Dark-light fusion: 2x crit damage, ignores GRT entirely.
  │   Passive: "Moonlit Edge" — 2x crit damage, ignores enemy GRT
  │   Color: Pale silver-blue with moon glow
  │
  └── 🌙 DREAM MASTER → "Dreamweaver"
      Sleep + dream: sleep target, deal 4 damage/turn while asleep.
  │   Passive: "Dream Catcher" — sleep 2 turns, 4 damage/turn, stats decay
      Color: Lavender with starry night sky

═══════════════════════════════════════════════════════════════════════════════
 DARK → DEATH (Reaper)
═══════════════════════════════════════════════════════════════════════════════
  ┌── 💀 EXECUTIONER MASTER → "Executioner"
  │   Kill threshold: +50% damage to targets below 30% HP.
  │   Passive: "Reaper's Mark" — +50% dmg to <30% HP targets, kills refund 3 EN
  │   Color: Deep crimson-black with skeletal aura
  │
  └── 💀 LICH MASTER → "Lich"
      Undeath: on KO, revive at 1 HP (once per battle), gain 20 shield.
  │   Passive: "Undeath" — first KO revives at 1 HP + 20 shield
      Color: Bone white with green necrotic flames

═══════════════════════════════════════════════════════════════════════════════
 DARK → SHADOW (Nightblade)
═══════════════════════════════════════════════════════════════════════════════
  ┌── 🌑 UMBRA MASTER → "Umbral"
  │   Perfect stealth: first attack each round auto-crits.
  │   Passive: "Shadow Strike" — first attack each round is guaranteed crit
  │   Color: Pure black with purple outline
  │
  └── 🌑 PHANTOM MASTER → "Phantom"
      Phase: 25% chance to phase through any attack (take 0 damage).
  │   Passive: "Phase Shift" — 25% chance to negate any incoming attack
      Color: Dark purple with ghostly afterimages

═══════════════════════════════════════════════════════════════════════════════
 DARK → VOID (Voidcaller)
═══════════════════════════════════════════════════════════════════════════════
  ┌── 🔮 ABYSS MASTER → "Abyssal"
  │   Gravity well: pull all enemies, 10 damage, -2 SPD for 2 turns.
  │   Passive: "Event Horizon" — pull all enemies + 10 dmg + slow on entry
  │   Color: Swirling black-purple with distorted light
  │
  └── 🔮 ENTROPY MASTER → "Entropy"
      Heat death: each turn, all enemies lose 1 HP and 1 EN permanently.
  │   Passive: "Heat Death" — enemies lose 1 HP + 1 EN per turn (permanent)
      Color: Dark red-black with fading star motes
```

### 2.5 Full Evolution Tree (Visual)

```
                                          BLOB (L0)
                                               │
                    ┌──────────┬──────────┬─────┴────┬──────────┬──────────┐
                    ▼          ▼          ▼          ▼          ▼          ▼
                 🔥 FIRE    💧 WATER   🌍 EARTH    💨 AIR     ☀️ LIGHT   🌙 DARK
                   (L1)       (L1)       (L1)       (L1)       (L1)       (L1)
                    │          │          │          │          │          │
              ┌─────┼────┐ ┌───┼───┐ ┌───┼───┐ ┌───┼───┐ ┌───┼───┐ ┌───┼───┐
              ▼     ▼    ▼ ▼   ▼   ▼ ▼   ▼   ▼ ▼   ▼   ▼ ▼   ▼   ▼ ▼   ▼   ▼
            Blaze Magma Smoke Frost Tide Glcr Steel Stone Crst Elec Storm Gale Solar Prsm Lunar Death Shdw Void
             (L5)  (L5)  (L5) (L5) (L5) (L5) (L5) (L5) (L5) (L5) (L5) (L5) (L5) (L5) (L5) (L5) (L5) (L5)
              │     │     │    │    │    │    │    │    │    │    │    │    │    │    │    │    │    │
            ┌─┘   ┌─┘   ┌─┘  ┌─┘  ┌─┘  ┌─┘  ┌─┘  ┌─┘  ┌─┘  ┌─┘  ┌─┘  ┌─┘  ┌─┘  ┌─┘  ┌─┘  ┌─┘  ┌─┘  ┌─┘
            A B   A B   A B  A B  A B  A B  A B  A B  A B  A B  A B  A B  A B  A B  A B  A B  A B  A B
           (L8) (L8) (L8) (L8) (L8) (L8) (L8) (L8) (L8) (L8) (L8) (L8) (L8) (L8) (L8) (L8) (L8) (L8)

  A = Mastery Option A    B = Mastery Option B
  
  6 L1 elements × 3 L5 refinements × 2 L8 masteries = 36 unique final forms
```

### 2.6 Evolution Choice Mechanics

**L1 — 6 cards (pick 1 of 6):**

```
  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
  │ 🔥 FIRE│ │💧 WATER│ │🌍 EARTH│ │ 💨 AIR │ │☀️ LIGHT│ │ 🌙 DARK│
  │        │ │        │ │        │ │        │ │        │ │        │
  │[sprite]│ │[sprite]│ │[sprite]│ │[sprite]│ │[sprite]│ │[sprite]│
  │ +3 PWR │ │ +3 GRT │ │ +3 GRT │ │ +3 SPD │ │ +3 INT │ │ +3 PWR │
  │ +1 VIT │ │ +1 INT │ │ +1 VIT │ │ +1 LCK │ │ +1 LCK │ │ +1 INT │
  │        │ │        │ │        │ │        │ │        │ │        │
  │⚔️ Ember │ │⚔️ Water │ │⚔️ Stone │ │⚔️ Gust │ │⚔️ Flash│ │⚔️ Shdw │
  │  Strike│ │   Jet  │ │  Throw │ │        │ │  Beam  │ │  Claw  │
  │🔄 Burn │ │🔄 Flow │ │🔄 Stone│ │🔄 Wind │ │🔄 Radi│ │🔄 Night│
  │  Touch │ │  State │ │  Skin  │ │  Step  │ │  ance  │ │  Veil  │
  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘
                    TAP TO CHOOSE →
```

**Card shows:** Stats AND the active + passive abilities you'll receive. Player sees exactly what they're committing to.

**L5 — 3 cards (pick 1 of 3, based on L1 element):**

```
  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
  │ 🔥 BLAZE   │  │ 🌋 MAGMA    │  │ 💨 SMOKE    │
  │             │  │             │  │             │
  │  [sprite]   │  │  [sprite]   │  │  [sprite]   │
  │ "Emberblade"│  │ "Magma Wall"│  │"Smoke Veil"│
  │ +4 PWR      │  │ +4 GRT      │  │ +4 INT      │
  │ +2 SPD      │  │ +2 VIT      │  │ +2 EN regen │
  │             │  │             │  │             │
  │⚔️ Flame Slsh│  │⚔️ Molten Shl│  │⚔️ Smoke Veil│
  │  + Inferno  │  │  + Eruption │  │  + Ash Strm │
  │ Burn DPS    │  │ Lava tank   │  │ Smoke mage  │
  └─────────────┘  └─────────────┘  └─────────────┘
       TAP TO CHOOSE →
```

**Card shows:** Stats, role identity, AND the two active abilities you'll receive.

**L8 — 2 cards (pick 1 of 2, based on L5 refinement):**

```
  ┌──────────────────┐  ┌──────────────────┐
  │ 🔥 INFERNAL      │  │ 🔥 PHOENIX       │
  │   MASTER         │  │   MASTER         │
  │                  │  │                  │
  │   [sprite]       │  │   [sprite]       │
  │  "Inferno"       │  │  "Phoenix"       │
  │                  │  │                  │
  │  +5 PWR          │  │  +5 VIT          │
  │  +2 INT          │  │  +2 SPD          │
  │                  │  │                  │
  │  DoT ticks twice │  │  Revive once    │
  │  Burn uncleanse- │  │  at 30% HP      │
  │  able            │  │  with fire aura  │
  └──────────────────┘  └──────────────────┘
         TAP TO CHOOSE →
```

**Key design rules:**
- Each path is **visually distinct** (different sprite, color, aura effect)
- L1: 6 primal elements, each with distinct stat bonuses and base abilities
- L5: 3 refinements per element (18 total) — element gets a specific identity (DPS, tank, mage)
- L8: 2 mastery options per refinement (36 total) — binary choice for ultimate form
- Evolution abilities are **fixed** — determined by path, cannot be swapped
- Previous path choices are **shown in the card** (e.g., "From Fire → Blaze → Inferno")
- Evolution is **permanent** — no re-spec (makes the choice weighty)
- L10 Prestige is **cosmetic only** — golden aura, prestige badge

---

## 3. SCREEN MOCKUPS

### 3A. VERSUS SPLASH / BATTLE INTRO SCREEN

This screen plays when a battle challenge is accepted. Shows both players' teams before the fight begins.

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  ╔═══════════════════════════════════════════════════╗  │
│  ║                                                   ║  │
│  ║   PLAYER A                          PLAYER B      ║  │
│  ║   "SAARE"                          "GUNGEONEER"   ║  │
│  ║                                                   ║  │
│  ║   ┌─────┐  ┌─────┐  ┌─────┐    ┌─────┐ ┌─────┐ ┌─────┐║
│  ║   │ 🔥  │  │ ❄️  │  │ ☠️  │    │ ⚔️  │ │ 🛡️  │ │ ✨  │║
│  ║   │ L7  │  │ L5  │  │ L3  │    │ L8  │ │ L6  │ │ L4  │║
│  ║   │████ │  │████ │  │██   │    │█████│ │████ │ │██   │║
│  ║   │████ │  │██   │  │     │    │█████│ │████ │ │██   │║
│  ║   └─────┘  └─────┘  └─────┘    └─────┘ └─────┘ └─────┘║
│  ║                                                   ║  │
│  ║                                                   ║  │
│  ║                    ╔═══════╗                      ║  │
│  ║                    ║       ║                      ║  │
│  ║                    ║  V S  ║                      ║  │
│  ║                    ║       ║                      ║  │
│  ║                    ╚═══════╝                      ║  │
│  ║                                                   ║  │
│  ║         ┌─────────────────────────┐               ║  │
│  ║         │   BATTLE STARTING...    │               ║  │
│  ║         │   ████░░░░░░  3... 2... │               ║  │
│  ║         └─────────────────────────┘               ║  │
│  ║                                                   ║  │
│  ╚═══════════════════════════════════════════════════╝  │
│                                                         │
│  [Player A team: 3 Roomians shown left]                 │
│  [Player B team: 3 Roomians shown right]                │
│  [VS badge animates in center with screen shake]        │
│  [Countdown 3→2→1→BATTLE START]                         │
│  [Each Roomian sprite does idle bounce animation]       │
│  [HP bars under each sprite show full health]           │
│  [Element icons glow with their tier color]             │
└─────────────────────────────────────────────────────────┘
```

**Animation sequence:**
1. Screen fades in from black
2. Player names slide in from edges (left/right)
3. Roomian sprites pop in one-by-one (staggered, 200ms apart)
4. VS badge slams into center with screen shake + haptic
5. Countdown 3-2-1 with pulse animation
6. Screen flashes white → transitions to battle screen

### 3B. BATTLE SCREEN (Simultaneous 3v3 Team Battle)

All 3 Roomians are on screen at once with idle animations. Each round, the player assigns actions to each Roomian. When all actions are assigned, the round resolves in Speed order.

**Two assignment modes:**
- **Quick Bar** (default): Compact action bar at bottom of screen — swipe between your 3 Roomians, tap ability icons directly. Fast. 3 taps total for simple rounds.
- **Detailed Modal** (tap-and-hold any Roomian): Full modal with ability descriptions, EN costs, target preview. For complex decisions.

This eliminates the modal-per-Roomian friction. Most rounds are 3 quick taps. Complex rounds get the full modal when needed.

#### 3B-1. Planning Phase (All Roomians Visible)

```
┌─────────────────────────────────────────────────────────┐
│  ENEMY: "GUNGEONEER"                     ROUND 3  ⏱ 15s │
│                                                         │
│  ┌───────────┐    ┌───────────┐    ┌───────────┐      │
│  │  🛡️       │    │  ⚔️       │    │  ✨       │      │
│  │ [sprite]  │    │ [sprite]  │    │ [sprite]  │      │
│  │ idle anim │    │ idle anim │    │ idle anim │      │
│  │ blue aura │    │ red aura  │    │ gold aura │      │
│  │           │    │           │    │           │      │
│  │ Glacier   │    │ Reaper    │    │ Flare     │      │
│  │ L8        │    │ L8        │    │ L8        │      │
│  │HP████████ │    │HP██████░░ │    │HP████████ │      │
│  │EN████████ │    │EN██████░░ │    │EN████████ │      │
│  │ [BURN]    │    │           │    │           │      │
│  └───────────┘    └───────────┘    └───────────┘      │
│  ▰▰▰ READY        ░░░ PENDING        ▰▰▰ READY          │
│  (action set)     (waiting)         (action set)        │
│                                                         │
│  ═══════════════════════════════════════════════════    │
│                                                         │
│  ┌───────────┐    ┌───────────┐    ┌───────────┐      │
│  │  🔥       │    │  ❄️       │    │  ☠️       │      │
│  │ [sprite]  │    │ [sprite]  │    │ [sprite]  │      │
│  │ idle anim │    │ idle anim │    │ idle anim │      │
│  │ red aura  │    │ cyan aura │    │ grn aura  │      │
│  │           │    │           │    │           │      │
│  │ Emberblade│    │ Frostfang │    │ Deathling │     │
│  │ L7  ★★    │    │ L5  ★     │    │ L3  ★     │      │
│  │HP██████░░ │    │HP████████ │    │HP███░░░░░ │      │
│  │EN██████░░ │    │EN████████ │    │EN██░░░░░░ │      │
│  │ [BURN]    │    │           │    │ [CURSE]   │      │
│  └───────────┘    └───────────┘    └───────────┘      │
│  ░░░ PENDING       ▰▰▰ READY        ░░░ PENDING        │
│  (tap to act)     (action set)     (tap to act)        │
│                                                         │
│  ═══════════════════════════════════════════════════    │
│                                                         │
│  ACTIONS: 1/3 ready                                     │
│  ┌─────────────────────────────────────────────────┐   │
│  │  ⏳ Waiting for all Roomians to have actions...  │   │
│  │  [EXECUTE ROUND] (disabled until 3/3 ready)     │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

**Planning phase details:**
- All 6 Roomians (3 yours, 3 enemy) visible simultaneously with idle animations
- Each Roomian shows 2 resource bars: **HP** (red), **EN** (cyan)
- Status effect icons appear below each Roomian
- **Quick Bar** at bottom: swipe between your 3 Roomians, tap ability icon to assign. Tap-and-hold for full modal.
- After assigning action, Roomian shows "▰▰▰ READY" with a checkmark
- Enemy Roomians also show READY/PENDING (you see when opponent has locked in)
- **EXECUTE ROUND** button activates when all 3 of your Roomians have actions
- Timer: **20s PvP, 30s PvE** — if you don't act, unassigned Roomians **Defend** automatically
- PvE timer is generous but present — prevents analysis paralysis, keeps pace snappy

#### 3B-2. Action Selection Modal (Slides Up on Tap)

When you tap a Roomian during planning phase, this modal opens:

```
┌─────────────────────────────────────────────────────────┐
│                    ┌──────────────┐                     │
│                    │  🔥 [sprite] │                     │
│                    │  idle anim   │                     │
│                    └──────────────┘                     │
│                    Emberblade  L7                       │
│                    HP 42/55  EN 15/37                   │
│                                                         │
│  ── CHOOSE ACTION ──────────────────────────────────   │
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │  ⚔️ ATTACK   │  │  ✨ MAGIC   │  │  🛡️ DEFEND  │    │
│  │  Uses EN    │  │  Uses EN    │  │  Uses EN    │    │
│  │  Physical   │  │  Special    │  │  Halve dmg  │    │
│  │  abilities  │  │  abilities  │  │  +1 SPD tmp │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
│                                                         │
│  ┌─────────────┐                                     │
│  │  💨 FLEE    │                                     │
│  │  50% escape │                                     │
│  │  punished   │                                     │
│  └─────────────┘                                     │
│                                                         │
│  ── ATTACK ABILITIES ───────────────────────────────   │
│  (shown when ATTACK is tapped)                          │
│                                                         │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │
│  │ ⚔️ Flame Slsh│ │ ⚔️ Inferno   │ │ ⚔️ Tackle    │   │
│  │ 🔥 5 EN     │ │ 🔥 8 EN     │ │ 3 EN         │   │
│  │ 35 PWR      │ │ 60 PWR      │ │ 20 PWR       │   │
│  │ [TAP]       │ │ [TAP]       │ │ [TAP]       │   │
│  └──────────────┘ └──────────────┘ └──────────────┘   │
│                                                         │
│  ── MAGIC ABILITIES ────────────────────────────────   │
│  (shown when MAGIC is tapped)                           │
│                                                         │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │
│  │ ✨ Fireball  │ │ ✨ Meteor   │ │ ✨ Flame Body│   │
│  │ 🔥 8 EN     │ │ 🔥 15 EN    │ │ 🔥 Passive  │   │
│  │ 40 PWR AoE  │ │ 65 PWR AoE  │ │ Burn on hit │   │
│  │ [TAP]       │ │ [TAP]       │ │ [EQUIPPED]  │   │
│  └──────────────┘ └──────────────┘ └──────────────┘   │
│                                                         │
│  [CANCEL]                               [CONFIRM]      │
└─────────────────────────────────────────────────────────┘
```

#### 3B-3. Target Selection (After Choosing an Action)

When an action requires a target, the modal transitions to target pick mode. Available targets glow with a pulsing highlight. Invalid targets are dimmed.

```
┌─────────────────────────────────────────────────────────┐
│  ┌──────────────┐                                      │
│  │  🔥 [sprite] │  Emberblade → Flame Slash            │
│  └──────────────┘  Cost: 5 EN | 35 PWR | 🔥 Fire      │
│                                                         │
│  ── SELECT TARGET ──────────────────────────────────   │
│                                                         │
│  ENEMY TEAM:                                            │
│                                                         │
│  ┌───────────┐    ┌───────────┐    ┌───────────┐      │
│  │  🛡️       │    │  ⚔️       │    │  ✨       │      │
│  │ [sprite]  │    │ [sprite]  │    │ [sprite]  │      │
│  │  GLOWING  │    │  GLOWING  │    │  dimmed   │      │
│  │  PULSE    │    │  PULSE    │    │  (dead)   │      │
│  │           │    │           │    │           │      │
│  │ Glacier   │    │ Reaper    │    │ Flare     │      │
│  │ L8  80HP  │    │ L8  60HP  │    │ L8  0HP   │      │
│  │ ◀ TAP     │    │ ◀ TAP     │    │  ✗ DEAD   │      │
│  └───────────┘    └───────────┘    └───────────┘      │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  ✨ AoE abilities target ALL alive enemies      │   │
│  │  🛡️ Support abilities can target ALLY Roomians  │   │
│  │  ⚔️ Single-target: pick ONE enemy               │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  [◄ BACK TO ACTIONS]                   [CANCEL]        │
└─────────────────────────────────────────────────────────┘
```

**Target selection rules:**
- **Single-target attacks:** Pick one enemy (alive enemies glow, dead are dimmed)
- **AoE attacks:** Auto-target all alive enemies (no pick needed, just confirm)
- **Support abilities:** Can target any ally Roomian (including self)
- Dead Roomians are dimmed with ✗ and cannot be selected

#### 3B-4. Round Execution Phase (Speed-Based Resolution)

Once both players lock in all actions, the round executes. Actions resolve one at a time in **Speed** order (highest to lowest). Each action plays its animation.

```
┌─────────────────────────────────────────────────────────┐
│  ROUND 3 — EXECUTING                        SPEED ORDER  │
│                                                         │
│  1. Frostfang (SPD 22) → Ice Shard → Reaper             │
│  2. Reaper (SPD 18) → Thunderclap Burn → Emberblade     │
│  3. Emberblade (SPD 14) → Flame Slash → Glacier         │
│  4. Glacier (SPD 10) → Molten Shell → (self)            │
│  5. Deathling (SPD 8) → Shadow Claw → Reaper          │
│  6. Flare (SPD 6) → Fireball → (AoE all allies)         │
│                                                         │
│  ═══════════════════════════════════════════════════    │
│                                                         │
│  ┌───────────┐    ┌───────────┐    ┌───────────┐      │
│  │  🔥       │    │  ❄️       │    │  ☠️       │      │
│  │ [sprite]  │    │ [sprite]  │    │ [sprite]  │      │
│  │ ATTACK    │    │  IDLE     │    │  WAITING  │      │
│  │ ANIM!     │    │  (next)   │    │  (queued) │      │
│  │ → Glacier │    │           │    │           │      │
│  └───────────┘    └───────────┘    └───────────┘      │
│                                                         │
│  ┌───────────┐    ┌───────────┐    ┌───────────┐      │
│  │  🛡️       │    │  ⚔️       │    │  ✨       │      │
│  │ [sprite]  │    │ [sprite]  │    │ [sprite]  │      │
│  │ HIT! -18  │    │  WAITING  │    │  WAITING  │      │
│  │ 62/80     │    │           │    │           │      │
│  └───────────┘    └───────────┘    └───────────┘      │
│                                                         │
│  ═══════════════════════════════════════════════════    │
│                                                         │
│  NOW: Emberblade uses Flame Slash on Glacier            │
│  ▰▰▰▰▰▰▰▰░░░░  animating...                            │
│                                                         │
│  [SKIP ANIMATION]                    [PAUSE]            │
└─────────────────────────────────────────────────────────┘
```

**Execution phase details:**
- Speed order shown at top (all 6 Roomians sorted by SPD stat)
- **Same-SPD actions resolve simultaneously** — if two Roomians have equal SPD, their animations play at the same time (dramatic clash, both take damage together)
- Current actor plays attack animation, target plays hit reaction
- Damage numbers float up from targets — **critical hits get slow-mo + screen shake + gold damage text**
- **Focus fire bonus:** if 2+ allies target the same enemy in one round, each subsequent hit gets +10% damage (encourages tactical coordination without adding a new system)
- HP/EN bars update in real-time
- Status effects applied with visual indicators
- **Animation timing: ~1.0s per action** (down from 1.5s — keeps execution phase snappy, ~6s total for a full round)
- **Skip Animation** button speeds up to 0.3s per action for experienced players
- If a Roomian is downed mid-round, its queued action is cancelled — **downing flash: full-screen white pulse + haptic**
- After all actions resolve → **non-blocking round recap toast** (top of screen, 1.5s auto-dismiss: "Round 3: 47 dmg dealt, 23 taken, 1 downed") → check for downed → death saves → next round planning

#### 3B-5. Three Resource Bars

Every Roomian has three resources shown as thin bars under their sprite:

```
  ┌───────────┐
  │  🔥       │
  │ [sprite]  │
  │ idle anim │
  │           │
  │ Emberblade│
  │ L7  ★★    │
  │HP██████░░░│  42/55  ← Red bar (Health)
  │EN████░░░░░│  15/37  ← Cyan bar (Energy)
  │ [BURN]    │
  └───────────┘
```

| Resource | Color | Regeneration | Used For |
|----------|-------|-------------|----------|
| **HP** | Red | 0/turn (only via abilities) | Health — 0 = downed |
| **EN** | Cyan | 3 + floor((GRT+INT)/5) per turn | All abilities (attacks, magic, defend, flee) |

**Energy costs by action type:**
| Action | EN Cost |
|--------|----------|
| Light attack (Tackle, etc.) | 3 |
| Medium attack (Flame Slash, etc.) | 5 |
| Heavy attack (Inferno Strike, etc.) | 8 |
| Defend | 4 |
| Flee attempt | 6 |
| Swap | N/A — no swap action (all 3 active) |

**If EN is 0:** Roomian can only use a basic 0-cost Tackle at **50% power**. This makes EN depletion feel punishing — you're not dead, but you're significantly weaker. Creates real resource management tension: do you spend EN on a heavy hit now, or save it to Defend next turn?

**Defend upgrade:** Defend now grants **3 benefits** instead of 2:
1. Halves incoming damage (before GRT subtraction)
2. +1 temporary SPD (helps initiative next round)
3. **+2 EN regen next turn** (rewards defensive play as resource building, not just damage avoidance)

This makes Defend an active tactical choice — you Defend to set up a bigger turn next round, not just to survive.

#### 3B-6. Full Battle Flow (Updated)

```
┌─────────────────────────────────────────────────────────┐
│  BATTLE LOOP                                           │
│                                                         │
│  1. PLANNING PHASE                                     │
│     ├── All 6 Roomians on screen with idle anims       │
│     ├── Player taps each of their 3 Roomians           │
│     │   ├── Action modal slides up (animated)          │
│     │   ├── Pick category: Attack / Magic / Defend /   │
│     │   │                 Flee                          │
│     │   ├── Pick specific ability from list            │
│     │   ├── If target needed → target pick mode        │
│     │   │   (valid targets glow, invalid dimmed)       │
│     │   └── Confirm → Roomian shows READY ✓            │
│     ├── Enemy player does same (simultaneous)          │
│     └── PvP: 20s shared timer → unassigned Defend     │
│        PvE: no timer — take your time                  │
│                                                         │
│  2. EXECUTION PHASE                                    │
│     ├── Sort all actions by SPD (highest first)        │
│     ├── Execute each action in order:                  │
│     │   ├── Actor plays attack animation               │
│     │   ├── Target plays hit reaction                  │
│     │   ├── Damage/effect calculated & applied         │
│     │   ├── HP/EN bars update                         │
│     │   ├── Status effects tick                        │
│     │   └── If target downed → skip their queued action│
│     ├── Regen: EN +3+floor((GRT+INT)/5) per Roomian│
│     └── Check win condition                            │
│                                                         │
│  3. DOWNED CHECK                                       │
│     ├── Any Roomian at 0 HP → Death Save screen        │
│     ├── Player rolls d20 (animated)                    │
│     │   ├── Success (10-19): survive + Scar            │
│     │   ├── Nat 20: revive at 1 HP                     │
│     │   ├── Failure (2-9): 1 failure mark              │
│     │   └── Nat 1: 2 failure marks                     │
│     ├── 3 failures = permanent death → memorial        │
│     └── Surviving Roomian enters cooldown              │
│                                                         │
│  4. WIN CHECK                                          │
│     ├── All enemy Roomians downed/dead → YOU WIN       │
│     ├── All your Roomians downed/dead → YOU LOSE       │
│     └── Otherwise → back to PLANNING (next round)      │
│                                                         │
│  5. BATTLE END                                         │
│     ├── XP awarded based on outcome                    │
│     ├── Scars/deaths are permanent                     │
│     └── Cooldowns applied to surviving Roomians        │
└─────────────────────────────────────────────────────────┘
```

### 3C. ROOMIAN INVENTORY / BELT SCREEN

Shows all owned Roomians. Max 3 can be in the active team.

```
┌─────────────────────────────────────────────────────────┐
│  ◄ BACK              ROOMIAN BELT              [⚙️]     │
│                                                         │
│  ── ACTIVE TEAM (3/3) ──────────────────────────────    │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐          │
│  │   🔥      │  │   ❄️      │  │   ☠️      │          │
│  │ [sprite]  │  │ [sprite]  │  │ [sprite]  │          │
│  │           │  │           │  │           │          │
│  │ Emberblade│  │ Frostfang │  │ Deathling │          │
│  │ L7  ★★    │  │ L5  ★     │  │ L3  ★     │          │
│  │ HP 42/55  │  │ HP 30/30  │  │ HP 18/22  │          │
│  │ EN 15/37  │  │ EN 20/20  │  │ EN  8/15  │          │
│  │ ⚠️ 2 SCARS│  │ ✅ READY  │  │ ⏰ COOL 4m│          │
│  └───────────┘  └───────────┘  └───────────┘          │
│  [TAP to view]  [TAP to view]  [TAP to view]           │
│                                                         │
│  ── STORAGE (5) ────────────────────────────────────    │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐              │
│  │ ☠️  │ │ 🔥  │ │ ❄️  │ │ ☠️  │ │ 🔥  │              │
│  │ L2  │ │ L0  │ │ L4  │ │ L1  │ │ L6  │              │
│  │Shade │ │Blob │ │Tide │ │Pebbl│ │Spark│              │
│  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘              │
│  [Tap to move to Belt]                                 │
│                                                         │
│  ── EMPTY ROOM BALLS ───────────────────────────────    │
│  ┌─────┐ ┌─────┐                                       │
│  │ 🟠  │ │ 🟠  │                                       │
│  │BALL │ │BALL │                                       │
│  └─────┘ └─────┘                                       │
│  [Tap to summon new Roomian]                            │
│                                                         │
│  ───────────────────────────────────────────────────    │
│  ┌─────────┐ ┌─────────┐                              │
│  │  ⚔️ BATTLE│ │ 📖 SKILLS │                              │
│  └─────────┘ └─────────┘                              │
└─────────────────────────────────────────────────────────┘
```

**Status icons:**
- ✅ READY — can battle/quest
- ⏰ COOL Xm — cooldown timer
- ⚠️ N SCARS — has N scars (tap to see details)
- 💀 DOWNED — needs death save (if in battle) or rest (if after battle)
- 🩸 TRAINING — currently in training (unavailable)
- 🧭 QUESTING — currently on a quest

### 3D. ROOMIAN DETAIL / ACTIONS SCREEN

Shows full stats, abilities, scars, and available actions for a single Roomian.

```
┌─────────────────────────────────────────────────────────┐
│  ◄ BACK              ROOMIAN DETAIL                     │
│                                                         │
│  ┌─────────────────────┐                               │
│  │                     │                               │
│  │    🔥 [SPRITE]      │  Emberblade                   │
│  │    red aura         │  L7  ★★                       │
│  │    idle anim        │  Fire → Blaze path            │
│  │                     │                               │
│  └─────────────────────┘  Evolution: L1 Fire, L5 Blaze  │
│                                                         │
│  ── STATS ─────────────────────────────────────────    │
│  ┌─────────────────────────────────────────────────┐   │
│  │  VIT  12  ████████████░░  HP 42/55             │   │
│  │  PWR  18  ██████████████████░░  ATK            │   │
│  │  GRT  10  ██████████░░░░░░░░  DEF              │   │
│  │  SPD  14  ██████████████░░░░░  INITIATIVE      │   │
│  │  LCK   8  ████████░░░░░░░░░░  CRIT 8%          │   │
│  │  INT  11  ███████████░░░░░░░  EN  15/37        │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ── ACTIVE ABILITIES (4/4) ────────────────────────   │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │
│  │ ⚔️ Tackle   │ │ ⚔️ Ember Strk│ │ ⚔️ Fire Spin │   │
│  │ 3 EN  20P   │ │ 5 EN  35P   │ │ 6 EN  30P   │   │
│  │ [FIXED L0]  │ │ [FIXED L1]  │ │ [CHOSEN L3] │   │
│  └──────────────┘ └──────────────┘ └──────────────┘   │
│  ┌──────────────┐                                      │
│  │ ⚔️ Flame Slsh│  Passive: Burn Touch (L1), Flame Body (L4)│
│  │ 8 EN  50P   │                                      │
│  │ [FIXED L5]  │                                      │
│  └──────────────┘                                      │
│                                                         │
│  ── SCARS (2) ──────────────────────────────────────   │
│  ┌──────────────┐ ┌──────────────┐                    │
│  │ 💀 Weakened  │ │ 🧠 Lobotomized│                    │
│  │ -2 PWR      │ │ 25% action fail│                    │
│  └──────────────┘ └──────────────┘                    │
│                                                         │
│  ── ACTIONS ────────────────────────────────────────   │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐     │
│  │ ⚔️ BATTLE│ │ 🧭 QUEST│ │ 🏋️ TRAIN│ │ 😴 REST │     │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘     │
│                                                         │
│  ── EVOLUTION ─────────────────────────────────────    │
│  ┌─────────────────────────────────────────────────┐   │
│  │  ⭐ NEXT EVOLUTION: Level 8                     │   │
│  │  Current: Emberblade (L5 Blaze)                │   │
│  │  Next: Choose Inferno / Phoenix at L8          │   │
│  │  Progress: L7 → L8  [████████████░░░░] 80%      │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### 3E. EVOLUTION CHOICE SCREEN

Appears when a Roomian reaches an evolution level (1, 5, or 8). The number of cards depends on the level.

**L1 — Choose Primal Element (6 cards, scrollable):**

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│              ✦ EVOLUTION AVAILABLE ✦                    │
│                                                         │
│         Your Blob has reached Level 1!                  │
│         Choose its primal element.                      │
│                                                         │
│  ┌────────┐ ┌────────┐ ┌────────┐                      │
│  │ 🔥 FIRE│ │💧 WATER│ │🌍 EARTH│                      │
│  │        │ │        │ │        │                      │
│  │[sprite]│ │[sprite]│ │[sprite]│                      │
│  │red-org │ │ blue   │ │brn-grn │                      │
│  │        │ │        │ │        │                      │
│  │+3 PWR  │ │+3 GRT  │ │+3 GRT  │                      │
│  │+1 VIT  │ │+1 INT  │ │+1 VIT  │                      │
│  └────────┘ └────────┘ └────────┘                      │
│                                                         │
│  ┌────────┐ ┌────────┐ ┌────────┐                      │
│  │ 💨 AIR │ │☀️ LIGHT│ │ 🌙 DARK│                      │
│  │        │ │        │ │        │                      │
│  │[sprite]│ │[sprite]│ │[sprite]│                      │
│  │wht-gry │ │ golden │ │ purple │                      │
│  │        │ │        │ │        │                      │
│  │+3 SPD  │ │+3 INT  │ │+3 PWR  │                      │
│  │+1 LCK  │ │+1 LCK  │ │+1 INT  │                      │
│  └────────┘ └────────┘ └────────┘                      │
│                                                         │
│  ⚠️ This choice is PERMANENT.                            │
│  [TAP A CARD TO EVOLVE]                                 │
└─────────────────────────────────────────────────────────┘
```

**L5 — Choose Element Refinement (3 cards):**

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│              ✦ EVOLUTION AVAILABLE ✦                    │
│                                                         │
│         Your Roomian has reached Level 5!               │
│         Refine your element.                            │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │  CURRENT FORM                                    │    │
│  │  ┌───────┐                                       │    │
│  │  │ 🔥    │  Fire (L1 → L5)                       │    │
│  │  │sprite │  Fire elemental                      │    │
│  │  └───────┘  Red-orange aura                      │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  CHOOSE ONE REFINEMENT:                                 │
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │ 🔥 BLAZE    │  │ 🌋 MAGMA    │  │ 💨 SMOKE    │    │
│  │             │  │             │  │             │    │
│  │  [sprite]   │  │  [sprite]   │  │  [sprite]   │    │
│  │  red glow   │  │  orange     │  │  grey-black │    │
│  │  aggressive │  │  defensive  │  │  mystical   │    │
│  │  stance     │  │  stance     │  │  stance     │    │
│  │             │  │             │  │             │    │
│  │ "Emberblade"│  │ "Magma Wall"│  │"Smoke Veil"│    │
│  │             │  │             │  │             │    │
│  │ +4 PWR      │  │ +4 GRT      │  │ +4 INT      │    │
│  │ +2 SPD      │  │ +2 VIT      │  │ +2 EN regen │    │
│  │             │  │             │  │             │    │
│  │ UNLOCKS:    │  │ UNLOCKS:    │  │ UNLOCKS:    │    │
│  │ Flame Slash │  │ Molten Shell│  │ Smoke Veil  │    │
│  │ Inferno Strk│  │ Eruption    │  │ Ash Storm   │    │
│  │             │  │             │  │             │    │
│  │ PLAYSTYLE:  │  │ PLAYSTYLE:  │  │ PLAYSTYLE:  │    │
│  │ High burst  │  │ Lava tank,  │  │ Smoke mage, │    │
│  │ glass cannon│  │ counter dmg │  │ blind + DoT │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
│                                                         │
│  ⚠️ This choice is PERMANENT.                          │
│  [TAP A CARD TO EVOLVE]                                 │
└─────────────────────────────────────────────────────────┘
```

**L8 — Choose Mastery Grade (2 cards):**

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│              ✦ MASTERY EVOLUTION ✦                      │
│                                                         │
│         Your Roomian has reached Level 8!               │
│         Choose its mastery path.                        │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │  CURRENT PATH                                    │    │
│  │  Fire → Blaze (Emberblade)                       │    │
│  │  Red-orange aura · Burn DPS                      │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  CHOOSE YOUR MASTERY:                                   │
│                                                         │
│  ┌──────────────────────┐  ┌──────────────────────┐    │
│  │ 🔥 INFERNAL MASTER   │  │ 🔥 PHOENIX MASTER    │    │
│  │                      │  │                      │    │
│  │   [sprite]           │  │   [sprite]           │    │
│  │   deep crimson       │  │   bright orange-red  │    │
│  │   black smoke aura   │  │   feathered fire wings│   │
│  │                      │  │                      │    │
│  │  "Inferno"           │  │  "Phoenix"           │    │
│  │                      │  │                      │    │
│  │  +5 PWR              │  │  +5 VIT              │    │
│  │  +2 INT              │  │  +2 SPD              │    │
│  │                      │  │                      │    │
│  │  PASSIVE:            │  │  PASSIVE:            │    │
│  │  Eternal Flame       │  │  Rebirth Flame       │    │
│  │  DoT ticks twice,    │  │  First KO auto-      │    │
│  │  burn uncleanseable  │  │  revives at 30% HP   │    │
│  │                      │  │                      │    │
│  │  PLAYSTYLE:          │  │  PLAYSTYLE:          │    │
│  │  Ultimate offense,   │  │  Immortal burner,    │    │
│  │  relentless burn     │  │  second life         │    │
│  └──────────────────────┘  └──────────────────────┘    │
│                                                         │
│  ⚠️ This choice is PERMANENT.                          │
│  [TAP A CARD TO EVOLVE]                                 │
└─────────────────────────────────────────────────────────┘
```

**Visual flair:**
- L1: 6 cards in a 2×3 grid, each with unique elemental aura color
- L5: 3 cards, each with refined element glow (different intensity/hue from L1)
- L8: 2 large cards, each with mastery-level visual effects (particle auras, animated borders)
- Sprite preview is unique to each path (different pose, different aura)
- Card expands on tap with confirmation dialog
- Evolution animation: old sprite dissolves → new sprite materializes with particle burst
- L8 mastery cards are larger and more detailed than L5/L1 cards

### 3F. SKILL LEARNING SCREEN

Roomians gain abilities through level-up rewards and ability scrolls found in quests. This screen shows the current ability loadout and scroll inventory.

```
┌─────────────────────────────────────────────────────────┐
│  ◄ BACK           ABILITIES & SCROLLS                   │
│                                                         │
│  ┌──────────────┐                                      │
│  │ 🔥 Emberblade│  Level 7  ★★                         │
│  │ Fire→Blaze   │  Path: Fire → Blaze → (L8 pending)    │
│  └──────────────┘                                      │
│                                                         │
│  ── ACTIVE ABILITIES (4/4) ────────────────────────    │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │
│  │ ⚔️ Tackle   │ │ ⚔️ Flame Slsh│ │ ⚔️ Inferno   │   │
│  │ 3 EN  20P   │ │ 5 EN  35P   │ │ 8 EN  60P   │   │
│  │ [FIXED L0]  │ │ [FIXED L1]  │ │ [FIXED L5]  │   │
│  └──────────────┘ └──────────────┘ └──────────────┘   │
│  ┌──────────────┐                                      │
│  │ ⚔️ Fire Spin │  ← Player chose at L3                │
│  │ 6 EN  30P   │                                      │
│  │ [CHOSEN L3] │  [SWAP] (from learned pool)          │
│  └──────────────┘                                      │
│                                                         │
│  ── PASSIVE ABILITIES (2/2) ───────────────────────    │
│  ┌──────────────┐ ┌──────────────┐                    │
│  │ � Burn Touch│ │ 🔄 Flame Body│                    │
│  │ Burn on hit  │ │ +10% fire dmg│                    │
│  │ [FIXED L1]  │ │ [CHOSEN L4]  │ [SWAP]             │
│  └──────────────┘ └──────────────┘                    │
│                                                         │
│  ── ABILITY SCROLLS ────────────────────────────────   │
│  ┌──────────────┐ ┌──────────────┐                    │
│  │ 📜 Scroll of │ │ 📜 Scroll of │                    │
│  │ Heat Wave    │ │ Smokescreen  │                    │
│  │ Teaches:     │ │ Teaches:     │                    │
│  │ Heat Wave    │ │ Smokescreen  │                    │
│  │ [USE SCROLL]│ │ [USE SCROLL]│                    │
│  └──────────────┘ └──────────────┘                    │
│                                                         │
│  ── LEARNING RULES ─────────────────────────────────    │
│  • Abilities gained via level-up rewards (L3, L4)      │
│  • Evolution abilities are fixed (L1, L5, L8)          │
│  • Choice abilities can be swapped from learned pool   │
│  • Scrolls teach instantly (no cost)                   │
│  • Higher INT unlocks more scroll options              │
│  • Max 4 active + 3 passive abilities                  │
└─────────────────────────────────────────────────────────┘
```

### 3G. DEATH SAVE SCREEN

When a Roomian's HP hits 0, this dramatic screen appears.

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│                    ⚠️ ROOMIAN DOWN ⚠️                    │
│                                                         │
│         ┌───────────────────────┐                      │
│         │                       │                      │
│         │    🔥 [SPRITE]        │                      │
│         │    desaturated        │                      │
│         │    flickering         │                      │
│         │                       │                      │
│         └───────────────────────┘                      │
│                                                         │
│         Emberblade  L7  ★★                              │
│                                                         │
│         DEATH SAVING THROW                               │
│         3 chances. Need 1 success to survive.           │
│         Resets every battle (does not persist).          │
│                                                         │
│         ┌───────────────────────────────────┐          │
│         │                                   │          │
│         │         ┌─────────┐               │          │
│         │         │         │               │          │
│         │         │  D 20  │               │          │
│         │         │         │               │          │
│         │         │  [ROLL] │               │          │
│         │         │         │               │          │
│         │         └─────────┘               │          │
│         │                                   │          │
│         │    [TAP DICE TO ROLL]             │          │
│         │                                   │          │
│         └───────────────────────────────────┘          │
│                                                         │
│         ATTEMPTS:  ● ● ○  (2 remaining)                 │
│         FAILURES: ● ○ ○  (1 failure so far)             │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  ROLL RESULTS:                                   │  │
│  │  Nat 1  = 2 failures (catastrophic)              │  │
│  │  2-9    = 1 failure                              │  │
│  │  10-19  = SUCCESS → survive + gain Scar          │  │
│  │  Nat 20 = SUCCESS → survive + revive at 1 HP     │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  [Red vignette pulses, screen shakes on roll]           │
│  [Dice animates with 3D tumble, slams down]             │
│  [Haptic heavy on result reveal]                        │
└─────────────────────────────────────────────────────────┘
```

**Death Save Result — SURVIVAL (10-19):**

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│                   ✅ SURVIVED! ✅                        │
│                                                         │
│              But at what cost...                        │
│                                                         │
│         Roll: 14  →  SUCCESS                            │
│                                                         │
│         Emberblade clings to life!                      │
│                                                         │
│         ┌───────────────────────────────────┐          │
│         │  SCAR ROLL (d6)                   │          │
│         │  ┌─────┐                          │          │
│         │  │  5  │  →  LOBOTOMIZED          │          │
│         │  └─────┘                          │          │
│         │                                   │          │
│         │  Effect: 25% chance any action    │          │
│         │  fails (does nothing)             │          │
│         │                                   │          │
│         │  ⚠️ This is PERMANENT             │          │
│         └───────────────────────────────────┘          │
│                                                         │
│         Cooldown: 10 minutes before next battle         │
│                                                         │
│         [CONTINUE]                                      │
└─────────────────────────────────────────────────────────┘
```

**Death Save Result — DEATH (3 failures):**

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│                   💀 PERISHED 💀                         │
│                                                         │
│         Roll: 3  →  FAILURE (3rd)                       │
│                                                         │
│         ┌───────────────────────┐                      │
│         │                       │                      │
│         │    🔥 [SPRITE]        │                      │
│         │    dissolving         │                      │
│         │    into particles     │                      │
│         │                       │                      │
│         └───────────────────────┘                      │
│                                                         │
│         Emberblade  L7  ★★                              │
│         Battles: 12  |  Scars: 2                        │
│         Final path: Fire → Blaze                        │
│                                                         │
│         "A brave Roomian. It will be remembered."       │
│                                                         │
│         ┌───────────────────────────────────┐          │
│         │  🪦 MEMORIAL                       │          │
│         │  Name: Emberblade                  │          │
│         │  Level: 7                          │          │
│         │  Battles won: 7                    │          │
│         │  Quests completed: 3               │          │
│         │  Scars survived: 2                 │          │
│         └───────────────────────────────────┘          │
│                                                         │
│         [FAREWELL]                                      │
└─────────────────────────────────────────────────────────┘
```

---

## 4. SKILL / ABILITY SYSTEM

### 4.1 Ability Categories

| Type | Icon | EN Cost | Description |
|------|------|---------|-------------|
| **Physical** | ⚔️ | 3-8 | Scales with PWR, reduced by GRT |
| **Magical** | ✨ | 5-15 | Scales with INT, reduced by GRT/2 |
| **Passive** | 🔄 | 0 | Always active, no action needed |
| **Field** | 🌫️ | 8-15 | Terrain/hazard effect, persists |
| **Support** | 🛡️ | 3-10 | Buff ally or debuff enemy |

### 4.2 Ability Slots

- **4 active ability slots** (filled progressively: 1 at L0, 2 at L1, 3 at L3, 4 at L5)
- **3 passive ability slots** (filled progressively: 1 at L1, 2 at L4, 3 at L8)
- Evolution abilities (L1, L5, L8) are **fixed** — cannot be swapped
- Evolution abilities **stack** — Roomian keeps all abilities from every evolution tier (L1 + L5 + L8)
- Choice abilities (L3, L4) are **player-selected** — can be swapped from learned pool

### 4.3 Learning New Skills

| Method | Cost | Requirement |
|--------|------|-------------|
| **Level-up rewards** | Free | Automatic at L3 (active) and L4 (passive) |
| **Evolution** | Free | Automatic at L1, L5, L8 (path-determined) |
| **Ability Scrolls** | Free (scroll consumed) | Found in quests/chests. Unlimited inventory, element-locked (can only learn scrolls matching your current element). Tradable scroll-for-scroll between players. |
| **Tutor** | Gold/shells | NPC teaches specific skills (future) |
| **Breeding** | N/A | Inherit parent's ability (future) |

### 4.4 Level Progression System (Custom)

Every level gives a specific reward. No dead levels, no skill points to bank — each level delivers its reward immediately.

```
Level  Reward                                    Running Total (Active / Passive)
─────  ────────────────────────────────────────  ────────────────────────────────
L0     Basic Attack (Tackle)                    1 active, 0 passive
L1     ★ EVOLUTION → +1 active (path) +1 passive (path)   2 active, 1 passive
L2     Attribute increase (+2 to 1 of 3 random stats)     2 active, 1 passive
L3     Choose 1 of 3 active abilities                      3 active, 1 passive
L4     Choose 1 of 3 passive abilities                     3 active, 2 passive
L5     ★ EVOLUTION → +1 active (path-determined)           4 active, 2 passive
L6     Attribute increase (+2 to 1 of 3 random stats)     4 active, 2 passive
L7     ★ MILESTONE — unlock ability swap (see §4.5b)      4 active, 2 passive
L8     ★ EVOLUTION → +1 passive (path-determined)          4 active, 3 passive
L9     Attribute increase (+2 to 1 of 3 random stats)     4 active, 3 passive
L10    ★ PRESTIGE — cosmetic aura + +1 to ALL stats        4 active, 3 passive
```

**What changed from original:**
- **L7** is no longer a duplicate attribute level. It's now a **milestone** — unlocks ability swap, letting you re-equip any learned ability into your choice slots (L3/L4). This gives L7 a distinct identity and adds tactical flexibility mid-game.
- **L10 Prestige** now grants **+1 to ALL stats** in addition to the cosmetic aura. This makes L10 feel like a real capstone, not a dead level. The +1 is small enough to not break balance but meaningful enough to feel rewarding.

**Key rules:**
- Evolution abilities (L1, L5, L8) are **fixed** — determined by evolution path, cannot be swapped
- Evolution abilities **stack** — a Roomian keeps all abilities from every evolution tier (L1 + L5 + L8)
- Choice abilities (L3, L4) are **player-selected** from 3 random options — can be swapped from the learned pool **after L7 milestone unlock**
- Attribute increases (L2, L6, L9) present 3 random stats, player picks one to +2
- L7 is a **milestone** — unlocks ability swap (re-equip learned abilities into choice slots)
- L10 Prestige grants +1 to ALL stats + golden aura shimmer + prestige badge on belt screen
- No skill points to bank — rewards are immediate and specific per level

### 4.4b Level-Up Screen Mockup (Non-Evolution Levels)

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│              ✦ LEVEL UP! ✦                              │
│                                                         │
│         Emberblade reached Level 6!                     │
│                                                         │
│         ┌───────────────────────────┐                  │
│         │  CHOOSE AN ATTRIBUTE       │                  │
│         │                            │                  │
│         │  ┌────────┐ ┌────────┐ ┌────────┐           │
│         │  │  +2    │ │  +2    │ │  +2    │           │
│         │  │  PWR   │ │  INT   │ │  SPD   │           │
│         │  │        │ │        │ │        │           │
│         │  │ [TAP]  │ │ [TAP]  │ │ [TAP]  │           │
│         │  └────────┘ └────────┘ └────────┘           │
│         │                            │                  │
│         │  Pick one to increase      │                  │
│         │  permanently by +2         │                  │
│         └───────────────────────────┘                  │
│                                                         │
│  [3 random stats presented from: VIT, PWR, GRT, SPD,    │
│   LCK, INT — weighted by current lowest stats]          │
└─────────────────────────────────────────────────────────┘
```

### 4.4c Level-Up Screen Mockup (L3/L4 — Ability Choice)

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│              ✦ LEVEL UP! ✦                              │
│                                                         │
│         Emberblade reached Level 3!                     │
│         Choose a new ACTIVE ABILITY.                    │
│                                                         │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐    │
│  │ ⚔️ Flame Slsh│ │ ⚔️ Combustion│ │ ⚔️ Fire Spin │    │
│  │ 🔥 5 EN     │ │ 🔥 8 EN     │ │ 🔥 6 EN     │    │
│  │ 35 PWR      │ │ 50 PWR      │ │ 30 PWR AoE  │    │
│  │ Single target│ │ Self-destruct│ │ Hits all    │    │
│  │              │ │ 15 recoil   │ │ enemies     │    │
│  │ [TAP TO PICK]│ │ [TAP TO PICK]│ │ [TAP TO PICK]│   │
│  └──────────────┘ └──────────────┘ └──────────────┘    │
│                                                         │
│  ⚠️ This choice is permanent for now.                         │
│  You can swap between learned abilities at L7.               │
└─────────────────────────────────────────────────────────┘
```

### 4.5b Ability Swap System (Unlocked at L7)

At L7, the Roomian reaches a milestone — it can now **swap choice abilities** (L3 active, L4 passive) from its learned pool.

```
┌─────────────────────────────────────────────────────────┐
│  ABILITY MANAGEMENT — Emberblade L7                      │
│                                                         │
│  ACTIVE SLOTS:                                          │
│  Slot 1: Tackle (L0 base)          🔒 FIXED             │
│  Slot 2: Ember Strike (L1 evolution) 🔒 FIXED            │
│  Slot 3: Fire Spin (L3 choice)     🔄 SWAPPABLE          │
│  Slot 4: Flame Slash (L5 evolution) 🔒 FIXED             │
│                                                         │
│  PASSIVE SLOTS:                                         │
│  Slot 1: Burn Touch (L1 evolution) 🔒 FIXED              │
│  Slot 2: Flame Body (L4 choice)    🔄 SWAPPABLE          │
│  Slot 3: (locked — unlocks at L8)  🔒 LOCKED             │
│                                                         │
│  LEARNED POOL (swappable):                              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐    │
│  │ ⚔️ Fire Spin │ │ ⚔️ Combustion│ │ ⚔️ Heat Wave │    │
│  │ 6 EN, 30 PWR│ │ 8 EN, 50 PWR│ │ 5 EN, 25 AoE│    │
│  │ [EQUIPPED]  │ │ [TAP TO EQ] │ │ [TAP TO EQ] │    │
│  └──────────────┘ └──────────────┘ └──────────────┘    │
│                                                         │
│  ⚠️ Evolution abilities are always fixed.               │
│  Only L3/L4 choice abilities can be swapped.            │
└─────────────────────────────────────────────────────────┘
```

**Design intent:** L7 gives the player a tactical reset point. As they approach the L8 evolution, they can re-tune their build. This makes L7 feel meaningful instead of being another +2 stat level.

### 4.6 INT Affects Learnable Skills

| INT Range | Skill Tier | Example |
|-----------|------------|---------|
| 5-9 | Basic | Tackle, Pulse Bolt, Guard |
| 10-14 | Intermediate | Flame Slash, Ice Wall, Gust Chain |
| 15-19 | Advanced | Inferno Strike, Blizzard, Thunderstorm |
| 20+ | Master | Meteor, Deep Freeze, Overload |

Higher INT also unlocks more ability scroll options and increases scroll learning speed.

---

## 5. BATTLE MECHANICS (3v3 Team)

### 5.1 Team Rules

- Each player brings **up to 3 Roomians** to a battle
- **All 3 Roomians are active simultaneously** — no front/reserve distinction
- **No Swap action** — all Roomians act each round
- Battle ends when **all 3 Roomians** on one side are downed/dead
- **1v1 format:** 1 Roomian each, same mechanics
- **2v2 format:** 2 Roomians each, same mechanics
- **3v3 format:** 3 Roomians each (default)

### 5.2 Turn Structure

**Damage Formula (Two-Roll System):**

```
Damage = (abilityPower + PWR) × rand(0.8–1.2) − GRT

Roll 1: abilityPower + PWR     (base damage)
Roll 2: × rand(0.8–1.2)         (variance roll)
Final:  subtract GRT             (mitigation)

Min damage: 1 (never zero on a hit)
Crit (LCK-based): ×1.5 after GRT subtraction
```

- **Physical abilities** scale with PWR, mitigated by full GRT
- **Magical abilities** scale with INT, mitigated by GRT/2
- **Variance roll** (0.8–1.2) creates organic highs and lows — no two hits feel identical
- **Crits** multiply the post-GRT damage by 1.5, making luck meaningful without dominating
- **Defending** halves incoming damage before GRT subtraction (stacks with GRT)

**Example:** Emberblade uses Flame Slash (abilityPower 20) with PWR 18 vs GRT 10:
  Base = 20 + 18 = 38
  Variance = 38 × 1.1 = 41.8 → 41
  Mitigation = 41 − 10 = **31 damage**
  If crit (8% LCK): 31 × 1.5 = **46 damage**

```
┌─────────────────────────────────────────────────────┐
│  ROUND START                                        │
│  ├── PLANNING PHASE                                │
│  │   PvP: 20s timer | PvE: 30s timer              │
│  │   ├── All Roomians on screen with idle anims    │
│  │   ├── Quick Bar: swipe → tap ability (fast)    │
│  │   │   OR tap-and-hold → full modal (detailed)   │
│  │   ├── Assign action per Roomian:                │
│  │   │   ├── Attack (pick ability, EN cost)        │
│  │   │   ├── Magic (pick ability, EN cost)         │
│  │   │   ├── Defend (halve dmg + +2 EN next turn)  │
│  │   │   └── Flee (PvE: per-Roomian, PvP: draw)    │
│  │   ├── If target needed → target pick mode       │
│  │   ├── Confirm → Roomian shows READY             │
│  │   └── Timer expires → auto-Defend               │
│  │                                                  │
│  ├── EXECUTION PHASE                               │
│  │   ├── Sort all actions by SPD (highest first)   │
│  │   ├── Same-SPD actions resolve simultaneously   │
│  │   ├── Execute each action (~1.0s, skippable):   │
│  │   │   ├── Actor plays attack animation          │
│  │   │   ├── Target plays hit reaction             │
│  │   │   ├── Focus fire: +10% per ally on same tgt │
│  │   │   ├── Crits: slow-mo + screen shake + gold  │
│  │   │   ├── Damage/effect calculated & applied    │
│  │   │   ├── HP/EN bars update                      │
│  │   │   ├── Status effects tick (DoT, regen)      │
│  │   │   └── If target downed → flash + skip queued│
│  │   ├── Regen: EN +3+floor((GRT+INT)/5)          │
│  │   └── Non-blocking recap toast (1.5s auto-dismiss)   │
│  │                                                  │
│  ├── DOWNED CHECK                                   │
│  │   ├── Any Roomian at 0 HP → Death Save screen  │
│  │   └── Player rolls d20 (dramatic zoom + shake)  │
│  │                                                  │
│  ├── WIN CHECK                                      │
│  │   ├── All enemy Roomians downed/dead → YOU WIN  │
│  │   ├── All your Roomians downed/dead → YOU LOSE  │
│  │   └── Otherwise → next round PLANNING           │
│  │                                                  │
│  └── BATTLE END                                     │
│      ├── XP awarded based on outcome               │
│      ├── Scars/deaths are permanent                │
│      └── Cooldowns applied to surviving Roomians   │
└─────────────────────────────────────────────────────┘
```

### 5.3 Team Synergy (Future)

When Roomians share an element or refinement, passive bonuses apply:
- 2 same primal element: +10% damage of that element
- 3 same primal element: +20% damage, immunity to that element
- 2 same refinement (e.g., both Blaze): +15% damage, shared passive tick
- 3 same refinement: +25% damage, immunity, shared EN regen +1/turn
- Diverse team (3 different primal elements): +5% to all stats team-wide

### 5.4 Battle Rewards

| Outcome | XP | Items | Notes |
|---------|-----|-------|-------|
| **Win (no losses)** | 50 XP per enemy level | None | Flawless victory bonus |
| **Win (1 downed)** | 35 XP per enemy level | None | Standard win |
| **Win (2 downed)** | 20 XP per enemy level | None | Pyrrhic victory |
| **Loss (survived)** | 10 XP per own level | None | Consolation XP |
| **Loss (all dead)** | 0 XP | None | Devastating |
| **Flee** | 0 XP | None | No rewards |

---

## 6. XP & LEVELING CURVE

### 6.1 XP Required Per Level

```
Level  0 →  1:   50 XP    ← FIRST EVOLUTION (pick 1 of 6 elements)
Level  1 →  2:   80 XP    ← Attribute increase (+2 to 1 of 3 stats)
Level  2 →  3:  120 XP    ← Choose 1 of 3 active abilities
Level  3 →  4:  170 XP    ← Choose 1 of 3 passive abilities
Level  4 →  5:  230 XP    ← SECOND EVOLUTION (pick 1 of 3 refinements)
Level  5 →  6:  300 XP    ← Attribute increase
Level  6 →  7:  380 XP    ← MILESTONE: unlock ability swap
Level  7 →  8:  470 XP    ← THIRD EVOLUTION (pick 1 of 2 masteries)
Level  8 →  9:  570 XP    ← Attribute increase
Level  9 → 10:  680 XP    ← MAX LEVEL (prestige: +1 all stats + cosmetic aura)
```

### 6.2 XP Sources

| Source | XP | Notes |
|--------|-----|-------|
| Battle win (flawless) | 50 × enemy level | No Roomians downed |
| Battle win (standard) | 35 × enemy level | 1 downed |
| Battle win (pyrrhic) | 20 × enemy level | 2 downed |
| Battle loss | 10 × own level | Survived |
| Quest: Forage | 15 XP | 5 min, safe |
| Quest: Scout | 40 XP | 15 min, low risk |
| Quest: Hunt | 80 XP | 30 min, medium risk |
| Quest: Deep Dive | 200 XP | 60 min, high risk |
| Training | 5 XP | Per session (stat focus) |
| Pre-evolution quest | +100 XP | One-time bonus quest at L7, eases the longest XP gap (L7→L8 = 470 XP) |

---

## 7. ROOM BALL CATCH SYSTEM

Room Balls are consumable items used to catch wild Roomians. **No battle required** — just throw the ball and see what happens.

### 7.1 Throw & Reveal Flow

```
┌─────────────────────────────────────────────────────────┐
│  ROOM BALL THROW                                        │
│                                                         │
│  1. Player finds a wild Roomian in the world            │
│  2. Player taps THROW ROOM BALL                         │
│  3. Ball arcs through the air (animated trajectory)     │
│  4. Ball hits wild Roomian → flash → SUSPENSE PHASE    │
│  5. Ball wobbles 3 times (1.5s total tension build)     │
│  6. Result reveal (see below)                           │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │  🎯 WILD ROOMIAN SPOTTED!                       │    │
│  │                                                  │    │
│  │     ┌───────┐                                   │    │
│  │     │  ???   │  Level 0 Blob                    │    │
│  │     │ [spr]  │  (silhouette — identity hidden)  │    │
│  │     │ ~glow~ │  (faint aura hint visible)       │    │
│  │     └───────┘                                   │    │
│  │                                                  │    │
│  │  Balls: ○○○ (3 Standard)                        │    │
│  │  [THROW ROOM BALL]                              │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  ── WOBBLE PHASE (suspense) ────────────────────────    │
│  ┌─────────────────────────────────────────────────┐    │
│  │  Ball seals → screen darkens → silence           │    │
│  │  Wobble 1... (left tilt)                         │    │
│  │  Wobble 2... (right tilt)                        │    │
│  │  Wobble 3... (center, hold)                      │    │
│  │  *** 1.5s of pure tension ***                    │    │
│  │  → Each wobble: haptic tick                      │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  ── SUCCESS (75%) ──────────────────────────────────    │
│  ┌─────────────────────────────────────────────────┐    │
│  │  ✅ CAUGHT!                                     │    │
│  │                                                  │    │
│  │  Ball cracks open → smoke clears → REVEAL:      │    │
│  │                                                  │    │
│  │     ┌───────────────────────┐                   │    │
│  │     │  🔥 [SPRITE REVEAL]   │                   │    │
│  │     │  "Emberblade"         │                   │    │
│  │     │  Level 0  Fire        │                   │    │
│  │     │  ★ NEW ROOMIAN!       │                   │    │
│  │     └───────────────────────┘                   │    │
│  │                                                  │    │
│  │  [Particle burst, neon flash, haptic]           │    │
│  │  [Added to storage]                             │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  ── FAILURE (25%) ─────────────────────────────────     │
│  ┌─────────────────────────────────────────────────┐    │
│  │  ❌ IT BROKE FREE!                               │    │
│  │                                                  │    │
│  │  Ball bursts open → Roomian stumbles but        │    │
│  │  DOESN'T flee immediately                        │    │
│  │                                                  │    │
│  │  [THROW AGAIN?] (+1 ball cost, -10% success)    │    │
│  │  [LEAVE IT]                                     │    │
│  │                                                  │    │
│  │  [Ball consumed either way]                     │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

**What changed:**
- **Wobble phase:** 3 wobbles with haptic ticks = 1.5s of pure tension before reveal. This is the "hold your breath" moment.
- **Silhouette aura hint:** The hidden Blob shows a faint colored glow — sharp-eyed players can guess the element before catching. Doesn't reveal identity, just a hint.
- **Failure isn't final:** Roomian doesn't flee immediately. Player can throw again at +1 ball cost and -10% success rate per retry. Max 2 retries (3 total throws). This turns failure from a dead end into a pressure decision: spend more balls or walk away?
- **Ball counter visible:** Player sees how many balls they have before throwing.

### 7.2 Room Ball Types

| Ball Type | Success Rate | Source | Notes |
|-----------|-------------|--------|-------|
| **Standard** | 75% | Starter pack, shop | Orange ball |
| **Quality** | 85% | Hunt quest reward | Blue ball, higher grade |
| **Master** | 100% | Deep Dive rare drop | Gold ball, guaranteed catch |

### 7.3 Catch Rules

- **No battle required** — throw the ball directly at the wild Roomian
- **Base success rate: 75%** — always a gamble
- **Wobble suspense:** Ball wobbles 3 times before reveal (1.5s tension build with haptic ticks)
- Wild Roomian identity is **hidden until caught** — but a faint aura glow hints at the element
- On success: Roomian is revealed with full stats, element, and name → added to storage. Particle burst + neon flash + haptic.
- On failure: Ball is consumed, but Roomian **stumbles, doesn't flee**. Player can retry:
  - Retry 1: +1 ball cost, success rate drops to 65%
  - Retry 2: +1 ball cost, success rate drops to 55%
  - After 3 total throws (fail or success), Roomian flees regardless
- Room Balls are consumed on use (success or fail)
- Wild Roomians are always Level 0 Blobs — their element is revealed on catch
- Quality Balls (85%) and Master Balls (100%) improve odds but are rarer
- **Rare encounters (5% chance):** Wild Blob has a golden shimmer instead of normal silhouette. Golden Blobs are guaranteed to be a random refinement-level element (L5 equivalent) instead of base element — a head start catch. Only visible as golden before throwing, element still hidden until reveal.

---

## 8. STATUS EFFECTS SYSTEM

### 8.1 Status Effects by Element

| Element | Status Name | Icon | Effect | Duration | Cure |
|---------|------------|------|--------|----------|------|
| **Fire** | Burning | 🔥 | 5 damage/turn, ignores GRT | 3 turns | Natural (expires) or Light cleanse abilities |
| **Water** | Chilled | ❄️ | -50% SPD, cannot Flee | 2 turns | Natural (expires) or Light cleanse abilities |
| **Earth** | Stunned | 💫 | Skip next action | 1 turn | Natural (expires) or Light cleanse abilities |
| **Air** | Paralyzed | ⚡ | 25% action fail, -2 EN/turn | 2 turns | Natural (expires) or Light cleanse abilities |
| **Light** | Blinded | 🌟 | -30% accuracy (attacks may miss) | 2 turns | Natural (expires) only |
| **Dark** | Cursed | 🌑 | -2 to all stats while active | 3 turns | Natural (expires) or Light cleanse abilities |
| **Light** | Charmed | ✨ | May attack allies instead of enemies | 1 turn | Natural (expires) or Light cleanse abilities |

**Cure Design Rule:** Cures are abilities, not items. Light-element Roomians (especially Solar path) have cleanse abilities that remove negative statuses. Some masteries grant immunity (e.g., Forge Master = stun immune, Bulwark Master = knockback immune). This aligns with Design Pillar 4: "No consumable clutter."

### 8.2 Status Stacking Rules

- Same status does NOT stack — refreshing resets duration to max
- Different statuses DO stack (e.g., Burning + Chilled at once)
- Burning + Chilled = "Steam" combo: +50% burn damage, Chilled duration halved
- Cursed reduces stats before other calculations (applied first)
- Stunned/Paralyzed skip action but still regen EN
- Death save roll is unaffected by status effects

---

## 9. SCAR SYSTEM

### 9.1 Scar Table (d6 roll on death save success)

| Roll | Scar Name | Effect | Severity |
|------|-----------|--------|----------|
| 1 | **Weakened** | -2 PWR | Minor |
| 2 | **Fractured** | -2 VIT (reduces Max HP) | Minor |
| 3 | **Slowed** | -2 SPD | Minor |
| 4 | **Dulled** | -2 INT (reduces Max EN) | Moderate |
| 5 | **Lobotomized** | 25% chance any action fails | Severe |
| 6 | **Cursed** | -1 to ALL stats | Severe |

### 9.2 Scar Rules

- Scars are **permanent** — cannot be removed by any means
- Each death save success grants 1 scar (roll d6 to determine which)
- **Death save counter resets every battle** — successes and failures do not persist between battles
- Multiple scars stack (a Roomian can have Weakened + Lobotomized)
- Same scar type can stack (two Weakened = -4 PWR)
- Scars do NOT affect evolution eligibility or ability slots
- A Roomian with 3+ scars gets a "Battle-Scarred" badge on belt screen
- Scars are shown on detail screen with individual effect breakdowns

---

## 10. WILD AI & BATTLE FORMATS

### 10.1 Wild Roomian AI (PvE Encounters)

When battling AI-controlled Roomians in PvE (raids, future PvE content), the AI follows simple rules:

```
┌─────────────────────────────────────────────────────┐
│  WILD AI DECISION TREE                              │
│                                                     │
│  IF HP ≤ 30% AND has EN:                           │
│    → 60% chance to Defend                           │
│    → 40% chance to Attack (weakest ability)         │
│  ELIF HP ≤ 50% AND has EN:                          │
│    → 50% Attack, 30% Magic, 20% Defend              │
│  ELIF has EN (≥6):                                  │
│    → 40% Attack, 35% Magic, 15% Defend, 10% Flee    │
│  ELIF has EN (≥3):                                  │
│    → 70% Attack, 20% Defend, 10% Flee               │
│  ELIF has EN (≥1):                                  │
│    → 80% Magic, 20% Defend                          │
│  ELSE:                                              │
│    → Defend (no resources)                           │
│                                                     │
│  Target selection: random alive enemy               │
│  Ability selection: random from available pool      │
│  No strategic targeting (no focus fire)             │
└─────────────────────────────────────────────────────┘
```

**Note:** Catching wild Roomians no longer involves battle — see Section 7 (Room Ball Catch System). This AI applies to PvE battles only (raids, future PvE content).

### 10.2 Battle Formats

| Format | Players | Roomians Each | Timer | Notes |
|--------|---------|---------------|-------|-------|
| **1v1 PvP** | 2 players | 1 each | 20s shared | Quick duels |
| **2v2 PvP** | 2 players | 2 each | 20s shared | Standard competitive |
| **3v3 PvP** | 2 players | 3 each | 20s shared | Default format |
| **1v3 Raid** | 1 player vs AI | 3 vs 1 boss | No timer | Future PvE content |

### 10.3 Flee Mechanics

**PvE — Per-Roomian Flee:**
- Flee costs 6 EN per Roomian
- Base success chance: 50%
- +5% per SPD advantage over fastest enemy
- -10% per level disadvantage
- **Success:** Roomian leaves the battle (downed but not dead, returns at 1 HP after battle)
- **Failed flee:** Roomian takes +50% damage next turn (punished)
- If all your Roomians flee = battle loss (no XP, no death saves)

**PvP — Team-Level Draw:**
- No individual flee in PvP — all 3 Roomians act together
- Either player can offer a draw from the action menu
- Both players must accept → battle ends as a draw (no XP for either side)
- If only one player offers and the other declines → battle continues

---

## 11. QUEST & TRAINING SYSTEM

### 11.1 Quest Types

| Quest | Duration | Risk | XP | Rewards | Notes |
|-------|----------|------|-----|---------|-------|
| **Forage** | 5 min | Safe | 15 XP | 10-30g, materials | No battle, stat-based success |
| **Scout** | 15 min | Low | 40 XP | 20-60g, ability scroll (chance) | 30% chance of wild encounter |
| **Hunt** | 30 min | Medium | 80 XP | 50-150g, Quality Room Ball | 60% chance of battle |
| **Deep Dive** | 60 min | High | 200 XP | 200-500g, Master Ball (rare) | Guaranteed boss battle |
| **Pre-Evolution** | 20 min | Medium | +100 XP | Bonus XP only | One-time, unlocks at L7 |

### 11.2 Quest Mechanics

- Send a Roomian on a quest → it's unavailable until quest completes
- Quest success chance based on Roomian stats + level
- Higher LCK = better rewards (gold + crit success chance)
- Higher GRT = safer quest (less risk of downing)
- Higher INT = faster quest completion (-20% duration, minimum 50% of base)
- Quest can fail → Roomian returns with reduced HP, no rewards
- Quest can crit succeed → bonus rewards (LCK-based, +50% gold + extra scroll)
- Roomian on a quest shows 🧭 icon on belt screen

**Quest progress events** (visible on belt screen, tap for detail):
```
┌─────────────────────────────────────────────────────────┐
│  🧭 Frostfang — Scout Quest                             │
│                                                         │
│  ▰▰▰▰▰▰░░░░ 60% complete (9 min remaining)             │
│                                                         │
│  EVENT LOG:                                             │
│  ✓ Found materials (+12g)                               │
│  ✓ Spotted wild Roomian (avoided)                       │
│  ⚠ Wild encounter triggering...                         │
│  → Auto-resolving battle...                             │
│  ✓ Battle won! (+40 XP, +1 ability scroll)              │
│  ▰▰▰▰▰▰▰▰░░ 80% complete (3 min remaining)             │
└─────────────────────────────────────────────────────────┘
```

**Design intent:** Quests aren't fire-and-forget. The event log gives players something to check — a mini-narrative of their Roomian's adventure. Seeing "battle won!" or "wild encounter avoided" creates micro-engagement during the wait. The log is non-interactive (no player input needed) but provides narrative payoff on return.

### 11.2b Quest Battle & Death Rules

Quests with battle risk (Scout, Hunt, Deep Dive) auto-resolve using the Wild AI (§10.1) — the Roomian plays itself, no player input.

- **Quest battles use the same death save system** — risk is real
- **Deep Dive explicitly warns:** "⚠️ WARNING: Your Roomian can permanently die on this quest"
- **If downed on quest:** Death save rolls automatically. On success → Roomian returns with 1 HP + scar. On 3 failures → Roomian permanently dies (memorial screen shown on return)
- **Mitigation:** Higher GRT reduces encounter difficulty. Higher level reduces failure chance. Deep Dive is the only quest with guaranteed battle — Scout/Hunt are chance-based
- **Forage:** Zero battle risk — completely safe, no death possible

### 11.3 Training

- Send a Roomian to training → unavailable for 10 min
- Returns with **+10 XP** and a **+1 permanent stat bump** to the trained stat
- Training stat is chosen by player (any of the 6 stats)
- Only 1 Roomian can train at a time
- Training shows 🩸 icon on belt screen
- Training CAN trigger level-ups if XP crosses the threshold — this is a feature, not a bug. The player returns to find their Roomian leveled up and ready to choose rewards.
- **Training efficiency scales with INT:** +1 XP per 5 INT (max +5 XP at INT 25). Smart Roomians train faster.

**Why +10 XP instead of +5:** At +5 XP, training was negligible — 68 training sessions to hit L10. At +10 XP, it's 34 sessions, still slow but meaningful as a supplementary XP source. Combined with quests and battles, training fills gaps when the player can't actively play.

### 11.4 Rest & Recovery

Since there are no potions, Roomians recover HP through rest:
- **Rest action:** Send a Roomian to rest → unavailable for 5 min → returns to full HP
- **Between battles:** Roomians automatically heal 50% HP after a battle ends (survivors only)
- **Downed Roomians:** Must rest to recover — they return at 1 HP after 10 min rest
- **Cooldowns:** After a battle, all surviving Roomians get a **5-min cooldown** (reduced from 10) before they can battle again. The shorter cooldown keeps the battle loop tight — 5 min is enough to rest or train another Roomian, not so long that the player disengages.
- Rest shows 😴 icon on belt screen
- Rest does NOT remove scars (scars are permanent)
- **Concurrent rest:** Multiple Roomians can rest simultaneously (unlike training, which is 1 at a time). This means after a 3v3 battle, all 3 survivors can rest in parallel and be ready in 5 min.

**Idle loop summary:**
```
After 3v3 battle (all survived):
  ├── All 3 Roomians: 5-min cooldown (can rest in parallel)
  ├── During cooldown:
  │   ├── Send 1 to Training (10 min, +10 XP, +1 stat)
  │   ├── Send 1 to Quest (5-60 min, XP + gold)
  │   └── Send 1 to Rest (5 min, full HP)
  ├── After 5 min: Resting Roomian ready, others still busy
  ├── After 10 min: Training Roomian ready (maybe leveled up!)
  └── Player checks event logs, manages team, returns to battle
```
This creates a natural rotation: battle → distribute tasks → check results → battle again. The player always has something to do or check.

---

## 11.5 SHOP & ECONOMY

### 11.5.1 Shop Inventory

| Item | Price | Unlock | Notes |
|------|-------|--------|-------|
| **Standard Room Ball** | 50g | Start | 75% catch rate |
| **Quality Room Ball** | 150g | Player L5 | 85% catch rate |
| **Master Room Ball** | 500g | Player L10 | 100% catch rate |
| **Random Ability Scroll** | 100g | Start | Random element, revealed on purchase |
| **Element Ability Scroll** | 300g | Player L5 | Choose element, random scroll from that element |
| **Specific Ability Scroll** | 800g | Player L8 | Choose element AND scroll from shop's rotating stock (3 scrolls available, rotates every 24h) |
| **Rest Boost** | 75g | Start | Instantly completes one Roomian's rest (skip the 5-min wait) |
| **Training Boost** | 100g | Player L3 | Instantly completes one Roomian's training (skip the 10-min wait, still get full rewards) |

### 11.5.2 Gold Sources

| Source | Gold | Notes |
|--------|------|-------|
| Quest: Forage | 10-30g | Scales with LCK |
| Quest: Scout | 20-60g | Scales with LCK |
| Quest: Hunt | 50-150g | Scales with LCK |
| Quest: Deep Dive | 200-500g | Scales with LCK |
| Quest: Pre-Evolution | 0g | Bonus XP only, no gold |
| Battle win (PvP) | 25g × enemy avg level | Small reward for PvP participation. Keeps PvP players solvent without making it a gold farm. |
| Battle win (PvE Raid) | 100-300g | Boss-level rewards |
| Battle win (flawless) | +50g bonus | Reward for no-loss victories |
| Training | 0g | Training is for stats, not gold |
| Selling Roomians | 0g | Cannot sell Roomians — they're companions, not commodities |
| Selling duplicate scrolls | 50g each | Scroll you already know → sell for gold. Gives scroll duplicates value. |

### 11.5.3 Design Rule
Gold has one purpose: buying Room Balls, Ability Scrolls, and time-skip Boosts. No pay-to-win, no premium currency. Gold is earned through risk (quests) and play (battles) and spent on opportunity (balls/scrolls) or convenience (boosts).

**Economy flow:**
```
EARN GOLD                    SPEND GOLD
┌──────────────┐             ┌───────────────────┐
│ Quests       │────────────▶│ Room Balls        │
│ (risk-based) │             │ (catch Roomians)  │
├──────────────┤             ├───────────────────┤
│ Battles      │────────────▶│ Ability Scrolls   │
│ (play-based) │             │ (learn abilities) │
├──────────────┤             ├───────────────────┤
│ Scroll sales │────────────▶│ Time Boosts       │
│ (duplicate)  │             │ (skip wait timers)│
└──────────────┘             └───────────────────┘

Early game: Gold is tight. 100g starter → 2 balls or 1 scroll.
             Every ball matters. Catching is a real decision.
Mid game:   Quests + battles provide steady income. Player buys
             Quality Balls and Element Scrolls. Gold feels earned.
Late game:  Deep Dive quests (200-500g) + flawless bonuses fund
             Master Balls and Specific Scrolls. Time Boosts become
             appealing for players who want to play faster.
```

**Why time-skip Boosts exist:** They give late-game players a gold sink without adding power. A player with 2000g and nothing to buy can skip rest/training timers. This is convenience, not power — the rewards are the same, just faster. It's the "whale sink" that doesn't break balance.

---

## 11.6 STARTER PACKAGE & ONBOARDING

### 11.6.1 Starter Package

New players begin with:
- **1 L0 Blob** (neutral, no element — element chosen at L1 evolution)
- **3 Standard Room Balls**
- **100g** (enough for 2 more balls or 1 random scroll)

### 11.6.2 Tutorial Flow (First Session)

```
Step 1: FIRST BATTLE (guided 1v1 vs AI Blob)
  ├── Player's Blob vs AI Blob (both L0, neutral)
  ├── Teaches: planning phase, action selection, execution
  ├── AI is passive (only uses Tackle, never Defends)
  └── Win → Level up to L1 → triggers Step 2

Step 2: FIRST EVOLUTION (guided L1 choice)
  ├── All 6 element cards shown
  ├── Teaches: evolution is permanent, each element has a playstyle
  ├── Tooltips explain: Fire = DPS, Water = Defense, Earth = Tank, etc.
  └── Pick → Blob evolves → triggers Step 3

Step 3: FIRST CATCH (guided wild encounter)
  ├── Wild L0 Blob appears on hub screen
  ├── Teaches: throw ball, 75% success, identity hidden until caught
  ├── This catch is scripted to succeed (100% for tutorial)
  └── Caught → added to storage → tutorial complete → free play unlocked
```

### 11.6.3 Design Rule
The tutorial teaches the three core verbs (battle, evolve, catch) in one 5-minute session. No text walls — the player does each thing once with gentle guidance, then they're free.

---

## 11.7 HUB STRUCTURE (MVP)

The MVP doesn't need a world map. A menu-driven hub is sufficient:

```
┌─────────────────────────────────────────────────────────┐
│                    ROOMIAN HUB                          │
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   EXPLORE   │  │   BATTLE    │  │   BELT      │    │
│  │   Find wild │  │   PvP/PvE  │  │   Manage    │    │
│  │   Roomians  │  │   Fight    │  │   Team      │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   QUEST     │  │   SHOP      │  │   TRAIN     │    │
│  │   Send on   │  │   Buy balls │  │   Stat drip │    │
│  │   missions  │  │   + scrolls │  │   + XP      │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
│                                                         │
│  Active Team: [🔥 L7] [❄️ L5] [☠️ L3]   Gold: 240g   │
└─────────────────────────────────────────────────────────┘
```

**Hub Actions:**
- **EXPLORE:** Generates a random wild L0 Blob encounter → catch opportunity (consumes a Room Ball)
- **BATTLE:** PvP matchmaking (challenge code or auto-match) or PvE raid selection
- **BELT:** Manage Roomians — view stats, swap active team, evolve, learn abilities, rest
- **QUEST:** Send a Roomian on a timed quest (Forage/Scout/Hunt/Deep Dive)
- **SHOP:** Buy Room Balls and Ability Scrolls with gold
- **TRAIN:** Send a Roomian to training (10 min, +5 XP + small stat bump)

**Design Rule:** The hub is a launchpad, not a destination. Players spend 90% of their time in battle, evolution, and management screens. The hub gets them there fast.

---

## 12. ROOMIAN DATA MODEL (Updated)

```json
{
  "id": "roomian_001",
  "name": "Emberblade",
  "species": "Blob",
  "level": 7,
  "xp": 320,
  "xpToNext": 380,
  
  "color": "#FF6B35",
  "auraColor": "#FFD23F",
  
  "evolutionPath": {
    "l1": "fire",
    "l5": "blaze",
    "l8": null,
    "l10": null
  },
  
  "stats": {
    "vit": 12,
    "pwr": 18,
    "grt": 10,
    "spd": 14,
    "lck": 8,
    "int": 11
  },
  
  "derivedStats": {
    "maxHp": 55,
    "currentHp": 42,
    "maxEn": 37,
    "currentEn": 15,
    "dodge": 7,
    "crit": 8
  },
  
  "abilities": {
    "active": {
      "slot1": {"id": "tackle", "source": "L0_base", "fixed": true},
      "slot2": {"id": "ember_strike", "source": "L1_evolution", "fixed": true},
      "slot3": {"id": "fire_spin", "source": "L3_choice", "fixed": false},
      "slot4": {"id": "flame_slash", "source": "L5_evolution", "fixed": true}
    },
    "passive": {
      "slot1": {"id": "burn_touch", "source": "L1_evolution", "fixed": true},
      "slot2": {"id": "flame_body", "source": "L4_choice", "fixed": false},
      "slot3": null
    },
    "learned": ["tackle", "ember_strike", "fire_spin", "flame_slash", "burn_touch", "flame_body", "pulse"]
  },
  
  "scars": [
    {"type": "weakened", "stat": "pwr", "amount": -2, "date": "2026-07-25"},
    {"type": "lobotomized", "failChance": 0.25, "date": "2026-07-25"}
  ],
  
  "status": "ready",
  "cooldownUntil": null,
  "deathSaves": {"successes": 0, "failures": 0, "resetPerBattle": true},
  "isDowned": false,
  
  "stats_tracked": {
    "battlesTotal": 12,
    "battlesWon": 7,
    "questsCompleted": 3,
    "deathsSurvived": 2,
    "scarsGained": 2
  }
}
```

---

## 13. SUMMARY OF ADDITIONS SINCE FIRST DOC

| Addition | Details |
|----------|---------|
| **INT stat** | Affects Energy pool, skill learning, quest success |
| **Two-roll damage formula** | (abilityPower + PWR) × rand(0.8–1.2) − GRT, crits ×1.5 post-GRT |
| **Energy (EN)** | Unified resource for all abilities, regens 3+floor((GRT+INT)/5) per turn |
| **SPD (Speed)** | Renamed from FOC — determines round initiative order |
| **3v3 simultaneous battles** | All 3 Roomians on screen at once with idle animations |
| **Tap-to-assign actions** | Tap each Roomian → animated modal opens for action selection |
| **Target selection** | Valid targets glow/pulse, invalid (dead) dimmed — tap to pick |
| **Speed-based round resolution** | All actions resolve in SPD order, one at a time with animations |
| **Versus splash screen** | Animated intro showing both teams before battle |
| **36 evolution forms** | 6 primal elements × 3 refinements × 2 masteries |
| **Evolution at L1/L5/L8** | Permanent branching choices, visually distinct |
| **Skill learning** | Level-up rewards, scrolls, INT-gated tiers |
| **Passive ability slots** | 3 total, filled at L1/L4/L8 |
| **Stat choice on level** | Pick +2 to one of 3 random stats each level |
| **Prestige at L10** | Cosmetic golden aura, no mechanical bonus |
| **Battle action types** | Attack, Magic, Defend, Flee (no Swap — all 3 active) |
| **Death save screens** | Full visual mockups for survival + death + scar roll |
| **Memorial system** | Downed Roomians get a memorial on permanent death |
| **2 resource bars** | HP (red), EN (cyan) under each Roomian sprite |
| **Planning timer** | 20s PvP, no timer PvE — unassigned Roomians auto-Defend |
| **Evolution ability stacking** | Roomians keep all abilities from every evolution tier (L1 + L5 + L8) |
| **Scroll system** | Unlimited inventory, element-locked, tradable scroll-for-scroll between players |
| **Throw-and-reveal catch** | No battle — throw ball, 75% success, hidden identity revealed on catch |
| **Status effects** | 7 element-based statuses with stacking rules |
| **Death save reset** | Counter resets every battle — scars persist, saves do not |
| **Wild AI** | Simple decision tree for PvE battles (raids, future content) |
| **Battle formats** | 1v1, 2v2, 3v3 PvP (20s timer) + 1v3 Raid (no timer) |
| **Flee mechanics** | PvE: per-Roomian, SPD-based, punished on fail. PvP: team-level draw, both must agree |
| **Quest system** | 4 quest types (Forage/Scout/Hunt/Deep Dive), auto-resolved battles, death risk on Deep Dive |
| **Training** | Slow stat drip, 10 min sessions |
| **Shop & economy** | Gold earned from quests/raids → spent on Room Balls + Ability Scrolls |
| **Starter package** | 1 L0 Blob + 3 Standard Balls + 100g, 3-step tutorial (battle → evolve → catch) |
| **Hub structure** | Menu-driven hub (Explore/Battle/Belt/Quest/Shop/Train) — no world map for MVP |
| **L8 stat bonuses** | +5 primary + +2 secondary per mastery, matching refinement identity (DPS/Tank/Mage) |
| **Status cures** | Ability-based (Light cleanse), not items — aligns with "no consumable clutter" pillar |
| **Quest death rules** | Quest battles auto-resolve with Wild AI, death saves apply, Deep Dive warns of permanent death |

---

*This document is the comprehensive visual pictation. See `roomian_systems_assessment.md` for dev readiness verdict. See `roomian_races_art_direction.md` for art pipeline.*
