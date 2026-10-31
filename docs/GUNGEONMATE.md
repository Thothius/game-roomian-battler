# GungeonMate — The Definitive Reference

> **One doc to rule them all.** App infrastructure, tech stack, features, every view, every option.
> Last updated: 2026-10-31 (v3.3.0+162) — see **v3.x delta** in `TECHNICAL_REFERENCE.md` §0: unified MP `mp.v2`, 3-tab nav + gear sheet, Ammonomicon rename, item-detail wiki/back-refs surfacing. Feature descriptions below are v2-era; where they conflict with the delta, the delta wins.
>
> **Companion docs:**
> - `TECHNICAL_REFERENCE.md` — agent operations (git, build commands, release checklist, PowerShell gotchas)
> - `REWORK_LESSONS_LEARNED.md` — design standards, mistakes to avoid, verification checklist
> - `USER_BUG_LIST.md` — active user-reported bug tracker
> - `docs/archive/` — historical assessments, plans, and audits (completed work)

---

## 1. What Is GungeonMate

A high-performance, dark-neon companion app for *Enter the Gungeon*. Built in Flutter/Dart. Tracks runs, inventory, synergies, stats. Multiplayer co-op via Nearby Connections. Customizable themes, particles, fonts, shaders.

**Current version:** 3.3.0+162
**Target platforms:** Android (primary), Windows (desktop), iOS (builds but not actively tested)
**Flutter SDK:** 3.47.9 stable / Dart 3.13.7

---

## 2. Tech Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| **Framework** | Flutter 3.29.0 | Material 3 base, heavily customized |
| **Language** | Dart 3.7.0+ | Null-safe, modern |
| **State management** | `provider` ^6.1.1 | `ChangeNotifier` + `MultiProvider` at root |
| **Persistence** | `shared_preferences` | Double-buffered JSON for run state |
| **Multiplayer transport** | `nearby_connections` ^4.2.0 (resolved 4.3.0) | Bluetooth + Wi-Fi Direct, no internet |
| **Fonts** | `google_fonts` ^6.2.1 | 68 fonts, 9 categories |
| **Video** | `video_player` ^2.9.2 + `video_player_media_kit` ^2.0.0 | libmpv backend for Windows |
| **Shaders** | Flutter Fragment shaders | GLSL `.frag` programs, GPU-composited |
| **CI/CD** | GitHub Actions | 3 jobs: analyze, test, build APK |

### Root provider tree

```
MultiProvider (root)
├── ChangeNotifierProvider<RunProvider>        — run state, character data, favorites
└── ChangeNotifierProxyProvider<RunProvider, MpSession>  — MP lifecycle, depends on RunProvider
```

### Persistence model

- **`current_run`** — primary serialized RunState (JSON string)
- **`current_run_backup`** — backup snapshot; if primary corrupts, backup restores
- **`favourites_v1`** — starred guns/items (independent of run state)
- **`vp.*` keys** — VisualPrefs fields (one per user preference)
- **`haptics.intensity`** — haptic feedback level
- **MP keys** — `mp.session.*` for active session, cleaned up on v2.0.3 launch

---

## 3. App Architecture

### Directory structure

```
gungeon_mate/
├── lib/
│   ├── main.dart                    — entry point, provider tree, lifecycle observer
│   ├── providers/
│   │   └── run_provider.dart        — single source of truth for run state
│   ├── services/
│   │   ├── app_theme.dart           — themes, VisualPrefs, fonts, shaders (3500+ lines)
│   │   ├── haptics.dart             — tactile feedback wrapper
│   │   ├── goop_talk_engine.dart    — Goopian language scrambler + GoopText widget
│   │   ├── damage_calculator.dart   — DPS math
│   │   ├── effect_tagger.dart       — passive effect extraction
│   │   ├── elemental_tagger.dart    — elemental tagging
│   │   ├── home_customization.dart  — home screen layout prefs
│   │   ├── mp_session.dart          — MP lifecycle facade
│   │   ├── paired_partners_store.dart — nickname persistence only
│   │   └── mp/
│   │       ├── mp_link.dart         — Nearby Connections transport
│   │       ├── mp_sync.dart         — handshake, snapshots, gifts, dice, shared state
│   │       ├── mp_recovery.dart     — reconnect + app-kill restore
│   │       └── mp_store.dart        — MP session persistence
│   ├── models/
│   │   ├── run_state.dart           — RunState (main + coop + shared state)
│   │   ├── player.dart              — Player (character + guns + items)
│   │   ├── gungeoneer.dart          — Character definition
│   │   ├── gun.dart / item.dart     — Gear models
│   │   ├── synergy.dart             — Synergy definitions
│   │   ├── shrine.dart              — Shrine definitions
│   │   ├── multiplayer_messages.dart — 17 wire message types
│   │   ├── codex_entry.dart         — Bestiary/lore entries
│   │   ├── rich_text.dart           — Rich text parser for wiki links
│   │   └── run_log_entry.dart       — Event log entries
│   ├── screens/                     — 25 screens (see §4)
│   ├── widgets/                     — 11 widget subdirectories (see §5)
│   └── utils/
│       ├── asset_paths.dart         — asset path helpers + kAppVersion
│       ├── responsive.dart          — screen-size scaling
│       ├── format.dart              — number/text formatting
│       └── fast_route.dart          — route transition helper
├── assets/
│   ├── data/                        — JSON data (guns, items, synergies, changelog)
│   └── images/themes/splash/        — 14 theme splash JPGs
├── test/                            — 105 tests (see §7)
├── .github/workflows/ci.yml         — GitHub Actions CI
└── pubspec.yaml
```

### Key design principles

1. **Offline-first** — no server, no cloud. All data local.
2. **Provider-only state** — no BLoC, no Riverpod. `ChangeNotifier` everywhere.
3. **Pure-Dart graphics** — CustomPainter, no Lottie, no Rive. Shaders are GLSL.
4. **Dark neon aesthetic** — `#0D1117` / `#1E1E22` scaffolds, neon tier highlights.
5. **Main-authoritative MP** — host owns shared state; joiner sends deltas.

---

## 4. Every Screen

### 4.1 Home & Navigation

| Screen | File | Purpose |
|--------|------|---------|
| **HomeScreen** | `home_screen.dart` | Routes to MainMenu (no run) or ActiveRunScreen (active run). Tabbed: Run / Browse / Settings |
| **MainMenuScreen** | `main_menu_screen.dart` | New run gateway. Character select panel, changelog dialog, version info |
| **CharacterSelectScreen** | `character_select_screen.dart` | Sliding roster of 8 Gungeoneers with starting gear and stats |

### 4.2 Active Run

| Screen | File | Purpose |
|--------|------|---------|
| **ActiveRunScreen** | `active_run_screen.dart` | Central run dashboard. Player slot switcher (Main/Coop), inventory lists, stat capsules, passive effects, dashboards |
| **StatsDetailScreen** | `stats_detail_screen.dart` | Detailed coolness/curse breakdown with GungeonMeter, run log |
| **EffectsSummaryScreen** | `effects_summary_screen.dart` | Aggregated passive effects view |
| **ShrinePickerScreen** | `shrine_picker_screen.dart` | Shrine tracker — tap shrines used during the run |

### 4.3 Browse / Encyclopedia

| Screen | File | Purpose |
|--------|------|---------|
| **BrowseScreen** | `browse_screen.dart` | Searchable offline encyclopedia of every gun, item, synergy, shrine. Omni-search, quality filters, synergy pills |
| **ItemDetailScreen** | `item_detail_screen.dart` | Per-item detail with stats, synergies, wiki description, destroy banner |
| **GunDetailScreen** | (via item_detail) | Per-gun detail with stats, synergies |
| **SynergiesOverviewScreen** | `synergies_overview_screen.dart` | All synergies list |
| **AllSynergiesScreen** | `all_synergies_screen.dart` | Full synergy browser |
| **GungeoneerDetailScreen** | `gungeoneer_detail_screen.dart` | Character detail with starting loadout, lore, stats |
| **CodexScreen** | `codex_screen.dart` | Bestiary: enemies, bosses, NPCs, objects, pickups |
| **CodexDetailScreen** | `codex_detail_screen.dart` | Per-entry codex detail |
| **FavouritesScreen** | `favourites_screen.dart` | Starred guns/items |

#### Codex variants (specialized bestiary tabs)

| Screen | File | Purpose |
|--------|------|---------|
| **BulletHellCodexScreen** | `bullet_hell_codex_screen.dart` | Bullet Hell bestiary |
| **ChallengeModeCodexScreen** | `challenge_mode_codex_screen.dart` | Challenge mode entries |
| **DrakeCodexScreen** | `drake_codex_screen.dart` | Drake entries |
| **GunslingerCodexScreen** | `gunslinger_codex_screen.dart` | Gunslinger entries |
| **ParadoxCodexScreen** | `paradox_codex_screen.dart` | Paradox entries |
| **RatCodexScreen** | `rat_codex_screen.dart` | Resourceful Rat entries |

### 4.4 Multiplayer

| Screen | File | Purpose |
|--------|------|---------|
| **MpLobbyScreen** | `mp_lobby_screen.dart` | Host/Join entry. Nickname field, 4-digit PIN field, HOST button, CONNECT button, How to Play modal |
| **MpConnectScreen** | `mp_connect_screen.dart` | Connecting/connected/error/reconnecting view. Status messages, pulsing animation, error with Bluetooth/Wi-Fi tip + RETRY |

### 4.5 Settings & Customization

| Screen | File | Purpose |
|--------|------|---------|
| **SettingsScreen** | `settings_screen.dart` | 2-tab layout: Appearance + Settings |
| **ExperienceStudioScreen** | `experience_studio_screen.dart` | Theme picker + customization. 4-tab picker (Theme/Particles/Typography/Ambiance) with fullscreen preview |

---

## 5. Widget Library

### 5.1 Root widgets

| Widget | File | Purpose |
|--------|------|---------|
| **ThemeOverlay** | `theme_overlay.dart` | Global visual stack — 12-layer composited overlay (see §6) |
| **GoopText** | `goop_talk_engine.dart` | Animated text with Goopian language scramble |
| **GlassContainer** | `glass_container.dart` | Frosted glass panel |
| **QualityBadge** | `quality_badge.dart` | S/A/B/C/D tier badge |
| **ScaleButton** | `scale_button.dart` | Tactile scale-on-tap button |
| **SynergyGlow** | `synergy_glow.dart` | Glowing synergy indicator |
| **ThemedNumber** | `themed_number.dart` | Theme-aware number display |
| **ThemedSectionTitle** | `themed_section_title.dart` | Theme-aware section header |
| **GameIcon** | `game_icon.dart` | Game asset icon loader |
| **AvatarAura** | `avatar_aura.dart` | Animated avatar aura (17 styles) |
| **RichLinkText** | `rich_link_text.dart` | Wiki-style hyperlinked text |
| **SpoilerTag** | `spoiler_tag.dart` | Spoiler warning tag |
| **PeriodicTile** | `periodic_tile.dart` | Periodic-table-style inventory tile |

### 5.2 Active Run widgets (`widgets/active_run/`)

| Widget | File | Purpose |
|--------|------|---------|
| **PlayerHeader** | `player_header.dart` | Character portrait, stats, coolness/curse capsules |
| **PlayerPage** | `player_page.dart` | Per-player scrollable page with inventory |
| **GungeonMeter** | `gungeon_meter.dart` | Interactive coolness/curse fill bar |
| **SummaryTab** | `summary_tab.dart` | Run summary tab |
| **DiceRoll** | `dice_roll.dart` | MP dice roll animation |
| **EmoteAnimations** | `emote_animations.dart` | MP emote animations (kiss, slap, etc.) |
| **EndRunConfirmDialog** | `end_run_confirm_dialog.dart` | End run confirmation |
| **SortPicker** | `sort_picker.dart` | Inventory sort options |
| **StarterHint** | `starter_hint.dart` | New-run hint card |
| **StatSheets** | `stat_sheets.dart` | Detailed stat breakdown sheets |

### 5.3 Backgrounds (`widgets/backgrounds/`)

| Widget | File | Purpose |
|--------|------|---------|
| **AnimatedWallpaperBackground** | `animated_wallpaper.dart` | MP4 video wallpaper (vortex portal) + fallback painter |
| **AmbientShader** | `ambient_shader.dart` | GLSL fragment shader layer (digital rain, dark neon fog) |
| **GungeonFallAnimation** | `gungeon_fall_animation.dart` | Gungeon fall animation |
| **PageFrame** | `page_frame.dart` | Decorative page border frame |

### 5.4 Particles (`widgets/particles/`)

| Widget | File | Purpose |
|--------|------|---------|
| **AmbientGlow** | `ambient_glow.dart` | Screen-edge ambient glow |
| **CrimsonDrip** | `crimson_drip.dart` | Curse-themed red drip |
| **CurseBreath** | `curse_breath.dart` | Curse breathing effect |
| **CurseFog** | `curse_fog.dart` | Curse fog overlay |
| **TouchParticle** | `touch_particle.dart` | Touch-spawned sparkle particles |

### 5.5 Other widget groups

| Directory | Key widgets |
|-----------|-------------|
| `widgets/browse/` | BrowsePills, BrowseRow, AnyEntry, ToolbarButton |
| `widgets/codex/` | AmmonomiconTabs |
| `widgets/dashboards/` | CompactDashboards, DashboardSwiper, HuntressDashboard, JunkanDashboard, RobotDashboard, SpecialGunDashboards |
| `widgets/easter_eggs/` | CatThrone (Cat Bullet King peek animation) |
| `widgets/home/` | HomeCustomizationSheet, JunkParticleField, RotatingGungeoneer, VortexConfig, VortexLightning |
| `widgets/item_detail/` | DestroyBanner, GunStats, Header, ItemBody, QuickJumpButton, SynergiesSection |
| `widgets/settings/` | ThemeVisualsTab, SettingsTab, DebugTab, RunLogScreen, SwipePicker |
| `widgets/sheets/` | DamageCalcSheet |

---

## 6. The Visual System (Themes, Particles, Layers)

This is the most complex subsystem. A full assessment of whether it needs a formal framework is in §9.

### 6.1 Theme System

**32 enum values** in `AppThemeMode`, **15 visible** in `kVisibleThemes`:

| # | Theme | Vibe | Element | Particle Default |
|---|-------|------|---------|-----------------|
| 1 | Minimalist | Clean | Neutral | gungeonDust |
| 2 | Unicorn | Magical | Rainbow | unicornSparkles |
| 3 | Forge Master | Industrial | Fire | forgeEmbers |
| 4 | Robot's Core | Tech | Electric | cosmicStars |
| 5 | Cat Lady | Whimsical | Cat | catPaws |
| 6 | Moonlit Chamber | Serene | Moon | moonlitShards |
| 7 | Storm Caller | Electric | Lightning | lightningSparks |
| 8 | Mr. Robot | Tech | Electric | cosmicStars |
| 9 | Valor of Marines | Military | Neutral | gungeonDust |
| 10 | The Bullet | Lore | Neutral | cosmicDust |
| 11 | The Paradox | Cosmic | Void | voidRift |
| 12 | Gunpowder | Industrial | Fire | forgeEmbers |
| 13 | Dragunfire | Epic | Fire | fireflies |
| 14 | Lich's Domain | Dark | Curse | cursedSkulls |
| 15 | Custom | User-defined | User-defined | gungeonDust |

**17 hidden themes** (legacy/lore, not user-selectable): ammonomicon, hollowChill, lordJammed, theBreach, bulletHell, resourcefulRat, gungeonProper, theOubliette, pastParadox, highPriestVoid, cultOfGundead, synergySurge, glitchedChest, lichsTomb, winchestersGame, unicornII/III/IV.

**Unicorn palettes:** 6 switchable sub-palettes for the Unicorn theme: Cotton Candy, Neon, Dreamy, Sunset, Bubblegum, Mulberry.

**Theme remixes:** Each theme has 1-4 remix variants (intensity levels). `AppTheme.remixNotifier` tracks the active remix index.

### 6.2 ThemeFlair (per-theme design tokens)

Each theme defines a `ThemeFlair` — essentially a CSS-like design token object:

| Token | Type | Purpose |
|-------|------|---------|
| `scaffold` | Color | Background base |
| `card` | Color | Card/panel background |
| `primary` | Color | Primary accent |
| `secondary` | Color | Secondary accent |
| `headlineStat` | Color | Stat highlight color |
| `bulletColor` | Color | List bullet color |
| `bulletGlyph` | String | Bullet character |
| `twinkleBullets` | bool | Animated bullet twinkle |
| `sparkleNumbers` | bool | Number sparkle effect |
| `numberGlowColor` | Color | Number glow |
| `tabularFigures` | bool | Monospace numbers |
| `numberSizeScale` | double | Number size multiplier |
| `numberWeight` | FontWeight | Number weight |
| `numberStyle` | FontStyle | Number style |
| `chipRadius` | double | Chip corner radius |
| `cardRadius` | double | Card corner radius |
| `dividerColor` | Color | Divider color |
| `dividerThickness` | double | Divider thickness |
| `glowPrimary` | Color | Primary glow |
| `glowSecondary` | Color | Secondary glow |
| `auraStyle` | AvatarAuraStyle | Avatar aura style (17 options) |
| `headerGlyph` | String | Header icon character |
| `headerUnderlineColor` | Color | Header underline |
| `statGroupCombat` | Color | Combat stat group color |
| `statGroupHandling` | Color | Handling stat group color |
| `statGroupMeta` | Color | Meta stat group color |
| `font` | AppFont | Theme's default font |
| `pageFrame` | bool | Show decorative page frame |

### 6.3 VisualPrefs (32 user-adjustable fields)

All persisted to SharedPreferences with `vp.*` keys:

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `glowIntensity` | double | 0.0 | Background glow intensity (0-1) |
| `particlesEnabled` | bool | false | Particle system on/off |
| `particlePreset` | ParticlePreset | gungeonDust | 37 presets (see §6.4) |
| `particleGlowEffect` | GlowEffect | none | 12 glow effects |
| `particleLineLinks` | bool | false | Connect nearby particles with lines |
| `particleBounce` | bool | false | Bounce off edges vs wrap |
| `glowColorIndex` | int | 0 | 12-color glow palette |
| `fontWeightBias` | int | 0 | Global font weight bias (-400 to +500) |
| `font` | AppFont | gungeon | 68 fonts (see §6.5) |
| `fontSize` | double | 14.0 | Base font size |
| `inventoryFontSize` | double | 14.0 | Inventory tile font size |
| `inventoryDisplayMode` | InventoryDisplayMode | list | Grid/list display |
| `customDiceType` | CustomDiceType | default | Dice visual style |
| `particleSizeScale` | double | 1.0 | Particle size multiplier |
| `particleOpacity` | double | 1.0 | Particle opacity |
| `particleCount` | int | 50 | Particle count |
| `dialogueHapticsEnabled` | bool | true | Haptics on dialogue |
| `dialogueTextSpeedMs` | int | 30 | Text speed |
| `isGoopianLanguage` | bool | false | Goopian language mode |
| `spongeActive` | bool | false | Sponge translation animation |
| `showEffectsPanel` | bool | true | Effects panel on run screen |
| `showShrinePanel` | bool | true | Shrine panel on run screen |
| `showDashboards` | bool | true | Special dashboards on run screen |
| `periodicGridColumnCount` | int | 0 | Periodic grid columns (0=auto, 2-4) |
| `particleColorSchema` | ParticleColorSchema | default | Particle color override |
| `particleSpeed` | ParticleSpeed | normal | 5 speed presets |
| `shaderEnabled` | bool | false | GLSL fragment shaders on/off |
| `shaderPreset` | ShaderPreset | digitalRain | Shader preset (2 options) |

### 6.4 Particle System

**37 presets** in `ParticlePreset` enum (`particle_engine.dart`):

gungeonDust, unicornSparkles, forgeEmbers, frostShards, jamHexes, cosmicDust, cosmicStars, bulletHell, goldenSparkle, cursedSmoke, voidRift, cursedSkulls, rainbowConfetti, catPaws, moonlitShards, lightningSparks, fireflies, snowflakes, cherryBlossoms, autumnLeaves, rainDrops, bubbles, steam, ash, embers, sparkles, stars, hearts, skulls, gears, hexagons, diamonds, souls, fire, ice, lightning

**12 glow effects** in `GlowEffect` enum:

none, softPulse, hardPulse, rainbow, fire, ice, electric, poison, shadow, holy, cosmic, cursed

**5 speed presets** in `ParticleSpeed`:

slow, relaxed, normal, brisk, fast

**16 color schemas** in `ParticleColorSchema`:

default, fire, ice, electric, poison, rainbow, monochrome, pastel, neon, earth, cosmic, shadow, holy, cursed, sunset, ocean

**Note:** Only 17 of 37 presets are user-selectable in the picker. The other 20 are auto-bound to themes via `kThemeParticleDefaults` but can't be manually chosen. (See `CUSTOMIZATION_AUDIT_2026.md` §0.)

### 6.5 Font System

**68 fonts** in `AppFont` enum, organized into **9 categories** in Experience Studio:

| Category | Count | Examples |
|----------|-------|---------|
| Featured (locked) | 2 | gungeon, megrim |
| Pixel & Retro | 8 | pressStart2p, silkscreen, vt323, pixelifySans |
| Sci-Fi & Tech | 11 | monoton, blackOpsOne, orbitron, shareTechMono |
| Display & Impact | 8 | archivoBlack, anton, rowdies, righteous |
| Casual & Fun | 10 | comicNeue, fredoka, sniglet, lemon |
| Clean & Modern | 7 | dmSans, outfit, syne, montserrat |
| Gothic & Fantasy | 9 | medievalSharp, cinzelDecorative, metalMania |
| Serif & Editorial | 6 | playfairDisplay, ebGaramond, merriweather |
| Handwritten & Script | 5 | architectsDaughter, rockSalt, lobster |

### 6.6 ThemeOverlay Layer Stack

The `ThemeOverlay` widget composites 12 layers in a `Stack`:

| Z-order | Layer | Visibility | Purpose |
|---------|-------|-----------|---------|
| 0 | Base solid color | Always | Scaffold background (`f.scaffold`) |
| 0.4 | Vortex video wallpaper | Home screen only (85% opacity) | MP4 portal animation, always mounted |
| 0.5 | Ambient fragment shader | If `shaderEnabled` | GLSL digital rain or dark neon fog |
| 0.6 | Home contrast backing | Home screen only | Black 35% scrim over vortex |
| 1a | Particle backdrop | If `particlesEnabled` | Theme-default or user-selected particles |
| 1b | Ambient glow | If glow intensity > 0 | Screen-edge color glow |
| 2 | **App content** | Always | The actual screen (routed by HomeScreen) |
| 3.5 | Chamber vignette | Always | Radial gradient shadow (depth effect) |
| 3.6 | Readability scrim | Home screen only | Linear gradient for text contrast |
| 3.7 | Page frame | If `f.pageFrame` | Decorative border frame |
| 4 | Edge drip | lordJammed theme only | Red curse drip from top edge |
| 5 | Touch particles | If particles + not home | Sparkles on touch |

### 6.7 Avatar Aura Styles

**17 styles** in `AvatarAuraStyle` enum — animated aura rings around character portraits:

none, softPulse, hardPulse, rainbow, fire, ice, electric, poison, shadow, holy, cosmic, cursed, pastelPulse, neonGlow, starburst, vortex, flame

### 6.8 Shaders

**2 GLSL fragment programs** in `assets/shaders/`:

| Shader | File | Effect |
|--------|------|--------|
| Digital Rain | `digital_rain.frag` | Purple Matrix-style falling glyph columns |
| Dark Neon Fog | `dark_neon_fog.frag` | 4-octave fBm noise fog, very low opacity |

GPU-composited via `FragmentProgram.fromAsset`, cached at class level. `Stopwatch`-driven `uTime` uniform. `AnimationController` for repaint ticks only. `RepaintBoundary` isolated.

### 6.9 GungeonMeter

Custom-painted horizontal fill bar for coolness/curse:
- Cyan gradient for coolness, oxblood-red for curse
- Threshold tick at 10.0 (Lord of the Jammed)
- Tap or drag to adjust
- Overflow state: pulsing red glow + skull icon
- Haptic feedback on threshold cross
- Provider clamps to [-100, 100], visual range 0-15

---

## 7. Multiplayer Architecture (v2.0.3)

### 7.1 Layered Design

```
┌─────────────────────────────────────────────────────┐
│                      UI Layer                        │
│  MpLobbyScreen · MpConnectScreen · MpReconnectBanner │
│  MpRequestListener (gifts/requests/dice/emotes)      │
└──────────────┬──────────────────────────────────────┘
               │ ChangeNotifier
┌──────────────▼──────────────────────────────────────┐
│                   MpSession                          │  ← thin facade
│  (the ONLY thing UI talks to)                        │
│  Owns: MpLink, MpSync, MpRecovery, MpStore           │
└───┬──────────┬──────────────┬───────────┬───────────┘
    │          │              │           │
┌───▼──┐  ┌───▼────┐  ┌──────▼─────┐  ┌──▼──────┐
│MpLink│  │MpSync  │  │MpRecovery  │  │MpStore  │
│      │  │        │  │            │  │         │
│trans-│  │state   │  │reconnect   │  │persist- │
│port  │  │sync    │  │+ app-kill  │  │ence     │
│layer │  │        │  │restore     │  │         │
└──────┘  └────────┘  └────────────┘  └─────────┘
```

### 7.2 Connection Flow

1. **Host:** Enter nickname → select character → tap HOST → auto-generated 4-digit PIN → starts advertising `nickname#PIN`
2. **Joiner:** Enter nickname → enter host's PIN → tap CONNECT → discovers endpoints → auto-connects to matching PIN
3. **Handshake:** Hello message validates role (main vs sidekick), PIN, protocol version (2), app version
4. **Snapshot exchange:** Both sides exchange character/loadout → `applyPeerSnapshot` routes to correct slot
5. **Connected:** Both devices show the active run. Host in main slot, joiner in coop slot.

### 7.3 Wire Protocol (17 message types)

| Message | Type string | Purpose |
|---------|------------|---------|
| `MpHello` | `hello` | Handshake: role, character, nickname, version, PIN |
| `MpSnapshot` | `snapshot` | Full player state: character, guns, items, coolness, curse, shrines |
| `MpGift` | `gift` | Send a gun/item to partner |
| `MpRequest` | `request` | Request a gun/item from partner |
| `MpRequestResp` | `requestResp` | Approve/deny a request |
| `MpEndRun` | `endRun` | End the run and tear down session |
| `MpPing` | `ping` | Heartbeat ping (timestamp) |
| `MpPong` | `pong` | Heartbeat pong (timestamp) |
| `MpDiceChallenge` | `diceChallenge` | Challenge partner to dice roll |
| `MpDiceAccept` | `diceAccept` | Accept dice challenge |
| `MpDiceDecline` | `diceDecline` | Decline dice challenge |
| `MpDiceCancel` | `diceCancel` | Cancel dice challenge |
| `MpDiceResult` | `diceResult` | Dice roll result (score + dice values) |
| `MpEmote` | `emote` | Emote (kiss, slap, etc.) |
| `MpSharedStateDelta` | `sharedStateDelta` | Signed coolness/curse delta + optional shrine name |

**Protocol version:** 2
**Service ID:** `com.saare.gungeon_mate.mp.v2`
**Heartbeat:** 5 seconds
**Reconnect cadence:** 5s on / 5s off (50% duty cycle)
**Connection timeout:** 45 seconds

### 7.4 Shared State Model (Main-authoritative)

- **Main (host)** owns shared state (coolness, curse, shrines)
- **Sidekick (joiner)** sends signed deltas → Main applies + rebroadcasts
- `RunProvider.applySharedStateFromPeer` — overwrites from Main snapshots
- `RunProvider.applySharedStateDelta` — adds deltas, clamps to [-100, 100], appends shrine names
- `RunProvider.applyPeerSnapshot` — routes peer data to opposite slot (host→coop, joiner→main)

### 7.5 Recovery

- **Transport loss:** Auto-reconnect with 50% duty cycle
- **App killed:** `MpStore` persists session → on next launch, `MpRecovery` restores
- **`MpEndRun` on cancel:** Peer tears down cleanly, no loops

---

## 8. Test Suite (105 tests)

| File | Tests | Coverage |
|------|-------|----------|
| `test/mp_flow_simulation_test.dart` | 11 | MP flow + `_runProvider` desync regression |
| `test/mp_message_test.dart` | 33 | Wire protocol round-trip + error handling |
| `test/mp_link_test.dart` | 20 | Transport logic, endpoint parsing, PIN matching |
| `test/run_provider_test.dart` | 24 | State management, shared state, restore, lifecycle |
| `test/widget/mp_lobby_screen_test.dart` | 10 | Lobby UI rendering + validation |
| `test/widget/mp_connect_screen_test.dart` | 7 | Connect screen states (connecting, error, restoring) |

**CI:** `.github/workflows/ci.yml` — 3 jobs (analyze, test, build APK) on every push/PR to `master` or `dev`.

---

## 9. Visual Framework Assessment

### The problem

The visual system has grown organically into a complex web of interdependent tokens:

- **32 VisualPrefs fields** controlling global state
- **37 particle presets** × **12 glow effects** × **16 color schemas** × **5 speeds** = **35,520 particle combinations**
- **15 themes** × **ThemeFlair** (25+ tokens) × **remixes** (1-4 per theme) = **60+ flair configurations**
- **12-layer composited overlay** with conditional visibility per theme/screen
- **68 fonts** × **font weight bias** (-400 to +500 in steps of 100) = **612 font configurations**
- **17 aura styles** × **2 shaders** = layered visual effects

Currently, all of this is managed by:
1. `ThemeFlair` — a flat data class with 25+ fields (no nesting, no categories)
2. `VisualPrefs` — a flat data class with 32 fields
3. `ThemeOverlay` — a 400-line `Stack` with inline conditionals
4. `kThemeParticleDefaults` — a hardcoded map binding themes to particles
5. No validation, no schema, no separation of concerns

### Do we need a formal framework?

**Short answer: Not a CSS engine, but yes a structured design-token system.**

The current approach works because one person (the user) is making all the decisions. But it's already at the edge of maintainability:

| Risk | Current state | Impact |
|------|--------------|--------|
| **Token drift** | ThemeFlair has 25+ flat fields, no validation | Adding a token means touching every theme |
| **Layer conflicts** | ThemeOverlay conditionals are inline | Hard to reason about z-order |
| **Particle preset lock-in** | 20 of 37 presets can't be user-selected | Dead variety |
| **No preview isolation** | Can't preview a theme without applying it globally | Slow iteration |
| **No composition** | Can't mix-and-match flair tokens across themes | Each theme is siloed |

### Recommendation: Design Token Registry (not a CSS engine)

A lightweight, Dart-native design token system — not a full CSS framework. The goal is to make the existing system **navigable, validated, and composable** without rewriting it.

**Proposed structure:**

```dart
// 1. Categorized tokens instead of flat class
class ThemeDesignTokens {
  final ColorTokens colors;      // scaffold, card, primary, secondary, headline, glow...
  final ShapeTokens shapes;      // chipRadius, cardRadius, dividerThickness...
  final TypographyTokens type;   // font, numberWeight, numberStyle, numberScale...
  final EffectTokens effects;    // auraStyle, pageFrame, twinkleBullets, sparkleNumbers...
  final StatGroupTokens stats;   // combat, handling, meta colors
}

// 2. Layer registry instead of inline conditionals
class OverlayLayerRegistry {
  static List<OverlayLayer> layersFor(AppThemeMode mode, VisualPrefs prefs, bool isHome) {
    return _registry.where((l) => l.visible(mode, prefs, isHome)).toList();
  }
}

// 3. Particle preset unlock — all 37 selectable
// User picks any preset for any theme. Theme defaults remain as suggestions.
```

**This is a refactor, not a rewrite.** The existing `ThemeFlair` becomes the data backing `ThemeDesignTokens`. The `ThemeOverlay` Stack becomes a layer registry. No user-facing changes — just internal structure.

**Priority: Medium.** Do this after the MP rework is stable. The visual system works today; it's just hard to extend. The MP system is the active fire.

---

## 10. What's Done, What's Next

### Done (v2.0.3, uncommitted)

- [x] MP rework: monolithic `MultiplayerSession` → layered `MpSession`/`MpLink`/`MpSync`/`MpRecovery`/`MpStore`
- [x] Critical bug fix: `_runProvider` desync (both players now see the run)
- [x] Pairing system removed (~600 lines dead code purged)
- [x] Auto-connect by PIN, Main-authoritative shared state
- [x] Connection timeout (45s), discovery race fix, heartbeat 5s
- [x] 105 tests passing (unit + widget)
- [x] CI/CD: GitHub Actions (analyze + test + build APK)
- [x] Docs reorganized, .gitignore cleaned

### Next priorities

1. **Commit and push** the v2.0.3 rework (both repos)
2. **Real-device MP testing** — two Android phones, verify:
   - Both see active run after connect
   - Correct host/coop slots
   - Inventory sync
   - Leave/end-run cleanup
   - Backgrounding, range loss, reconnect
3. **Theme system fixes** (from `THEME_UX_ASSESSMENT_2026.md`):
   - Fix `splashSlug` getter (blocks Experience Studio)
   - Remove `RunDisplayMode.matrix` enum value (blocks display mode switcher)
   - Delete orphaned `_PaletteStep` dead code
   - Unlock all 37 particle presets for user selection
4. **Design Token Registry** (from §9 above) — after MP is stable
5. **Integration tests** — emulator-driven end-to-end MP flow
6. **Golden tests** — visual regression for key screens
