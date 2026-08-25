# 📜 Winchester Minigame & Huntress Overhaul — Architecture Plan

This document outlines the detailed technical specifications and implementation roadmap for recreating **Winchester's 2D Billiard-Physics Minigame** and developing the **bespoke Huntress Character HUD**.

---

## 🏛️ Part 1: Winchester's 2D Canvas-Physics Minigame

We will implement the minigame as a standalone, self-contained **2D canvas engine** using Flutter's native `CustomPainter` and coordinate tick loop.

### 1. Game State & Mathematics
*   **The Projectile**:
    *   State: `Offset position`, `Offset velocity` (constant magnitude $V$), `int bounces` (max 4).
    *   Physics: No gravity. Clean elastic bounce reflection:
        $$\vec{v}_{\text{reflected}} = \vec{v}_{\text{incident}} - 2 (\vec{v}_{\text{incident}} \cdot \vec{n}) \vec{n}$$
        where $\vec{n}$ is the collision surface normal vector.
*   **Collision Detection Matrix**:
    *   The stage is represented by a grid of cells (blocks) and absolute coordinates for circular targets.
    *   *Grid Resolution*: $16 \times 12$ tiles to match the proportions in the game screenshots.
*   **Block Behaviors**:
    *   **Blue Blocks (Solid)**: Clean normal reflection.
    *   **Green Blocks (Glass)**: Clean normal reflection, immediately flagged as `destroyed` and removed from collision checks.
    *   **Red Blocks (Magma/Spikes)**: Projectile immediately deleted, trigger fizzle particle effect.
    *   **Face Targets (Bullseye)**: Target destroyed (flagged), increment `targetsHit`, destroy projectile.
*   **Moving Obstacles**:
    *   Local coordinates of shifting blocks updated inside the tick loop using simple linear ping-pong loops on a localized timer (`cos(time)`).

### 2. Laser Sight & Touch Drag Aiming
*   **Aiming (Touch Drag)**:
    *   Input: `GestureDetector` captures drag anywhere on the screen. Calculates target angle $\theta$ relative to the static cannon in the bottom-left.
*   **Built-in Laser Sight**:
    *   Calculates a raycast from the cannon along the aiming vector to the *first* collision boundary.
    *   Renders as a thin dotted neon-red line.

### 3. Chest Tier Reward Ceremony
*   At the end of 4 shots:
    *   4 Hits: Black Chest (S-Tier)
    *   3 Hits: Red Chest (A-Tier)
    *   2 Hits: Blue / Green Chest (B/C-Tier)
    *   1 Hit: Brown Chest (D-Tier)
    *   *Note*: Reward chest and item simulations are reserved for stage 2 polish, but the tier animation and particle confetti will trigger instantly on stage 1!

---

## 🐕 Part 2: The Huntress "Junior II" & Crossbow HUD

We will implement a premium **Huntress Details Drawer / Info Overlay** triggered from a dedicated button on the character card panel (no screen cluttering graph graphics, pure compact premium list designs!).

### 1. The "Junior II" Drop Probability Engine
*   **Dig Probability Display**: Fixed 5% dig chance on room clear.
*   **Adaptive Dig Pool Weights**: Segmented progress list updating in real-time based on Huntress's health:
    *   **If Full Health**: Blanks (34%), Armor (23%), Keys (21%), Normal Ammo (17%), High-Tier Ammo (4%), other (1%).
    *   **If Injured (Health < Max)**: Heart Drops (22%), Blanks (20%), Armor (19%), Ammo (17%), Keys (17%), other Ammo (4%), other (1%).
*   **Room Clear Tracker**:
    *   Interactive counter.
    *   Displays **Cumulative Drop Chance** calculated mathematically on the spot:
        $$P(\text{drop}) = 1 - (0.95)^N$$
        where $N$ is the number of room clears without a drop.

### 2. Early-Game Crossbow Breakpoint Calculator
*   **Database**:
    *   Bullet Kin (15 HP), Bandana Kin (20 HP), Shotgun Kin (30 HP).
*   **Dynamic Calculation**:
    *   Base Crossbow Damage = 22.
    *   Breakpoint = $22 \times \text{Damage Multiplier}$ (fetched dynamically from registered passive damage items!).
*   **Interactive List**:
    *   If Breakpoint $\ge$ Enemy HP: Displays green text `"1-Shot Kill"` (Efficiency badge).
    *   If Breakpoint $<$ Enemy HP: Displays orange text `"1 Crossbow + 1 Starter Pistol Shot"`.

### 3. Special Companion & Secret Path Guides
*   **Alerts**:
    *   *Baby Good Mimic*: Clones Junior II, giving two dogs digging at 5% chance.
    *   *Companion Grouping (Wolf/Badge/Owl)*: Alert for Battle Standard multiplier (+25% damage boost to companions).
    *   *Huntsman*: Alert for "Insight" synergy (reveals chest contents and increases reload).
*   **Key Economy checklist**:
    *   Monitors floor and current Key inventory. If Key count $\ge 2$ on Chamber 1, prints a green checkmark next to "Oubliette Ready".
