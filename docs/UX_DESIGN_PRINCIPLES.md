# GungeonMate UX & Color Design Principles

Distilled from three reference sheets (Laws of UX, Science of Color in UI,
Color Combination Cheatsheet) and mapped onto the app's existing patterns.
Use this as the checklist when building or polishing a screen — especially
the Customization hub.

---

## 1. The laws that matter for GungeonMate

| Law | What it says | Where it applies in the app |
|-----|--------------|------------------------------|
| **Hick's Law** | Decision time grows with choice count | Why the hub is 5 tabs, not one wall of options. Swatch grids are curated (64+32), not an infinite picker. Particle palettes are 18 named sets, not RGB sliders |
| **Miller's Law** | ~7±2 items in working memory | Tab strip stays ≤5. Preset grid is 6. Physics is 3 toggles. If a section wants >9 items → group or scroll, never a dump |
| **Fitts's Law** | Big near targets are fast to hit | Action bar is full-width APPLY. Tab pills are full-width. Swatches are tappable circles, not points. Min touch ~40px |
| **Jakob's Law** | Users expect familiar patterns | Bottom-sheet picker, drag handle, page dots, tab strip — all stock mobile patterns, no bespoke gestures to learn |
| **Doherty Threshold** | <400ms feedback or users feel wait | Every tap writes VisualPrefs → LIVE LOOK re-renders same frame. AnimatedContainer 140-200ms everywhere. Never a silent state change |
| **Aesthetic-Usability** | Pretty reads as usable | The dark neon token system + glow/particles IS the polish — keep every surface skinned, nothing default-gray |
| **Law of Proximity** | Near = related | `_StepLabel` + tight gap + grouped controls. Related controls live inside one bordered container |
| **Law of Common Region** | Bounded = grouped | Palette panels, slider cards, section borders — every cluster gets a rounded container with hairline border |
| **Von Restorff** | The different thing is remembered | ACTIVE badge (green), preview border (accent), selected rings (white + glow) — exactly one standout state per element |
| **Cognitive Load** | Working memory is finite | Progressive disclosure: role descriptions under labels ('app background'), swatch sheet only on tap, Unicorn variants only when relevant |
| **Postel's Law** | Liberal in what you accept | `loadOr('[]')` asset fallbacks, `?? defaultTheme` on every pref read, errorBuilder on every Image, clamped indices on persisted enums |
| **Peak-End Rule** | Users judge by peak + end | APPLY is the last tap → make it feel good (haptic + state commit). First impression = LIVE LOOK renders instantly |
| **Selective Attention** | One focus at a time | One accent color leads per screen (flair.primary); secondary stuff at 40-60% white. Never two screaming elements competing |
| **Occam's Razor** | Simplest complete form | BACK+APPLY only (the PREVIEW button died for this). CUSTOM tab: 6 rows + save. No feature exists twice |
| **Law of Similarity** | Same look = same function | All selectable chips share: rounded rect + border + accent-fill-when-active. Users learn the pattern once |

---

## 2. Color rules for GungeonMate

From the Science of Color sheet, adapted to a dark-neon game UI:

### The 60-30-10 rule, translated
- **60% = scaffold + surface darks** (flair.scaffold, flair.card) — the canvas. Deep desaturated, never pure black.
- **30% = secondary/structure** (borders, secondary text, divider tones) — ~0.08-0.4 alpha whites + flair.secondary.
- **10% = accent energy** (flair.primary, headlineStat) — the neon. Buttons, selection rings, stats. Restraint is what makes it feel premium.

### Accent discipline
- ONE primary accent per theme leads the eye. headlineStat is the second voice (numbers only). Secondary fills structure, not another accent.
- Dark-mode contrast: never pure #000 backgrounds or pure #FFF body text — off-dark surfaces + off-white text (tokens already enforce).
- Glow = atmosphere, not information. It should be felt at the edges (vignette/ambient), never wash over text (that's why effectiveGlow caps at 1.8).

### Curated-choice principle
Users pick from *designed* palettes, never raw color space:
- Theme presets = complete identities (6 now)
- Particle palettes = named curated sets (18)
- Swatch sheet = 64 general + 32 metallic, arranged by family
- This is Hick's + Color Psychology together: every offered option is already good, so any choice looks intentional.

### Emotional palette mapping (for future themes)
- Trust/calm → blues, teals (moonlit/paperInk family)
- Energy/loot-tier → amber, gold, orange (forge/dragunfire)
- Danger/curse → crimson, dark red (lichs/jammed)
- Mystic/rare → violet, magenta (unicorn/void)
- Nature/organic → jade, moss, olive

---

## 3. The customization-hub checklist

When touching the hub, verify against this list:

- [ ] Every option visibly changes the LIVE LOOK (or its own preview) in the same frame — no dead controls
- [ ] Every label has a plain-English description where the name is jargon
- [ ] Curated sets over free-form inputs (swatches > raw pickers)
- [ ] ≤7 items per ungrouped section; scroll/page for more
- [ ] Selected/active states are unmistakable (ring + fill + optional badge)
- [ ] Affordances animate: drag handles bob, pagers show dots, sheets slide
- [ ] Nothing persists silently — staged until APPLY, restored on BACK
- [ ] Off-white text, off-black surfaces, single accent lead
- [ ] Tap targets ≥40px, touch feedback within 200ms
- [ ] Falls back gracefully on every asset/pref/index (Postel)
