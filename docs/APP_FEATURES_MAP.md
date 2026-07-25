# GungeonMate - App Feature Map & Navigation Directories (v1.6.7)

This document maps all user views, interactive screens, persistent databases, and narrative flow matrices within GungeonMate.

---

## 🗺️ 1. GungeonMate View Map

```
               [ Start / Boot Screen ]
                          │
            (Is there a saved active run?)
             ├── YES ──➔ [ Tabbed Home Screen ]
             │             ├── Tab 0: Active Run Dashboard (Inventory)
             │             ├── Tab 1: Ammonomicon Database (Browse/Search)
             │             └── Tab 2: System Settings Suite
             │
             └── NO ───➔ [ Main Menu / New Run Screen ]
                           ├── Character Select Panel (Tappable avatars)
                           └── Quick Changelog Panel
```

---

## 📺 2. Detailed View Directories

### Ⅰ. Main Menu Screen (`MainMenuScreen`)
* **Purpose:** The onboarding gateway for Gungeoneers. Used to configure and launch fresh dungeon crawls.
* **Core Layout Modules:**
  * **Beveled Selection Buttons:** Start New Run, Quick Changelog dialog, and custom character picker.
  * **Character Select Panel:** A sliding roster of Gungeoneers (The Marine, Pilot, Convict, Hunter, Robot, Bullet, Paradox, Gunslinger) complete with starting guns, items, and retro stats.
  * **Changelog Dialog:** Loads `assets/data/changelog.json` dynamically to display current release updates.

### Ⅱ. Active Run Screen (`ActiveRunScreen`)
* **Purpose:** The central operational dashboard during a game session.
* **Core Layout Modules:**
  * **Interactive `GungeoneerHeader`:** Displays selected character's portrait, names, and core metrics:
    * **PORTRAIT TAP:** Triggers a character-specific, lore-friendly speech bubble (e.g., Pilot bragging about charisma, Robot complaining about squishy humans) with soft selection haptics.
    * **Coolness & Curse Capsules:** Dynamic count bubbles that dim when zero and highlight in cyan/crimson when active. Long-press launches a mini quick-adjuster bar.
    * **Stat Displays:** Tracks active cooldown reduction (CD RED), passive ammo modifiers, active synergies (SYN), and top dps output (DPS).
  * **Player Slot Switcher:** Compact tab buttons to toggle dashboard scope between the Host (`Main`) and the Co-Op Partner (`Coop`).
  * **Passive Effect Dashboard:** Aggregates passive benefits (flight, double-roll, damage boost) as tidy category chips with auto-extracted values.
  * **Inventory Lists:** Vertical list rows of collected guns and items, offering quick swaps, transfers, or disposals.

### Ⅲ. Ammonomicon Database (`BrowseScreen`)
* **Purpose:** A complete, searchable offline encyclopedia of every gun, item, synergy, and shrine in the game.
* **Core Layout Modules:**
  * **Omni Search Bar:** Live, debounced query parser filtering entities dynamically by name, quality tiers (S, A, B, C, D), and item types (Passive, Active, Gun).
  * **Interactive Rich Links:** Renders wikia-style hypertext maps inside descriptions, allowing users to deep-link tap from an item directly to its matching synergies.
  * **Referenced By Registry:** Generates a cross-referenced reverse lookup index displaying every other entity that is linked to or shares a synergy with the active item.

### Ⅳ. Codex Encyclopedia (`CodexScreen`)
* **Purpose:** Browse Gungeon bestiary and lore — enemies, bosses, NPCs, objects, pickups.
* **Core Layout Modules:**
  * **Tabbed Categories:** Enemies (146 entries with health values), Bosses (27 entries with health data), NPCs, Objects, Pickups.
  * **Search & Filter:** Live debounced search across all codex entries.
  * **Detail View:** Per-entry page with description, stats, and wiki-sourced icon.

### Ⅴ. System Settings Suite (`SettingsScreen`)
* **Purpose:** The app's configurations dashboard.
* **Core Layout Modules:**
  * **THEME & FONT TAB:** Adjust font sizes, toggle animated floating particles, and configure hypnotic trippy background GIFs.
  * **RUN UTILITIES TAB:** Initialize Wi-Fi co-op sync lobbies, swap characters mid-run, clear inventory caches, and cleanly end active sessions.
  * **HELP & TIPS TAB:** Launches comprehensive survival directories containing map generation hints, secret room finders, and boss mechanics.

---

## 🐱 3. Secret Easter Egg: The Curious Cat Bezel Tracker
* **Trigger Item:** `Cat Bullet King Throne` (Passive, B-Tier).
* **The Routine:** If the item is in the current player's loadout (verified on-the-fly over host/co-op inventories), a stateful bezel listener is initialized.
* **The Animation:** Every 35 seconds, the Cat Bullet King slides out of the right screen border, stares curiously, wiggles its head in real-time sine-wave rotations, and slides back into the bezel. Light haptic bumps accompany its peek milestones.
