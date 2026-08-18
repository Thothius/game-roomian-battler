# GungeonMate Art Prompt Plan

> **Created:** 2026-08-18 session (XEENU-ANIMATOR, Slot 1)
> **Purpose:** Centralized documentation of all Gemini Nano Banana image-generation prompts prepared for GungeonMate splash images, codex art, and branding. Copy-paste ready.
> **Status:** Planning/research only — no code changes, no assets generated yet. Prompts are ready for the user to generate images at their discretion.

---

## Table of Contents

1. [Theme Palette Assessment](#1-theme-palette-assessment)
2. [4-Palette-Per-Theme Plan (I–IV)](#2-4-palette-per-theme-plan-iiiv)
3. [Theme Splash Prompts (15 themes × 2 variants)](#3-theme-splash-prompts)
4. [Robot Theme Technical Refinement](#4-robot-theme-technical-refinement)
5. [Gungeoneer Splash Prompts (9 characters)](#5-gungeoneer-splash-prompts)
6. [Enemy Codex Art Prompts](#6-enemy-codex-art-prompts)
7. [Consumable Splash Prompts (16 items)](#7-consumable-splash-prompts)
8. [Art Direction Standards](#8-art-direction-standards)
9. [Pending / Optional Follow-Up](#9-pending--optional-follow-up)

---

## 1. Theme Palette Assessment

### Total enum values in `AppThemeMode`: 33

Source: `gungeon_mate/lib/services/app_theme.dart`

### A. Visible Themes (`kVisibleThemes`) — 15 shown in picker

| # | Theme | Vibe | Current Palettes |
|---|-------|------|-----------------|
| 1 | Minimalist | CLEAN | 1 |
| 2 | Unicorn | MAGICAL | 6 (via `UnicornPalette` enum) |
| 3 | Forge Master | INDUSTRIAL | 1 |
| 4 | Robot's Core | CYBER | 1 |
| 5 | Cat Lady | COZY | 1 |
| 6 | Moonlit Chamber | LUNAR | 1 |
| 7 | Storm Caller | ELECTRIC | 1 |
| 8 | Mr. Robot | CYBERNETIC | 1 |
| 9 | Valor of Marines | TACTICAL | 1 |
| 10 | The Bullet | HEROIC | 1 |
| 11 | The Paradox | FRACTURED | 1 |
| 12 | Gunpowder | EXPLOSIVE | 1 |
| 13 | Dragunfire | MOLTEN | 1 |
| 14 | Lich's Domain | NECROTIC | 1 |
| 15 | Custom | TACTICAL | ∞ (user picks) |

### B. Hidden/Legacy Themes (NOT in `kVisibleThemes`) — 18 in enum

| # | Theme | Vibe |
|---|-------|------|
| 1 | Unicorn II | NEON |
| 2 | Unicorn III | DREAMY |
| 3 | Unicorn IV | SUNSET |
| 4 | Ammonomicon | ARCHIVAL |
| 5 | Hollow Chill | ETHEREAL |
| 6 | Lord Jammed | CURSED |
| 7 | The Breach | COZY |
| 8 | Bullet Hell | HELLISH |
| 9 | Resourceful Rat | SNEAKY |
| 10 | Gungeon Proper | CLASSIC |
| 11 | The Oubliette | TOXIC |
| 12 | Past Paradox | COSMIC |
| 13 | High Priest Void | MYSTIC |
| 14 | Cult of Gundead | RETRO |
| 15 | Synergy Surge | ENERGETIC |
| 16 | Glitched Chest | CORRUPTED |
| 17 | Lich's Tomb | ELDRITCH |
| 18 | Winchester's Game | CARNIVAL |

### C. Unicorn Palettes (`UnicornPalette` enum) — 6

| Palette | Key Colors |
|---------|-----------|
| Cotton Candy (I) | Pink #FF69B4 + Lavender #E8A7F0 |
| Neon (II) | Hot pink #FF1493 + Orchid #DA70D6 |
| Dreamy (III) | Blush #F8BBD0 + Dusty lavender #D1C4E9 |
| Sunset (IV) | Coral #FF6B9D + Peach #FFAB91 |
| Bubblegum | Bubblegum pink #FF80AB + Magenta #E040FB |
| Mulberry | Deep magenta #C2185B + Purple #9C27B0 |

### Grand Total

| Category | Themes | Palettes |
|----------|--------|---------|
| Visible (picker) | 15 | 20 (Unicorn has 6) |
| Hidden/legacy | 18 | 18 |
| **Total** | **33 enum values** | **38 palettes** |

---

## 2. 4-Palette-Per-Theme Plan (I–IV)

User requested 4 palette variants per visible theme, labelled `<Name> <Roman Numeral>` I to IV.

### Scope

| Theme | Existing | New needed | Total |
|-------|----------|-----------|-------|
| Unicorn | 6 already | 0 (use existing I–IV + Bubblegum/Mulberry as V–VI) | 6 |
| Minimalist | 1 | 3 | 4 |
| Forge Master | 1 | 3 | 4 |
| Robot's Core | 1 | 3 | 4 |
| Cat Lady | 1 | 3 | 4 |
| Moonlit Chamber | 1 | 3 | 4 |
| Storm Caller | 1 | 3 | 4 |
| Mr. Robot | 1 | 3 | 4 |
| Valor of Marines | 1 | 3 | 4 |
| The Bullet | 1 | 3 | 4 |
| The Paradox | 1 | 3 | 4 |
| Gunpowder | 1 | 3 | 4 |
| Dragunfire | 1 | 3 | 4 |
| Lich's Domain | 1 | 3 | 4 |
| Custom | ∞ | 0 (it IS the custom palette) | ∞ |
| **Total new prompts needed** | | | **52 splash prompts** |

### Proposed Palette Direction Per Theme (I–IV concepts)

| Theme | I (Base) | II | III | IV |
|-------|----------|-----|------|-----|
| Minimalist | White/Grey (current) | Warm White (cream tint) | Cool White (blue tint) | Green Phosphor (CRT) |
| Unicorn | Cotton Candy (pink) | Neon (hot pink) | Dreamy (blush) | Sunset (coral) |
| Forge Master | Dragun Orange | Blue Flame | Molten Copper | Ash Ember |
| Robot's Core | Electric Teal | Amber Circuit | Red Alert | Violet AI |
| Cat Lady | Warm Amber | Cozy Pink | Midnight Cat (blue) | Calico (orange+white) |
| Moonlit Chamber | Silver Blue | Blood Moon (red) | Eclipse (gold) | New Moon (void purple) |
| Storm Caller | Electric Yellow | Red Lightning | Ice Storm (cyan) | Void Storm (purple) |
| Mr. Robot | Circuit Green | Battery Blue | Rust Decay | Overclocked (white-hot) |
| Valor of Marines | Olive Drab | Desert Tan | Arctic Camo | Night Ops (black+red) |
| The Bullet | Brass Gold | Silver Knight | Crimson Blade | Shadow Bullet (dark gold) |
| The Paradox | Paradox Purple | Time Rift (teal) | Blood Paradox (red) | Void Paradox (black) |
| Gunpowder | Ember Red | White Phosphorus | Toxic Powder (green) | Black Powder (pure dark) |
| Dragunfire | Dragun Orange | Black Dragun (purple) | Frost Dragun (cyan) | Gold Dragun (royal) |
| Lich's Domain | Crypt Teal | Bone & Blood (red) | Shadow Lich (purple) | Solar Lich (gold) |

**Status:** Palette direction table approved by user. 52 prompts NOT yet written — pending user request to generate.

---

## 3. Theme Splash Prompts

**Format:** 15 visible themes × 2 variance versions (A/B) = 30 prompts total.
**Style:** Dark minimalist background, popping themed label text, explicit Enter the Gungeon imagery.
**Status:** ALL 30 PROMPTS WRITTEN AND DELIVERED TO USER.

### Prompt Index

| # | Theme | Variant A | Variant B |
|---|-------|-----------|-----------|
| 1 | MINIMALIST | Bullet-Kin Silhouette | Chamber Key |
| 2 | UNICORN | Bullet-Kin With Horn | Rainbow Chest |
| 3 | FORGE MASTER | High Dragun Forge | Forge Hammer + Molten Bullet |
| 4 | ROBOT'S CORE | Chassis Cross-Section | Terminal Boot-Up |
| 5 | CAT LADY | Hearth + Cat-Kin | Juniper the Cat |
| 6 | MOONLIT CHAMBER | Crescent Through Grates | Kill Pillars Moonlight |
| 7 | STORM CALLER | Gungeoneer With Lightning Gun | Beholster Storm |
| 8 | MR. ROBOT | Robot In Chamber | Junk Hoard |
| 9 | VALOR OF MARINES | Marine Salute | Supply Drop |
| 10 | THE BULLET | Blade Pose | Blade-King Crown |
| 11 | THE PARADOX | Fractured Self | Glitch Portal |
| 12 | GUNPOWDER | Spent Casings | Powder Keg |
| 13 | DRAGUNFIRE | High Dragun Portrait | Dragun Scale Armor |
| 14 | LICH'S DOMAIN | Lich Portrait | Bone Throne |
| 15 | CUSTOM | Paint Palette | Rainbow Bullet |

### Key EtG References Used

- **Named bosses:** High Dragun, Lich, Beholster, Kill Pillars, Bullet-King
- **Named playable characters:** Robot, Marine, Bullet, Paradox
- **Named NPCs:** Juniper (cat), Bullet-King
- **Named items:** Junk items, Chamber Key, Rainbow Chest, Megahand
- **Named locations:** The Forge, The Breach, chamber rooms, Oubliette
- **Gungeon environment:** Checkered floor tiles, stone walls, brass-trimmed doors, grate slots

---

## 4. Robot Theme Technical Refinement

User specifically requested: *"make sure we add more enter the gungeon style technical prompting to robot themed ones"*

### Technical Details Added to Robot Prompts

- Named the actual playable Robot character (rectangular head, visor, tank-tread feet, junk-fuel mechanic)
- Gungeon chamber environment details (checkered floor tiles, stone walls, brass-trimmed doors)
- HUD/terminal diagnostic elements (ammo counters, junk-fuel gauges, scanlines, CRT phosphor glow)
- Specific junk items as props (bent spoon, broken spring, cracked cog — actual EtG junk items)
- Circuit-trace underlines with nodes instead of plain underlines
- Gungeon floor tile grid pattern in backgrounds
- Pixel-font text treatment matching the terminal/CRT aesthetic

### Robot's Core Palette (exact hex from `app_theme.dart`)

| Field | Hex |
|-------|-----|
| Scaffold | `#0A0F0E` |
| Card | `#101818` |
| Primary | `#00F5D4` (electric teal) |
| Secondary | `#69F0AE` (neon green) |
| Headline/Stat | `#B2DFDB` (pale teal) |
| Bullet Glyph | `🤖` |
| Aura | `frostRing` |

### Mr. Robot Palette (exact hex from `app_theme.dart`)

| Field | Hex |
|-------|-----|
| Primary | `#69F0AE` (circuit green) |
| Secondary | `#40C4FF` (battery blue) |
| Meta | `#B9F6CA` (light green) |
| Aura | `tacticalRing` |
| Header Glyph | `⚙` |

---

## 5. Gungeoneer Splash Prompts

**Count:** 9 gungeoneers (all playable characters from `assets/data/gungeoneers.json`)
**Format:** 1:1 square splash, dark bg, popping label text, hero eyes (NOT googly — these are heroes)
**Status:** ALL 9 PROMPTS WRITTEN AND DELIVERED TO USER.

### Gungeoneer Index

| # | Gungeoneer | Key Visual | Label Color |
|---|-----------|-----------|-------------|
| 1 | The Marine | Olive uniform, Marine Sidearm, supply drop crate, star stencil | White |
| 2 | The Pilot | Aviator jacket + goggles, Rogue Special, lockpick set, coin flip | Cyan #00E5FF |
| 3 | The Convict | Orange prison jumpsuit, Sawed-Off + Budget Revolver, molotov, Enraging Photo | Crimson #FF1744 |
| 4 | The Hunter | Khaki vest + adventurer hat, Crossbow + Rusty Sidearm, Dog companion | Green #64DD17 |
| 5 | The Bullet | Bullet-Kin hero with red cape, Blasphemy sword, Live Ammo glow | Gold #FFD740 |
| 6 | The Robot | Boxy head + visor, tank treads, arm-cannon, junk pile, Battery Bullets | Green #69F0AE |
| 7 | The Cultist | Purple robe + gold trim, Dart Gun, Friendship Cookie, Number 2 ghost | Purple #CE93D8 |
| 8 | The Paradox | Glitchy silhouette, afterimages, shapeshifting gun, rift cracks | Purple #CE93D8 |
| 9 | The Gunslinger | Duster coat + cowboy hat, Slinger revolver, magical bullet belt, Lich aura | Teal-Gold |

### Existing Gungeoneer Assets

All 9 have existing sprite assets at `assets/images/gungeoneers/` (animated GIFs + static WebPs). The splash prompts are for NEW branded splash art, not replacement of existing sprites.

---

## 6. Enemy Codex Art Prompts

### Current Codex Art State

| Category | Total Entries | Icon Files | Real Art | Stubs |
|----------|--------------|------------|----------|-------|
| Bosses | 26 | 27 | 17 | 10 stubs (<3KB) |
| Enemies | 146 | 146 | 0 | 146 ALL stubs |
| **Total** | **172** | **173** | **17** | **156** |

### Tier Plan

| Tier | What | Count | Status |
|------|------|-------|--------|
| Tier 1 | Stub bosses (replace 10 stubs) | 10 prompts | Written (first batch) |
| Tier 2 | All bosses (regenerate all 26) | 26 prompts | Not written |
| Tier 3 | Top 30 common enemies | 30 prompts | Written (first batch) |
| Tier 4 | All 146 enemies | 146 prompts | Not written |
| Tier 5 | Everything (172 total) | 172 prompts | Not written |

### Delivered Prompts

#### Batch 1: 10 Stub Bosses (portrait icon format, doopey goopey eyed)

| # | Boss | Key Visual |
|---|------|-----------|
| 1 | Trigger Twins | Smiley + Shades, bullet brothers |
| 2 | Treadnaught | Tank with dopey face, tiny bullet-kin in hatch |
| 3 | High Priest | Robed cultist, hood too big, homing skulls |
| 4 | Blockner | Knight bullet-kin with shield, dodge-roll X symbol |
| 5 | Door Lord | Massive door mimic, googly eyes on panels |
| 6 | Blobulord | Giant blue slime blob, general's hat, tiny arms |
| 7 | Old King | Dark Bullet King, oversized mustache, Old Chancellor |
| 8 | Agunim | Dark wizard bullet-kin, pointy hat, flickering staff |
| 9 | Black Stache | Hegemony official, comically huge mustache |
| 10 | The Last Human | Resistance fighter, oversized gun, robot skull trophy |

#### Batch 2: 30 Common Enemies (portrait icon format, doopey goopey eyed)

All 30 prompts written and delivered. Key enemies include:
- Bullet Kin family (Bandana, Veteran, Ashen, Mutant, Pirate, Western)
- Shotgun Kin family (Red, Blue, Veteran, Ashen)
- Blob family (Blobulin, Blobuloid, Blobulon, Bloodbulon, Poisbulin)
- Kamikaze family (Bullat, Shotgat, Spent)
- Special (Skullmet, Gun Nut, Spectral Gun Nut, Arrowkin, Bookllet, Blue Bookllet, Gunreaper, Lead Maiden, Fridge Maiden, Mouser, Nitra, Gigi)

#### Batch 3: 6 Hyper-Explicit Basic Enemies

User requested: *"make even more explicitly described please! make basic common ones 6 to be exactly to start ok. they doopey but must resemble real enemy in every way"*

| # | Enemy | Key Details |
|---|-------|------------|
| 1 | Bandana Bullet Kin | Brass casing body, red bandana on HEAD, sideways pistol, 1.8:1 height ratio |
| 2 | Red Shotgun Kin | Reddish-brass body, red bandana on NECK, oversized shotgun, bracing stance |
| 3 | Blobulin | Tiny blue slime dome, 40% of body is eyes, jellybean with googly eyes |
| 4 | Bullat | Live bullet (pointed tip), grey body + brass cone, fins, flame trail, THRILLED expression |
| 5 | Arrowkin | Brass body, brown headband, wooden bow, quiver, crosseyed aiming |
| 6 | Spent | CRIMPED brass casing (not pointed), jagged crimped top, sprinting, RAGING, more sprouting from ground |

**Key distinction:** Each prompt specifies exact body shape (casing vs live bullet vs slime vs crimped casing), exact hex colors, exact proportions, exact accessory placement, and exact pose matching the JSON description.

---

## 7. Consumable Splash Prompts

**Count:** 16 consumables (from `assets/data/pickups.json`)
**Format:** 1:1 square splash, dark bg, popping label text, mechanic-visual integration
**Status:** ALL 16 PROMPTS WRITTEN AND DELIVERED TO USER.

### Consumable Index

| # | Consumable | Category | Key Visual |
|---|-----------|----------|-----------|
| 1 | Shells / Copper Casing | Currency | Brass casing, $1 |
| 2 | Silver Casing | Currency | Silver casing, $5 |
| 3 | Gold Casing | Currency | Gold casing, $50, treasure glow |
| 4 | Hegemony Credit | Currency | Hexagonal steel token, boss-kill reward |
| 5 | Half Heart | Health | Half red heart, clean vertical cut |
| 6 | Full Heart | Health | Complete red heart, glossy highlight |
| 7 | Armor | Defense | Steel shield plate, blank-burst ring |
| 8 | Glass Guon Stone | Defense | Translucent cyan teardrop gem, orbital trail |
| 9 | Blank | Utility | White blank cartridge, expanding clear-wave rings |
| 10 | Key | Utility | Brass skeleton key, diagonal, unlock shimmer |
| 11 | Cell Key | Utility | Prison-bar bow key, tarnished brass |
| 12 | Rat Key | Utility | Rat-head bow key, dirty sewer brass |
| 13 | Map | Utility | Aged parchment scroll, floor layout, secret room revealed |
| 14 | Ammo | Ammo | Green military ammo box, open lid showing bullets |
| 15 | Spread Ammo | Ammo | Steel-blue ammo box, mixed bullet types, co-op share |
| 16 | Supply Drop | Ammo | Parachute crate with star, green smoke trail |

### Mechanic-Visual Integration

Each consumable prompt integrates the item's game mechanic into the visual:
- **Blank** → shows expanding clear-wave rings (the blank effect)
- **Armor** → shows blank-burst-on-break ring (armor breaks → free blank)
- **Map** → shows secret room revealed on the parchment
- **Supply Drop** → shows parachute descent + green smoke flare
- **Glass Guon Stone** → shows orbital trail (orbits the player)
- **Spent (enemy)** → shows more spawning from ground (kill one → waves spawn)

### Current Consumable Asset State

All 16 pickup icons at `assets/images/pickups/` are tiny stubs (109–250 bytes). No real art exists.

---

## 8. Art Direction Standards

### Consistent Composition Rules (all splash images)

1. **1:1 square canvas**
2. **Solid dark minimalist background** (theme-specific dark color, no gradient)
3. **Central Gungeon-inspired focal subject**
4. **Theme palette used throughout** (subject, glow, accents)
5. **Controlled pixel-art lighting** (no smooth bloom)
6. **Theme-specific motif/glyph**
7. **Bottom or lower-third label text**
8. **Theme name in bold pixel-style typography** with themed glow
9. **Negative prompt clause** for unwanted rendering styles

### Negative Prompt Clause (all prompts)

```
Avoid photorealism, smooth 3D CGI, anime styling, generic cyberpunk city scenery, realistic human anatomy, oversized Hollywood robot proportions, excessive bloom, blurry gradients, modern app UI mockups, random illegible text, misspelled title text, and non-pixel-art rendering.
```

### Enemy-Specific Standards (doopey goopey)

- **Doopey goopey cute eyes** — huge googly eyes, derpy expressions, crosseyed aiming
- **1:1 with codex JSON description** — every mechanic, attack pattern, and visual detail matches
- **Portrait icon format** — 1:1 square, dark bg, no text/border, ready for codex grid
- **Exact real in-game appearance** — shape, color, material, proportions match the sprite
- **Googly eyes are the ONLY departure** from the real sprite design

### Hero-Specific Standards (gungeoneers)

- **Hero eyes** — normal/brave/determined, NOT googly (these are heroes, not enemies)
- **Named starting weapons** referenced in prompts
- **Named starting items** referenced in prompts
- **Character-specific details** (dog companion, junk pile, cape, tank treads, glitching afterimages)

### Robot Theme Technical Standards

- Stylized Enter the Gungeon bullet-kin/robot silhouette (not generic humanoid robot)
- Chunky retro pixel-sprite proportions
- Visible rivets, bolts, segmented armor, exposed circuitry, mechanical joints
- Central power core or reactor with controlled emissive pixels
- Gungeon weapon/casing language (brass bullet casings, shell motifs, dungeon stone)
- Pixel-art dithering and stepped highlights
- CRT scanlines, terminal glyphs, circuit traces, tactical HUD motifs
- Limited palette based on actual theme colors
- Dark dungeon background with readable silhouette

---

## 9. Pending / Optional Follow-Up

### Immediate (user-requested, not yet done)

- **52 new palette-variant splash prompts** (14 themes × 3 new variants + Unicorn's 5 missing palettes) — palette direction table approved, prompts not yet written
- **3 Bubblegum Unicorn color schemas for logo rework** — user requested, interrupted before starting

### Optional follow-up

- Write remaining 116 enemy prompts (Tier 4: all 146 enemies)
- Write all 26 boss prompts in consistent style (Tier 2)
- Add hidden/legacy theme prompts (18 themes) — only if user un-hides them
- Generate alternate costume variants for gungeoneers
- Write splash prompts for NPCs (34 entries in `npcs.json`)
- Write splash prompts for objects/chests (42 entries in `objects.json`)

### Not pending

- No Flutter code changes requested
- No asset generation being performed (user generates images separately)
- No splash assets wired into `pubspec.yaml`
- No changes to theme definitions in `app_theme.dart`
- No commits or version bumps

---

## Source Files Referenced

| File | Purpose |
|------|---------|
| `gungeon_mate/lib/services/app_theme.dart` | Theme definitions, palettes, `kVisibleThemes`, `UnicornPalette` |
| `gungeon_mate/assets/data/enemies.json` | 146 enemy entries (name, description, health, location, tips) |
| `gungeon_mate/assets/data/bosses.json` | 26 boss entries (name, description, ammonomicon, health, location) |
| `gungeon_mate/assets/data/gungeoneers.json` | 9 gungeoneer entries (name, short_desc, playstyle, starting_guns, starting_items, past) |
| `gungeon_mate/assets/data/pickups.json` | 17 pickup entries (name, category, description, location, tips) |
| `gungeon_mate/assets/images/enemies/` | 146 stub icon files (all <3KB, no real art) |
| `gungeon_mate/assets/images/bosses/` | 27 icon files (17 real, 10 stubs) |
| `gungeon_mate/assets/images/pickups/` | 16 stub icon files (all <250 bytes) |
| `gungeon_mate/assets/images/gungeoneers/` | 9 gungeoneer sprite sets (animated GIFs + static WebPs) |
| `gungeon_mate/assets/images/GM-logo.png` | App logo (790KB) |
| `gungeon_mate/assets/images/app_icon.png` | App icon (4.8MB) |
| `gungeon-mate-app-logo.png` (root) | App logo variant (6.2MB) |

---

## Prompt Count Summary

| Category | Prompts Written | Prompts Pending |
|----------|----------------|-----------------|
| Theme splashes (15 × 2 variants) | 30 | 0 |
| Theme palette variants (I–IV) | 0 | 52 |
| Gungeoneer splashes | 9 | 0 |
| Enemy codex (batch 1: stub bosses) | 10 | 0 |
| Enemy codex (batch 2: common enemies) | 30 | 0 |
| Enemy codex (batch 3: hyper-explicit basics) | 6 | 0 |
| Enemy codex (remaining 116 enemies) | 0 | 116 |
| Boss codex (all 26 consistent) | 0 | 26 |
| Consumable splashes | 16 | 0 |
| Logo rework (Bubblegum Unicorn) | 0 | 3 |
| **Total written** | **101** | **197 pending** |
