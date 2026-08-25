# Roomian Races & Art Direction — Sprite Generation Pipeline

> **Status:** Active design document  
> **Date:** Jul 25, 2026  
> **Scope:** Race definitions, L1 evolution visual sheets, Midjourney prompt JSONs, L5/L8 grid planning

---

## 1. RACE OVERVIEW

Six races are planned. Three are defined now; the remaining three will follow the same structure.

| Race | Archetype | Stat Modifiers | Visual Identity | Personality |
|------|-----------|---------------|-----------------|-------------|
| **Blob** | Amorphous gel | +2 VIT, -2 SPD | Round, translucent, wobbly, dot eyes | Content, simple, aloof |
| **Mothkin** | Fuzzy moth-folk | +2 LCK, +2 SPD, -2 GRT, -2 VIT | Fuzzy body, compound eyes, wing-nubs, antennae | Skittish, curious, drawn to light |
| **Cragling** | Living mineral | +2 GRT, +2 VIT, -2 SPD, -2 LCK | Angular crystalline body, jagged edges, mineral veins | Stoic, ancient, unbothered |
| _*(planned)*_ | _*Sproutlet*_ | _*TBD*_ | _*Plant-like, leafy*_ | _*TBD*_ |
| _*(planned)*_ | _*Pip*_ | _*TBD*_ | _*Small round bird-like*_ | _*TBD*_ |
| _*(planned)*_ | _*Wisp*_ | _*TBD*_ | _*Ghostly flame-like*_ | _*TBD*_ |

### Race Stat Modifiers (applied to base stats at L0)

```
Base stats (all races): VIT 5, PWR 5, GRT 5, SPD 5, LCK 5, INT 5

Blob:      VIT +2, SPD -2  →  VIT 7, PWR 5, GRT 5, SPD 3, LCK 5, INT 5
Mothkin:   LCK +2, SPD +2, GRT -2, VIT -2  →  VIT 3, PWR 5, GRT 3, SPD 7, LCK 7, INT 5
Cragling:  GRT +2, VIT +2, SPD -2, LCK -2  →  VIT 7, PWR 5, GRT 7, SPD 3, LCK 3, INT 5
```

---

## 2. SHARED ART STYLE — Midjourney Technical Base

All Roomian sprites share a consistent visual language derived from the GungeonMate aesthetic:

```
STYLE TAGS (append to every prompt):
32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick,
classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures,
low resolution, highly saturated focal colors, deep high-contrast dark shadowed background,
video game character sprite, full body front view, idle pose

TECHNICAL PARAMS:
--ar 1:1 --s 300 --niji 6 --style raw --no text, watermark, blur, gradient

NOTES:
- Niji 7 (--niji 7) is more literal/follows prompts more closely. Good for final production sprites.
- Niji 6 (--niji 6) is more "vibey". Good for initial exploration.
- Use --sref [CODE] once you find a good style code for cross-generation consistency.
- Use --seed [VALUE] to reproduce similar results when iterating on a design.
- Keep prompts under ~60 words for best results (MJ truncates very long prompts).
- See docs/midjourney_reference_guide.md for complete parameter reference.
```

### Color Palette per Element

| Element | Primary | Secondary | Glow/Accent | Background Tint |
|---------|---------|-----------|-------------|-----------------|
| **Fire** | #FF6B35 (amber-orange) | #D62828 (deep red) | #FFD23F (gold) | #1A0A00 |
| **Water** | #4ECDC4 (cyan-teal) | #2196F3 (blue) | #E0F7FA (ice white) | #001A1A |
| **Earth** | #8BC34A (moss green) | #795548 (bark brown) | #C5E1A5 (pale green) | #0A1A0A |
| **Air** | #B0BEC5 (silver-grey) | #90A4AE (steel) | #E1F5FE (pale blue) | #0F0F1A |
| **Light** | #FFEB3B (radiant yellow) | #FFC107 (gold) | #FFFFFF (pure white) | #1A1500 |
| **Dark** | #7B1FA2 (deep purple) | #4A148C (void purple) | #E1BEE7 (pale lavender) | #0A0014 |

---

## 3. RACE 1: BLOB — L1 Evolution Sheet (6 Elements)

### Visual Identity

The Blob is the simplest race — a round, translucent, gelatinous body with two dot eyes. No limbs, no mouth. It wobbles. At L1, the element infuses the gel, changing its color, internal patterns, and surface texture. The silhouette stays round but the details transform.

### L1 Evolution Descriptions

| Element | Name | Visual Description |
|---------|------|-------------------|
| **Fire** | **Lavablob** | Molten amber-orange gel, glowing lava cracks across surface, steam rising, internal magma swirl visible through translucent body, ember particles floating |
| **Water** | **Tideblob** | Liquid cyan-teal gel, internal waves and bubbles, ice crystal formations on surface, water droplets dripping, bioluminescent depth glow |
| **Earth** | **Mossblob** | Muddy green-brown gel, embedded pebbles and small stones, moss patches growing on surface, tiny sprouts poking through, root veins visible inside |
| **Air** | **Cloudblob** | Semi-transparent silver-white gel, tiny lightning bolts crackling inside, wispy cloud-like edges dissolving into mist, static charge particles |
| **Light** | **Prismblob** | Radiant golden-yellow gel, intense internal glow, halo particles orbiting, rainbow light refractions through body, pure white core |
| **Dark** | **Voidblob** | Deep purple-black gel, empty white ring eyes, shadow miasma trailing, light-absorbing surface, faint purple cracks, void particles being pulled in |

### Midjourney Prompt JSONs

```json
[
  {
    "id": "blob_l1_fire",
    "race": "Blob",
    "level": 1,
    "element": "Fire",
    "name": "Lavablob",
    "prompt": "round translucent gelatinous blob creature, molten amber-orange glowing gel body, lava cracks across surface, internal magma swirl visible through translucent body, steam rising, ember particles floating, two small dot eyes, no limbs, wobbly round silhouette, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated amber and red colors, deep dark shadowed background, video game character sprite, full body front view, idle pose --ar 1:1 --s 300 --niji 6 --style raw",
    "colors": {"primary": "#FF6B35", "secondary": "#D62828", "glow": "#FFD23F", "bg": "#1A0A00"},
    "grid_position": "A1"
  },
  {
    "id": "blob_l1_water",
    "race": "Blob",
    "level": 1,
    "element": "Water",
    "name": "Tideblob",
    "prompt": "round translucent gelatinous blob creature, liquid cyan-teal gel body, internal waves and bubbles, ice crystal formations on surface, water droplets dripping, bioluminescent depth glow, two small dot eyes, no limbs, wobbly round silhouette, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated teal and blue colors, deep dark shadowed background, video game character sprite, full body front view, idle pose --ar 1:1 --s 300 --niji 6 --style raw",
    "colors": {"primary": "#4ECDC4", "secondary": "#2196F3", "glow": "#E0F7FA", "bg": "#001A1A"},
    "grid_position": "A2"
  },
  {
    "id": "blob_l1_earth",
    "race": "Blob",
    "level": 1,
    "element": "Earth",
    "name": "Mossblob",
    "prompt": "round translucent gelatinous blob creature, muddy green-brown gel body, embedded pebbles and small stones on surface, moss patches growing, tiny sprouts poking through, root veins visible inside, two small dot eyes, no limbs, wobbly round silhouette, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated moss green and bark brown colors, deep dark shadowed background, video game character sprite, full body front view, idle pose --ar 1:1 --s 300 --niji 6 --style raw",
    "colors": {"primary": "#8BC34A", "secondary": "#795548", "glow": "#C5E1A5", "bg": "#0A1A0A"},
    "grid_position": "A3"
  },
  {
    "id": "blob_l1_air",
    "race": "Blob",
    "level": 1,
    "element": "Air",
    "name": "Cloudblob",
    "prompt": "round translucent gelatinous blob creature, semi-transparent silver-white gel body, tiny lightning bolts crackling inside, wispy cloud-like edges dissolving into mist, static charge particles, two small dot eyes, no limbs, wobbly round silhouette, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated silver and pale blue colors, deep dark shadowed background, video game character sprite, full body front view, idle pose --ar 1:1 --s 300 --niji 6 --style raw",
    "colors": {"primary": "#B0BEC5", "secondary": "#90A4AE", "glow": "#E1F5FE", "bg": "#0F0F1A"},
    "grid_position": "B1"
  },
  {
    "id": "blob_l1_light",
    "race": "Blob",
    "level": 1,
    "element": "Light",
    "name": "Prismblob",
    "prompt": "round translucent gelatinous blob creature, radiant golden-yellow gel body, intense internal glow, halo particles orbiting, rainbow light refractions through body, pure white glowing core, two small dot eyes, no limbs, wobbly round silhouette, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated gold and yellow colors, deep dark shadowed background, video game character sprite, full body front view, idle pose --ar 1:1 --s 300 --niji 6 --style raw",
    "colors": {"primary": "#FFEB3B", "secondary": "#FFC107", "glow": "#FFFFFF", "bg": "#1A1500"},
    "grid_position": "B2"
  },
  {
    "id": "blob_l1_dark",
    "race": "Blob",
    "level": 1,
    "element": "Dark",
    "name": "Voidblob",
    "prompt": "round translucent gelatinous blob creature, deep purple-black gel body, empty white ring eyes, shadow miasma trailing, light-absorbing surface, faint purple cracks, void particles being pulled inward, no limbs, wobbly round silhouette, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated deep purple colors, deep dark shadowed background, video game character sprite, full body front view, idle pose --ar 1:1 --s 300 --niji 6 --style raw",
    "colors": {"primary": "#7B1FA2", "secondary": "#4A148C", "glow": "#E1BEE7", "bg": "#0A0014"},
    "grid_position": "B3"
  }
]
```

---

## 4. RACE 2: MOTHKIN — L1 Evolution Sheet (6 Elements)

### Visual Identity

Mothkin are fuzzy, round-bodied moth-folk with large compound eyes, small wing-nubs on their backs, and feathery antennae. At L1, the element infuses their fuzz color, wing-nub texture, and antennae shape. They're smaller and more delicate than Blobs — their silhouette has wing-nubs and antennae protruding.

### L1 Evolution Descriptions

| Element | Name | Visual Description |
|---------|------|-------------------|
| **Fire** | **Emberwing** | Warm orange fuzz, glowing ember wing-nubs, ash particles trailing, heat shimmer around body, red compound eyes, smoldering antennae tips |
| **Water** | **Frostweb** | Pale blue fuzz, crystalline ice wing-nubs, frost crystals on antennae, frozen breath mist, icy blue compound eyes, snowflake patterns on body |
| **Earth** | **Mossback** | Green fuzz, leafy wing-nubs, bark-textured body segments, root-like antennae, earthy brown compound eyes, small mushrooms growing on back |
| **Air** | **Galewing** | Silver-grey fuzz, translucent wind-swept wing-nubs, static-charged fur standing on end, whirlwind antennae, pale grey compound eyes, tiny cyclones around feet |
| **Light** | **Prismwing** | White-gold fuzz, iridescent rainbow wing-nubs, glowing antennae, radiant compound eyes like tiny suns, light particles drifting, halo around body |
| **Dark** | **Voidmoth** | Dark purple-black fuzz, tattered shadow wing-nubs, purple glowing compound eyes, dark mist antennae, shadow particles trailing, starry void pattern on body |

### Midjourney Prompt JSONs

```json
[
  {
    "id": "mothkin_l1_fire",
    "race": "Mothkin",
    "level": 1,
    "element": "Fire",
    "name": "Emberwing",
    "prompt": "small fuzzy moth creature, round fluffy body, warm orange fuzz, glowing ember wing-nubs on back, ash particles trailing, feathery antennae with smoldering tips, large red compound eyes, heat shimmer around body, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated orange and red colors, deep dark shadowed background, video game character sprite, full body front view, idle pose --ar 1:1 --s 300 --niji 6 --style raw",
    "colors": {"primary": "#FF6B35", "secondary": "#D62828", "glow": "#FFD23F", "bg": "#1A0A00"},
    "grid_position": "A1"
  },
  {
    "id": "mothkin_l1_water",
    "race": "Mothkin",
    "level": 1,
    "element": "Water",
    "name": "Frostweb",
    "prompt": "small fuzzy moth creature, round fluffy body, pale blue fuzz, crystalline ice wing-nubs on back, frost crystals on feathery antennae, frozen breath mist, large icy blue compound eyes, snowflake patterns on body, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated teal and blue colors, deep dark shadowed background, video game character sprite, full body front view, idle pose --ar 1:1 --s 300 --niji 6 --style raw",
    "colors": {"primary": "#4ECDC4", "secondary": "#2196F3", "glow": "#E0F7FA", "bg": "#001A1A"},
    "grid_position": "A2"
  },
  {
    "id": "mothkin_l1_earth",
    "race": "Mothkin",
    "level": 1,
    "element": "Earth",
    "name": "Mossback",
    "prompt": "small fuzzy moth creature, round fluffy body, green fuzz, leafy wing-nubs on back, bark-textured body segments, root-like feathery antennae, large earthy brown compound eyes, small mushrooms growing on back, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated moss green and brown colors, deep dark shadowed background, video game character sprite, full body front view, idle pose --ar 1:1 --s 300 --niji 6 --style raw",
    "colors": {"primary": "#8BC34A", "secondary": "#795548", "glow": "#C5E1A5", "bg": "#0A1A0A"},
    "grid_position": "A3"
  },
  {
    "id": "mothkin_l1_air",
    "race": "Mothkin",
    "level": 1,
    "element": "Air",
    "name": "Galewing",
    "prompt": "small fuzzy moth creature, round fluffy body, silver-grey fuzz, translucent wind-swept wing-nubs on back, static-charged fur standing on end, whirlwind feathery antennae, large pale grey compound eyes, tiny cyclones around feet, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated silver and pale blue colors, deep dark shadowed background, video game character sprite, full body front view, idle pose --ar 1:1 --s 300 --niji 6 --style raw",
    "colors": {"primary": "#B0BEC5", "secondary": "#90A4AE", "glow": "#E1F5FE", "bg": "#0F0F1A"},
    "grid_position": "B1"
  },
  {
    "id": "mothkin_l1_light",
    "race": "Mothkin",
    "level": 1,
    "element": "Light",
    "name": "Prismwing",
    "prompt": "small fuzzy moth creature, round fluffy body, white-gold fuzz, iridescent rainbow wing-nubs on back, glowing feathery antennae, large radiant compound eyes like tiny suns, light particles drifting, halo around body, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated gold and yellow colors, deep dark shadowed background, video game character sprite, full body front view, idle pose --ar 1:1 --s 300 --niji 6 --style raw",
    "colors": {"primary": "#FFEB3B", "secondary": "#FFC107", "glow": "#FFFFFF", "bg": "#1A1500"},
    "grid_position": "B2"
  },
  {
    "id": "mothkin_l1_dark",
    "race": "Mothkin",
    "level": 1,
    "element": "Dark",
    "name": "Voidmoth",
    "prompt": "small fuzzy moth creature, round fluffy body, dark purple-black fuzz, tattered shadow wing-nubs on back, dark mist feathery antennae, large purple glowing compound eyes, shadow particles trailing, starry void pattern on body, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated deep purple colors, deep dark shadowed background, video game character sprite, full body front view, idle pose --ar 1:1 --s 300 --niji 6 --style raw",
    "colors": {"primary": "#7B1FA2", "secondary": "#4A148C", "glow": "#E1BEE7", "bg": "#0A0014"},
    "grid_position": "B3"
  }
]
```

---

## 5. RACE 3: CRAGLING — L1 Evolution Sheet (6 Elements)

### Visual Identity

Craglings are angular, crystalline beings made of living mineral. Their bodies are jagged and faceted, with visible mineral veins and small glowing eyes set into the stone. At L1, the element infuses the mineral composition, changing the crystal color, vein patterns, and surface texture. Their silhouette is spiky and geometric — the opposite of the Blob's roundness.

### L1 Evolution Descriptions

| Element | Name | Visual Description |
|---------|------|-------------------|
| **Fire** | **Magmacore** | Dark obsidian crust with glowing red-orange magma veins, heat shimmer, cracks radiating orange light, small ember eyes, smoke trailing from jagged peaks |
| **Water** | **Geode** | Blue crystal interior visible through cracked grey shell, icy blue surface crystals, frozen dew drops, pale blue glowing eyes, frost patterns on facets |
| **Earth** | **Mossstone** | Stone body covered in moss patches, embedded pebbles and roots, small flowers growing in cracks, green mineral veins, earthy brown glowing eyes |
| **Air** | **Sandstone** | Wind-eroded smooth sandy surface, hollow cavities, sand particles drifting off edges, swirling wind patterns carved into body, pale grey glowing eyes |
| **Light** | **Prismstone** | Refractive crystal facets catching and splitting light, internal golden glow, rainbow reflections on surface, bright white glowing eyes, light beams from cracks |
| **Dark** | **Voidstone** | Deep black obsidian body, purple mineral veins absorbing light, dark energy crackling, void portals in cracks, dim purple glowing eyes, shadow particles |

### Midjourney Prompt JSONs

```json
[
  {
    "id": "cragling_l1_fire",
    "race": "Cragling",
    "level": 1,
    "element": "Fire",
    "name": "Magmacore",
    "prompt": "angular crystalline mineral creature, jagged geometric body made of dark obsidian crust, glowing red-orange magma veins through cracks, heat shimmer, small ember glowing eyes, smoke trailing from jagged peaks, spiky silhouette, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated red and orange colors, deep dark shadowed background, video game character sprite, full body front view, idle pose --ar 1:1 --s 300 --niji 6 --style raw",
    "colors": {"primary": "#FF6B35", "secondary": "#D62828", "glow": "#FFD23F", "bg": "#1A0A00"},
    "grid_position": "A1"
  },
  {
    "id": "cragling_l1_water",
    "race": "Cragling",
    "level": 1,
    "element": "Water",
    "name": "Geode",
    "prompt": "angular crystalline mineral creature, jagged geometric body, blue crystal interior visible through cracked grey shell, icy blue surface crystals, frozen dew drops, pale blue glowing eyes, frost patterns on facets, spiky silhouette, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated teal and blue colors, deep dark shadowed background, video game character sprite, full body front view, idle pose --ar 1:1 --s 300 --niji 6 --style raw",
    "colors": {"primary": "#4ECDC4", "secondary": "#2196F3", "glow": "#E0F7FA", "bg": "#001A1A"},
    "grid_position": "A2"
  },
  {
    "id": "cragling_l1_earth",
    "race": "Cragling",
    "level": 1,
    "element": "Earth",
    "name": "Mossstone",
    "prompt": "angular crystalline mineral creature, jagged geometric body, stone surface covered in moss patches, embedded pebbles and roots, small flowers growing in cracks, green mineral veins, earthy brown glowing eyes, spiky silhouette, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated moss green and brown colors, deep dark shadowed background, video game character sprite, full body front view, idle pose --ar 1:1 --s 300 --niji 6 --style raw",
    "colors": {"primary": "#8BC34A", "secondary": "#795548", "glow": "#C5E1A5", "bg": "#0A1A0A"},
    "grid_position": "A3"
  },
  {
    "id": "cragling_l1_air",
    "race": "Cragling",
    "level": 1,
    "element": "Air",
    "name": "Sandstone",
    "prompt": "angular crystalline mineral creature, jagged geometric body, wind-eroded smooth sandy surface, hollow cavities, sand particles drifting off edges, swirling wind patterns carved into body, pale grey glowing eyes, spiky silhouette, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated silver and pale blue colors, deep dark shadowed background, video game character sprite, full body front view, idle pose --ar 1:1 --s 300 --niji 6 --style raw",
    "colors": {"primary": "#B0BEC5", "secondary": "#90A4AE", "glow": "#E1F5FE", "bg": "#0F0F1A"},
    "grid_position": "B1"
  },
  {
    "id": "cragling_l1_light",
    "race": "Cragling",
    "level": 1,
    "element": "Light",
    "name": "Prismstone",
    "prompt": "angular crystalline mineral creature, jagged geometric body, refractive crystal facets catching and splitting light, internal golden glow, rainbow reflections on surface, bright white glowing eyes, light beams from cracks, spiky silhouette, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated gold and yellow colors, deep dark shadowed background, video game character sprite, full body front view, idle pose --ar 1:1 --s 300 --niji 6 --style raw",
    "colors": {"primary": "#FFEB3B", "secondary": "#FFC107", "glow": "#FFFFFF", "bg": "#1A1500"},
    "grid_position": "B2"
  },
  {
    "id": "cragling_l1_dark",
    "race": "Cragling",
    "level": 1,
    "element": "Dark",
    "name": "Voidstone",
    "prompt": "angular crystalline mineral creature, jagged geometric body, deep black obsidian surface, purple mineral veins absorbing light, dark energy crackling, void portals in cracks, dim purple glowing eyes, shadow particles, spiky silhouette, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated deep purple colors, deep dark shadowed background, video game character sprite, full body front view, idle pose --ar 1:1 --s 300 --niji 6 --style raw",
    "colors": {"primary": "#7B1FA2", "secondary": "#4A148C", "glow": "#E1BEE7", "bg": "#0A0014"},
    "grid_position": "B3"
  }
]
```

---

## 6. L1 GRID GENERATION — 3x3 Sprite Sheet Prompts

Instead of generating 6 individual sprites per race, we can generate one 3x3 grid image per race. The grid contains 6 element variants plus 3 cells for the base L0 Blob form (or empty/label cells).

### Grid Layout (per race)

```
┌─────────────┬─────────────┬─────────────┐
│  A1: Fire   │  A2: Water  │  A3: Earth  │
├─────────────┼─────────────┼─────────────┤
│  B1: Air    │  B2: Light  │  B3: Dark   │
├─────────────┼─────────────┼─────────────┤
│  C1: L0     │  C2: L0     │  C3: EMPTY  │
│  Base form  │  Alt pose   │  (label)    │
└─────────────┴─────────────┴─────────────┘
```

### Grid Prompt JSONs

```json
[
  {
    "id": "blob_l1_grid",
    "race": "Blob",
    "level": 1,
    "type": "grid_3x3",
    "prompt": "3x3 grid sprite sheet of 9 variations of a round translucent gelatinous blob creature with dot eyes and no limbs, top row: fire element with molten amber lava cracks, water element with ice crystals and bubbles, earth element with moss and pebbles, middle row: air element with lightning and cloud wisps, light element with golden glow and rainbow refractions, dark element with purple void and shadow miasma, bottom row: plain base form, plain base form side view, empty space with label text, each cell full body front view idle pose, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated colors, dark background, video game character sprite sheet --ar 1:1 --s 300 --niji 6 --style raw",
    "cells": [
      {"pos": "A1", "id": "blob_l1_fire", "name": "Lavablob"},
      {"pos": "A2", "id": "blob_l1_water", "name": "Tideblob"},
      {"pos": "A3", "id": "blob_l1_earth", "name": "Mossblob"},
      {"pos": "B1", "id": "blob_l1_air", "name": "Cloudblob"},
      {"pos": "B2", "id": "blob_l1_light", "name": "Prismblob"},
      {"pos": "B3", "id": "blob_l1_dark", "name": "Voidblob"},
      {"pos": "C1", "id": "blob_l0_base", "name": "Blob (base)"},
      {"pos": "C2", "id": "blob_l0_side", "name": "Blob (side)"},
      {"pos": "C3", "id": "empty", "name": "label"}
    ]
  },
  {
    "id": "mothkin_l1_grid",
    "race": "Mothkin",
    "level": 1,
    "type": "grid_3x3",
    "prompt": "3x3 grid sprite sheet of 9 variations of a small fuzzy moth creature with round fluffy body, compound eyes, wing-nubs and feathery antennae, top row: fire element with orange ember wings and ash, water element with ice crystal wings and frost, earth element with leafy wings and moss, middle row: air element with translucent wind wings and static, light element with iridescent rainbow wings and glow, dark element with tattered shadow wings and void, bottom row: plain base form, plain base form side view, empty space with label text, each cell full body front view idle pose, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated colors, dark background, video game character sprite sheet --ar 1:1 --s 300 --niji 6 --style raw",
    "cells": [
      {"pos": "A1", "id": "mothkin_l1_fire", "name": "Emberwing"},
      {"pos": "A2", "id": "mothkin_l1_water", "name": "Frostweb"},
      {"pos": "A3", "id": "mothkin_l1_earth", "name": "Mossback"},
      {"pos": "B1", "id": "mothkin_l1_air", "name": "Galewing"},
      {"pos": "B2", "id": "mothkin_l1_light", "name": "Prismwing"},
      {"pos": "B3", "id": "mothkin_l1_dark", "name": "Voidmoth"},
      {"pos": "C1", "id": "mothkin_l0_base", "name": "Mothkin (base)"},
      {"pos": "C2", "id": "mothkin_l0_side", "name": "Mothkin (side)"},
      {"pos": "C3", "id": "empty", "name": "label"}
    ]
  },
  {
    "id": "cragling_l1_grid",
    "race": "Cragling",
    "level": 1,
    "type": "grid_3x3",
    "prompt": "3x3 grid sprite sheet of 9 variations of an angular crystalline mineral creature with jagged geometric body and small glowing eyes, top row: fire element with obsidian and magma veins, water element with blue geode crystals, earth element with moss and stone, middle row: air element with wind-eroded sandstone, light element with refractive prism facets, dark element with void obsidian and purple veins, bottom row: plain base form, plain base form side view, empty space with label text, each cell full body front view idle pose, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated colors, dark background, video game character sprite sheet --ar 1:1 --s 300 --niji 6 --style raw",
    "cells": [
      {"pos": "A1", "id": "cragling_l1_fire", "name": "Magmacore"},
      {"pos": "A2", "id": "cragling_l1_water", "name": "Geode"},
      {"pos": "A3", "id": "cragling_l1_earth", "name": "Mossstone"},
      {"pos": "B1", "id": "cragling_l1_air", "name": "Sandstone"},
      {"pos": "B2", "id": "cragling_l1_light", "name": "Prismstone"},
      {"pos": "B3", "id": "cragling_l1_dark", "name": "Voidstone"},
      {"pos": "C1", "id": "cragling_l0_base", "name": "Cragling (base)"},
      {"pos": "C2", "id": "cragling_l0_side", "name": "Cragling (side)"},
      {"pos": "C3", "id": "empty", "name": "label"}
    ]
  }
]
```

---

## 7. L5 & L8 EVOLUTION GRID PLANNING

### Evolution Structure Recap

```
L0: Base form (race only, no element)
L1: Element chosen (6 paths)          → 6 variations per race
L5: Refinement chosen (3 per element)  → 18 variations per race
L8: Mastery chosen (2 per refinement)  → 36 variations per race
```

### L5 Grid Layout (2 grids per race, 9 cells each)

Each element has 3 refinements. We group 3 elements per grid:

**Grid L5-A (Fire + Water + Earth refinements):**
```
┌──────────────────┬──────────────────┬──────────────────┐
│  A1: Fire-R1     │  A2: Fire-R2     │  A3: Fire-R3     │
│  (e.g. Blaze)    │  (e.g. Inferno)  │  (e.g. Phoenix)  │
├──────────────────┼──────────────────┼──────────────────┤
│  B1: Water-R1    │  B2: Water-R2    │  B3: Water-R3    │
│  (e.g. Frost)    │  (e.g. Tide)     │  (e.g. Abyss)    │
├──────────────────┼──────────────────┼──────────────────┤
│  C1: Earth-R1    │  C2: Earth-R2    │  C3: Earth-R3    │
│  (e.g. Root)     │  (e.g. Mountain) │  (e.g. Crystal)  │
└──────────────────┴──────────────────┴──────────────────┘
```

**Grid L5-B (Air + Light + Dark refinements):**
```
┌──────────────────┬──────────────────┬──────────────────┐
│  A1: Air-R1      │  A2: Air-R2      │  A3: Air-R3      │
│  (e.g. Storm)    │  (e.g Cyclone)   │  (e.g. Vacuum)   │
├──────────────────┼──────────────────┼──────────────────┤
│  B1: Light-R1    │  B2: Light-R2    │  B3: Light-R3    │
│  (e.g. Solar)    │  (e.g. Prism)    │  (e.g. Radiant)  │
├──────────────────┼──────────────────┼──────────────────┤
│  C1: Dark-R1     │  C2: Dark-R2     │  C3: Dark-R3     │
│  (e.g. Shadow)   │  (e.g. Eclipse)  │  (e.g. Null)     │
└──────────────────┴──────────────────┴──────────────────┘
```

### L8 Grid Layout (4 grids per race, 9 cells each)

Each refinement has 2 masteries. 6 elements × 3 refinements × 2 masteries = 36. We split into 4 grids of 9:

**Grid L8-A (Fire: 6 + Water: 3):**
```
┌──────────────────┬──────────────────┬──────────────────┐
│  A1: Fire-R1-M1  │  A2: Fire-R1-M2  │  A3: Fire-R2-M1  │
├──────────────────┼──────────────────┼──────────────────┤
│  B1: Fire-R2-M2  │  B2: Fire-R3-M1  │  B3: Fire-R3-M2  │
├──────────────────┼──────────────────┼──────────────────┤
│  C1: Water-R1-M1 │  C2: Water-R1-M2 │  C3: Water-R2-M1 │
└──────────────────┴──────────────────┴──────────────────┘
```

**Grid L8-B (Water: 3 + Earth: 6):**
```
┌──────────────────┬──────────────────┬──────────────────┐
│  A1: Water-R2-M2 │  A2: Water-R3-M1 │  A3: Water-R3-M2 │
├──────────────────┼──────────────────┼──────────────────┤
│  B1: Earth-R1-M1 │  B2: Earth-R1-M2 │  B3: Earth-R2-M1 │
├──────────────────┼──────────────────┼──────────────────┤
│  C1: Earth-R2-M2 │  C2: Earth-R3-M1 │  C3: Earth-R3-M2 │
└──────────────────┴──────────────────┴──────────────────┘
```

**Grid L8-C (Air: 6 + Light: 3):**
```
┌──────────────────┬──────────────────┬──────────────────┐
│  A1: Air-R1-M1   │  A2: Air-R1-M2   │  A3: Air-R2-M1   │
├──────────────────┼──────────────────┼──────────────────┤
│  B1: Air-R2-M2   │  B2: Air-R3-M1   │  B3: Air-R3-M2   │
├──────────────────┼──────────────────┼──────────────────┤
│  C1: Light-R1-M1 │  C2: Light-R1-M2 │  C3: Light-R2-M1 │
└──────────────────┴──────────────────┴──────────────────┘
```

**Grid L8-D (Light: 3 + Dark: 6):**
```
┌──────────────────┬──────────────────┬──────────────────┐
│  A1: Light-R2-M2 │  A2: Light-R3-M1 │  A3: Light-R3-M2 │
├──────────────────┼──────────────────┼──────────────────┤
│  B1: Dark-R1-M1  │  B2: Dark-R1-M2  │  B3: Dark-R2-M1  │
├──────────────────┼──────────────────┼──────────────────┤
│  C1: Dark-R2-M2  │  C2: Dark-R3-M1  │  C3: Dark-R3-M2  │
└──────────────────┴──────────────────┴──────────────────┘
```

### Total Grid Count

| Level | Grids per Race | 3 Races | Description |
|-------|---------------|---------|-------------|
| L1 | 1 | 3 | 6 elements + 3 base/label |
| L5 | 2 | 6 | 3 elements × 3 refinements per grid |
| L8 | 4 | 12 | 1.5 elements × 3 refinements × 2 masteries per grid |
| **Total** | **7** | **21** | **Complete sprite coverage** |

### L5 Grid Prompt Template

```
3x3 grid sprite sheet of 9 variations of [RACE NAME] at L5 refinement stage,
[BASE VISUAL DESCRIPTION],
top row: [ELEMENT 1] refinement 1 [DESC], refinement 2 [DESC], refinement 3 [DESC],
middle row: [ELEMENT 2] refinement 1 [DESC], refinement 2 [DESC], refinement 3 [DESC],
bottom row: [ELEMENT 3] refinement 1 [DESC], refinement 2 [DESC], refinement 3 [DESC],
each cell full body front view idle pose, more detailed and larger than L1,
evolved form with enhanced element features and secondary characteristics,
32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick,
classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures,
low resolution, highly saturated colors, dark background, video game character sprite sheet
--ar 1:1 --s 300 --niji 6 --style raw
```

### L8 Grid Prompt Template

```
3x3 grid sprite sheet of 9 variations of [RACE NAME] at L8 mastery stage,
[BASE VISUAL DESCRIPTION],
[CELL-BY-CELL DESCRIPTIONS WITH MASTERY NAMES],
each cell full body front view idle pose, most detailed and powerful form,
master form with dramatic element features, aura effects, and signature visual flair,
32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick,
classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures,
low resolution, highly saturated colors, dark background, video game character sprite sheet
--ar 1:1 --s 300 --niji 6 --style raw
```

### Visual Progression Rules (L1 → L5 → L8)

| Aspect | L1 (Element) | L5 (Refinement) | L8 (Mastery) |
|--------|-------------|-----------------|--------------|
| **Size** | Small (base silhouette) | Medium (15-20% larger, more detail) | Large (30% larger than L5, dramatic) |
| **Complexity** | Simple element infusion | Secondary element features emerge | Signature visual flair + aura |
| **Accessories** | None | Minor (e.g. small crystals, embers) | Major (e.g. crown of flames, ice wings) |
| **Glow** | Subtle internal glow | Visible aura around body | Dramatic aura + particle effects |
| **Eyes** | Element-colored dots | Element-colored with shape | Intense glowing element-shaped eyes |
| **Pose** | Neutral idle | Slightly dynamic idle | Confident/powerful idle |

---

## 8. PLANNED RACES (Future — Not Yet Detailed)

### Sproutlet
- **Archetype:** Plant-like creature with leaves and buds
- **Visual:** Small bulb body, root-feet, leaf arms, bud on head
- **Stat direction:** +2 INT, +2 VIT, -2 SPD, -2 PWR (smart and durable, slow and weak)
- **L1 concept:** Element changes the plant type (fire = cactus, water = lily, earth = oak, air = dandelion, light = sunflower, dark = mushroom)

### Pip
- **Archetype:** Small round bird-like creature
- **Visual:** Round body, tiny wings, beak, small feet, feathered crest
- **Stat direction:** +2 SPD, +2 LCK, -2 GRT, -2 INT (fast and lucky, fragile and dumb)
- **L1 concept:** Element changes feather type and beak shape (fire = phoenix, water = penguin, earth = ostrich, air = hummingbird, light = dove, dark = raven)

### Wisp
- **Archetype:** Ghostly flame-like being
- **Visual:** Floating flame body, no legs, wispy tail, small arm-nubs, glowing core
- **Stat direction:** +2 INT, +2 PWR, -2 VIT, -2 LCK (powerful caster, fragile and unlucky)
- **L1 concept:** Element changes the flame type (fire = bonfire, water = will-o-wisp, earth = foxfire, air = st-elmo, light = holy flame, dark = hellfire)

---

## 9. PRODUCTION WORKFLOW

### Step 1: Generate L1 Grids (3 images)
1. Run each race's `*_l1_grid` prompt in Midjourney
2. Upscale each of the 9 cells individually
3. Extract individual sprites from the grid
4. Clean up backgrounds (remove dark BG → transparent PNG)
5. Name files: `[race]_l1_[element].png` (e.g. `blob_l1_fire.png`)

### Step 2: Review & Iterate
1. Check visual consistency across races
2. Verify element colors match the palette table
3. Ensure silhouettes are distinct between races
4. Iterate on any unsatisfactory cells with individual prompts

### Step 3: Generate L5 Grids (6 images)
1. Define refinement names and visual descriptions for each element
2. Build grid prompts using the L5 template
3. Generate, upscale, extract, clean
4. Name files: `[race]_l5_[element]_[refinement].png`

### Step 4: Generate L8 Grids (12 images)
1. Define mastery names and visual descriptions for each refinement
2. Build grid prompts using the L8 template
3. Generate, upscale, extract, clean
4. Name files: `[race]_l8_[element]_[refinement]_[mastery].png`

### File Organization

```
assets/roomians/
├── blob/
│   ├── l0/
│   │   └── blob_l0_base.png
│   ├── l1/
│   │   ├── blob_l1_fire.png
│   │   ├── blob_l1_water.png
│   │   ├── blob_l1_earth.png
│   │   ├── blob_l1_air.png
│   │   ├── blob_l1_light.png
│   │   └── blob_l1_dark.png
│   ├── l5/
│   │   ├── blob_l5_fire_blaze.png
│   │   ├── blob_l5_fire_inferno.png
│   │   ├── blob_l5_fire_phoenix.png
│   │   └── ... (15 more)
│   └── l8/
│       ├── blob_l8_fire_blaze_ember.png
│       ├── blob_l8_fire_blaze_ash.png
│       └── ... (34 more)
├── mothkin/
│   └── ... (same structure)
├── cragling/
│   └── ... (same structure)
└── _grids/
    └── ... (raw grid images for reference)
```

---

## 10. REFINEMENT & MASTERY NAME SEEDS

These are placeholder names for L5 refinements and L8 masteries. They'll be finalized during game design but are needed for grid prompts.

### Fire
| L5 Refinement | L8 Mastery A | L8 Mastery B |
|--------------|-------------|-------------|
| Blaze | Ember | Ash |
| Inferno | Magma | Nova |
| Phoenix | Reborn | Eternal |

### Water
| L5 Refinement | L8 Mastery A | L8 Mastery B |
|--------------|-------------|-------------|
| Frost | Glacier | Permafrost |
| Tide | Maelstrom | Tsunami |
| Abyss | Voidsea | Leviathan |

### Earth
| L5 Refinement | L8 Mastery A | L8 Mastery B |
|--------------|-------------|-------------|
| Root | Ancient | Overgrowth |
| Mountain | Bedrock | Titan |
| Crystal | Geode | Prism |

### Air
| L5 Refinement | L8 Mastery A | L8 Mastery B |
|--------------|-------------|-------------|
| Storm | Thunder | Tempest |
| Cyclone | Hurricane | Vacuum |
| Vacuum | Voidwind | Silence |

### Light
| L5 Refinement | L8 Mastery A | L8 Mastery B |
|--------------|-------------|-------------|
| Solar | Corona | Supernova |
| Prism | Spectrum | Rainbow |
| Radiant | Halo | Dawn |

### Dark
| L5 Refinement | L8 Mastery A | L8 Mastery B |
|--------------|-------------|-------------|
| Shadow | Umbra | Shade |
| Eclipse | Totality | Penumbra |
| Null | Entropy | Oblivion |

---

## 11. COMPLETE VISUAL ASSET AUDIT

> Cross-referenced against all UI mockups in `roomian_visual_pictation.md` to identify every visual asset the game needs.

### Asset Categories — What We Have vs What's Missing

| # | Category | Status | Count (3 races) | Notes |
|---|----------|--------|-----------------|-------|
| 1 | L0 base race sprites | ❌ MISSING | 3 | Base form before elemental evolution |
| 2 | L1 elemental sprites | ✅ Prompted | 18 | 3 races × 6 elements — JSONs in this doc |
| 3 | L5 refinement sprites | 📋 Planned | 54 | 3 races × 6 elements × 3 refinements — grid structure planned |
| 4 | L8 mastery sprites | 📋 Planned | 108 | 3 races × 6 elements × 3 refinements × 2 masteries |
| 5 | Battle poses (per sprite) | ❌ MISSING | ~183 poses | idle, attack, hit, defend, downed per evolution |
| 6 | Avatar thumbnails | ❌ MISSING | ~183 icons | Cropped/resized headshots for belt & battle slots |
| 7 | Ability icons | ❌ MISSING | ~40+ icons | Attack, magic, defend, flee action icons |
| 8 | Passive ability icons | ❌ MISSING | ~36+ icons | One per L8 mastery passive (stack system) |
| 9 | Status effect icons | ❌ MISSING | 7 icons | Burning, Chilled, Stunned, Paralyzed, Blinded, Cursed, Charmed |
| 10 | Element icons | ❌ MISSING | 6 icons | Fire, Water, Earth, Air, Light, Dark |
| 11 | Belt/state icons | ❌ MISSING | 6 icons | READY, COOLDOWN, DOWNED, TRAINING, QUESTING, SCARS |
| 12 | Room Ball sprites | ❌ MISSING | 3 sprites | Standard (orange), Quality (blue), Master (gold) |
| 13 | Scar icons | ❌ MISSING | 6 icons | Weakened, Fractured, Slowed, Dulled, Lobotomized, Cursed |
| 14 | Evolution card art | ❌ MISSING | ~24 cards | L1 choice cards (6), L5 choice cards (18), L8 choice cards (36) |
| 15 | Battle VFX sprites | ❌ MISSING | ~12+ effects | Hit spark, slash, elemental burst, shield, heal, death dissolve |
| 16 | Catch screen VFX | ❌ MISSING | 3 effects | Ball throw, silhouette, reveal flash |
| 17 | Battle UI frame | ❌ MISSING | 1 set | Slot frame, resource bar templates, action button templates |

### Priority Tiers

**Tier 1 — MVP (need before any playable prototype):**
- L0 base race sprites (3)
- L1 elemental sprites (18) — already prompted
- Avatar thumbnails (cropped from L0/L1)
- Element icons (6)
- Status effect icons (7)
- Belt/state icons (6)
- Ability icons for basic actions (4: attack, magic, defend, flee)
- Room Ball sprites (3)

**Tier 2 — Vertical Slice (need for full battle flow):**
- Battle poses: idle + attack + hit + downed (4 poses × 21 L0+L1 sprites = 84)
- Battle VFX: hit spark, slash, elemental burst, shield, death dissolve (5+)
- Scar icons (6)
- Evolution card art (L1 set: 6 cards)
- Catch screen VFX (3)

**Tier 3 — Full Game (need for complete evolution system):**
- L5 refinement sprites (54)
- L8 mastery sprites (108)
- Passive ability icons (36+)
- Evolution card art (L5 + L8 sets)
- Defend pose, flee pose per sprite

---

### 11.1 L0 Base Race Sprites (MISSING — Tier 1)

We have L1 prompts but no L0 base form prompts. L0 is what appears on the belt, in catch reveals, and in evolution choice cards.

**L0 Sprite Requirements:**
- Neutral coloring (no element) — grey-white translucent body
- Smallest/simplest form of the race
- Front view, idle pose
- Same style tags as L1

**L0 Midjourney Prompt JSONs:**

```json
{
  "id": "blob_l0",
  "race": "Blob",
  "level": 0,
  "description": "Small round translucent grey-white gelatinous blob, two small dot eyes, no limbs, simple wobbly round silhouette, neutral coloring, no element",
  "prompt": "small round translucent grey-white gelatinous blob creature, two small dot eyes, no limbs, simple wobbly round silhouette, neutral pale coloring, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, muted pale colors, deep dark shadowed background, video game character sprite, full body front view, idle pose --ar 1:1 --s 300 --niji 6 --style raw --no text, watermark, blur, gradient"
}
```

```json
{
  "id": "mothkin_l0",
  "race": "Mothkin",
  "level": 0,
  "description": "Small fuzzy grey moth creature, large compound eyes, small wing-nubs, short antennae, fuzzy round body, neutral grey-white coloring",
  "prompt": "small fuzzy grey moth creature, large compound eyes, small wing-nubs, short antennae, fuzzy round body, neutral grey-white coloring, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, muted pale colors, deep dark shadowed background, video game character sprite, full body front view, idle pose --ar 1:1 --s 300 --niji 6 --style raw --no text, watermark, blur, gradient"
}
```

```json
{
  "id": "cragling_l0",
  "race": "Cragling",
  "level": 0,
  "description": "Small angular grey stone creature, crystalline body, jagged mineral edges, glowing white vein cracks, simple geometric form, neutral grey coloring",
  "prompt": "small angular grey stone creature, crystalline body, jagged mineral edges, glowing white vein cracks, simple geometric form, neutral grey coloring, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, muted pale colors, deep dark shadowed background, video game character sprite, full body front view, idle pose --ar 1:1 --s 300 --niji 6 --style raw --no text, watermark, blur, gradient"
}
```

**L0 Grid Prompt (all 3 races in one 3x1 grid):**
```json
{
  "id": "l0_race_grid",
  "description": "All 3 L0 base races in one image",
  "prompt": "3x1 grid sprite sheet of three small neutral creature sprites, left: small round translucent grey-white blob with dot eyes, center: small fuzzy grey moth with compound eyes and wing-nubs, right: small angular grey stone creature with crystalline body, all neutral coloring no elements, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, stippled dithered shading, clear cell separation, solid dark background, video game character sprites, full body front view, idle pose --ar 3:1 --s 300 --niji 6 --style raw --no text, watermark, blur, gradient"
}
```

---

### 11.2 Battle Poses & Animation Frames (MISSING — Tier 2)

Each sprite needs multiple poses for battle. Rather than generating per-pose individually, use a **pose grid per Roomian** — one 3x2 grid with all 6 poses.

**Required Poses:**
| Pose | Description | Used In |
|------|-------------|---------|
| **Idle** | Breathing, slight bob | Battle slots, belt, detail screen |
| **Attack** | Lunge forward, element flaring | Execution phase |
| **Hit** | Recoil, flash white | Taking damage |
| **Defend** | Guard stance, shield glow | Defend action |
| **Downed** | Collapsed, faded, ✗ over | Death/perish |
| **Flee** | Turned away, motion lines | Flee action (optional) |

**Pose Grid Prompt Template:**
```
3x2 grid sprite sheet of 6 poses of [RACE] [ELEMENT] Roomian: top-left idle breathing, top-right attack lunge with [ELEMENT] flare, bottom-left hit recoil, bottom-right defend guard stance, center-left downed collapsed, center-right flee turned away, [VISUAL DESCRIPTION], 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, stippled dithered shading, clear cell separation, solid dark background, video game character sprites, full body --ar 3:2 --s 300 --niji 6 --style raw --no text, watermark, blur, gradient
```

**Pose Grid Count:**
- L0: 3 races × 1 grid = 3 grids (6 poses each)
- L1: 3 races × 6 elements × 1 grid = 18 grids
- L5: 54 grids (when L5 sprites exist)
- L8: 108 grids (when L8 sprites exist)
- **MVP: 21 pose grids** covering L0 + L1

---

### 11.3 Avatar Thumbnails (MISSING — Tier 1)

Small icon-sized crops (32×32 or 48×48) of each Roomian's face/upper body for:
- Belt screen storage slots
- Battle slot headers (element + sprite)
- Evolution choice cards
- Catch reveal splash

**Approach:** Crop from full sprite — no Midjourney generation needed. Post-process in image editor:
1. Take full sprite PNG
2. Crop to head/upper-body bounding box
3. Resize to 48×48
4. Save as `[race]_l[level]_[element]_avatar.png`

**File naming:**
```
assets/roomians/avatars/
├── blob_l0_avatar.png
├── blob_l1_fire_avatar.png
├── blob_l1_water_avatar.png
├── ...
├── mothkin_l0_avatar.png
├── ...
└── cragling_l0_avatar.png
```

---

### 11.4 Ability Icons (MISSING — Tier 1+2)

The action modal shows ability cards with icons. Currently using emoji placeholders (⚔️✨🛡️💨). Need pixel art icons.

**Tier 1 — Basic Action Icons (4):**
| Icon | Name | Description |
|------|------|-------------|
| ⚔️ | Attack | Crossed swords, pixel art |
| ✨ | Magic | Sparkle/star burst, pixel art |
| 🛡️ | Defend | Shield with glow, pixel art |
| 💨 | Flee | Motion lines / dust cloud, pixel art |

**Tier 2 — Element-Specific Ability Icons (12+):**
Each element needs at least 2 ability icons (one attack, one magic):
| Element | Attack Icon | Magic Icon |
|---------|------------|------------|
| Fire | Flame slash | Fireball |
| Water | Ice shard | Frost wave |
| Earth | Rock throw | Stone wall |
| Air | Wind blade | Lightning |
| Light | Light beam | Holy flash |
| Dark | Shadow claw | Curse bolt |

**Ability Icon Grid Prompt:**
```json
{
  "id": "ability_icons_basic",
  "description": "4 basic action icons in 2x2 grid",
  "prompt": "2x2 grid icon sheet of four pixel art game icons: crossed swords attack, sparkling star magic burst, glowing shield defend, motion dust cloud flee, 32-bit chunky retro pixel art, Enter the Gungeon style, thick black pixel outlines, simple bold shapes, high contrast, solid dark background, video game UI icons --ar 1:1 --s 300 --niji 6 --style raw --no text, watermark, blur, gradient"
}
```

```json
{
  "id": "ability_icons_elements",
  "description": "12 elemental ability icons in 4x3 grid",
  "prompt": "4x3 grid icon sheet of twelve pixel art game ability icons: row1 flame-slash fireball ice-shard frost-wave, row2 rock-throw stone-wall wind-blade lightning-bolt, row3 light-beam holy-flash shadow-claw curse-bolt, 32-bit chunky retro pixel art, Enter the Gungeon style, thick black pixel outlines, simple bold shapes, element-colored, high contrast, solid dark background, video game UI icons --ar 4:3 --s 300 --niji 6 --style raw --no text, watermark, blur, gradient"
}
```

---

### 11.5 Passive Ability Icons (MISSING — Tier 3)

L8 masteries each grant a passive. With 36 masteries (6 elements × 3 refinements × 2 masteries), we need 36 passive icons.

**Approach:** Generate as a single 6x6 grid per element family, or one big 6x6 grid for all 36.

**Passive Icon Grid Prompt Template:**
```
6x6 grid icon sheet of 36 pixel art passive ability icons for monster collecting game, each icon represents a mastery passive: fire passives (burn aura, phoenix revive, ember trail), water passives (frost armor, tidal regen, abyss drain), earth passives (stone skin, root bind, crystal reflect), air passives (wind evade, storm charge, vacuum pull), light passives (holy shield, radiant heal, prism beam), dark passives (shadow cloak, curse touch, entropy decay), 32-bit chunky retro pixel art, Enter the Gungeon style, thick black pixel outlines, simple bold shapes, element-colored, high contrast, solid dark background, video game UI icons --ar 1:1 --s 300 --niji 6 --style raw --no text, watermark, blur, gradient
```

---

### 11.6 Status Effect Icons (MISSING — Tier 1)

7 status effects need pixel art icons. Currently emoji placeholders.

| Status | Current Emoji | Visual Description |
|--------|--------------|-------------------|
| Burning | 🔥 | Small flame icon, animated flicker |
| Chilled | ❄️ | Snowflake / ice crystal |
| Stunned | 💫 | Spiral stars / dizzy effect |
| Paralyzed | ⚡ | Lightning bolt / spark |
| Blinded | 🌟 | Eye with slash / dark flash |
| Cursed | 🌑 | Dark orb with purple aura |
| Charmed | ✨ | Heart with sparkles / pink swirl |

**Status Icon Grid Prompt:**
```json
{
  "id": "status_icons",
  "description": "7 status effect icons in 4x2 grid (1 empty cell)",
  "prompt": "4x2 grid icon sheet of seven pixel art status effect icons for monster collecting game: burning flame, frozen snowflake, dizzy spiral stars, paralyzed lightning bolt, blinded eye-with-slash, cursed dark purple orb, charmed pink heart sparkles, 32-bit chunky retro pixel art, Enter the Gungeon style, thick black pixel outlines, simple bold shapes, high contrast, solid dark background, video game UI icons --ar 2:1 --s 300 --niji 6 --style raw --no text, watermark, blur, gradient"
}
```

---

### 11.7 Element Icons (MISSING — Tier 1)

6 element icons for use in battle slots, belt, evolution cards, ability cards.

| Element | Visual Description |
|---------|-------------------|
| Fire | Stylized flame, amber-orange |
| Water | Water drop / wave, cyan-teal |
| Earth | Mountain / leaf, moss green |
| Air | Wind swirl / cloud, silver-grey |
| Light | Sun / star burst, pale gold |
| Dark | Moon / shadow, deep purple |

**Element Icon Grid Prompt:**
```json
{
  "id": "element_icons",
  "description": "6 element icons in 3x2 grid",
  "prompt": "3x2 grid icon sheet of six pixel art element icons for monster collecting game: fire flame amber-orange, water drop cyan-teal, earth mountain moss-green, air swirl silver-grey, light sun-burst pale-gold, dark moon deep-purple, 32-bit chunky retro pixel art, Enter the Gungeon style, thick black pixel outlines, simple bold shapes, element-colored, high contrast, solid dark background, video game UI icons --ar 3:2 --s 300 --niji 6 --style raw --no text, watermark, blur, gradient"
}
```

---

### 11.8 Belt/State Icons (MISSING — Tier 1)

6 status state icons for the belt/inventory screen.

| State | Current Emoji | Visual Description |
|-------|--------------|-------------------|
| READY | ✅ | Green checkmark in circle |
| COOLDOWN | ⏰ | Clock / hourglass |
| DOWNED | 💀 | Skull / fainted icon |
| TRAINING | 🩸 | Dumbbell / sweat drop |
| QUESTING | 🧭 | Compass / map |
| SCARS | ⚠️ | Warning / bandage / crack |

**State Icon Grid Prompt:**
```json
{
  "id": "state_icons",
  "description": "6 belt state icons in 3x2 grid",
  "prompt": "3x2 grid icon sheet of six pixel art status state icons for monster collecting game: green checkmark ready, clock cooldown, skull downed, dumbbell training, compass questing, bandage-crack scars, 32-bit chunky retro pixel art, Enter the Gungeon style, thick black pixel outlines, simple bold shapes, high contrast, solid dark background, video game UI icons --ar 3:2 --s 300 --niji 6 --style raw --no text, watermark, blur, gradient"
}
```

---

### 11.9 Room Ball Sprites (MISSING — Tier 1)

3 ball types for the catch mechanic.

| Ball | Color | Description |
|------|-------|-------------|
| Standard | Orange | Simple round ball, orange with white button |
| Quality | Blue | Round ball, blue with silver ring |
| Master | Gold | Round ball, gold with ornate engraving |

**Room Ball Grid Prompt:**
```json
{
  "id": "room_balls",
  "description": "3 Room Ball sprites in 3x1 grid",
  "prompt": "3x1 grid sprite sheet of three pixel art capture ball sprites: left simple orange ball with white center button, center blue ball with silver ring, right ornate gold ball with engraved details, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, stippled dithered shading, high contrast, solid dark background, video game item sprites --ar 3:1 --s 300 --niji 6 --style raw --no text, watermark, blur, gradient"
}
```

---

### 11.10 Scar Icons (MISSING — Tier 2)

6 scar types from the d6 death save table.

| Scar | Visual Description |
|------|-------------------|
| Weakened | Cracked sword / broken blade |
| Fractured | Cracked shield / bone crack |
| Slowed | Broken wing / snail shell |
| Dulled | Cracked crystal / faded glow |
| Lobotomized | Cracked skull / brain glitch |
| Cursed | Dark sigil / purple curse mark |

**Scar Icon Grid Prompt:**
```json
{
  "id": "scar_icons",
  "description": "6 scar icons in 3x2 grid",
  "prompt": "3x2 grid icon sheet of six pixel art scar/debuff icons for monster collecting game: cracked broken sword weakened, cracked shield fractured, broken wing slowed, faded cracked crystal dulled, cracked skull lobotomized, dark purple sigil cursed, 32-bit chunky retro pixel art, Enter the Gungeon style, thick black pixel outlines, simple bold shapes, desaturated red-purple tones, high contrast, solid dark background, video game UI icons --ar 3:2 --s 300 --niji 6 --style raw --no text, watermark, blur, gradient"
}
```

---

### 11.11 Battle VFX Sprites (MISSING — Tier 2)

Visual effects for battle execution phase.

| VFX | Description | Frames |
|-----|-------------|--------|
| Hit Spark | White/yellow impact burst | 3-4 frames |
| Slash | Arcing blade trail | 3-4 frames |
| Elemental Burst | Element-colored explosion | 4-6 frames per element |
| Shield | Blue hexagonal shield pop | 3-4 frames |
| Heal/Regen | Green sparkles rising | 3-4 frames |
| Death Dissolve | Pixel scatter / fade | 6-8 frames |
| Level Up | Golden burst + stars | 4-6 frames |
| Evolution | White flash + particle swirl | 6-8 frames |

**VFX Grid Prompt:**
```json
{
  "id": "battle_vfx",
  "description": "8 battle VFX sprites in 4x2 grid",
  "prompt": "4x2 grid sprite sheet of eight pixel art battle effect sprites: white impact hit-spark, arcing slash trail, fiery elemental explosion, blue hexagonal shield pop, green healing sparkles, pixel scatter death dissolve, golden level-up burst, white evolution flash swirl, 32-bit chunky retro pixel art, Enter the Gungeon style, thick black pixel outlines, bright neon colors, high contrast, solid dark background, video game VFX sprites --ar 2:1 --s 300 --niji 6 --style raw --no text, watermark, blur, gradient"
}
```

---

### 11.12 Catch Screen VFX (MISSING — Tier 2)

3 effects for the throw-and-reveal catch mechanic.

| VFX | Description |
|-----|-------------|
| Ball Throw | Ball arc trail (3-4 frames) |
| Silhouette | Dark blob outline with ??? |
| Reveal Flash | Bright neon particle burst |

**Catch VFX Grid Prompt:**
```json
{
  "id": "catch_vfx",
  "description": "3 catch screen VFX in 3x1 grid",
  "prompt": "3x1 grid sprite sheet of three pixel art catch mechanic effects: ball throw arc trail with motion lines, dark mystery silhouette with question marks, bright neon particle reveal burst, 32-bit chunky retro pixel art, Enter the Gungeon style, thick black pixel outlines, bright neon colors, high contrast, solid dark background, video game VFX sprites --ar 3:1 --s 300 --niji 6 --style raw --no text, watermark, blur, gradient"
}
```

---

### 11.13 Evolution Card Art (MISSING — Tier 2+3)

The evolution choice screens show cards with sprite previews. The card art is a combination of:
- Roomian sprite (already generated)
- Element icon (already generated)
- Card frame border (needs design)

**Card Frame Approach:**
Generate a single card frame template, then composite sprites + stats in code (Flutter widget), not in Midjourney. The card frame is a UI element, not a sprite.

**Card Frame Prompt:**
```json
{
  "id": "evolution_card_frame",
  "description": "Card frame border for evolution choice UI",
  "prompt": "pixel art card frame border for monster collecting game evolution choice UI, ornate dark grey-purple frame with neon element-colored accent slots, empty center for sprite display, top banner for name, bottom strip for stats, 32-bit chunky retro pixel art, Enter the Gungeon style, thick black pixel outlines, deep dark background --ar 3:4 --s 300 --niji 6 --style raw --no text, watermark, blur, gradient"
}
```

---

### 11.14 Updated File Organization

```
assets/roomians/
├── blob/
│   ├── l0/
│   │   ├── blob_l0_base.png          ← NEW (Tier 1)
│   │   └── blob_l0_poses.png         ← NEW (Tier 2, 3x2 grid)
│   ├── l1/
│   │   ├── blob_l1_fire.png
│   │   ├── blob_l1_fire_poses.png    ← NEW (Tier 2)
│   │   ├── blob_l1_water.png
│   │   ├── blob_l1_water_poses.png   ← NEW (Tier 2)
│   │   └── ... (4 more elements × sprite + poses)
│   ├── l5/ ... (Tier 3)
│   └── l8/ ... (Tier 3)
├── mothkin/ ... (same structure)
├── cragling/ ... (same structure)
├── avatars/                          ← NEW (Tier 1, cropped from sprites)
│   ├── blob_l0_avatar.png
│   ├── blob_l1_fire_avatar.png
│   └── ...
└── _grids/                           (raw grid images for reference)

assets/ui/
├── icons/
│   ├── elements/                     ← NEW (Tier 1)
│   │   ├── icon_fire.png
│   │   ├── icon_water.png
│   │   └── ... (4 more)
│   ├── abilities/                    ← NEW (Tier 1+2)
│   │   ├── icon_attack.png
│   │   ├── icon_magic.png
│   │   ├── icon_defend.png
│   │   ├── icon_flee.png
│   │   └── elements/ (12 elemental ability icons)
│   ├── passives/                     ← NEW (Tier 3)
│   │   └── ... (36 passive icons)
│   ├── status/                       ← NEW (Tier 1)
│   │   ├── status_burning.png
│   │   └── ... (6 more)
│   ├── states/                       ← NEW (Tier 1)
│   │   ├── state_ready.png
│   │   └── ... (5 more)
│   └── scars/                        ← NEW (Tier 2)
│       ├── scar_weakened.png
│       └── ... (5 more)
├── items/
│   └── room_balls/                   ← NEW (Tier 1)
│       ├── ball_standard.png
│       ├── ball_quality.png
│       └── ball_master.png
├── vfx/                              ← NEW (Tier 2)
│   ├── vfx_hit_spark.png
│   ├── vfx_slash.png
│   ├── vfx_shield.png
│   ├── vfx_heal.png
│   ├── vfx_death_dissolve.png
│   ├── vfx_levelup.png
│   ├── vfx_evolution.png
│   └── elements/ (6 elemental burst VFX)
├── catch/                            ← NEW (Tier 2)
│   ├── vfx_ball_throw.png
│   ├── vfx_silhouette.png
│   └── vfx_reveal_flash.png
└── frames/
    └── evolution_card_frame.png     ← NEW (Tier 2)
```

---

### 11.15 Generation Order (Recommended Pipeline)

```
Phase 1 — MVP Sprites & Icons (Tier 1)
├── 1a. L0 race grid (1 image → 3 sprites)                    ~5 min
├── 1b. L1 individual sprites (18 prompts, already ready)     ~30 min
├── 1c. Element icon grid (1 image → 6 icons)                 ~5 min
├── 1d. Status icon grid (1 image → 7 icons)                  ~5 min
├── 1e. State icon grid (1 image → 6 icons)                   ~5 min
├── 1f. Basic ability icon grid (1 image → 4 icons)           ~5 min
├── 1g. Room Ball grid (1 image → 3 sprites)                  ~5 min
├── 1h. Crop avatars from L0+L1 sprites (post-process)        ~15 min
└── Total: ~8 Midjourney generations + post-processing

Phase 2 — Battle Assets (Tier 2)
├── 2a. L0 pose grids (3 images → 18 poses)                   ~10 min
├── 2b. L1 pose grids (18 images → 108 poses)                 ~45 min
├── 2c. Battle VFX grid (1 image → 8 effects)                 ~5 min
├── 2d. Catch VFX grid (1 image → 3 effects)                  ~5 min
├── 2e. Scar icon grid (1 image → 6 icons)                    ~5 min
├── 2f. Elemental ability icon grid (1 image → 12 icons)      ~5 min
├── 2g. Evolution card frame (1 image)                        ~5 min
└── Total: ~25 Midjourney generations + post-processing

Phase 3 — Full Evolution System (Tier 3)
├── 3a. L5 refinement grids (6 images per race = 18)          ~45 min
├── 3b. L8 mastery grids (12 images per race = 36)            ~90 min
├── 3c. Passive icon grid (1 image → 36 icons)                ~5 min
├── 3d. L5 pose grids (54 images)                             ~120 min
├── 3e. L8 pose grids (108 images)                            ~240 min
└── Total: ~216 Midjourney generations + post-processing

GRAND TOTAL: ~249 Midjourney generations for complete asset coverage
```

---

*This document is the art direction companion to `roomian_visual_pictation.md`. All prompts are ready to paste into Midjourney. Refinement and mastery names are seeds — finalize during game balance. See `midjourney_reference_guide.md` for complete parameter reference.*
