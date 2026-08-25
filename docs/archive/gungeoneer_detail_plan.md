# GungeonMate — Gungeoneer Detail Views & Spoiler System Plan

> Created: Aug 2026, v1.9.28
> Status: PLANNING ONLY — no code changes yet
> Depends on: wiki.gg Gungeoneers page (verified), existing character_select_screen.dart, codex_screen.dart
>
> **Sources cross-referenced (5):**
> 1. wiki.gg — Official Enter the Gungeon Wiki (primary) — enterthegungeon.wiki.gg
> 2. Fandom Wiki (secondary) — enterthegungeon.fandom.com
> 3. IGN Guides (third) — ign.com/wikis/enter-the-gungeon
> 4. Giant Bomb Wiki (fourth) — giantbomb.com/wiki/Games/Enter_the_Gungeon
> 5. Gameranx (fifth) — gameranx.com (Paradox/Gunslinger unlock guides)
>
> **Cross-source agreement: 100% on starting loadouts.** All 5 sources agree on
> weapons, items, and armor for all 9 gungeoneers. No discrepancies found between
> sources on any starting loadout data.

---

## 1. Objective

Add a **? info button** to each gungeoneer card on the Character Select screen. Tapping it opens a **Gungeoneer Detail View** — a rich, scrollable page showing:

1. Character art (large)
2. Short description / lore intro
3. Starting loadout (guns + items) as tappable inventory tiles → link to existing ItemDetailScreen
4. Gameplay tips section
5. Spoiler-tagged sections (collapsed by default):
   - Past story summary
   - Past kill details
   - Unlock method
   - Alternate costume / weapon skin unlocks

The same detail view is also accessible from the **Codex** under a new "Gungeoneers" category.

A reusable **SpoilerTag widget** powers the collapsed/expanded spoiler sections.

---

## 2. Wiki-Verified Starting Loadout Data

Source: https://enterthegungeon.wiki.gg/wiki/Gungeoneers (verified Aug 2026)

### Default Gungeoneers (available from start)

| Gungeoneer | Starting Weapons | Starting Items | Notes |
|---|---|---|---|
| **The Convict** | Budget Revolver, Sawed-Off | Molotov, Enraging Photo | — |
| **The Hunter** | Rusty Sidearm, Crossbow | Dog | Smallest loadout (3 items) |
| **The Marine** | Marine Sidearm | Supply Drop, Military Training, 1× Armor | Starts with extra armor |
| **The Pilot** | Rogue Special | Trusty Lockpicks, Disarming Personality, Hidden Compartment | Largest item loadout |
| **The Cultist** | Dart Gun | Friendship Cookie, Number 2 | Co-op only |

### Unlockable Gungeoneers

| Gungeoneer | Starting Weapons | Starting Items | Unlock Method |
|---|---|---|---|
| **The Bullet** | Blasphemy | Live Ammo | Spare 5 Red-Caped Bullet Kin |
| **The Robot** | Robot's Right Hand | Battery Bullets, Coolant Leak | Bring Busted Television to the Blacksmith |
| **The Paradox** | Random starter weapon + Random non-starter weapon | Random passive item | Find & interact with cosmic rift after defeating any Gungeoneer's past, then defeat the Lich or kill the character's past |
| **The Gunslinger** | Slinger | Lich's Eye Bullets | As The Paradox, defeat the Lich, then kill the Gunslinger's past on the next run |

### Current JSON vs Wiki — Discrepancies Found (confirmed by all 5 sources)

| Gungeoneer | Current JSON | All Sources Say | Fix Needed |
|---|---|---|---|
| The Marine | items: [Supply Drop] | Supply Drop, Military Training, 1× Armor | **ADD** Military Training + Armor |
| The Paradox | guns: [], items: [] | Random starter + random non-starter weapon, random passive | **ADD** descriptive placeholders |
| The Gunslinger | items: [] | Lich's Eye Bullets | **ADD** Lich's Eye Bullets |

### Cross-Source Verification Notes

**Starting loadouts** — 100% agreement across all 5 sources. No discrepancies.

**The Marine's armor** — wiki.gg, Fandom, IGN, and Giant Bomb all confirm he starts with 1 extra piece of Armor. IGN specifically calls it "Helmet (Starts with 1 Armor)". This is not an item in `items.json` — it's a gameplay mechanic. We'll represent it as a `starting_armor: 1` field and show a special armor tile in the UI.

**The Robot's armor** — wiki.gg and Fandom both confirm: starts with 6 armor, no hearts, cannot gain heart containers, immune to electricity, each piece of Junk grants 5% damage increase. This is a unique mechanic worth highlighting in the playstyle section.

**The Paradox's cost** — wiki.gg and Fandom confirm it costs 5 Hegemony Credits to play. The Gunslinger costs 7 Hegemony Credits. These are the only two characters with a play cost.

**The Paradox's random loadout** — wiki.gg and Fandom confirm: random starting sidearm from other Gungeoneers (excluding Slinger), plus another random gun (non-starter), plus a random passive item. Can spawn with weapons from unlocked Gungeoneers. Items are chosen at character select time but the item doesn't appear until run starts.

**The Cultist's past** — wiki.gg and Fandom confirm: The Cultist's past is a PvP duel in The Breach against Player 1 using Magnums. Each player has 3 hearts and 2 blanks. Regardless of who wins, the alternate costume is unlocked. This is unique — the only PvP past.

**The Gunslinger's past** — wiki.gg confirms: unlike other pasts, you keep all health and items from the run. Fight two Liches simultaneously (one normal, one Paradox-jammed with increased health). Both use only first phase. Must get Bullet That Can Kill The Past from Blacksmith before entering Aimless Void or it just shows credits.

**The Bullet's unlock** — wiki.gg confirms: spare 5 Red-Caped Bullet Kin (not kill — they must teleport away naturally after 10-30 seconds). They only spawn on first wave. Multiple can appear in one run. More likely in later chambers.

**The Robot's unlock** — wiki.gg and IGN confirm: bring Busted Television from Gungeon Proper elevator maintenance room to Blacksmith in the Forge. TV can be thrown across pits. Avoid dodge rolling into closed rooms.

---

## 3. Data Model Changes

### 3.1 `gungeoneers.json` — Extended Schema

Current schema:
```json
{
  "name": "The Marine",
  "starting_guns": ["Marine Sidearm"],
  "starting_items": ["Supply Drop"],
  "icon": ""
}
```

Proposed extended schema:
```json
{
  "name": "The Marine",
  "starting_guns": ["Marine Sidearm"],
  "starting_items": ["Supply Drop", "Military Training"],
  "starting_armor": 1,
  "icon": "",
  "short_desc": "A reliable soldier who starts with extra armor and accurate weaponry.",
  "lore_intro": "The Marine was a guard stationed at Primerdyne R&D when an experiment went awry, unleashing an Interdimensional Horror into the facility. He chose to flee, abandoning his fellow guardsmen. Wracked by guilt, he travelled to the Gungeon to undo the past.",
  "playstyle": "Reliable and durable. The Marine has the least variance in playstyle — his starting weapon has high clip size, decent damage, and high accuracy. The extra armor makes him more forgiving for new players.",
  "tips": [
    "Military Training increases accuracy — use it at mid-range",
    "Supply Drop provides ammo in a pinch — save it for boss fights",
    "The extra armor absorbs one hit — play slightly more aggressively early"
  ],
  "nicknames": ["Tough Guy", "Soldier", "Meathead"],
  "voice": "manly",
  "hegemony_cost": 0,
  "unlock_method": "Available from the start",
  "is_default": true,
  "is_coop_only": false,
  "past_name": "Primerdyne R&D",
  "past_summary": "SPOILER: The Marine returns to Primerdyne R&D before he left for the escape pods. He must defeat the Interdimensional Horror to save his fellow soldiers.",
  "past_loadout": "Marine Sidearm, Hegemony Carbine, Military Training",
  "past_details": "SPOILER: An injured scientist reveals something came through a dimensional opening. The Marine enters the lab to find soldiers taking cover. The Interdimensional Horror emerges from a portal. Defeating it saves everyone (except the hallway scientist).",
  "past_unlocks": "Galactic Medal of Valor + Military Training (for all characters)",
  "alt_costume_name": "Knight",
  "alt_costume_unlock": "Kill The Marine's past",
  "alt_weapon_skin_unlock": "Kill The Marine's past with alternate costume equipped",
  "wiki_url": "https://enterthegungeon.wiki.gg/wiki/The_Marine"
}
```

### 3.2 `Gungeoneer` Dart Model — Extended Fields

```dart
class Gungeoneer {
  final String name;
  final String icon;
  final List<String> startingGuns;
  final List<String> startingItems;
  final int startingArmor;           // NEW
  final String shortDesc;            // NEW
  final String loreIntro;            // NEW
  final String playstyle;            // NEW
  final List<String> tips;           // NEW
  final List<String> nicknames;      // NEW (fun trivia)
  final String voice;                // NEW (fun trivia)
  final int hegemonyCost;            // NEW (0 = free, 5 = Paradox, 7 = Gunslinger)
  final String unlockMethod;         // NEW
  final bool isDefault;              // NEW
  final bool isCoopOnly;             // NEW
  final String pastName;             // NEW (spoiler)
  final String pastSummary;          // NEW (spoiler)
  final String pastLoadout;          // NEW (spoiler)
  final String pastDetails;          // NEW (spoiler)
  final String pastUnlocks;          // NEW (spoiler — what killing past grants)
  final String altCostumeName;       // NEW (spoiler — skin name)
  final String altCostumeUnlock;     // NEW (spoiler)
  final String altWeaponSkinUnlock;  // NEW (spoiler)
  final String wikiUrl;              // NEW
  // ... existing constructor/fromJson/toJson
}
```

---

## 4. UI Components

### 4.1 `SpoilerTag` Widget (reusable)

**File:** `lib/widgets/spoiler_tag.dart`

A collapsible section that hides content behind a "SPOILER" banner. Tapping reveals the content with a smooth expand animation.

```
┌─────────────────────────────────────┐
│  ⚠ SPOILER — Past Story             │  ← tap to reveal
│  TAP TO REVEAL                      │
└─────────────────────────────────────┘
         (collapsed state)

┌─────────────────────────────────────┐
│  ⚠ SPOILER — Past Story          ▼  │  ← tap to collapse
│─────────────────────────────────────│
│  The Marine returns to Primerdyne   │
│  R&D before he left for the escape  │
│  pods...                            │
└─────────────────────────────────────┘
         (expanded state)
```

**Props:**
- `title` — section label (e.g. "Past Story", "Past Kill Details", "Unlock Method")
- `child` — the spoiler content widget
- `defaultExpanded` — false by default

**Behavior:**
- Uses `AnimatedSize` for smooth expand/collapse
- Amber/warning color for the spoiler banner (consistent with Gungeon aesthetic)
- Haptics on tap
- State is local (resets on close — no persistence needed)

### 4.2 `GungeoneerDetailScreen`

**File:** `lib/screens/gungeoneer_detail_screen.dart`

A full-page scrollable detail view. Layout (top to bottom):

```
┌─────────────────────────────────────┐
│  ←  THE MARINE                      │  AppBar
├─────────────────────────────────────┤
│                                     │
│         [Large Character Art]       │  Hero section
│         (animated card asset)       │  200px height
│                                     │
│  "A reliable soldier who starts     │  Short desc
│   with extra armor..."              │  (italic, dim)
│                                     │
│  Nicknames: Tough Guy, Soldier,     │  Trivia (small, dim)
│  Meathead · Voice: manly            │
│                                     │
├─────────────────────────────────────┤
│  STARTING LOADOUT                   │  Section label
│                                     │
│  ┌──────┐ ┌──────┐                  │  Gun tiles
│  │Marine│ │  —   │                  │  (tappable →
│  │Sidearm│ │      │                  │   ItemDetailScreen)
│  └──────┘ └──────┘                  │
│  WEAPONS                             │
│                                     │
│  ┌──────┐ ┌──────┐ ┌──────┐        │  Item tiles
│  │Supply│ │Milit.│ │Armor │        │  (tappable →
│  │ Drop │ │Train.│ │  ×1  │        │   ItemDetailScreen)
│  └──────┘ └──────┘ └──────┘        │
│  ITEMS                               │
│                                     │
├─────────────────────────────────────┤
│  PLAYSTYLE                           │  Section label
│                                     │
│  Reliable and durable. The Marine   │  Playstyle text
│  has the least variance in          │
│  playstyle...                       │
│                                     │
├─────────────────────────────────────┤
│  TIPS                                │  Section label
│                                     │
│  • Military Training increases      │  Tip bullets
│    accuracy — use at mid-range      │
│  • Supply Drop saves ammo for       │
│    boss fights                      │
│  • Extra armor absorbs one hit      │
│                                     │
├─────────────────────────────────────┤
│  ⚠ SPOILER — Past Story             │  SpoilerTag
│  TAP TO REVEAL                      │  (collapsed)
│                                     │
│  ⚠ SPOILER — Past Kill Details      │  SpoilerTag
│  TAP TO REVEAL                      │  (collapsed)
│  (includes past loadout + boss)     │
│                                     │
│  ⚠ SPOILER — Past Kill Unlocks      │  SpoilerTag (NEW)
│  TAP TO REVEAL                      │  (what killing past grants)
│                                     │
│  ⚠ SPOILER — Unlock Method          │  SpoilerTag
│  TAP TO REVEAL                      │  (collapsed)
│                                     │
│  ⚠ SPOILER — Alternate Unlocks      │  SpoilerTag
│  TAP TO REVEAL                      │  (alt costume name + skin)
│                                     │
├─────────────────────────────────────┤
│  [View on Wiki.gg →]                │  External link
└─────────────────────────────────────┘
```

**For Paradox/Gunslinger only — additional cost badge:**
```
│  Cost: 5 Hegemony Credits           │  Below short desc (amber badge)
```

**For The Cultist only — co-op badge:**
```
│  [CO-OP ONLY]                       │  Below short desc (cyan badge)
```

**For The Robot only — special mechanics callout:**
```
│  SPECIAL: 6 Armor, No Hearts        │  Below short desc (amber badge)
│  Junk = +5% permanent damage        │
```

**Key behaviors:**
- Character art uses existing `gungeoneerAnimatedCardPath()` asset
- Loadout tiles are compact 64×64 icons with name labels below
- Tapping a gun tile → `Navigator.push(fastRoute(ItemDetailScreen(gun: g)))`
- Tapping an item tile → `Navigator.push(fastRoute(ItemDetailScreen(item: i)))`
- Armor shown as a special tile with "×1" badge if `startingArmor > 0`
- The Paradox shows "Random" tiles with question mark icons
- Spoiler sections use `SpoilerTag` widget
- Wiki link opens external browser via `url_launcher`

### 4.3 Character Select Card — `?` Button

**File:** `lib/screens/character_select_screen.dart` (modify `_CharacterCard`)

Add a `?` icon button to the top-right corner of each card:

```
┌─────────────┐
│          [?]│  ← new info button
│   [art]     │
│             │
│  The Marine │
└─────────────┘
```

- 20×20 circular button, semi-transparent background
- `Icons.help_outline` or `Icons.question_mark`
- Tapping opens `GungeoneerDetailScreen` via `Navigator.push`
- Does NOT trigger character selection (separate tap target)
- Positioned in `Stack` over the card art, `Alignment.topRight`

### 4.4 Codex — New "Gungeoneers" Category

**File:** `lib/screens/codex_screen.dart` (modify)

Add a new category tile to the codex category strip:

```dart
_CategoryDef(
  label: 'Gungeoneers',
  icon: Icons.person_pin,
  color: Color(0xFF42A5F5),
  isSpecial: true,  // renders as special page, not data list
),
```

The special page is a simple grid of gungeoneer cards (same art as character select, but tap opens `GungeoneerDetailScreen` instead of selecting).

**File:** `lib/screens/gungeoneer_codex_screen.dart` (new)

A simple grid showing all gungeoneers. Tapping any card opens `GungeoneerDetailScreen`. No search needed (only 9 entries).

---

## 5. Implementation Phases

### Phase 1: Data Layer (no UI changes)
1. Extend `gungeoneers.json` with all new fields for all 9 gungeoneers:
   - `short_desc`, `lore_intro`, `playstyle`, `tips[]`
   - `nicknames[]`, `voice`, `hegemony_cost`
   - `starting_armor`, `is_default`, `is_coop_only`
   - `past_name`, `past_summary`, `past_loadout`, `past_details`, `past_unlocks`
   - `alt_costume_name`, `alt_costume_unlock`, `alt_weapon_skin_unlock`
   - `unlock_method`, `wiki_url`
2. Fix the 3 data discrepancies (Marine items, Paradox loadout, Gunslinger items)
3. Extend `Gungeoneer` Dart model with new fields + `fromJson`/`toJson`
4. Verify JSON loads correctly

### Phase 2: SpoilerTag Widget
1. Create `lib/widgets/spoiler_tag.dart`
2. Collapsible banner with amber warning color
3. `AnimatedSize` expand/collapse
4. Haptics on tap
5. Hide entirely if content is empty
6. Test in isolation

### Phase 3: GungeoneerDetailScreen
1. Create `lib/screens/gungeoneer_detail_screen.dart`
2. Hero art section (animated card asset)
3. Short desc + lore intro
4. Nicknames/voice trivia line (if non-empty)
5. Special badges: CO-OP ONLY (Cultist), Cost (Paradox/Gunslinger), SPECIAL MECHANICS (Robot)
6. Starting loadout grid (guns + items + armor)
7. Tappable tiles → `ItemDetailScreen`
8. Playstyle + tips sections
9. 5 spoiler sections: Past Story, Past Kill Details, Past Kill Unlocks, Unlock Method, Alternate Unlocks
10. Wiki link button
11. Handle The Paradox's random loadout (placeholder tiles)
12. Handle The Robot's armor display (6 armor tiles or special badge)

### Phase 4: Character Select Integration
1. Add `?` button to `_CharacterCard` in `character_select_screen.dart`
2. Position in `Stack` top-right
3. Tap → `GungeoneerDetailScreen`
4. Verify it doesn't interfere with card tap-to-select

### Phase 5: Codex Integration
1. Add "Gungeoneers" category to `codex_screen.dart`
2. Create `lib/screens/gungeoneer_codex_screen.dart` (grid of cards)
3. Tap → `GungeoneerDetailScreen`
4. Verify navigation works from both entry points

### Phase 6: Polish & Test
1. Verify all 9 gungeoneers display correctly
2. Verify spoiler tags collapse/expand properly
3. Verify loadout tiles link to correct ItemDetailScreen
4. Verify The Paradox shows random placeholders
5. Verify The Cultist shows "Co-op only" badge
6. Verify The Robot shows special mechanics badge
7. Verify Paradox/Gunslinger show Hegemony cost
8. Verify empty fields hide their sections gracefully
9. Run `flutter analyze`
10. Test on small screen (overflow check)

---

## 6. Gungeoneer Data Summary (for JSON enrichment)

> Cross-referenced against wiki.gg, Fandom, IGN, Giant Bomb, and Gameranx.
> All starting loadouts confirmed by 100% of sources. Strategy text adapted
> from wiki.gg individual character pages (most detailed).

### The Marine
- **Short desc:** "A reliable soldier who starts with extra armor and accurate weaponry."
- **Lore:** Guard at Primerdyne R&D. Fled when experiment unleashed Interdimensional Horror, abandoning fellow guardsmen. Seeks to undo his cowardice.
- **Playstyle:** Reliable, low variance. Marine Sidearm has high clip size, decent damage, high accuracy, quick reload — viable for entire first floor. Military Training boosts accuracy and reload speed. Extra armor makes him more durable and forgiving for beginners. Best for players who want to simply blast through the Gungeon.
- **Tips:**
  - Military Training makes shotguns effective at medium-long range
  - Supply Drop is a guaranteed ammo drop — save it for emergencies or later floors
  - Extra armor absorbs one hit — play slightly more aggressively early
  - His sidearm is the most powerful of the standard infinite-ammo weapons
  - Lacks special bonuses like Hunter's Dog or Pilot's item variety
- **Past:** Primerdyne R&D — defeat the Interdimensional Horror to save fellow soldiers. Loadout: Marine Sidearm, Hegemony Carbine, Military Training.
- **Unlocks:** Available from the start. Alt costume: kill past. Alt weapon skin: kill past with alt costume.

### The Pilot
- **Short desc:** "A smuggler with lockpicks, charm, and a hidden compartment — high variance, high reward."
- **Lore:** Space smuggler who abandoned his friend Z to the Hegemony. Seeks to change the past and save Z.
- **Playstyle:** Highest variance of all Gungeoneers. Rogue Special is the weakest starting weapon — low damage, high spread, pitiful range. But his items make up for it: Trusty Lockpicks open any locked object, Disarming Personality reduces shop prices, Hidden Compartment gives 10% extra ammo and an extra active slot. Best for resource-gathering runs and Tinker quests.
- **Tips:**
  - Lockpicks can break — if you have a key, use it on the more valuable chest
  - Disarming Personality stacks with other price reductions
  - Hidden Compartment is huge for active-item builds — carry 2 actives
  - Hidden Compartment makes retrieving Prime Primer, Arcane Gunpowder, and Busted TV easier
  - Early game is tough — prioritize finding decent weapons quickly
- **Past:** Hegemony Space — fight HM Absolution in a spaceship. No weapons — uses ship's built-in weapons and a rocket-firing active item. Choice: "Divert power to forward weapons" or "Escape to the Warp" (only first option progresses).
- **Unlocks:** Available from the start. Alt costume: kill past. Alt weapon skin: kill past with alt costume.

### The Convict
- **Short desc:** "A damage-focused fighter with a sawed-off and an enraging photo."
- **Lore:** Former crime boss "Laser Lily." Betrayed by Hegemony official Black Stache. Chooses Gungeon over life imprisonment.
- **Playstyle:** High damage, low range. Budget Revolver has fast fire rate but only 5-round magazine — hit-and-run playstyle. Sawed-Off is devastating up close but damage falls off quickly with distance. Enraging Photo boosts damage AND instantly reloads after taking damage. Molotov provides reusable area denial. Best for aggressive players who don't mind taking hits.
- **Tips:**
  - Enraging Photo also instantly reloads your weapon — can disrupt guns with special final shots (Teapot, Mailbox, Judge)
  - Molotov isn't consumed on use — reuse throughout the run
  - Molotov is risky in small rooms — get fire resistance items first
  - Wait for enemies to finish attack cycles before closing range with Sawed-Off
  - Intentionally taking damage for the buff is NOT advised unless you really know what you're doing
- **Past:** Nightclub 'Confession' — fight Black Stache and Hegemony goons. Loadout: Budget Revolver, Thompson Sub-Machinegun, Enraging Photo, Molotov. Escape in a Hovercar.
- **Unlocks:** Available from the start. Alt costume: kill past. Alt weapon skin: kill past with alt costume.

### The Hunter
- **Short desc:** "A patient hunter with a dog companion and a crossbow for precise shots."
- **Lore:** Fought Dr. Wolfenclaw at Blacksword Manor 1,147 years ago. Captured and stored in a cryo-pod until the Gungeon events. How she escaped is unknown.
- **Playstyle:** Smallest loadout (3 items). Rusty Sidearm is average — decent damage but only 6 shots and slower bullets. Crossbow is the strongest starting gun in damage — can 1-2 shot first-floor enemies, extremely ammo efficient, can clear most of floor 1 alone. Dog has 5% chance to dig up pickups (coins, hearts, armor, blanks, keys, ammo, maps) after clearing rooms. Strongest early game of the 4 main Gungeoneers.
- **Tips:**
  - Dog's finds are separate from room rewards — you can get both
  - Resourceful Rat steals armor and ammo left in rooms — pick them up immediately
  - Dog barks at Mimics — less useful for experienced players
  - Crossbow is extremely ammo efficient — use it as primary on floor 1
  - Crossbow has extreme range — stay far from enemies to take less damage
- **Past:** Blacksword Manor — defeat Dr. Wolfenclaw's monster. Use a Blank to escape bullet trap. Loadout: Colt 1851, Sticky Crossbow, Wolf. Can choose "Give up" but Hunter refuses: "Never! I'm not getting frozen again!"
- **Unlocks:** Available from the start. Alt costume: kill past. Alt weapon skin: kill past with alt costume.

### The Bullet
- **Short desc:** "A sentient bullet that slashes enemy projectiles with Blasphemy."
- **Lore:** A Bullet Kin who took up a sword to save their home against the invading threat of Cannon. Became a pariah among their people for using forbidden weaponry.
- **Playstyle:** Unique melee playstyle. Blasphemy cleaves bullets with every slice and fires a piercing sword projectile at full health. Live Ammo grants immunity to contact damage and makes dodge rolls an attack. Excellent for earning Master Rounds. Drawback: losing even one heart piece removes ranged attack and halves damage. Must top off health or hoard armor. Damage output drops on later floors as enemies gain health.
- **Tips:**
  - Blasphemy only fires piercing projectile at FULL health — prioritize healing
  - Live Ammo makes contact-damage enemies (Spent, Blobulons, cubes) completely harmless
  - Swinging causes a slight lunge — don't swing carelessly near pits
  - Hoard armor to maintain full health and keep ranged attack
  - Many challenging bosses become trivial due to bullet-cleaving
- **Past:** Gungeon Proper — retrieve Blasphemy from a dying elder bullet. Fight two Chain Gunners, then Agunim, then Cannon. Thrust wooden Blasphemy into Cannon's head to create the true Blasphemy.
- **Unlocks:** Spare 5 Red-Caped Bullet Kin (let them teleport away naturally after 10-30 seconds — do NOT kill them). They only spawn on first wave. Multiple can appear per run. More likely in later chambers. Alt costume: kill past. Alt weapon skin: kill past with alt costume.

### The Robot
- **Short desc:** "A mechanical gungeoneer with 6 armor, no hearts, and a junk-powered damage boost."
- **Lore:** A "Shock Troop" killbot manufactured by the Imperial Hegemony of Man. Broke protocol and refused to eliminate the last human warrior, turning the tide of the ten days war. Fled to the Gungeon, pursued by a detective.
- **Playstyle:** Armor-as-health gimmick: starts with 6 armor (equivalent of 3 hearts), cannot gain hearts or pick up health. Armor grants free blank effect when hit (reveals secret rooms). Negates jammed enemy extra damage. Each piece of Junk grants permanent 5% damage increase (persists even if junk is dropped/sold). Battery Bullets give double accuracy and electricity immunity. Coolant Leak leaves ice goop. Master Rounds grant armor instead of hearts. Heart-container items give 5-10 shells instead.
- **Tips:**
  - Destroy chests for Junk instead of buying keys — 5% damage per junk is permanent
  - Armor is lost permanently when hit — buy armor in shops to recover
  - Free blank effect on hit reveals secret rooms — pay attention after taking damage
  - Coolant Leak + Battery Bullets = electrified ice combo
  - Better against jammed enemies than other characters (no extra damage taken)
  - Dodge roll deals 1 more damage than other Gungeoneers
- **Past:** Gladiatorial arena of robot overlord EMP-R0R. Instead of breaking protocol, successfully eliminates The Last Human. Powered down with the rest of the killbot army.
- **Unlocks:** Bring Busted Television from Gungeon Proper elevator maintenance room to Blacksmith in the Forge. TV can be thrown across pits. Avoid dodge rolling into closed rooms (TV gets stuck). Pilot's Hidden Compartment helps carry it. Alt costume: kill past. Alt weapon skin: kill past with alt costume.

### The Cultist
- **Short desc:** "A co-op-only companion who supports their partner — born to be P2."
- **Lore:** A child of the Gungeon, implied to have been born there. Grows jealous of the protagonist's importance over the course of a run. NPCs never call them "Cultist" — always "Mysterious Companion" or a random nickname.
- **Playstyle:** Co-op only. Dart Gun is very weak. Friendship Cookie is a single-use revive for Player 1. Number 2 provides backup support. When entering another Gungeoneer's past, only has a Dart Gun.
- **Tips:**
  - Friendship Cookie is single-use — save it for emergencies
  - Stay close to your partner — you're support, not the protagonist
  - Dart Gun is for tagging enemies, not killing
  - If Player 1 dies, they become a ghost that can detonate free blanks
  - Beat floor bosses to revive a dead partner
- **Past:** The Breach — a PvP duel against Player 1 using Magnums. Each player has 3 hearts and 2 blanks. The Breach is empty of NPCs and all doorways are blocked. If Cultist wins, they declare themself the hero — then realize they might be the villain. Alternate costume unlocks regardless of who wins.
- **Unlocks:** Available from the start (co-op only). Alt costume: kill past (win or lose the duel).

### The Paradox
- **Short desc:** "A glitched gungeoneer with a random loadout — chaos incarnate. Costs 5 Hegemony Credits."
- **Lore:** A consequence of the other Gungeoneers recklessly using the Gun That Can Kill The Past. A physical representation of temporal paradoxes from wounding the timestream. Appearance changes randomly on dodge-roll, table flip, or barrel roll.
- **Playstyle:** Random starter sidearm (from other Gungeoneers, excluding Slinger), random non-starter weapon, random passive item. Every run is completely different. Can spawn with weapons from unlocked Gungeoneers. Items chosen at select time but item doesn't appear until run starts. Can spawn with a synergy between its gun and item. Highest variance of any character. No past — cannot obtain the Bullet That Can Kill The Past.
- **Tips:**
  - Adapt to what you're given — no fixed strategy
  - Can start with Gunknight Armor pieces for bonus armor on floor 1
  - Quick Restart returns to your selected default character if you lack credits
  - In co-op, Cultist gets a different randomized loadout
  - Appearance changes on dodge-roll/table-flip — cosmetic only
  - Cannot reach Gun That Can Kill The Past until Gunslinger is unlocked
- **Past:** No traditional past. Used to unlock The Gunslinger.
- **Unlocks:** After killing at least one past, 20% chance for a cosmic rift to appear in a random room on Gungeon Proper, Black Powder Mine, or Hollow. Interact with rift to gain paradox effect. Kill the past or defeat the Lich with effect active to unlock. Multiple rifts can appear per run. Save/quit retains the effect.

### The Gunslinger
- **Short desc:** "The original gungeoneer who built the Gungeon — grants all synergies via Lich's Eye Bullets. Costs 7 Hegemony Credits."
- **Lore:** Ancient gunslinging wizard who constructed the Gungeon out of concern that guns would out-compete old magics. Pre-mortem version of the Lich. Threw empty guns at foes and drew new ones from a magical belt. Fearing guns would replace magic, retreated to Gunymede and built a fortress. Was working on a gun that could kill the past when the Great Bullet crashed from the heavens. Never seen alive again.
- **Playstyle:** Generally considered the easiest Gungeoneer. Lich's Eye Bullets grants any synergy without needing the counterpart item — makes weak shop guns excellent options. Slinger is a powerful revolver that is thrown on reload (can stun enemies). Keeps all health and items when entering his past (unique among Gungeoneers).
- **Tips:**
  - Lich's Eye Bullets is incredibly powerful — every synergy activates
  - Cheap low-quality shop guns become excellent purchases
  - Slinger's throw-on-reload can stun enemies — use it tactically
  - Don't die or quick restart — you lose the entire unlock attempt
  - Must get Bullet That Can Kill The Past from Blacksmith BEFORE entering Aimless Void
  - If you don't get the Bullet, firing the Gun just shows credits — start over
- **Past:** Bullet Hell — fight two Liches simultaneously (one normal, one Paradox-jammed with increased health, fires jammed bullets). Both use only first phase. Win when both defeated. Final scene: Gungeon before the Bullet crashed. Victory screen: Gunslinger throws away his gun — time rewritten, Gungeon never created. Leads into Exit the Gungeon.
- **Unlocks:** As The Paradox, defeat the Lich → immediately start new run as Gunslinger. Must get Bullet That Can Kill The Past from Blacksmith in the Forge, then kill his past. If you die, quick restart, or exit without saving before finishing — start the entire process over with another Paradox run.

---

## 7. Codex Rework — Compact Categorization

Current codex has 11 categories in a horizontal strip:
- 6 special pages (Paradox, Gunslinger, Bullet Hell, Drake, Challenge, Rat)
- 5 data categories (Objects, Pickups, NPCs, Enemies, Bosses)

### Proposed: Add "Gungeoneers" as 7th special page

New order (Gungeoneers first among special pages, since it's character-focused):
1. **Gungeoneers** (NEW — blue, person_pin icon)
2. Paradox
3. Gunslinger
4. Bullet Hell
5. Drake
6. Challenge
7. Rat
8. Objects
9. Pickups
10. NPCs
11. Enemies
12. Bosses

This keeps the existing structure intact and just adds one more tile. The Gungeoneers page is a grid of 9 cards (not a searchable list — too few entries for search).

---

## 8. Files to Create/Modify

### New files:
| File | Purpose |
|---|---|
| `lib/widgets/spoiler_tag.dart` | Reusable spoiler collapsible widget |
| `lib/screens/gungeoneer_detail_screen.dart` | Full detail view for one gungeoneer |
| `lib/screens/gungeoneer_codex_screen.dart` | Codex grid of all gungeoneers |

### Modified files:
| File | Changes |
|---|---|
| `assets/data/gungeoneers.json` | Extended schema with all new fields + 3 data fixes |
| `lib/models/gungeoneer.dart` | New fields in model + fromJson/toJson |
| `lib/screens/character_select_screen.dart` | Add `?` button to `_CharacterCard` |
| `lib/screens/codex_screen.dart` | Add Gungeoneers category tile + special page routing |

### No changes needed:
- `lib/screens/item_detail_screen.dart` — already handles gun/item navigation
- `lib/providers/run_provider.dart` — already loads gungeoneers.json
- `lib/utils/asset_paths.dart` — already has `gungeoneerAnimatedCardPath()`

---

## 9. Edge Cases

| Case | Handling |
|---|---|
| The Paradox (random loadout) | Show "?" placeholder tiles with "Random Weapon" / "Random Item" labels |
| The Cultist (co-op only) | Show "CO-OP ONLY" badge in detail view header |
| The Gunslinger (no traditional past) | Past section says "Bullet Hell — fight two Liches" instead of standard past |
| The Robot (6 armor, no hearts) | Show "SPECIAL: 6 Armor, No Hearts" badge + junk damage callout |
| Hegemony Credit cost (Paradox 5, Gunslinger 7) | Show "Cost: N Hegemony Credits" badge below short desc |
| Armor as a starting item | Show as a special tile with shield icon + "×1" badge (not a real item in items.json) |
| Missing wiki data for some fields | Fall back to empty string — SpoilerTag hidden if content is empty |
| Character art missing | Fall back to existing `_buildFallbackIcon()` pattern |
| Past unlocks field empty (Cultist, Gunslinger) | Hide the "Past Kill Unlocks" spoiler tag entirely |
| Nicknames empty | Hide the nicknames/voice trivia line |

---

## 10. Visual Design Notes

- **SpoilerTag banner:** Amber/warning color (`Color(0xFFFFB300)`) with `Icons.warning_amber` icon
- **Loadout tiles:** 64×64, rounded corners, same card style as inventory tiles
- **Gun tiles:** Blue accent border (matches gun quality color scheme)
- **Item tiles:** Quality-colored border (D/C/B/A/S tier colors)
- **Armor tile:** Grey/silver border with shield icon
- **Random tile (Paradox):** Purple accent with `Icons.help` icon
- **Section labels:** Same uppercase, letter-spaced, dim style as existing codex labels
- **Detail screen background:** Transparent (inherits theme), same as all other screens

---

## 10.5 Past Kill Unlocks (wiki.gg + Fandom verified)

Killing each Gungeoneer's past unlocks their starting items for ALL characters, plus a unique unlock item. These are spoiler-worthy since they reveal what you get before you've done it.

| Gungeoneer | Past Kill Unlocks (for all characters) | Unique Unlock |
|---|---|---|
| **The Marine** | Military Training | Galactic Medal of Valor |
| **The Pilot** | Trusty Lockpicks, Disarming Personality | Wingman |
| **The Convict** | Enraging Photo | Briefcase of Cash |
| **The Hunter** | Dog | Wolf |
| **The Bullet** | Blasphemy, Live Ammo | Chicken Flute |
| **The Robot** | Robot's Right Hand (cannot be dropped/obtained by others normally) | Robot's Left Hand, Chest Teleporter |
| **The Cultist** | — (alt costume unlocks regardless of duel outcome) | — |
| **The Paradox** | No past | The Fat Line (defeat High Dragun), The Gunslinger (defeat Lich + kill past) |
| **The Gunslinger** | Lich's Eye Bullets (already starts with it) | — (ending rewrites time) |

### Alternate Costumes (skins)

Each Gungeoneer (except Paradox and Gunslinger) has alternate costumes unlocked by killing their past. Killing past with alt costume equipped unlocks alternate starting weapon skin (activated at shrine near The Bullet in the Breach).

| Gungeoneer | Default Skin | Alt Skin (kill past) | Notes |
|---|---|---|---|
| **The Marine** | Soldier | Knight | Knight resembles medieval knight, crest emblem is a gun |
| **The Pilot** | Default | Alt | — |
| **The Convict** | Default | Alt | — |
| **The Hunter** | Default | Alt | Skins don't change Dog's appearance |
| **The Bullet** | Default | Alt | Alt icon used on character select |
| **The Robot** | Default | Alt | Alt weapon skin: bullets become bones |
| **The Cultist** | Default | Alt | Unlocks regardless of duel win/loss |

---

## 10.6 Additional Useful Info (from wiki.gg individual pages)

### Nicknames & Aliases (fun trivia for detail view)

| Gungeoneer | Nicknames | Aliases | Voice |
|---|---|---|---|
| **The Marine** | Tough Guy, Soldier, Meathead | — | manly |
| **The Pilot** | Flyboy, Rogue, Taffer, Scoundrel | — | spacerogue |
| **The Convict** | Jumpsuit, Jailbird, Lawbreaker | Laser Lily, Hegemony Citizen 83H4-I59 | convict |
| **The Hunter** | Pilgrim, Prof, Lady, Ma'am | Scholar (internal), Guide (internal) | convict |
| **The Bullet** | Slug, Ammo, Round, Shell, Little guy, Betrayer | bullet... person | — |
| **The Robot** | Machine, Automaton, Android, Mechano-man, Can-opener, Robert, Number 4, Colonel Klink, Toaster, Metal Head | — | computer (Breach), truthknower (unlock) |
| **The Cultist** | Somebody, Some guy, Rando, Extra, Guy next to the protagonist, Assistant gun user | Mysterious Companion, Child of the Gungeon, Coopcultist (internal), Purple guy (internal) | coop |
| **The Paradox** | Whatever you are, Time blob, Glitch, Temporal horror, Purple ghost | Eevee (internal) | manly |
| **The Gunslinger** | Slinger | Gungeon Master, The Lich, Legendary Hero | manly |

### Hegemony Credit Costs

| Gungeoneer | Cost |
|---|---|
| The Marine | Free |
| The Pilot | Free |
| The Convict | Free |
| The Hunter | Free |
| The Cultist | Free (co-op only) |
| The Bullet | Free (after unlock) |
| The Robot | Free (after unlock) |
| **The Paradox** | **5 Hegemony Credits** |
| **The Gunslinger** | **7 Hegemony Credits** |

### The Robot's Unique Mechanics (detailed)

- Starts with 6 armor, 0 hearts — cannot gain heart containers
- Cannot interact with hearts at all (can move them by contact)
- Immune to electricity damage (from Battery Bullets)
- Each piece of Junk or Gold Junk: permanent +5% damage increase (persists even if junk dropped/sold)
- Master Rounds grant 1 armor (not heart)
- Heart-container items give 5-10 shells instead
- Dodge roll deals 1 more damage than other Gungeoneers
- Armor grants free blank effect when hit (reveals secret rooms)
- Negates jammed enemy extra damage (takes normal damage from jammed)

### The Paradox's Unique Mechanics (detailed)

- Appearance changes randomly on dodge-roll, table flip, or barrel roll (cosmetic only — sliding over a table does NOT change appearance)
- If picks up appearance-changing item (e.g. Clown Mask), that appearance adds to the random pool
- Items chosen at character select time, but item doesn't appear until run starts
- Can spawn with a synergy between its gun and item
- Can start with weapons from unlocked Gungeoneers (e.g. Robot's Right Hand)
- Can also get weapon skins that haven't been unlocked yet
- Quick Restart returns to selected default character if lacking credits
- In co-op, Cultist gets a different randomized loadout
- Quick Restart in co-op: Cultist and Paradox get identical loadouts
- Cannot reach Gun That Can Kill The Past until Gunslinger is unlocked (Lich's hand drags to Bullet Hell)
- Killing Lich as Paradox (without Gunslinger unlocked) does NOT count as a real Lich kill — no Ammonomicon entry, no unlockables
- If starts with Gunknight Armor pieces, enters first chamber with 2 armor (level transition counts as floor change)
- Blacksmith will talk to Paradox but won't give Bullet That Can Kill The Past

### The Gunslinger's Unique Mechanics (detailed)

- Lich's Eye Bullets: grants any synergy without needing the counterpart item
- Slinger: thrown on reload (can stun enemies), then draws a new one from magical belt
- Keeps all health and items when entering past (unique — all others get a set loadout)
- Past is Bullet Hell — fight two Liches simultaneously (one normal, one Paradox-jammed)
- Both Liches use only first phase
- Paradox Lich fires jammed bullets, has increased health
- Win when both defeated
- Ending: time rewritten, Gungeon never created → leads into Exit the Gungeon
- Generally considered the easiest Gungeoneer to play

### The Bullet's Unique Mechanics (detailed)

- Blasphemy: cleaves bullets with every slice, fires piercing sword projectile at FULL health only
- Losing even 1 heart piece: loses ranged attack, damage halved, range becomes pitiful
- Swinging causes slight forward lunge — don't swing near pits
- Live Ammo: complete immunity to contact damage, dodge roll becomes an attack
- Contact-damage enemies (Spent, Blobulons, cubes) become completely harmless
- Excellent for earning Master Rounds — many bosses become trivial
- Damage output drops on later floors as enemies gain health
- Must top off health or hoard armor to maintain ranged attack

---

## 11. Open Questions for User

1. **Spoiler persistence:** Should spoiler reveal state persist across sessions (SharedPreferences), or reset every time the detail view is opened? (Default: reset — simpler, respects players who don't want to accidentally see spoilers)

2. **The Lamb (mobile-only gungeoneer):** wiki.gg lists "The Lamb" as a mobile-only gungeoneer with Crusader's Blade and Red Crown. Fandom and other sources do not cover it. Should we include it? (Default: skip — not in the main game, only 1 source mentions it)

3. **Codex category position:** Should "Gungeoneers" be the first tile (before Paradox) or last among special pages? (Default: first — it's the most fundamental category)

4. **Past loadout display:** Should the past kill loadout be shown as tappable tiles (like starting loadout) or as plain text? (Default: plain text inside spoiler — past loadout weapons like "Thompson Sub-Machinegun" and "Hegemony Carbine" aren't in our guns.json)

5. **Hegemony Credit cost display:** The Paradox (5 credits) and The Gunslinger (7 credits) are the only characters with a play cost. Should we show this in the detail view? (Default: yes — add a "Cost: 5 Hegemony Credits" line for these two)

6. **The Robot's unique mechanics:** The Robot has several unique mechanics (6 armor, no hearts, junk damage boost, free blank on hit). Should these go in the playstyle section or get their own "Special Mechanics" section? (Default: playstyle section — keeps it simpler)

---

## 12. Estimated Scope

| Component | Complexity |
|---|---|
| JSON enrichment (9 gungeoneers) | Medium — research + writing (DONE — all data in this plan) |
| Gungeoneer model extension | Small |
| SpoilerTag widget | Small |
| GungeoneerDetailScreen | Medium — multiple sections, loadout grid, 5 spoiler tags |
| Character select `?` button | Small |
| Codex integration | Small |
| Testing & polish | Small |

**Total: ~6-8 files, 1 new widget, 1 new screen, 2 modified screens, 1 data file**

---

## 13. Sources

All data in this plan was cross-referenced against multiple sources. Starting loadouts confirmed by 100% of sources.

| # | Source | URL | Used For |
|---|---|---|---|
| 1 | wiki.gg (primary) | https://enterthegungeon.wiki.gg/wiki/Gungeoneers | Starting loadouts, all individual character pages (full fetch) |
| 2 | Fandom Wiki (secondary) | https://enterthegungeon.fandom.com/wiki/Gungeoneers | Past kill unlocks, loadout confirmation |
| 3 | IGN Guides (third) | https://www.ign.com/wikis/enter-the-gungeon/ | Strategy tips, loadout confirmation (Marine, Hunter, Pilot, Robot, Cultist) |
| 4 | Giant Bomb Wiki (fourth) | https://giantbomb.com/wiki/Games/Enter_the_Gungeon | Full character table with loadouts |
| 5 | Gameranx (fifth) | https://gameranx.com/features/id/172785/ | Paradox & Gunslinger unlock guides |
| 6 | Game Rant | https://gamerant.com/best-characters-enter-the-gungeon/ | Character rankings, playstyle descriptions |
| 7 | wiki.gg Unlockables | https://enterthegungeon.wiki.gg/wiki/Unlockables | All unlock methods, past kill rewards |
| 8 | wiki.gg Achievements | https://enterthegungeon.wiki.gg/wiki/Achievements | Achievement-linked unlocks |

### Individual wiki.gg pages fetched in full:
- https://enterthegungeon.wiki.gg/wiki/The_Marine
- https://enterthegungeon.wiki.gg/wiki/The_Pilot
- https://enterthegungeon.wiki.gg/wiki/The_Convict
- https://enterthegungeon.wiki.gg/wiki/The_Hunter
- https://enterthegungeon.wiki.gg/wiki/The_Bullet
- https://enterthegungeon.wiki.gg/wiki/The_Robot
- https://enterthegungeon.wiki.gg/wiki/The_Paradox
- https://enterthegungeon.wiki.gg/wiki/The_Gunslinger
- https://enterthegungeon.wiki.gg/wiki/The_Cultist

---

## 14. Plan Completion Checklist

- [x] Objective defined
- [x] Starting loadout data verified (5 sources, 100% agreement)
- [x] 3 JSON discrepancies identified
- [x] Extended JSON schema designed
- [x] Dart model extension designed
- [x] SpoilerTag widget specified
- [x] GungeoneerDetailScreen layout designed (with all new fields)
- [x] Character select `?` button specified
- [x] Codex integration specified
- [x] Edge cases documented (10 cases)
- [x] Visual design notes
- [x] Implementation phases (6 phases, detailed)
- [x] All 9 gungeoneers have full data summary (lore, playstyle, tips, past, unlocks)
- [x] Past kill unlocks table (all 9)
- [x] Alternate costume/skin table (all 7 applicable)
- [x] Nicknames & aliases table (all 9)
- [x] Hegemony credit costs (all 9)
- [x] Unique mechanics detailed (Robot, Paradox, Gunslinger, Bullet)
- [x] Open questions for user (6)
- [x] Sources cited (8 sources, 9 individual pages)
- [x] Scope estimated

**Plan is COMPLETE. Ready for implementation when user approves.**
