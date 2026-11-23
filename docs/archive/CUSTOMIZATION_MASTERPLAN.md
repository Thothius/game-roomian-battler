# Customization Masterplan — Final Form

> **STATUS: COMPLETE (2026-11-25, Session A).** Every section shipped except the
> "session seed" label polish — tracked as H23 in `HOUSEKEEPING_MASTERPLAN.md`.
> Archived to `docs/archive/` — kept for design rationale, not active work.


> Technical roadmap for taking the Experience Studio (customization) and
> its surrounding surfaces (preview, particles, avatars, MP connect)
> to their finished state. Written 2026-11 by Slot 2 (CORE).
>
> **Status legend:** ✅ shipped · 🟡 in flight (code exists, UI pending) · ⬜ planned

---

## 1. Vision — what "final form" means

- **One living preview.** The fullscreen preview is a real interactive
  run slice (real `ActiveRunScreen` on an isolated mock `RunProvider`),
  re-rolled every open. Users don't *look at* views — they *play* a
  throwaway session and see their theme on real UI.
- **Particles as products, not sliders.** 12 hand-crafted LOOKS apply a
  full behavior config in one tap; manual knobs remain for tweaking;
  any gun/item sprite can become the particle itself.
- **Color picking without guesswork.** 6 persistent favorite slots +
  inline mock-element previews so every role is visible where you pick
  it — no "open preview and hope".
- **Alive surfaces.** Wallpapers can breathe (immersive parallax),
  avatars idle-animate, and MP connect gets a proper handshake ritual.

---

## 2. Architecture map (as built)

```
ExperienceStudioScreen (dashboard = _buildHub, editor = _buildEditor)
├── Stage machine: choose → gallery/source → wizard → editor
│   (user's uncommitted dashboard/editor split — PRESERVE)
├── Staging: AppTheme.previewNotifier + CustomThemeData draft
│   APPLY commits · BACK restores entry snapshot · SAVE/UPDATE persists
├── VisualPrefs (ChangeNotifier via VisualPrefs.notifier)
│   → persisted SharedPreferences + serialized into saved presets
│   → consumed by ThemeOverlay / buildBackdropParticleField app-wide
└── Preview: _MockPreviewScreen
    ├── isolated RunProvider (loadData → random char + 6 guns + 6 items)
    ├── inner Navigator → real ActiveRunScreen (FAB quick-add,
    │   item-detail pushes, run tools, dice — all on mock state)
    ├── _PreviewDock: RUN (popToFirst) / BROWSE (push BrowseScreen)
    ├── PopScope: system back pops inner route, then exits preview
    └── casino button re-rolls a fresh session in place
```

Key invariants to preserve:

- Preview **never** touches the real `RunProvider` — `ChangeNotifierProvider.value`
  scopes the mock inside the preview route only.
- Every visual surface reads `VisualPrefs.notifier` / `AppTheme.displayed*`
  so draft edits reflect live everywhere (studio pane, preview, mocks).
- `_with()` + single `_persist()` per logical change; presets round-trip
  through `toJson`/`fromJson` — **new pref fields MUST be added in all
  six places** (field, ctor, key, init, _with, toJson, fromJson, persist).

---

## 3. Workstream status

> **ALL SESSIONS SHIPPED 2026-11-20 — v3.6.0+166** (`0df69ee`).
> S1 `4a2cd69` · S2 `7877b45`+`51c2ab5` · S3 `e6cd8cb` ·
> S4 `c48df52` · S5 `37890ba` · S6 `0df69ee` (+`db9a488` preview shield).
> Full analyze clean, 603 tests pass.

### A. Studio core ✅

- Sprite orientation fix (WEBP fallback) — shipped `246ddfb`.
- Direct preset editing (`CustomThemeStore.update`, EDIT action,
  UPDATE PRESET) — shipped `246ddfb`.
- Dashboard/editor split — user's in-flight work, preserve.

### B. Living preview ✅ (this session)

- Real `ActiveRunScreen` + mock `RunProvider`, random session per open,
- casino re-roll, RUN/BROWSE dock, nested-nav back handling.
- Remaining polish (⬜): consider a tiny "session seed" label; verify
  MP-only widgets never appear (MpSession.isActive=false path already).

### C. Particles — final form ✅ (`4a2cd69`)

All items landed: `ItemIconField` path refactor, overlay sprite branch,
LOOKS row (12 tiles), ANY SPRITE picker over all gun/item WEBPs,
mutual-exclusion taps, tests. Plus 10 new `ParticleType`s appended
(star/bolt/heart/skull/paw/crescent/hexagon/smoke/scale/triangle —
persisted indices untouched) and all 11 glow effects exposed.

### D. Color system ✅ (`7877b45`)

- **6 favorite slots** shipped as `ColorFavorites` service
  (`vp.color_favorites` key) — stable indices, start empty, tap
  filled = use / tap empty = fill / long-press = change-or-clear.
  Lives inside `_PaletteColorSheet` so every color control gets it.
- **Inline role mocks**: live composite app-slice (stat, card, prime
  button, bullet glyph, secondary text) in COLORS & BG repaints all
  six roles at once.
- **Panel-chrome mock**: card + nav-pill rendered from resolved
  `flairFor` output inside the PANELS section.

### E. Wallpaper immersion ✅ (`e6cd8cb`)

- `VisualPrefs.wallpaperImmersive` (bool, persist + theme JSON,
  `vp.wallpaper_immersive_v1`).
- `CustomWallpaper` is now stateful: 18s breathing zoom
  (1.18× overscan → 1.23× peak) + tilt parallax (±16px) off the
  shared `ThemeOverlay.tiltNotifier`; scrim stays frame-locked.
- Toggle = IMMERSIVE chip in the wallpaper picker sheet.
- Reduced-motion renders a static composed frame.

### F. MP polish ✅ (`c48df52` + `37890ba`)

1. **Name beside avatar** ✅ — `ParadoxPlayerPanel` shows nickname +
   YOU/PARTNER tag inline right of the avatar; COOL/CURSE/SYN pinned
   right via scale-down FittedBox.
2. **Avatar idle life** ✅ — `FramedAvatar(idle: true)` wraps portraits
   in a 4s breathing/sway/bob loop, phase-offset per avatar id,
   reduced-motion safe. Enabled on run panel, player tab header,
   lobby, connect.
3. **Connect handshake + splash** ✅ — `MpConnectScreen` connected
   state is now a VS splash (108sf portraits, pulsing VS medallion,
   drifting player-color glows). Fresh pairings: host taps READY →
   `session.sendStartRun()` fires the existing `MpStartRun` wire
   message; sidekick enters via `onStartRun` callback; both run timers
   arm on receipt (`_startRunTimer` wired into both onStartRun paths).
   Reconnects/restores/demo skip the gate and auto-enter, followed by
   an ENTERING THE GUNGEON beat. Protocol-safe — no wire changes.

---

## 4. Session plan

| # | Session | Scope | Files (primary) | Verify |
|---|---------|-------|-----------------|--------|
| S1 | **Particles final form** | Finish C: ItemIconField path refactor, overlay branch, LOOKS row, sprite picker sheet, mutual-exclusion taps, tests | `particle_engine.dart`, `theme_overlay.dart`, `studio_particles.dart`, `experience_studio_screen.dart`, `experience_studio_test.dart` | analyze + studio tests |
| S2 | **Color favorites + role mocks** | D: 6-slot favorites persistence/UI, `_RoleMock` per role, panel-chrome live mock | `studio_flow.dart` (palette sheet), `experience_studio_screen.dart` (color rows), `theme_flair_prefs.dart` or new small store for favorites | analyze + tests (slot persistence, stable indices) |
| S3 | **Wallpaper immersion** | E: pref + toggle + zoom/parallax in `CustomWallpaper`, reduced-motion path | `theme_flair_prefs.dart`, `custom_wallpaper.dart`, `studio_ambiance.dart` | analyze; manual tilt check |
| S4 | **MP name layout + avatar idle** | F1+F2: name-beside-avatar panel, avatar idle wrapper | `paradox_player_panel.dart`, `avatar_frame.dart`/new `avatar_idle.dart`, maybe `gungeoneer_header.dart` | analyze + widget test for layout |
| S5 | **MP connect splash + handshake** | F3: handshake state in MpSession, splash route, lobby confirm UX | `mp_session.dart`, `mp_lobby`/`mp_connect` screens, new `connect_splash.dart` | analyze + MP protocol tests must stay green |
| S6 | **Masterplan verify + docs** | Full analyze + `flutter test`, bug-list updates, changelog.json + VERSION_HISTORY entries, AGENT_STATUS release | docs, tests | full suite green |
| S7 | **(optional) LIVE LOOK mini-slice** | Interactive elements inside the studio's small preview pane if wanted after S1–S3 | `experience_studio_screen.dart` | — |

Ordering rationale: S1–S3 are self-contained studio work (this slot's
current lane). S4–S5 touch MP surfaces — check `AGENT_STATUS.md` for
slot conflicts before starting; S5 is the riskiest (session state +
UI timing) and benefits from being alone on the tree.

---

## 5. Risks / open questions

- **Sprite picker coverage**: every JSON name → slugged `.webp`
  assumed present (239 guns / 270 items match asset counts). Missing
  files degrade to `errorBuilder` fallback — acceptable, but a
  verification pass (`tools/` script) could confirm 1:1.
- **Parallax sensors**: `sensors_plus` may not be a dependency —
  check pubspec; fallback is `DeviceOrientation`/manual drag-tilt or
  skip parallax, keep zoom. Decide in S3.
- **Handshake semantics**: "confirm connect" is UI-side unless we add
  a wire ack — keep it session-local first (lobby → splash → run)
  unless user wants protocol change.
- **Neo-Skeuo toggle inside preview** mutates global `AppTheme` state
  (not staged) — known edge, acceptable; document.
- **Preset schema**: new prefs auto-flow into saved presets via
  `VisualPrefs.toJson` — old presets load with defaults (verified
  pattern). No migration needed.
