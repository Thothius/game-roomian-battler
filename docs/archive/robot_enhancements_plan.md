# 🤖 Robot Damage Scaling & "Smash or Buy" Calculator — Architecture Plan

This document outlines the design, dynamic math formulas, and interactive controls to implement the **Robot absolute damage scaling tracker** and the real-time **"Smash or Buy" Decision Calculator**.

---

## 🧮 Part 1: The Mathematical Damage Engine

The Robot gets a permanent, additive $+5\%$ damage boost for every piece of Junk (and Lies) carried, and $+500\%$ if Gold Junk is possessed.

### 1. Variables & Modifiers
*   **Base Robot Damage Multiplier**: $1.0$ (100% baseline)
*   **Standard Junk Modifier**: $+0.05$ per piece ($+5\%$ additive)
*   **Lies Modifier**: $+0.05$ per piece ($+5\%$ additive)
*   **Gold Junk Modifier**: $+5.00$ ($+500\%$ massive multiplier + missile companion)
*   **Other Passive Items**: Double-precision floating value representing sum of all owned items that boost global damage (e.g., *Metronome*, *Plus One Bullets*).

### 2. Formula Blueprint
```dart
double calculateRobotDamage(int junkCount, bool hasGoldJunk, bool hasLies, double otherPassives) {
  double junkDamage = (junkCount + (hasLies ? 1 : 0)) * 0.05;
  double goldJunkDamage = hasGoldJunk ? 5.0 : 0.0;
  
  // Total damage output multiplier (e.g. 1.25 = +25% boost)
  return 1.0 + junkDamage + goldJunkDamage + otherPassives;
}
```

---

## 🎛️ Part 2: Interactive Stat Steppers

We will integrate these controls directly on the active Robot systems HUD below the Armor display:
1.  **Standard Junk Stepper**: Row layout `[-]  [ 0 ]  [+]` updating the multiplier immediately on tap.
2.  **Special Toggles**:
    *   `[ ] Gold Junk`: checking instantly spikes the multiplier by $+500\%$ and turns the HUD background to a warm gold gradient.
    *   `[ ] Lies (Brother Albern)`: checking adds a $+5\%$ boost.

---

## 💡 Part 3: The "Smash or Buy" Decision Advisor

This module sits directly below the steppers, providing real-time strategic assistance to players deciding whether to buy a shop item from Bello or smash chests for free Junk damage.

### 1. Input Layout
*   **Input 1 (Shop Cost)**: A numeric text entry field to specify the Casing price of an item currently on sale in Bello's shop.
*   **Input 2 (Item Rarity)**: A chip-selection bar: `[ D-Tier ]` | `[ C-Tier ]` | `[ B-Tier ]` | `[ A-Tier ]` | `[ S-Tier ]`.

### 2. Dynamic Decision Logic
When both parameters are input, the app renders a highly stylized **Advice Card** with specific Gungeon strategic suggestions:

*   **IF D-Tier or C-Tier Selected**:
    *   *Advice*: **SMASH IT.**
    *   *Text*: `"👉 Strategy: **SMASH IT.** This item costs [X] Casings but offers low overall value. Shooting/smashing the chest instead guarantees a chance of an immediate, permanent **+5% global damage boost** for 0 Casings."`
*   **IF B-Tier Selected**:
    *   *Advice*: **SITUATIONAL.**
    *   *Text*: `"👉 Strategy: **SITUATIONAL.** B-tier items (Green) often carry powerful utility or synergies. If you have plenty of Casings and need gun coverage, **BUY IT**. Otherwise, if you have ample ammo, smashing the chest for a **+5% damage boost** is highly cost-efficient."`
*   **IF A-Tier or S-Tier Selected**:
    *   *Advice*: **BUY IT (If affordable).**
    *   *Text*: `"👉 Strategy: **BUY IT (If affordable).** High-tier items (Red/Black) typically outclass a flat 5% damage boost due to their extreme combat impact or passive modifiers. However, if your budget is tight, smashing the chest saves [X] Casings for the Blacksmith's past-killing bullet components later."`
