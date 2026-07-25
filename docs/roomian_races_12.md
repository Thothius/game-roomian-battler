# Roomian Races v2 — 16 Humanoid Races & L1 Grid Prompts

> **Status:** Active design — supersedes race definitions in `roomian_races_art_direction.md`  
> **Date:** Jul 25, 2026  
> **Scope:** 16 humanoid-ish races (Palworld-style), L1 3x3 grid Midjourney prompts  
> **MJ params:** `--ar 1:1 --s 300 --niji 6 --style raw` (add `--sref [CODE]` if you have style refs)

---

## 1. RACE OVERVIEW

All 16 races are humanoid-ish — bipedal, expressive, characterful. Each has a distinct silhouette that stays recognizable across all 6 elemental variants. Element-neutral base forms; the 6 elements (Fire, Water, Earth, Air, Light, Dark) are applied as color/texture infusions at L1.

| # | Race | Archetype | Stat Modifiers | Silhouette | Personality |
|---|------|-----------|---------------|------------|-------------|
| 1 | **Kongur** | Ape-brute | +3 PWR, +2 VIT, -2 SPD, -2 LCK | Widest, heaviest | Aggressive, loyal, simple |
| 2 | **Corvus** | Avian scout | +3 SPD, +2 LCK, -2 GRT, -2 VIT | Tallest, leanest | Skittish, curious, proud |
| 3 | **Cragborn** | Living stone | +3 GRT, +2 VIT, -2 SPD, -2 LCK | Blockiest, densest | Stoic, ancient, patient |
| 4 | **Sproutkin** | Plant-folk | +2 INT, +2 VIT, -2 SPD, -2 PWR | Medium, organic curves | Gentle, wise, slow |
| 5 | **Naga** | Serpent-folk | +2 PWR, +2 INT, -2 GRT, -2 LCK | Medium, coiled lower | Cunning, graceful, territorial |
| 6 | **Chitin** | Beetle-folk | +3 GRT, +2 PWR, -2 SPD, -2 INT | Medium-wide, armored | Industrious, stubborn, hive-minded |
| 7 | **Plasmoid** | Gel-humanoid | +2 VIT, +2 LCK, -2 PWR, -2 INT | Medium, soft edges | Adaptable, cheerful, blank |
| 8 | **Wraith** | Ghost-folk | +2 INT, +2 SPD, -2 VIT, -2 GRT | Medium, wispy lower | Mysterious, melancholic, detached |
| 9 | **Forgekin** | Mech-folk | +3 PWR, +2 GRT, -2 LCK, -2 INT | Medium, angular metal | Literal, tireless, dutiful |
| 10 | **Beastkin** | Feral humanoid | +3 SPD, +2 PWR, -2 INT, -2 GRT | Medium, athletic | Energetic, impulsive, pack-oriented |
| 11 | **Stellar** | Cosmic-folk | +3 INT, +2 LCK, -2 VIT, -2 PWR | Medium, starry body | Otherworldly, calm, cryptic |
| 12 | **Mimic** | Shape-shifter | +2 LCK, +2 INT, -2 VIT, -2 GRT | Medium, unstable form | Mischievous, unpredictable, chaotic |
| 13 | **Ratling** | Rat-scavenger | +3 LCK, +2 SPD, -2 VIT, -2 GRT | Short, hunched, wiry | Cunning, nervous, opportunistic |
| 14 | **Froggian** | Frog-brawler | +2 VIT, +2 PWR, -2 INT, -2 LCK | Short-wide, stocky, no neck | Blunt, stubborn, voracious |
| 15 | **Mycelio** | Fungal-sage | +2 INT, +2 GRT, -2 SPD, -2 PWR | Medium, spongy, cap-headed | Contemplative, slow, networked |
| 16 | **Ethereal** | Crystal-energy | +3 INT, +2 SPD, -2 GRT, -2 VIT | Tall, translucent, floating shards | Serene, analytical, fragile |

### Base Stats (all races at L0)
```
VIT 5, PWR 5, GRT 5, SPD 5, LCK 5, INT 5
```
Modifiers applied on top — see table above.

---

## 2. SHARED ART STYLE

```
STYLE TAGS (in every prompt):
32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated focal colors, deep high-contrast dark shadowed background, video game character sprite, full body front view, idle pose

PARAMS:
--ar 1:1 --s 300 --niji 6 --style raw

IF USING STYLE REFS:
--sref [YOUR_CODE] --sw 300
```

### Element Color Palette

| Element | Primary | Secondary | Glow/Accent |
|---------|---------|-----------|-------------|
| **Fire** | #FF6B35 | #D62828 | #FFD23F |
| **Water** | #4ECDC4 | #2196F3 | #E0F7FA |
| **Earth** | #8BC34A | #795548 | #C5E1A5 |
| **Air** | #B0BEC5 | #90A4AE | #E1F5FE |
| **Light** | #FFEB3B | #FFC107 | #FFFFFF |
| **Dark** | #7B1FA2 | #4A148C | #E1BEE7 |

---

## 3. L1 GRID LAYOUT (all races)

```
┌─────────────┬─────────────┬─────────────┐
│  A1: Fire   │  A2: Water  │  A3: Earth  │
├─────────────┼─────────────┼─────────────┤
│  B1: Air    │  B2: Light  │  B3: Dark   │
├─────────────┼─────────────┼─────────────┤
│  C1: Base   │  C2: Side   │  C3: Label  │
└─────────────┴─────────────┴─────────────┘
```

---

## 4. RACE DEFINITIONS & L1 GRID PROMPTS

### Race 1: KONGUR — Ape-Brute

**Visual:** Massive humanoid ape. Broad flat-topped skull, heavy brow ridge, four eyes (two large below two small), underbite with protruding tusks, wide flat nose slits, barrel chest, thick neck merging into shoulders, arms longer than legs, leathery skin.

**Grid Prompt:**
```
3x3 grid sprite sheet of 9 variations of a Kongur, massive humanoid ape-creature standing in hunched wide stance, broad flat-topped skull with heavy brow ridge, four eyes two large below two small all glowing, underbite with protruding upward-curving tusks, wide flat nose slits, barrel chest twice as wide as waist, thick neck merging directly into shoulders no visible neck gap, arms longer than legs knuckles near ground, leathery grey-green skin with visible texture lines, top row: fire variant with molten amber lava cracks splitting across skin surface, ember particles floating from cracks, eyes blazing orange, steam rising from shoulders, tusks glowing red-hot, water variant with ice crystallizing in layers on tusks and knuckles, frost breath mist visible, frozen blue skin patches with dithered frost patterns, icicle growths on brow ridge, earth variant with thick moss carpeting shoulders and chest, stone armor plates fused to forearms, root veins crawling across skin, small mushrooms sprouting from tusk bases, middle row: air variant with fur standing on end from static charge, miniature whirlwinds swirling around clenched fists, pale grey-blue skin with lightning flicker between eyes, light variant with radiant golden skin glowing from within, all four eyes blazing white-gold, halo of sparks orbiting skull, golden light bleeding from tusk tips, dark variant with deep purple shadow aura trailing behind, eyes void-black with purple ring, dark miasma dripping from fists, tusks stained black with void energy, bottom row: plain neutral grey-green leathery base form, plain base form side profile view, empty cell with label text, each cell full body front view idle pose, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated focal colors, deep high-contrast dark shadowed background, video game character sprite sheet --ar 1:1 --s 300 --niji 6 --style raw
```

---

### Race 2: CORVUS — Avian Scout

**Visual:** Tall lean bird-humanoid. Tall narrow skull with backward-sweeping bony crest, single pair large forward-facing golden eyes with no visible whites, sharp converging hooked jaw (not full beak), long thin neck, narrow sloped shoulders, smooth fine scales, feathered crest along scalp and jawline, wing-arm nubs.

**Grid Prompt:**
```
3x3 grid sprite sheet of 9 variations of a Corvus, tall lean bird-humanoid standing upright with narrow posture, tall narrow skull with backward-sweeping bony crest like a mohawk, single pair large forward-facing golden eyes with no visible whites, sharp converging hooked jaw not a full beak splitting into two pointed segments, long thin neck, narrow sloped shoulders, smooth fine scales covering body, feathered crest running along scalp and jawline, small wing-arm nubs on back with feather tips visible, top row: fire variant with orange ember feathers igniting along crest, ash particles trailing upward, smoldering glowing tips on crest feathers, heat shimmer distorting air around body, scales tinted amber, water variant with crystalline ice feathers frosting over, frost crystals growing along crest, frozen breath mist pouring from jaw, ice-blue scales with dithered frost, earth variant with leafy wing-nubs sprouting green, bark-textured scales browning, moss climbing crest feathers, small twigs growing from jaw, middle row: air variant with translucent wind-swept feathers streaming, static-charged crest crackling with sparks, tiny cyclones spiraling around feet, silver-grey scales, light variant with iridescent rainbow feathers shimmering, glowing radiant white-gold eyes, halo of light particles drifting, feathers refracting into spectrum, dark variant with tattered shadow feathers dissolving at tips, purple glowing eyes, dark mist trailing from wing-nubs, void-black scales with purple veins, bottom row: plain neutral slate-blue smooth-scaled base form, plain base form side profile view, empty cell with label text, each cell full body front view idle pose, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated focal colors, deep high-contrast dark shadowed background, video game character sprite sheet --ar 1:1 --s 300 --niji 6 --style raw
```

---

### Race 3: CRAGBORN — Living Stone

**Visual:** Angular geometric golem-humanoid. Faceted skull with no smooth curves, recessed glowing amber slit-eyes, wide flat mouth with jagged mineral teeth, asymmetrical body (one shoulder has rocky crystal growth), broad dense blocky silhouette, dark granite skin, amber crystal deposits embedded.

**Grid Prompt:**
```
3x3 grid sprite sheet of 9 variations of a Cragborn, angular geometric golem-humanoid with broad dense blocky silhouette standing wide, faceted skull with no smooth curves all angular planes, recessed glowing amber slit-eyes set deep into face, wide flat mouth with jagged mineral teeth of varying sizes, asymmetrical body with one shoulder having large rocky crystal growth protruding upward, dark granite skin with visible mineral grain texture, amber crystal deposits embedded randomly across torso, thick blocky limbs with flat planes, top row: fire variant with obsidian crust blackened, glowing magma veins pulsing orange through cracks, smoke trailing from crystal peaks, eyes blazing red-orange, ember particles in cracks, water variant with blue geode interior visible through cracked shell sections, icy surface crystals growing in clusters, frozen dew drops on facets, pale blue glow from within, earth variant with thick moss patches carpeting shoulders, embedded river stones in chest, green mineral veins pulsing, small flowers growing in crack crevices, middle row: air variant with wind-eroded smooth sandy surface, hollow cavities visible, sand particles drifting off edges, swirling wind patterns carved into body, pale grey erosion, light variant with refractive prism facets catching light, internal golden glow blazing, rainbow reflections on surface planes, bright white eyes, light beams shooting from cracks, dark variant with deep black obsidian surface, purple mineral veins absorbing surrounding light, void portals flickering in cracks, dim purple eyes, shadow particles sinking into body, bottom row: plain neutral grey granite base form with amber deposits, plain base form side profile view, empty cell with label text, each cell full body front view idle pose, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated focal colors, deep high-contrast dark shadowed background, video game character sprite sheet --ar 1:1 --s 300 --niji 6 --style raw
```

---

### Race 4: SPROUTKIN — Plant-Folk

**Visual:** Wooden humanoid body, bark-textured skin, leafy crown instead of hair, vine-like limbs with small leaf blades, small flowers growing from joints, root-feet, gentle expression with dark oval eyes.

**Grid Prompt:**
```
3x3 grid sprite sheet of 9 variations of a Sproutkin, wooden humanoid plant-creature standing with gentle posture, bark-textured skin with visible grain lines and knots, leafy crown instead of hair with multiple leaf shapes, vine-like limbs with small leaf blades growing at joints, small flowers blooming from elbow and knee joints, root-feet spreading into ground, dark oval eyes with warm expression, small bark mouth, top row: fire variant with red autumn leaves blazing on crown, smoldering bark with glowing ember lines, ember flowers blooming orange, smoke rising from shoulders, charred vine tips, water variant with lily pads resting on shoulders, water droplets beading on leaves, blue lotus flowers opening at joints, ice crystals on bark, rippling water aura, earth variant with thick moss coverage spreading across body, mushroom growths sprouting from shoulders, deep extended root-feet, small ferns growing from crown, green bark, middle row: air variant with dandelion seeds floating around crown, wind-blown petals streaming, pale silver leaves shimmering, wind swirls around limbs, bark turning pale, light variant with golden sunflower crown blooming, radiant glowing sap visible through bark, light particles drifting from flowers, golden bark, warm halo, dark variant with withered purple leaves drooping, thorny vines wrapping limbs, shadow pollen drifting, dark cracked bark, purple glowing eyes, bottom row: plain neutral green-brown bark base form, plain base form side profile view, empty cell with label text, each cell full body front view idle pose, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated focal colors, deep high-contrast dark shadowed background, video game character sprite sheet --ar 1:1 --s 300 --niji 6 --style raw
```

---

### Race 5: NAGA — Serpent-Folk

**Visual:** Serpentine lower body (coiled), scaled humanoid upper body, finned head crest, slit-pupil eyes, forked tongue, webbed hands, sleek scales, cobra-like hood flaring from neck.

**Grid Prompt:**
```
3x3 grid sprite sheet of 9 variations of a Naga, serpent-humanoid with thick coiled serpentine lower body in loose spiral, scaled humanoid upper body with sleek muscle definition, finned head crest sweeping backward, cobra-like hood flaring from neck sides, slit-pupil eyes with vertical membranes, forked tongue flicking from jaw, webbed hands with clawed fingertips, sleek overlapping scales covering entire body, top row: fire variant with red-orange scales shimmering with heat, glowing hood radiating heat waves, ember particles rising from coil, magma veins visible under scales, eyes blazing red, water variant with blue-green iridescent scales, bioluminescent fins glowing along crest, water sheen on scales, ice forming on hood edges, ripple patterns on body, earth variant with brown stone-textured scales, moss growing on hood, cracked serpentine skin showing earthy layers, root veins across coil, middle row: air variant with silver reflective scales, static electricity arcing between crest fins, wind swirling around coil lifting debris, pale grey hood, light variant with golden glowing scales radiating light, radiant hood blazing like sun, light particles drifting from crest, white-gold eyes, dark variant with purple-black scales absorbing light, void-filled hood with stars visible inside, shadow trail from coil, purple slit eyes, bottom row: plain neutral emerald-green sleek-scaled base form, plain base form side profile view, empty cell with label text, each cell full body front view idle pose, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated focal colors, deep high-contrast dark shadowed background, video game character sprite sheet --ar 1:1 --s 300 --niji 6 --style raw
```

---

### Race 6: CHITIN — Beetle-Folk

**Visual:** Armored exoskeleton humanoid, dome-shaped head, large compound eyes, mandible jaw, spiked shoulder plates, four-armed (two small utility arms, two large primary), chitinous plating, insectoid legs.

**Grid Prompt:**
```
3x3 grid sprite sheet of 9 variations of a Chitin, armored beetle-humanoid standing wide with four arms two small utility arms tucked near chest two large primary arms at sides, hard glossy exoskeleton with visible segment lines, dome-shaped head with ridge details, large multi-faceted compound eyes, mandible jaw with serrated edges, spiked shoulder plates protruding outward, chitinous plating across chest and legs, insectoid digitigrade legs, top row: fire variant with glowing red-hot armor plates, ember mandibles sparking, smoke trailing from shoulder spikes, cracks showing molten orange underneath, eyes blazing, water variant with icy blue shell frosting over, frost crystals growing on plate edges, frozen compound eyes dimmed, icicle spikes, cold mist, earth variant with mossy green shell, mushroom growths in plate crevices, stone-textured armor segments, vines wrapping limbs, middle row: air variant with translucent buzzing wings extended, static-charged spikes crackling, silver polished shell, wind vortex around body, light variant with golden iridescent shell shimmering, glowing compound eyes, light refracting off plates into rainbow, radiant mandibles, dark variant with black-purple glossy shell, void-filled compound eyes, shadow dripping from spikes, dark energy crackling between plates, bottom row: plain neutral dark-brown glossy exoskeleton base form, plain base form side profile view, empty cell with label text, each cell full body front view idle pose, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated focal colors, deep high-contrast dark shadowed background, video game character sprite sheet --ar 1:1 --s 300 --niji 6 --style raw
```

---

### Race 7: PLASMOID — Gel-Humanoid

**Visual:** Translucent gel body in humanoid shape, no distinct facial features, floating glowing core in chest, two dot eyes, amorphous edges that drip and reform, soft round silhouette but standing upright.

**Grid Prompt:**
```
3x3 grid sprite sheet of 9 variations of a Plasmoid, translucent gel humanoid with soft rounded body in standing humanoid shape, no distinct facial features except two small dot eyes, floating glowing core visible swirling inside chest cavity, amorphous edges that drip downward and reform at base, semi-transparent surface showing internal currents, smooth rounded limbs with no joints, top row: fire variant with molten amber-orange gel bubbling, lava cracks splitting across surface, blazing ember core pulsing, steam rising from drips, glowing veins, water variant with liquid cyan-teal gel flowing, internal bubbles rising and popping, ice crystals forming on surface in dithered patterns, cool blue core, earth variant with muddy green-brown gel thickening, embedded pebbles floating inside, moss patches growing on surface, small roots visible inside, middle row: air variant with semi-transparent silver gel shimmering, tiny lightning bolts arcing inside, wispy edges dissolving into mist, static crackle on surface, light variant with radiant golden gel glowing intensely, internal light pulsing from core, rainbow refractions bending through body, blinding core, dark variant with deep purple-black gel absorbing light, empty white ring eyes, shadow miasma trailing from base, void particles pulled inward, bottom row: plain neutral grey-white translucent gel base form, plain base form side profile view, empty cell with label text, each cell full body front view idle pose, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated focal colors, deep high-contrast dark shadowed background, video game character sprite sheet --ar 1:1 --s 300 --niji 6 --style raw
```

---

### Race 8: WRAITH — Ghost-Folk

**Visual:** Dark translucent humanoid body, wispy lower half (no legs, trails into shadow), hollow white eyes, tattered cloak-like form, shadow particles trailing, no visible mouth, long thin arms.

**Grid Prompt:**
```
3x3 grid sprite sheet of 9 variations of a Wraith, dark translucent ghost-humanoid floating with wispy lower half trailing into shadow instead of legs, hollow white eyes with no pupils, no visible mouth, tattered cloak-like body with ragged edges dissolving, long thin arms with elongated fingers, shadow particles trailing from body, hood-like shape on head, top row: fire variant with burning wisp body flickering, ember particles spiraling upward, flame-tattered cloak edges igniting, orange glow inside hood, smoke trail, water variant with icy mist body swirling, frozen tears dropping from eye sockets, frost wisp trail crystallizing, blue-white glow, ice crystals on cloak, earth variant with mossy tattered form, root-like arms with visible veins, decaying stone fragments falling from body, green-brown cloak, middle row: air variant with swirling wind body, static-charged wisp crackling, cyclone lower half spinning, silver-grey cloak, wind streaks, light variant with radiant white-gold body shining, glowing eyes blazing, light particles drifting upward, golden cloak edges, warm halo, dark variant with deep purple-black body, void-filled eyes with faint purple ring, dark miasma pooling at base, shadow dripping from cloak, bottom row: plain neutral dark grey translucent base form, plain base form side profile view, empty cell with label text, each cell full body front view idle pose, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated focal colors, deep high-contrast dark shadowed background, video game character sprite sheet --ar 1:1 --s 300 --niji 6 --style raw
```

---

### Race 9: FORGEKIN — Mech-Folk

**Visual:** Metallic humanoid body with visible joints, rectangular head with single horizontal visor eye, steam vents on shoulders, cog-like shoulder pauldrons, piston limbs, riveted plates, industrial aesthetic.

**Grid Prompt:**
```
3x3 grid sprite sheet of 9 variations of a Forgekin, metallic humanoid robot-creature standing rigid with visible mechanical joints, rectangular head with single horizontal visor eye glowing, steam vents on shoulders emitting puffs, cog-like shoulder pauldrons with teeth visible, piston limbs with hydraulic lines, riveted plates across torso, industrial aesthetic with visible bolts and seams, top row: fire variant with red-hot glowing metal, furnace core visible through chest grate, smoke pouring from vents, ember sparks from joints, orange visor, water variant with blue-steel polished finish, ice forming on joints, frozen steam icicles from vents, frost on visor, cold blue glow, earth variant with rusted copper patina, moss growing on plates, stone-textured limbs, vines wrapping pistons, green patina, middle row: air variant with polished silver chrome, electric arcs jumping between joints, wind whistling through vents, static charge on surface, light variant with golden chrome gleaming, radiant visor blazing white, light beams from seam gaps, golden glow from core, dark variant with black iron body, purple energy core pulsing through chest, void leaking from cracks, dark visor with purple line, bottom row: plain neutral gunmetal-grey metal base form, plain base form side profile view, empty cell with label text, each cell full body front view idle pose, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated focal colors, deep high-contrast dark shadowed background, video game character sprite sheet --ar 1:1 --s 300 --niji 6 --style raw
```

---

### Race 10: BEASTKIN — Feral Humanoid

**Visual:** Furry humanoid, pointed ears, clawed hands, fanged teeth, bushy tail, wild mane, athletic lean build, muzzle-like jaw, whisker marks on cheeks.

**Grid Prompt:**
```
3x3 grid sprite sheet of 9 variations of a Beastkin, furry feral humanoid in athletic crouched stance, pointed ears twitching upward, clawed hands with visible sharp nails, fanged teeth visible in snarl, bushy tail swishing behind, wild unkempt mane framing face, lean muscular build, muzzle-like jaw extending forward, whisker marks on cheeks, top row: fire variant with red-orange fur bristling, ember mane crackling with sparks, smoldering claws glowing red, heat shimmer around body, ash particles, water variant with blue-silver fur sleeked down, ice claws frost-tipped, frost breath misting, frozen whiskers, ice crystals in mane, earth variant with brown-green fur thickening, moss growing in mane, stone-textured claws, vines wrapped around limbs, earthy fur, middle row: air variant with silver-grey fur streaming, static-charged mane standing on end, wind streaks around body, claws crackling with static, light variant with golden-white fur gleaming, radiant glowing eyes, halo mane of light particles, luminous claws, warm aura, dark variant with purple-black fur, shadow trail from body, void-filled eyes with purple ring, dark claws dripping shadow, bottom row: plain neutral brown fur base form, plain base form side profile view, empty cell with label text, each cell full body front view idle pose, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated focal colors, deep high-contrast dark shadowed background, video game character sprite sheet --ar 1:1 --s 300 --niji 6 --style raw
```

---

### Race 11: STELLAR — Cosmic-Folk

**Visual:** Body made of starry void skin, constellation patterns glowing on surface, crescent-shaped head, no visible mouth, glowing point-eyes like stars, nebula-colored patches, floating slightly above ground.

**Grid Prompt:**
```
3x3 grid sprite sheet of 9 variations of a Stellar, cosmic humanoid floating slightly above ground with no feet, body made of starry void skin with deep blue-black surface, constellation patterns glowing on skin in connected dot lines, crescent-shaped head curving upward, no visible mouth, glowing star-point eyes like tiny supernovas, nebula-colored patches swirling across torso, arms ending in star-shaped tips, top row: fire variant with red nebula skin swirling, supernova patterns exploding on surface, ember star-points blazing, heat distortion around body, orange constellations, water variant with blue nebula cooling, ice constellation lines crystallizing, frozen star-eyes dimmed, frost patterns on void skin, ice shards orbiting, earth variant with green cosmic dust settling, mossy nebula patches, stone-textured void skin hardening, root constellation lines, middle row: air variant with silver cosmic wind streaming, swirling star patterns rotating, static star-points crackling, wind vortex around body, light variant with golden radiant nebula blazing, blinding star-eyes, light constellations connecting across body, golden glow, light particles, dark variant with black void body deepening, purple absorbing stars pulling in light, collapsing nebula fragments, void dripping from arms, bottom row: plain neutral dark blue starry void base form, plain base form side profile view, empty cell with label text, each cell full body front view idle pose, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated focal colors, deep high-contrast dark shadowed background, video game character sprite sheet --ar 1:1 --s 300 --niji 6 --style raw
```

---

### Race 12: MIMIC — Shape-Shifter

**Visual:** Unstable humanoid form, body parts in slight flux, one eye larger than the other, jagged uneven teeth, patchwork skin textures (some smooth, some rough, some scaly), glitching edges, extra mouth on shoulder.

**Grid Prompt:**
```
3x3 grid sprite sheet of 9 variations of a Mimic, unstable shape-shifter humanoid with body parts in slight visual flux, one eye noticeably larger than the other, jagged uneven teeth of different sizes, patchwork skin textures with some areas smooth some rough some scaly some fuzzy, glitching pixel edges where body parts don't quite align, small extra mouth on left shoulder with teeth visible, asymmetrical limbs with slightly different textures, top row: fire variant with flickering flame-body parts shifting, ember glitch edges sparking, molten patchwork skin with lava dripping from seams, fire spitting from extra mouth, water variant with liquid shifting body flowing, ice crystals forming and reforming across surface, frozen extra mouth with icicle teeth, ripple patterns, earth variant with shifting stone bark moss patches appearing and vanishing, unstable mineral growths sprouting randomly, tectonic seam cracks, middle row: air variant with swirling wind body parts, static glitch edges crackling, semi-transparent shifting sections, wind vortex around unstable parts, light variant with radiant golden shifting body, blinding uneven eyes, light refracting through patchwork creating prisms, golden glow from seams, dark variant with void-consuming body parts dissolving, purple glitch edges tearing, shadow dripping from extra mouth, void portals flickering on skin, bottom row: plain neutral patchwork grey base form, plain base form side profile view, empty cell with label text, each cell full body front view idle pose, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated focal colors, deep high-contrast dark shadowed background, video game character sprite sheet --ar 1:1 --s 300 --niji 6 --style raw
```

---

### Race 13: RATLING — Rat-Scavenger

**Visual:** Short hunched rat-humanoid with wiry frame, long pointed snout with whiskers, large round ears, sharp incisors, pink hairless tail, clawed fingers, tattered scavenger satchel, hunched posture, nervous darting eyes.

**Grid Prompt:**
```
3x3 grid sprite sheet of 9 variations of a Ratling, short hunched rat-humanoid with wiry thin frame, long pointed snout with visible whiskers, large round ears twitching, sharp protruding incisors, long pink hairless tail curling behind, clawed fingers with dirty nails, small tattered scavenger satchel slung across chest, hunched nervous posture, small dark darting eyes, patchy fur on arms and legs, top row: fire variant with singed blackened fur tips, ember whiskers glowing, smoldering satchel smoking, red-hot incisors, ash particles, water variant with sleeked-down dark blue-grey fur, ice crystals on whiskers, frozen satchel with frost, icy breath, frost on ears, earth variant with mossy green-brown fur, mushrooms growing from satchel, root vines wrapping tail, soil-caked claws, middle row: air variant with silver-grey fur streaming in wind, static-charged whiskers crackling, tiny cyclones around feet, wind-blown ears, light variant with golden-white clean fur gleaming, radiant glowing eyes, halo of light particles, glowing incisors, warm aura, dark variant with purple-black mangy fur, void-filled eyes with purple ring, shadow dripping from tail, dark miasma from satchel, bottom row: plain neutral brown-grey wiry fur base form, plain base form side profile view, empty cell with label text, each cell full body front view idle pose, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated focal colors, deep high-contrast dark shadowed background, video game character sprite sheet --ar 1:1 --s 300 --niji 6 --style raw
```

---

### Race 14: FROGGIAN — Frog-Brawler

**Visual:** Short wide stocky frog-humanoid with no visible neck, bulbous eyes on top of head, wide flat mouth, thick muscular arms, webbed hands and feet, bumpy moist skin, pot-bellied torso, squat powerful legs.

**Grid Prompt:**
```
3x3 grid sprite sheet of 9 variations of a Froggian, short wide stocky frog-humanoid with no visible neck, large bulbous eyes protruding from top of head, wide flat mouth with thick lips, thick muscular arms hanging at sides, webbed three-fingered hands, webbed wide feet, bumpy moist skin texture, round pot-bellied torso, squat powerful bent legs, top row: fire variant with red-orange bumpy skin glowing, ember particles from mouth, blazing bulbous eyes, steam rising from moist skin, lava-textured warts, water variant with blue-green slick wet skin, water droplets beading, bioluminescent throat pouch glowing, ripple patterns on skin, ice forming on webbing, earth variant with brown-green bark-textured skin, moss growing in wart crevices, stone warts hardening, root veins across belly, mushrooms on back, middle row: air variant with pale silver-grey skin, wind swirling around body, static charge crackling on warts, translucent webbing, light variant with golden radiant skin gleaming, glowing bulbous eyes, light particles from mouth, warm golden throat pouch, dark variant with purple-black dark skin, void-filled bulbous eyes, shadow dripping from mouth, dark miasma pooling at feet, bottom row: plain neutral green bumpy moist skin base form, plain base form side profile view, empty cell with label text, each cell full body front view idle pose, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated focal colors, deep high-contrast dark shadowed background, video game character sprite sheet --ar 1:1 --s 300 --niji 6 --style raw
```

---

### Race 15: MYCELIO — Fungal-Sage

**Visual:** Medium spongy humanoid with mushroom cap head, pale stalk-like body, gills visible under cap, spore particles drifting, root-like mycelium feet, small fungal growths on shoulders, calm expression with dark crease eyes, no visible mouth.

**Grid Prompt:**
```
3x3 grid sprite sheet of 9 variations of a Mycelio, medium spongy fungal-humanoid with large mushroom cap covering head like a hat, pale smooth stalk-like body texture, visible gills under cap edges, spore particles drifting from cap, root-like mycelium feet spreading into ground, small fungal growths sprouting from shoulders, calm expression with dark crease-line eyes, no visible mouth, soft rounded body, top row: fire variant with red-orange mushroom cap with glowing ember gills, smoldering stalk body, ember spores sparking, smoke rising from cap, lava-textured fungal growths, water variant with blue-teal moist cap, water droplets on gills, bioluminescent spore trails, ice crystals on stalk, rippling moisture, earth variant with brown-green mossy cap, thick moss covering body, extended mycelium root network, mushrooms sprouting abundantly, middle row: air variant with pale silver-grey cap, wind-swept spores streaming, static-charged gills crackling, tiny cyclones around feet, light variant with golden glowing cap radiant, blinding crease eyes, light spores drifting upward, warm golden stalk, dark variant with purple-black withered cap, void-filled crease eyes, shadow spores sinking, dark miasma from gills, bottom row: plain neutral pale cream-and-brown mushroom cap base form, plain base form side profile view, empty cell with label text, each cell full body front view idle pose, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated focal colors, deep high-contrast dark shadowed background, video game character sprite sheet --ar 1:1 --s 300 --niji 6 --style raw
```

---

### Race 16: ETHEREAL — Crystal-Energy

**Visual:** Tall translucent humanoid made of floating crystal shards, body composed of angular crystalline segments with gaps between them, glowing energy lines connecting shards, no solid skin, sharp geometric head, single glowing diamond eye, shards float slightly apart.

**Grid Prompt:**
```
3x3 grid sprite sheet of 9 variations of an Ethereal, tall translucent humanoid made of floating angular crystal shards with visible gaps between body segments, glowing energy lines connecting shards like circuits, no solid skin surface, sharp geometric diamond-shaped head, single large glowing diamond eye in center of face, crystalline arms with floating shard fingers, legs composed of stacked floating crystals, inner glow visible through translucent shards, top row: fire variant with red-orange crystal shards glowing molten, magma energy lines pulsing between shards, ember particles from gaps, heat distortion, blazing diamond eye, water variant with blue-teal ice crystal shards, frozen energy lines, frost forming on shard edges, ice particles, cold blue glow, earth variant with green-brown jade crystal shards, moss growing in shard gaps, root veins replacing energy lines, stone-textured shards, middle row: air variant with silver-clear crystal shards, wind swirling through gaps, static electricity arcing between shards, translucent shimmering, light variant with golden radiant crystal shards, blinding diamond eye, light beams refracting through shards into rainbows, intense inner glow, dark variant with purple-black dark crystal shards, void energy lines absorbing light, void-filled diamond eye, shadow particles pulled into gaps, bottom row: plain neutral pale blue-white translucent crystal shard base form, plain base form side profile view, empty cell with label text, each cell full body front view idle pose, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated focal colors, deep high-contrast dark shadowed background, video game character sprite sheet --ar 1:1 --s 300 --niji 6 --style raw
```

---

## 5. SILHOUETTE DIFFERENTIATION GUIDE

| Race | Height | Width | Key Silhouette Feature |
|------|--------|-------|----------------------|
| Kongur | Short-wide | Widest | Hunched, long arms, flat-top skull |
| Corvus | Tallest | Narrowest | Crest spike, thin neck, wing-nubs |
| Cragborn | Medium | Wide | Blocky angular, crystal shoulder spike |
| Sproutkin | Medium | Medium | Leafy crown, root-feet splay |
| Naga | Medium-tall | Medium | Coiled tail base, hood flare |
| Chitin | Medium | Wide | Four arms, dome head, spiked shoulders |
| Plasmoid | Medium | Medium | Soft rounded edges, dripping base |
| Wraith | Medium | Narrow | Wispy lower half, tattered top |
| Forgekin | Medium | Medium | Rectangular head, piston limbs, cog shoulders |
| Beastkin | Medium | Medium | Tail, pointed ears, mane |
| Stellar | Medium (floating) | Medium | Crescent head, no legs (floats) |
| Mimic | Medium | Medium | Asymmetrical, glitching edges, extra mouth |
| Ratling | Short | Narrow | Hunched, long snout, tail, big ears |
| Froggian | Short-wide | Wide | No neck, bulbous eyes, pot-belly |
| Mycelio | Medium | Medium | Mushroom cap head, spongy body, spore trail |
| Ethereal | Tall | Narrow | Floating crystal shards with gaps, diamond eye |

---

## 6. PRODUCTION NOTES

- **16 L1 grids** = 16 Midjourney generations (one per race)
- Each grid yields 9 cells: 6 elemental + base + side + label
- **Prompt length:** Each prompt is ~1400-1900 chars, well under 3000 max
- **Style refs:** Add `--sref [CODE] --sw 300` after the base params if you have a style reference
- **Niji version:** `--niji 6` for vibey exploration, `--niji 7` for more literal adherence
- **If results are too smooth:** Add "no anti-aliasing, sharp blocky pixels, visible pixel grid" more prominently
- **For individual sprites:** After grid generation, upscale each cell, extract, clean background to transparent PNG
- **File naming:** `[race]_l1_[element].png` (e.g. `kongur_l1_fire.png`)
- **L5 grids:** 2 per race (32 total) — 3 elements × 3 refinements per grid
- **L8 grids:** 4 per race (64 total) — 1.5 elements × 3 refinements × 2 masteries per grid
- **Total grids for all 16 races:** 16 (L1) + 32 (L5) + 64 (L8) = **112 grid images**
