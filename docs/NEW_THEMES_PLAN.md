# New Themes Plan — 3 punk/glow originals (user request 2026-11-25)

**STATUS: SHIPPED** — app `c9d4cca`. Deviations from spec below:
Neon Riot font is `AppFont.monoton` (audiowide isn't in the curated
font set — it would migrate to fjallaOne); glowStyle values used:
ember/prism/drip; splashSlug `''` → gradient thumbs everywhere.

User: *"make us 3 new themes made by you. punky bold glowy stuff that
has character!"* — designed by SUPPORT (Devin). All three reuse ONLY
existing `ThemeFlair` fields, `AppFont`s with bundled assets, and
existing `GlowStyle`/`AvatarAuraStyle` values — no engine changes, no
new assets required (splash art optional, `splashSlug: ''` falls back
to the palette-gradient thumb everywhere splash is used).

## Registration checklist (per theme)

1. `enum AppThemeMode` — new member with `label`, `vibe`, `diff`,
   `elem`, `whimsicalDescription`, `staticFlair` (copy spec below).
2. `splashSlug` switch — return `''` (gradient fallback; art can be
   added later as `assets/images/themes/splash/<slug>.jpg`).
3. Verify persistence: themes persist by name/index — confirm new
   members don't shift existing indices OR that migration handles it
   (lesson 1.4 in REWORK_LESSONS_LEARNED).
4. Picker surfaces pick up enum members automatically — verify in
   Experience Studio gallery + quick slots.
5. `version_lockstep` unaffected; add VERSION_HISTORY Unreleased entry.

---

## Theme 1 — POPRIOT *("The Pop Riot")*

**Fantasy:** pop-punk flyer pasted over a mosh pit — acid pink and
radioactive lime screamed across tar black. Bold, joyful, slightly
delinquent. The theme for Gungeoneers who came to start something.

- `label: 'Popriot'`, `vibe: 'REBELLIOUS'`, `diff: 'CHAOS'`,
  `elem: 'LIGHTNING'`
- `whimsicalDescription`: 'Photocopied punk flyers and dry-ice fog.
  Acid pink and radioactive lime on tar black — loud on purpose.'
- `font: AppFont.bungee` (chunky display, bundled)
- Palette:
  - scaffold `0xFF0B0710` (tar black w/ violet undertone)
  - card `0xFF1D1020`
  - primary `0xFFFF2E88` (acid hot pink)
  - secondary `0xFFBFFF00`?? → use `0xFFA6FF00` (radioactive lime,
    keeps AA contrast on dark)
  - headlineStat `0xFFFF6EC7`
  - bulletColor `0xFFFF2E88`, bulletGlyph `'✖'`, twinkleBullets true
  - sparkleNumbers true, numberGlowColor `0xFFFF2E88`
  - tabularFigures false, numberSizeScale 1.08, w800, italic
  - chipRadius 6, cardRadius 10 (angular, not round — punk zine)
  - cardBorderColor `0x66A6FF00`, cardBorderWidth 1.2
  - dividerColor `0x55FF2E88`, dividerThickness 1.4
  - glowPrimary `0x66FF2E88`, glowSecondary `0x44A6FF00`
  - glowStyle `GlowStyle.ember` (flickering hazard glow)
  - auraStyle `AvatarAuraStyle.pastelPulse` (closest existing;
    optional future `riotRing` aura)
  - headerGlyph `'⚡'`, headerUnderlineColor `0xAAFF2E88`
  - statGroupCombat `0xFFFF2E88`, statGroupHandling `0xFFA6FF00`,
    statGroupMeta `0xFF7DF9FF`

## Theme 2 — NEON RIOT *(synthwave nights)*

**Fantasy:** a dead mall at 2AM — magenta neon tubes over a cyan grid.
Smooth, expensive, humming. The theme for players who rage in style.

- `label: 'Neon Riot'`, `vibe: 'NEON'`, `diff: 'STEADY'`,
  `elem: 'CIRCUIT'`
- `whimsicalDescription`: 'A closed arcade at 2AM. Magenta tubes over
  a cyan grid — smooth, expensive, humming.'
- `font: AppFont.monoton`?? → check readability at body sizes;
  fallback `AppFont.audiowide` (synth, readable). **Decision: audiowide.**
- Palette:
  - scaffold `0xFF0A0618` (deep violet-black)
  - card `0xFF171029`
  - primary `0xFFFF2EC4` (magenta tube)
  - secondary `0xFF00E5FF` (cyan grid)
  - headlineStat `0xFFFF7AD9`
  - bulletColor `0xFF00E5FF`, bulletGlyph `'◆'`, twinkleBullets true
  - sparkleNumbers true, numberGlowColor `0xFFFF2EC4`
  - tabularFigures true (synth = technical), numberSizeScale 1.06,
    w700, normal style
  - chipRadius 4, cardRadius 6 (sharp tech edges)
  - cardBorderColor `0x5500E5FF`, cardBorderWidth 1.0
  - dividerColor `0x4400E5FF`, dividerThickness 1.0
  - glowPrimary `0x66FF2EC4`, glowSecondary `0x5500E5FF`
  - glowStyle `GlowStyle.prism` (rotating color-wheel = synthwave)
  - auraStyle `AvatarAuraStyle.cosmicTemporal` (cyan/gold rings fit)
  - headerGlyph `'▮'`? prefer `'◢'`… use `'✦'`→ too unicorn; use `'◈'`
  - headerUnderlineColor `0xAA00E5FF`
  - statGroupCombat `0xFFFF2EC4`, statGroupHandling `0xFF00E5FF`,
    statGroupMeta `0xFFB388FF`

## Theme 3 — TOXIRIOT *(hazmat outbreak)*

**Fantasy:** a contained breach that escaped containment — biohazard
lime and warning-stripe orange over sickly purple. The theme for
players who treat the Gungeon like a spill.

- `label: 'Toxi Riot'`, `vibe: 'TOXIC'`, `diff: 'BRUTAL'`,
  `elem: 'ACID'`
- `whimsicalDescription`: 'A containment breach with commitment
  issues. Hazard lime and warning orange over sickly violet — handle
  with care (don\'t).'
- `font: AppFont.silkscreen`?? → pixel may clash with "bold glowy";
  **decision: `AppFont.wallpoet`** (heavy poster type).
- Palette:
  - scaffold `0xFF0D0F08` (sickly near-black green)
  - card `0xFF1A1F12`
  - primary `0xFF7CFF00` (hazard lime)
  - secondary `0xFFFF6B00` (warning orange)
  - headlineStat `0xFFA8FF3E`
  - bulletColor `0xFF7CFF00`, bulletGlyph `'☣'`, twinkleBullets false
  - sparkleNumbers false, numberGlowColor `0xFF7CFF00`
  - tabularFigures true, numberSizeScale 1.05, w800, normal
  - chipRadius 3, cardRadius 4 (industrial/square)
  - cardBorderColor `0x557CFF00`, cardBorderWidth 1.4
  - dividerColor `0x557CFF00`, dividerThickness 1.2
  - glowPrimary `0x667CFF00`, glowSecondary `0x44FF6B00`
  - glowStyle `GlowStyle.drip` (slow toxic seep)
  - auraStyle `AvatarAuraStyle.toxicOoze` (existing bubbling green —
    perfect fit)
  - headerGlyph `'☣'` (radioactive — already the elem sign; check it
    renders in the font stack, fallback `'✚'`)
  - headerUnderlineColor `0xAA7CFF00`
  - statGroupCombat `0xFFFF6B00`, statGroupHandling `0xFF7CFF00`,
    statGroupMeta `0xFF9D7BFF`

---

## Open questions for user (non-blocking)

1. **Splash art** — ship with `''` (gradient thumbs) or commission 3
   splash jpgs later? Recommend ship now, art later.
2. **Ordering** — append at end of enum (before `custom`?) or group
   with other "loud" themes? Enum order affects picker listing only
   if the picker iterates all values — verify.
3. **Aura upgrades** — all three reuse existing aura styles; a custom
   `riotRing`/`hazmatBubbling` aura is a possible VISUAL follow-up.
