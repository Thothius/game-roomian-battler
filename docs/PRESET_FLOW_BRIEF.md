# Preset Flow Brief — pick-or-create customization

> Status: SPEC for Slot 1 VISUAL / customization agent. Supersedes the
> current studio landing layout. User request 2026-11-18.
> Goal: **simplify** — two doors, one wizard, live mock preview.

## Flow

```
ENTRY ──► CHOOSE: [PRESETS] [NEW PRESET]
 │
 ├─ PRESETS ──► full-screen swipeable gallery (PageView)
 │              • one card per preset: palette strip, name, vibe,
 │                mini live particle swatch
 │              • built-ins (kPickerThemes) + saved customs
 │                (CustomThemeStore / SavedCustomTheme)
 │              • bottom bar: [PICK PRESET] → apply + pop. Done.
 │
 └─ NEW PRESET ──► name dialog (reuse existing save-dialog pattern,
        │           incl. duplicate-name check)
        └─► SOURCE: [COPY EXISTING] [START FROM SCRATCH]
             │
             ├─ COPY ──► same gallery, select-only → seeds the
             │           wizard draft from that preset's
             │           {baseMode, prefs, customData, splashSlug}
             │
             └─ SCRATCH ──► blank draft (custom mode defaults)
                    │
                    └─► WIZARD — persistent TOP tab strip at all times:
                       [DETAILS] [COLORS & BG] [PARTICLES] [AMBIANCE] [SAVE]
                       • DETAILS — super-compact summary chips
                         (palette dots, particle preset, bg mode,
                         font, glow) + [PREVIEW] button
                       • PREVIEW — fullscreen mock, PageView ×2:
                         ① fake active-run view (gun + item tiles,
                           real icons via localGunIcon/localItemIcon)
                         ② item-detail view of ONE gun open
                         Both render through the REAL ThemeOverlay
                         path with the draft applied via
                         AppTheme.previewNotifier — mock data only,
                         seeded/isolated RunProvider so real run
                         state is untouched.
                       • COLORS & BG — palette editor + BG MODE:
                         GRADIENT / SOLID / NONE / WALLPAPER
                         (absorbs the in-flight custom-wallpaper
                         work — wp_01..46.webp already landed in
                         assets/images/wallpapers/custom/)
                       • PARTICLES / AMBIANCE — existing step
                         widgets (_ParticlesStep, _AmbianceStep,
                         typography folded in or kept as tab)
                       • SAVE — last tab, review summary →
                         CustomThemeStore.save(SavedCustomTheme)
```

## Data model

- Preset = `SavedCustomTheme { id, name, splashSlug, baseMode,
  prefs: VisualPrefs, customData }` — already exists, reuse as-is.
- Wizard edits a **draft** of that shape; nothing commits until SAVE.
- Copy-source = read any preset (built-in curation via
  `kThemeCuration`/`applyCuration`, or saved custom) into the draft.

## Hard rules

- Mock preview MUST go through `ThemeOverlay`/`buildBackdropParticleField`
  — no simplified replica — so particle-on-top / bg-mode layering bugs
  are visible in preview (ties to the theme/bg bughunt).
- Particles always render above bg; particle preset must match the
  picked theme (kThemeParticleDefaults binding stays authoritative).
- BG modes: gradient / solid / none / wallpaper — persisted per preset
  (new VisualPrefs field; Slot 1 owns theme_flair_prefs.dart).
- Dispose every controller; `context.mounted` before pops; haptics on
  picks; GoopText everywhere; Responsive.factor scaling.

## Coordination

- Slot 1 is mid-flight on `experience_studio_screen.dart` +
  `theme_overlay.dart` + `theme_custom_data.dart` (custom wallpaper).
  This flow REPLACES the studio landing — build on their branch or
  rebase after their merge; do not fork the file.
- Assets ready: `assets/images/avatars/custom_01..11.webp` (live in
  kAvatarIds), `assets/images/wallpapers/custom/wp_01..46.webp`.
- Source pools if more wanted: `X:\XXXXXXXXX\avatar-base`,
  `X:\XXXXXXXXX\bgs`, `X:\XXXXXXXXX\Masterworks_Avatars` (unused).

## Open questions (defaults chosen — flag if wrong)

1. Entry point: chooser replaces studio landing (assumed).
2. Gallery is pick-or-create only; edit/delete of saved presets is a
   follow-up (needs CustomThemeStore.remove).
3. Fonts live inside AMBIANCE tab (keeps 4 content tabs + SAVE).
