# Midjourney Reference Guide for GungeonMate

> **Source:** Official Midjourney docs (docs.midjourney.com), Jul 25, 2026  
> **Purpose:** Quick-reference cheat sheet for generating Roomian sprites and game art

---

## 1. CURRENT VERSIONS (Jul 2026)

| Model | Released | Key Traits |
|-------|----------|------------|
| **V8.2** | Jul 24, 2026 | Default. Creative, bold, sophisticated, edgy. Better Personalization. |
| **Niji 7** | Jan 9, 2026 | Anime model. Cleaner, flatter, better line work. More literal. Less "vibey". |
| V8.1 | Jun 2026 | Previous default. |
| V7 | Apr 2025 | Omni Reference, Draft Mode. Richer textures. |
| V6.1 | Jul 2024 | 25% faster than V6, more coherent. |
| V6 | Dec 2023 | Enhanced prompt accuracy, longer inputs. |
| Niji 6 | Jun 2024 | Improved anime eyes, Japanese text rendering. |

---

## 2. PROMPT ANATOMY

```
[text description] [image references] [parameters]
```

### Prompt Tips
- **Short and specific wins.** Avoid long instruction lists — MJ truncates very long prompts.
- Use precise synonyms: "enormous" not "big", "crimson" not "red"
- Use exact numbers: "three cats" not "cats"
- Describe what you WANT, not what you don't (use `--no` for exclusions)
- Key areas to specify: Subject, Medium, Environment, Lighting, Color, Mood, Composition

### Example (GungeonMate sprite)
```
round translucent gelatinous blob creature, molten amber-orange glowing gel body, lava cracks across surface, two small dot eyes, no limbs, wobbly round silhouette, 32-bit chunky retro pixel art, Enter the Gungeon style, thick solid black pixel-art outlines 1-2px thick, classic 16-bit stippled dithered shading, checkerboard gradients, hand-drawn pixel textures, low resolution, highly saturated amber and red colors, deep dark shadowed background, video game character sprite, full body front view, idle pose --ar 1:1 --s 300 --niji 6 --style raw
```

---

## 3. COMPLETE PARAMETER REFERENCE

### Core Parameters

| Param | Alias | Description | Range | Default |
|-------|-------|-------------|-------|---------|
| `--ar` | `--aspect` | Aspect ratio | `1:1`, `16:9`, `9:16`, any | `1:1` |
| `--s` | `--stylize` | Artistic flair strength | `0–1000` | `100` |
| `--c` | `--chaos` | Variety between 4 outputs | `0–100` | `0` |
| `--w` | `--weird` | Unconventional aesthetics | `0–3000` | `0` |
| `--q` | `--quality` | Render quality/time | `0.25–2` (V6), `0.25–1` (Niji) | `1` |
| `--no` | — | Negative prompt (exclude) | text | — |
| `--seed` | — | Reproducible noise seed | `0–4294967295` | random |
| `--tile` | — | Seamless repeating tiles | — | off |
| `--r` | `--repeat` | Run prompt N times | `1–40` | `1` |
| `--stop` | — | Stop at partial progress | `10–100` | 100 |

### Image Reference Parameters

| Param | Description | Range | Default |
|-------|-------------|-------|---------|
| `--iw` | Image prompt weight | `0–3` (V6), `0.2–2` (Niji) | `1` |
| `--sref` | Style reference (URL or code) | URL / code / `random` | — |
| `--sw` | Style reference weight | `0–1000` | `100` |
| `--sv` | Style reference version | `1–6` | `4` (V6) / `6` (V7) |
| `--cw` | Character reference weight (V6) | `0–100` | `100` |
| `--ow` | Omni reference weight (V7 only) | `1–1000` | `100` |
| `--p` | Personalization profile | profile ID / code | — |

### Model & Mode Parameters

| Param | Description | Options |
|-------|-------------|---------|
| `--v` | Model version | `6`, `6.1`, `7`, `8.1`, `8.2` |
| `--niji` | Niji anime model | `6`, `7` |
| `--raw` | Raw mode (less auto-styling) | — |
| `--fast` | Fast GPU mode | — |
| `--relax` | Relax GPU mode | — |
| `--turbo` | Turbo GPU mode | — |

### Parameter Formatting Rules
- Always at the **end** of the prompt, after text description
- Space before `--`, no space between `--` and param name
- **No punctuation** in parameters (no commas, periods)
- ✅ `vibrant California poppies --ar 2:3 --s 300`
- ❌ `vibrant California poppies--ar 2:3` (no space before `--`)
- ❌ `vibrant California poppies --ar 2:3,` (comma after param)
- ❌ `vibrant California --ar 2:3 poppies` (text after params)

---

## 4. MULTI-PROMPTS & WEIGHTS

Separate concepts with `::` to control them independently:

```
space:: ship          → "space" and "ship" treated as separate ideas
space::2 ship          → "space" is 2x more important than "ship"
space::1.5 ship::0.5   → Decimal weights (V4+)
still life:: fruit::-0.5  → Negative weight (removes fruit)
```

- No space on left of `::`, single space on right
- Parameters still go at the very end
- `--no red` is equivalent to `::red::-0.5`
- Total of all weights must be positive

---

## 5. IMAGE REFERENCE TYPES

| Type | Param | What It Does | Version |
|------|-------|-------------|---------|
| **Image Prompt** | URL at start + `--iw` | Influences content, composition, colors | All |
| **Style Reference** | `--sref` + `--sw` | Captures visual vibe (colors, textures, lighting) | V6+ |
| **Character Reference** | `--cw` | Maintains character consistency (face + clothing) | V6 only |
| **Omni Reference** | `--ow` | Replaces Character Ref. Object/character consistency | V7 only |

### Style Reference Details
- `--sref URL` — Use an image as style reference
- `--sref random` — Random style code from MJ internal library
- `--sref <numeric_code>` — Specific style code
- `--sw 0–1000` — Control how strongly style influences result (default 100)
- Mix multiple: `--sref URL1 URL2 code3`
- Weight individual: `--sref URL1::2 URL2::1`
- **Best practice:** Keep text prompt simple when using sref. Don't add conflicting style words. Focus on content, not instructions.

### Character Reference Details
- `--cw 100` — Full detail (face, hair, clothing)
- `--cw 0` — Face only
- Only works in V6 and Niji 6

---

## 6. RAW MODE

- `--raw` — Turns off Midjourney's auto-styling
- Simple prompts → more realistic/photo-like
- Detailed prompts → more control over final look
- **For pixel art with Niji:** Use `--style raw` to reduce anime auto-styling and get more literal results

---

## 7. PERSONALIZATION

- `--p` — Applies your personal aesthetic profile
- Unlock by selecting images on midjourney.com/personalize
- Multiple profiles, each with unique ID
- `--p pID` — Use specific profile
- Liking images on Explore feeds your Global Profile
- V7 profiles work in V8.x

---

## 8. WEB INTERFACE (midjourney.com)

### Imagine Bar
- Type prompt → Enter or click send
- **Ctrl+Enter** (Cmd+Enter) — Run prompt AND keep text for reuse
- Image icon — Upload images, drag into Image Prompt / Style Ref / Omni Ref sections
- Lock icon — Pin images for reuse across prompts
- Settings icon — Default aspect ratio, model, raw mode, stylize, weirdness, variety, GPU speed

### Creation Feed
- Real-time generation view
- Hover for quick actions: trash, like, variations, video
- Click image for fullscreen + more options

### Folders
- Click folder button next to search bar
- Generate images directly inside a folder
- Click X to leave folder

### More Options (per image)
- Copy prompt, Job ID, seed, image URL
- Report, make private/public, download
- Search similar, run as HD, open in Discord

### Style Creator
- Interactive grid tool for building custom `--sref` codes
- Pick images you like → MJ generates a custom style code
- Use the code in future prompts for consistent style

---

## 9. PIXEL ART & GAME SPRITE BEST PRACTICES

### Prompt Keywords
- **Style:** "16-bit pixel art", "32-bit chunky retro pixel art", "Enter the Gungeon style"
- **Quality:** "no anti-aliasing", "sharp edges", "no blur", "no gradient blending", "strict color separation"
- **Palette:** "strict 8-color NES palette", "maximum 15 simultaneous colors", "vibrant SNES color palette"
- **Grid:** "64x64 canvas", "32x32 sprite", "exact 1:1 pixel ratio"
- **View:** "orthographic view", "front view", "full body"
- **Background:** "solid green background", "isolated on white", "solid dark background"
- **Format:** "sprite sheet", "3x3 grid", "game asset", "character sprite"

### Parameter Recommendations for Pixel Art
| Parameter | Recommended | Why |
|-----------|------------|-----|
| `--s` | `300–500` | Strict style adherence. Higher = more MJ artistic freedom. |
| `--c` | `20–50` | Prevents over-smoothing. Adds variety between 4 outputs. |
| `--ar` | `1:1` | Square for sprites and grid sheets. |
| `--niji` | `6` or `7` | Anime model works well for game art. |
| `--style raw` | — | Reduces Niji's auto-anime styling. More literal. |
| `--no` | `text, watermark, blur, gradient` | Excludes common artifacts. |
| `--seed` | specific value | Reproduce similar results when iterating. |

### Niji 6 vs Niji 7 for Pixel Art
| Aspect | Niji 6 | Niji 7 |
|--------|--------|--------|
| Prompt following | More "vibey", interprets loosely | More literal, follows closely |
| Line work | Good | Cleaner, flatter |
| Detail | Good | Better eyes, reflections, small elements |
| Best for | Experimental, stylistic | Precise, repeatable designs |
| Recommendation | Good for initial exploration | Better for final production sprites |

---

## 10. GUNGEONMATE SPRITE GENERATION WORKFLOW

### Phase 1: Style Discovery
1. Generate a few test sprites with different `--sref random` codes
2. Find a style code that produces the right Gungeon aesthetic
3. Save that code for all future generations

### Phase 2: Individual Sprite Generation
```
[creature description] [element details] [style tags] --ar 1:1 --s 300 --niji 6 --style raw --sref [CODE] --no text, watermark, blur, gradient
```

### Phase 3: Grid Sheet Generation
```
3x3 grid sprite sheet of 9 variations of [creature], [cell-by-cell descriptions], [style tags] --ar 1:1 --s 300 --niji 6 --style raw --sref [CODE] --no text, watermark, blur, gradient
```

### Phase 4: Iteration
1. Pick the best of 4 outputs
2. Upscale it
3. If close but not perfect, use Vary (Subtle) or Vary (Strong)
4. Copy the seed from the best result
5. Re-run with `--seed [VALUE]` for similar results with tweaks

### Phase 5: Post-Processing
1. Download upscaled image
2. Remove background (Photoshop, remove.bg, or similar)
3. Crop individual sprites from grid sheets
4. Save as transparent PNGs
5. Name files: `[race]_l[level]_[element].png`

---

## 11. COMMON ISSUES & FIXES

| Issue | Fix |
|-------|-----|
| Blurry pixels | Add "no anti-aliasing, no blur, sharp 1:1 pixels" |
| Wrong colors | Specify "strict [N]-color palette" or exact hex names |
| Too much MJ style | Use `--raw` or `--style raw` with Niji |
| Inconsistent style across generations | Use `--sref` with a reference image or style code |
| Prompt too long / ignored | Shorten to under ~60 words. Move less critical details to `--no` |
| Good seed, want variations | Copy seed from result, re-run with `--seed [VALUE]` |
| Grid cells blending together | Add "clear cell separation", "grid lines", "each cell isolated" |
| Niji too anime | Use `--style raw`, or switch to `--v 6` standard model |

---

*This document is the companion reference to `roomian_races_art_direction.md`. All prompts in the art direction doc are pre-formatted with the correct parameters from this guide.*
