# GungeonMate — Customization Variety & Particle/Font Audit (2026 Standards)

**Assessor:** XEENU-ANIMATOR (Slot 1)
**Date:** 2026-08-25
**Audited commit:** `fe1a16c` (master HEAD)
**Companion to:** `docs/THEME_UX_ASSESSMENT_2026.md`

---

## 0. Executive Summary

The customization surface is **deep** — 32 user-adjustable `VisualPrefs` fields, 37 particle presets, 12 glow effects, 16 color schemas, 5 speeds, 68 fonts in 9 categories, 15 themes × remixes/unicorn palettes, a custom theme editor, 4 display modes, ambient shaders, 2.5D inventory tilt, dialogue haptics, Goopian language. This is genuinely top-tier variety for a companion app.

**But the presentation doesn't match the depth.** The three headline issues:

1. **20 of 37 particle presets are invisible to the user.** The picker shows a "curated" 17; the other 20 are auto-bound to themes but can't be manually selected. A user who likes Cat Lady's paw particles can't use them on, say, the Forge Master theme.
2. **Font picker is duplicated with divergent UX.** Experience Studio has a beautiful 9-category grid; Settings has a flat 68-item swipe picker. Same data, two experiences, one is 2026-grade and one isn't.
3. **6 VisualPrefs fields have no UI.** `shaderEnabled`, `shaderPreset`, `customDiceType`, `showDamageCalculator`, `showEffectsPanel`, `showShrinePanel`, `showDashboards` are persisted and loaded but have no control surface the user can reach.

Details below.

---

## 1. FONT AUDIT — Do we need all 68?

### 1.1 The inventory

`AppFont` enum (`app_theme.dart:1221`) has **68 values**. The Experience Studio `_FontFamilyGrid` (`experience_studio_screen.dart:1966`) organizes them into **9 categories**:

| Category | Count | Fonts |
|----------|-------|-------|
| **Featured** (locked) | 2 | gungeon, megrim |
| Pixel & Retro | 8 | pressStart2p, silkscreen, vt323, pixelifySans, bungee, bungeeShade, rubik8bit, dotgothic16 |
| Sci-Fi & Tech | 11 | monoton, blackOpsOne, orbitron, shareTechMono, syncopate, rajdhani, audiowide, russoOne, fasterOne, spaceGrotesk, jetBrainsMono |
| Display & Impact | 8 | archivoBlack, anton, rowdies, righteous, teko, fjallaOne, bebasNeue, kanit |
| Casual & Fun | 10 | comicNeue, fredoka, sniglet, lemon, lilitaOne, spicyRice, chewy, boogaloo, carterOne, permanentMarker |
| Clean & Modern | 7 | dmSans, outfit, syne, montserrat, lexend, comfortaa, alata |
| Gothic & Fantasy | 9 | medievalSharp, cinzelDecorative, almendra, metalMania, unifrakturMaguntia, newRocker, rye, nosifer, cinzel |
| Serif & Editorial | 6 | playfairDisplay, ebGaramond, merriweather, libreBaskerville, specialElite, coustard |
| Handwritten & Script | 5 | architectsDaughter, rockSalt, shadowsIntoLight, lobster, caveat |
| **Total** | **66** | (2 featured + 66 categorized = 68) |

### 1.2 The two locked fonts

**gungeon** and **megrim** are pinned in "Featured" and must stay. They are the app's identity:
- **gungeon** (`EnterTheGungeonBig`) — the official EtG pixel font. Non-negotiable. This is the brand.
- **megrim** — the app's signature thin-wire display font used for headlines and the GungeonMate wordmark. Established visual identity.

**Verdict: keep both locked. No question.**

### 1.3 Do we need the other 66?

**Yes, but with caveats.** The variety is a feature, not a bug — GungeonMate is a companion app for a game with strong art direction, and letting users match the app's voice to their character/run mood is on-brand. A Marine player wants `shareTechMono`; a Cultist player wants `medievalSharp`; a Bullet player wants `cinzel`.

**However, 68 is at the edge of cognitive load.** The 2026 question isn't "do we need them" but "are they presented so the user isn't overwhelmed?" The Experience Studio's 9-category grid solves this well. The Settings tab's flat swipe picker does not.

**Recommendation:** Keep all 68. Fix the Settings presentation (see §1.4). The categories are the right abstraction — no font feels redundant within its category.

**One trim candidate:** `comicNeue` (Casual & Fun) is a Comic Sans derivative. It's a meme font. If the user wants whimsical, `fredoka` or `sniglet` do it better without the Comic Sans stigma. **Low priority — leave it, it's harmless.**

### 1.4 The duplication problem

| Surface | Widget | Categorization | Live preview | UX grade |
|---------|--------|---------------|--------------|----------|
| Experience Studio → Typography tab | `_FontFamilyGrid` | 9 categories | Font name rendered in itself | **A** |
| Settings → Appearance tab | `SwipePicker<AppFont>` | None — flat 68-item swipe | Name + "The Breach: Bello's Shop" sample | **C** |

The Settings swipe picker is the weak link. A 68-item horizontal swipe with no categories is exhausting. The user swipes through 68 cards to find one font.

**Fix (low effort, high impact):** Replace the Settings `SwipePicker<AppFont>` with the same `_FontFamilyGrid` widget (or a shared `FontPickerGrid` widget both surfaces import). One component, two surfaces, consistent UX. The font size/weight sliders below it can stay as-is.

### 1.5 Font descriptions

The Experience Studio grid shows the font name rendered in the font itself — which IS the preview. No text description needed; the font speaking its own name is the clearest possible affordance. **This is correct.** The Settings picker adds "The Breach: Bello's Shop" as a second sample line, which is nice but redundant with the name-in-its-own-font preview.

**Verdict: no descriptions needed. The name-in-font preview is the 2026 standard.**

---

## 2. PARTICLE PRESENTATION AUDIT

### 2.1 The 37 presets — what's shown vs. hidden

The `_PresetGrid` (`experience_studio_screen.dart:1644`) shows a **curated 17**:

**Shown (17):**
- 8 originals: gungeonDust, cosmicStars, forgeEmbers, frostShards, unicornSparkles, goldenSparkle, cursedSmoke, bulletHell
- 6 artful: auroraVeil, crystalLattice, inkSplatter, solarFlare, tidePool, stainedGlass
- 3 Gungeon-unique: blankShells, hegemonyCredits, masterRoundAura

**Hidden (20) — auto-bound to themes but not manually selectable:**
toxicBubbles, brassCasings, voidRift, cosmicDust, rainbowConfetti, bulletKin, heartContainers, cursedSkulls, masterRounds, jamHexes, **catPaws, moonlight, lightningBolts, paradoxShards, gunpowderSmoke, dragunScales, circuitTraces, shellCasings, heroicBlades, boneShards**

The bolded 13 are the themed presets that `kThemeParticleDefaults` binds to visible themes. The user gets them automatically when they pick Cat Lady / Moonlit / Storm Caller / etc. — but if they want, say, `lightningBolts` on the Forge Master theme, they can't. The preset is invisible in the picker.

**This is the biggest particle UX defect.** The curated list was presumably trimmed to avoid overwhelm, but it created an asymmetry: the theme system references presets the user can't see or pick.

**Fix:** Show all 37, grouped by category. Suggested categories:
- **Themed** (13): catPaws, moonlight, lightningBolts, paradoxShards, gunpowderSmoke, dragunScales, circuitTraces, shellCasings, heroicBlades, boneShards, bulletKin, heartContainers, cursedSkulls
- **Classic** (8): gungeonDust, cosmicStars, forgeEmbers, frostShards, unicornSparkles, goldenSparkle, cursedSmoke, bulletHell
- **Artful** (6): auroraVeil, crystalLattice, inkSplatter, solarFlare, tidePool, stainedGlass
- **Gungeon-Unique** (3): blankShells, hegemonyCredits, masterRoundAura
- **Misc** (7): toxicBubbles, brassCasings, voidRift, cosmicDust, rainbowConfetti, masterRounds, jamHexes

A "Themed" category header could note: "These pair with specific themes — try them with their matching theme!" This educates the user without hiding options.

### 2.2 Glow effects — blurbs exist but aren't shown

`GlowEffect` has 12 values with a `blurb` getter (`particle_engine.dart:896-908`):
- none → "No glow — pure particles"
- smokey → "Soft diffuse blur"
- ripple → "Expanding ring waves"
- pulse → "Steady brightness pulse"
- cursed → "Hue-shifting cursed aura"
- neon → "Crisp bright neon halo"
- aurora → "Cycling hue rainbow halo"
- ember → "Warm flickering fire glow"
- spectral → "Ghostly translucent echo"
- plasma → "Swirling electric rings"
- prism → "Rainbow refraction shards"

The `_GlowRow` widget (`experience_studio_screen.dart:1880`) shows **only the label** — not the blurb. A user sees "Spectral" and has to guess what it means.

**Fix:** Show the blurb as a subtitle under the label, or as a tooltip on long-press. The blurbs are already written — just render them. One-line change per chip.

### 2.3 Particle preset descriptions — same issue

`ParticlePresetX.description` (`particle_engine.dart:288-326`) has a human-readable description for every preset:
- forgeEmbers → "Fire embers rising with lively flicker, orange/red/gold"
- catPaws → "Tiny cat paw prints drifting upward with warm amber glow"
- lightningBolts → "Electric lightning bolts striking downward with flash glow"

The `_PresetGrid` chip shows the label + a color swatch + a shape icon — but **not the description**. The description is the most useful text for a user deciding between 37 presets.

**Fix:** Add the description as a second line in each preset chip (small, muted), or show it in a detail panel when a preset is hovered/selected. The text exists — surface it.

### 2.4 Color schemas — well done

`_SchemaGrid` (`experience_studio_screen.dart:1762`) shows all 16 `ParticleColorSchema` values with color swatch strips. `presetDefault` and `themeMatch` get icons instead of swatches. **This is good 2026 UX** — visual representation + label, no text description needed (the swatch IS the description).

**One nit:** `themeMatch` is the most powerful option (particles auto-match the active theme) but it's just an icon. Consider a one-line hint: "Match the active theme's colors automatically."

### 2.5 Speed, count, size, opacity — clean

- Speed: 5-button row (Very Slow → Very Fast). Clear.
- Count: slider 1–32. Reasonable range.
- Size: slider 0.3×–2.0×. Good.
- Opacity: slider 0–100%. Standard.

**No issues. These are well-tuned.**

### 2.6 Line links + edge bounce — toggles, fine

Two `_ToggleRow` switches. Simple, clear. No issue.

### 2.7 The live preview gap

The Particles tab has no live particle preview. The user picks a preset, then has to navigate to the home screen to see it. The Experience Studio's preview scene (in the Theme tab) shows a sample item card but **not particles**.

**This is a 2026 gap.** A particle picker without a live particle preview is like a font picker without showing the font. The `ParticleField` widget is self-contained (`RepaintBoundary` + `CustomPaint`) and could be embedded as a small preview pane at the top of the Particles tab.

**Fix:** Add a 120px-tall `ParticleField` preview at the top of `_ParticlesStep`, reflecting the current preset/schema/glow/speed/count/size/opacity in real-time. This is the single highest-impact particle UX improvement.

---

## 3. CUSTOMIZATION VARIETY — Full Surface Audit

### 3.1 The 32 VisualPrefs fields — UI coverage

| # | Field | UI Location | Status |
|---|-------|-------------|--------|
| 1 | glowIntensity | Studio Ambiance + Settings Glow | ✅ Both |
| 2 | particlesEnabled | Studio Particles | ✅ |
| 3 | particlePreset | Studio Particles (17 of 37) | ⚠️ Partial |
| 4 | particleGlowEffect | Studio Particles | ✅ |
| 5 | particleLineLinks | Studio Particles | ✅ |
| 6 | particleBounce | Studio Particles | ✅ |
| 7 | glowColorIndex | Studio Ambiance + Settings Glow | ✅ Both |
| 8 | fontWeightBias | Studio Typography + Settings Font | ✅ Both |
| 9 | font | Studio Typography + Settings Font | ⚠️ Divergent UX |
| 10 | fontSize | Studio Typography + Settings Font | ✅ Both |
| 11 | inventoryFontSize | Studio Typography + Settings Font | ✅ Both |
| 12 | inventoryDisplayMode | Settings Inventory | ✅ |
| 13 | customDiceType | **NO UI** | ❌ Orphaned |
| 14 | particleSizeScale | Studio Particles | ✅ |
| 15 | particleOpacity | Studio Particles | ✅ |
| 16 | particleCount | Studio Particles | ✅ |
| 17 | dialogueHapticsEnabled | Studio Ambiance | ✅ |
| 18 | dialogueTextSpeedMs | Studio Ambiance | ✅ |
| 19 | isGoopianLanguage | main_menu (commented out) | ⚠️ Hidden |
| 20 | spongeActive | summary_tab (only if Goopian on) | ⚠️ Hidden |
| 21 | showDamageCalculator | **NO UI found** | ❌ Orphaned |
| 22 | showEffectsPanel | **NO UI found** | ❌ Orphaned |
| 23 | showShrinePanel | **NO UI found** | ❌ Orphaned |
| 24 | showDashboards | **NO UI found** | ❌ Orphaned |
| 25 | periodicGridColumnCount | Settings Inventory | ✅ |
| 26 | particleColorSchema | Studio Particles | ✅ |
| 27 | particleSpeed | Studio Particles | ✅ |
| 28 | runDisplayMode | Run display mode bar | ✅ Contextual |
| 29 | runDisplayModeBarCollapsed | Run display mode bar | ✅ Contextual |
| 30 | depthInventory | Run display mode bar prefs | ✅ Contextual |
| 31 | depthTiltIntensity | Run display mode bar prefs | ✅ Contextual |
| 32 | shaderEnabled | **NO UI** | ❌ Orphaned |
| 33 | shaderPreset | **NO UI** | ❌ Orphaned |
| 34 | showModePickerOnNewRun | Onboarding dialog | ✅ Contextual |

**Scorecard:**
- ✅ Fully surfaced: 22
- ⚠️ Partial / divergent / hidden: 4
- ❌ Orphaned (no UI): 6 — customDiceType, showDamageCalculator, showEffectsPanel, showShrinePanel, showDashboards, shaderEnabled, shaderPreset

### 3.2 The 6 orphaned fields

These are persisted, loaded on startup, but have no user-facing control:

1. **`shaderEnabled` + `shaderPreset`** — The Q3 ambient fragment shaders (digital_rain.frag, dark_neon_fog.frag) were implemented in v1.9.51 with full `VisualPrefs` persistence, but no toggle was ever added to any settings surface. The shaders exist, the prefs exist, the user can't turn them on. **This is a finished feature that was never wired to a switch.**

2. **`customDiceType`** — 7 dice styles (themeDefault, classicWhite, goldGlimmer, frostShard, moltenAmber, voidPurple, toxicOoze) with labels. No UI found anywhere. The dice roller presumably uses `themeDefault` forever.

3. **`showDamageCalculator` + `showEffectsPanel` + `showShrinePanel` + `showDashboards`** — These control dashboard panel visibility on the active-run screen. They may be toggled by contextual buttons on that screen (not in Settings/Studio), but the subagent didn't find explicit toggles. If they're contextual-only, that's fine — but they should be documented as such.

**Fix priority:**
- **HIGH:** Add shader toggle + preset picker to the Ambiance tab (the natural home). The feature is built, just not surfaced.
- **MEDIUM:** Add dice type picker to Ambiance or a Gameplay tab.
- **VERIFY:** Confirm the 4 dashboard toggles have contextual controls on the active-run screen. If not, add them to Settings.

### 3.3 Custom theme editor — gaps

`_CustomColorsStep` (`experience_studio_screen.dart:1312`) lets the user edit 6 colors (scaffold, card, primary, secondary, headlineStat, bulletColor) with a 24-color preset palette + an HSV picker dialog. It has a "Randomize" button that picks from 20 curated Gungeon schemas with a lore name.

**Missing from the editor (but present in `CustomThemeData`):**
- **`auraStyle`** — The data model supports 17 `AvatarAuraStyle` values, but the editor doesn't let the user pick one. The custom theme always gets `AvatarAuraStyle.none`.
- **`font`** — The data model has a `font` field, but the editor doesn't expose it. The custom theme uses the global font setting.
- **Name field** — `CustomThemeData.name` exists and the randomizer generates lore names, but the user can't name their custom theme. It's always "Custom" (or whatever the randomizer last set).

**Fix:** Add three rows to `_CustomColorsStep`:
1. Aura style picker (dropdown or chip row of 17 styles)
2. Font picker (reuse the `_FontFamilyGrid` or a compact dropdown)
3. Name text field

This would make the custom theme a complete peer to the curated themes.

### 3.4 Theme remixes — well done but under-explained

`_RemixPalettes` (`experience_studio_screen.dart:1230`) shows remix variants as a 2-column grid with 3-color swatch strips. Available for:
- Forge Master: Original / Ember / Magma / Inferno (4)
- Robot's Core: Original / Rust / Arc Flash / Voltage (4)
- Minimalist: Original / Graphite / Platinum / Charcoal / Obsidian (5)

**This is good.** The swatch strip communicates the variant visually. **One nit:** no description of what changes. "Ember" vs "Magma" vs "Inferno" — the user guesses from the swatch. A one-line subtitle ("+25° hue shift", "Full purple refactor") would help.

### 3.5 Unicorn palettes — well done

`_UnicornPalettes` (`experience_studio_screen.dart:1153`) shows all 6 UnicornPalette variants as a grid with color swatches. Clear, visual, on-brand. **No issues.**

---

## 4. 2026 STANDARDS CHECKLIST

| Standard | Status | Notes |
|----------|--------|-------|
| **Live preview for every visual choice** | ⚠️ Partial | Fonts: yes. Font size: yes. Particles: **no**. Themes: yes (splash). Custom colors: yes (live refresh). |
| **Categorized option lists (not flat)** | ⚠️ Partial | Fonts in Studio: yes (9 categories). Fonts in Settings: **no** (flat swipe). Particles: **no** (curated flat list, 20 hidden). |
| **Descriptions/blurbs surfaced** | ❌ No | Glow blurbs exist, not shown. Particle descriptions exist, not shown. Remix descriptions missing. |
| **No orphaned features** | ❌ 6 orphaned | Shaders, dice type, dashboard toggles — built but not surfaced. |
| **Consistent UX across surfaces** | ❌ Divergent | Font picker: Studio = categorized grid, Settings = flat swipe. |
| **Every persisted pref has a control** | ❌ 6 missing | See §3.1. |
| **Custom theme is a complete peer** | ⚠️ Partial | Missing aura, font, name. |
| **Contextual controls documented** | ⚠️ Unknown | Dashboard toggles may be contextual-only — needs verification. |
| **No hidden features** | ⚠️ 2 hidden | Goopian language + sponge mode are commented out. Intentional? If so, document. |
| **Performance: RepaintBoundary on animating layers** | ✅ Yes | ParticleField wrapped. Touch particles wrapped. (Main field in overlay missing — noted in prior assessment.) |

---

## 5. RECOMMENDED ACTIONS (ranked)

| # | Action | Severity | Effort | Impact |
|---|--------|----------|--------|--------|
| 1 | Add live `ParticleField` preview to Particles tab | HIGH | Med | Highest single UX win — particles are visual, preview must be visual |
| 2 | Show all 37 particle presets, grouped by category | HIGH | Low | Unlocks 20 hidden presets, educates user on theme pairing |
| 3 | Surface glow blurbs + particle descriptions in chips | HIGH | Trivial | Text exists, just render it |
| 4 | Add shader toggle + preset picker to Ambiance tab | HIGH | Low | Feature is built, just wire the switch |
| 5 | Replace Settings flat font SwipePicker with categorized grid | MED | Low | Consistency — reuse `_FontFamilyGrid` |
| 6 | Add aura/font/name to custom theme editor | MED | Med | Makes custom a complete peer |
| 7 | Verify/surface the 4 dashboard panel toggles | MED | Low | Confirm contextual controls exist |
| 8 | Add dice type picker to Ambiance or Gameplay | LOW | Low | 7 styles built, unused |
| 9 | Add remix subtitle descriptions | LOW | Trivial | One line per variant |
| 10 | Add `themeMatch` hint text to schema grid | LOW | Trivial | "Match the active theme's colors" |
| 11 | Document Goopian/sponge as intentional hidden features | LOW | Trivial | Or remove if abandoned |

---

## 6. VERDICT — Is the variety justified?

**Yes.** 37 presets, 68 fonts, 16 schemas, 12 glows, 15 themes × remixes — none of it is gratuitous. Each category serves a clear aesthetic purpose, and the Gungeon's lore-rich world justifies the breadth. A Marine player, a Cultist player, and a Bullet player should have different app experiences.

**The variety is not the problem. The presentation is.** The system has more depth than the UI exposes. The fix is not to cut options — it's to surface them with the categorization, descriptions, and live previews that the data already supports.

**One-sentence summary:** GungeonMate's customization engine is a 9/10; its customization UI is a 6/10 because it hides its own best features.

---

*End of customization audit. Pairs with `docs/THEME_UX_ASSESSMENT_2026.md`.*
