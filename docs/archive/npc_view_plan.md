# 📜 Gungeon NPC & Annex Spawn Analytics — Architecture Plan

This document outlines the design specifications, data models, and dynamic mathematics required to build the **Bespoke Gungeon NPC & Annex Spawn Analytics View** as an interactive, tabbed mobile component.

---

## 🏛️ Part 1: Data Models & Global Multipliers

### 1. Bello Shop Price Tables
*   **Chamber Base Multipliers**:
    *   Chamber 1 / Secret Floors: $1.0\times$
    *   Chamber 2 (Gungeon Proper): $1.15\times$
    *   Chamber 3 (Black Powder Mine): $1.3\times$
    *   Chamber 4 (Hollow): $1.45\times$
*   **Item Base Prices**:
    *   S-Tier (Black): 100 Casings
    *   A-Tier (Red): 68 Casings
    *   B-Tier (Green): 46 Casings
    *   C-Tier (Blue): 32 Casings
    *   D-Tier (Brown): 22 Casings
    *   Hearts / Armor: 20 Casings
    *   Keys: 25 Casings
*   **Price Formula**:
    $$\text{Final Cost} = \lfloor \text{Base Price} \times \text{Floor Multiplier} \times \text{Aggro Multiplier} \rfloor$$

### 2. Annex Spawn Matrix Weights
*   **Vendor Pool**:
    *   Muncher: Weight $0.53$ (Base $30.21\%$)
    *   Sell Creep: Weight $0.53$ (Base $30.21\%$)
    *   Vampire: Weight $0.25$ (Base $15.10\%$, requires Rescued Cell check)
    *   Old Red: Weight $0.10$ (Base $6.04\%$, requires Rescued Cell check)
    *   Cursula: Weight $0.10$ (Base $6.04\%$, requires Rescued Cell check)
    *   Flynt: Weight $0.10$ (Base $6.04\%$, requires Rescued Cell check)
    *   Goopton: Weight $0.10$ (Base $6.04\%$, requires Rescued Cell check)
    *   Evil Muncher: Weight $0.005$ (Base $0.30\%$)

---

## 🛒 Part 2: NPC Dashboard Cards

We will wrap Bello, Winchester, and the Annex Manager into an incredibly sleek **Segmented Tab Bar Layout**:
`[ Bello Shop ]` | `[ Winchester Game ]` | `[ Annex Spawn Analytics ]`

### 1. Card 1: Bello (The Shopkeeper)
*   **Layout**: Animated asset placeholder on the left, Name & Description on the right.
*   **Dynamic Price Calculator**: Interactive Dropdowns for floor and item rarity immediately outputs final cost based on the formula above.
*   **Aggro & Punishment Tracker**:
    *   "Discharge Weapon" button increments `aggroCount` (0 to 3):
        *   *Count 1*: Yellow warning banner.
        *   *Count 2*: Prices doubled ($\text{Aggro Multiplier} = 2.0$), Orange fury banner.
        *   *Count 3*: Shop permanently closed (clears displayed prices, flashes red blinking warning: "Bello shoots you for 'Justice' and vanishes!").
    *   *Clean Reset Button*: Placed at the bottom to easily clear aggro/prices back to default values.
*   **Wisdom checklist**: Explains Stealing mechanics and Elevator resets.

### 2. Card 2: Winchester (The Minigame Host)
*   **Layout**: Shotgun-spinning animated placeholder, details and entry fee descriptions.
*   **Item Modifier Compatibility list**:
    *   *Remote Bullets (Green)*: "TRIVIALIZES MINIGAME. Manually steer the Prize Pistol bullet with your touchscreen."
    *   *Wings / Jetpack / Cat Throne (Green)*: "AUTO-WIN CHEAT. Allows flying over the pits directly point-blank into targets."
    *   *Scattershot / Crutch (Yellow)*: "Double-Edged Sword. Splits bullets or bends angles, increasing hitbox coverage but making traditional shots unpredictable."
    *   *Backup Gun / Helix / Bloody 9mm (Red)*: "CRITICAL HAZARD. Drastically warps precision lines. Drop before playing!"
*   **Trickshot checklist**: Track lifetime Ace runs -> unlocks Seven-Leaf Clover golden ribbon indicator.

### 3. Card 3: The Annex Manager (Spawn Analytics)
*   **Checklist Array**: Toggle rescued status of Vampire, Old Red, Cursula, Flynt, and Professor Goopton.
*   **Floor Context Selection**: Keep of Lead Lord, Gungeon Proper, Mine, Hollow, Secret Floors, plus a "Has Master Round" checkbox.
*   **Recalculation Engine**:
    *   If Floor == Keep: Muncher & Evil Muncher weights = 0.
    *   If Floor != Hollow: Evil Muncher weight = 0.
    *   If Floor == Hollow AND Has Master Round: Sell Creep weight = 0.
    *   If Rescue Checkbox is false: NPC weight = 0.
    *   *Probability Math*:
        $$Sum\_Weights = \sum_{i \in \text{Valid NPCs}} w_i$$
        $$Live\_Percentage_i = \left(\frac{w_i}{Sum\_Weights}\right) \times 100\%$$
*   **Output viewport**: Renders elegant, colored progress bar indicators with adjusted probability percentages. Grays out locked NPCs with "[LOCKED / NOT AVAILABLE]" tags.

#### 🧮 Pure-Dart Annex Probability Engine Code

```dart
class GungeonNpc {
  final String name;
  final double baseWeight;
  final String conditionMessage;

  GungeonNpc({
    required this.name,
    required this.baseWeight,
    required this.conditionMessage,
  });
}

class AnnexCalcEngine {
  // 1. Define our structural static dataset matching the wiki rules
  final List<GungeonNpc> allAnnexNpcs = [
    GungeonNpc(name: "Muncher", baseWeight: 0.53, conditionMessage: "Not in Keep / Requires Proper visited"),
    GungeonNpc(name: "Sell Creep", baseWeight: 0.53, conditionMessage: "Not in Hollow if holding Master Round"),
    GungeonNpc(name: "Vampire", baseWeight: 0.25, conditionMessage: "Requires Cell Rescue"),
    GungeonNpc(name: "Old Red", baseWeight: 0.10, conditionMessage: "Requires Cell Rescue"),
    GungeonNpc(name: "Cursula", baseWeight: 0.10, conditionMessage: "Requires Cell Rescue"),
    GungeonNpc(name: "Flynt", baseWeight: 0.10, conditionMessage: "Requires Cell Rescue"),
    GungeonNpc(name: "Professor Goopton", baseWeight: 0.10, conditionMessage: "Requires Cell Rescue"),
    GungeonNpc(name: "Evil Muncher", baseWeight: 0.005, conditionMessage: "Only in Hollow or later"),
  ];

  // 2. The Core Math Resolver
  Map<String, double> calculateLiveChances({
    required String currentFloor,          // e.g., "Keep", "Proper", "Hollow", "Mines"
    required bool hasMasterRound,          // Specific to Sell Creep override
    required Map<String, bool> rescueState,// Map tracking if ['Vampire', 'Flynt', etc] are unlocked
    required bool hasVisitedProper,        // Global progression flag
    required bool hasVisitedHollow,        // Global progression flag
  }) {
    Map<String, double> calculatedPercentages = {};
    double totalActiveWeight = 0.0;
    Map<String, double> activeWeights = {};

    // Step A: Evaluate every NPC against floor limits and rescue profile flags
    for (var npc in allAnnexNpcs) {
      double activeWeight = npc.baseWeight;

      // Rule 1: Muncher & Evil Muncher environmental bans
      if (currentFloor == "Keep") {
        if (npc.name == "Muncher" || npc.name == "Evil Muncher") activeWeight = 0.0;
      }
      if (!hasVisitedProper && npc.name == "Muncher") activeWeight = 0.0;
      if (!hasVisitedHollow && npc.name == "Evil Muncher") activeWeight = 0.0;

      // Rule 2: Sell Creep Master Round penalty in the Hollow
      if (currentFloor == "Hollow" && hasMasterRound && npc.name == "Sell Creep") {
        activeWeight = 0.0;
      }

      // Rule 3: Check permanent cell unlock states
      if (rescueState.containsKey(npc.name) && rescueState[npc.name] == false) {
        activeWeight = 0.0;
      }

      // Save calculated operational weight and add to total pool sum
      activeWeights[npc.name] = activeWeight;
      totalActiveWeight += activeWeight;
    }

    // Step B: Resolve final percentage allocations
    activeWeights.forEach((npcName, weight) {
      if (totalActiveWeight > 0.0 && weight > 0.0) {
        // Standard formula: (Individual Weight / Sum of Weights) * 100
        double percentage = (weight / totalActiveWeight) * 100;
        calculatedPercentages[npcName] = double.parse(percentage.toStringAsFixed(2));
      } else {
        // Explicitly flag dead weights as 0%
        calculatedPercentages[npcName] = 0.0;
      }
    });

    return calculatedPercentages;
  }
}
```

### 4. Extensibility Placeholders
*   Cards for Rea, Blacksmith, Synergies, and Vampire economies are held in elegant static placeholder panels for future updates.

---

## 🏛️ Part 3: Section 5 — Breach Game-Modifiers & Hunting Data

We will add two more highly interactive cards to our tabbed NPC view dashboard:

### 1. Card 8: Frifle & Grey Mauser (The Hunting Team)
*   **Layout**: Left column shows Frifle holding his rifle with Grey Mauser tucked in his cloak. Right column displays Title & Description.
*   **Quest Selection**: Multi-run localized dropdown with all 12 major Gungeon Hunting Quests:
    1.  30 Bullet Kin (Sunlight Javelin/Rejects unlocked)
    2.  30 Shroomers (Sunlight Javelin)
    3.  25 Ashen Bullet Kin (Grey Mauser gun)
    4.  15 Mutant Shotgun Kin (its/a/gun)
    5.  20 Spenders (Huntsman)
    6.  15 Gunzooms (Cat Claw)
    7.  15 Skullets (Skull Spitter)
    8.  10 Lead Maiden (Fleshbox)
    9.  15 Shambling Rounds (Blood Brooch)
    10. 15 Gunjurors (Magic Lamp)
    11. 30 Killpillars (Microtransaction Gun)
    12. 1 Dragun (Hunting Trophy / Finished Gun eligibility)
*   **Quest Tracker Counter**: Incremental progress checklist (e.g. `[ ] Count: 0 / 15 Shambling Rounds`) with `-` and `+` buttons. Counts are dynamically tracked and saved!

### 2. Card 9: Daisuke (Challenge Mode Host)
*   **Layout**: Left column displays Daisuke the die, right column shows description and Hegemony entry fee (6 credits).
*   **Room Modifier Risk Sheet**: Interactive selectable multi-chip selection panel describing challenge status:
    *   *Gulls-Eye View*: Periodically fires air strike crosshair exploding shells.
    *   *Gorgun's Gaze*: Turn away from the center flash to avoid petrification.
    *   *Hammer Time*: Forge Hammer constantly follows and slams down.
    *   *High Stress*: Damage reduces player health directly to half a heart/1 armor for 5 seconds.
*   **Mathematical Link**: Activating Challenge Mode checkbox automatically appends a flat **2x multiplier** to final Hegemony Credit payout calculations on run summary screens!

