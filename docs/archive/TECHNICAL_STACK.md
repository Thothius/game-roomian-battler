# GungeonMate - Technical Stack Specification (v1.9.62)

> **See also:** `docs/TECHNICAL_REFERENCE.md` — the canonical technical reference for all agents (git auth, build commands, platform quirks, release checklist).

This document outlines the software engineering architecture, state-management topologies, local storage strategies, and real-time networking protocols driving GungeonMate.

---

## 🛠️ 1. Core Platform & Framework Stack

* **Cross-Platform Engine:** Flutter SDK (`Dart 3.7.0+` / `Flutter 3.22+` compatible).
* **Target Platforms:** Android (`minSdkVersion 21`, `targetSdkVersion 34`), iOS (`iOS 12.0+`), and Windows Native Desktop (x64 runner).
* **UI Paradigms:** Highly reactive Material 3 base layer, customized with deep-space dark containers (`#1E1E22`) and high-contrast neon tier highlights.

---

## 🧭 2. State Management Topology

GungeonMate implements a **Root-Level MultiProvider** structure, declaring core state streams at the application entry point (`main.dart`):

```
                       [ MultiProvider (Root) ]
                       ├── ChangeNotifierProvider<RunProvider>
                       └── ChangeNotifierProxyProvider<RunProvider, MultiplayerSession>
```

### Key Providers:
1. **`RunProvider`:**
   * Acts as the single-source-of-truth for active runs, character data lookup maps, user favorites, and special stats (Spice usage, sprun indices, robot armor counts).
   * Exposes raw models as read-only getters (`allGuns`, `allItems`) and emits reactive notification pulses on state mutations.
2. **`MultiplayerSession`:**
   * Utilizes `ChangeNotifierProxyProvider` to consume the active `RunProvider` stream.
   * Manages remote socket state, broadcast payloads, client/server sync schedules, and connection-restoration loops.

---

## 💾 3. Data Persistence & Double-Buffered Saving

GungeonMate is an **offline-first** application utilizing `SharedPreferences` for local disk persistence.

### Double-Buffered Save Routine:
To protect against database corruption during OS interrupts or sudden battery dropouts, active runs are persisted via an asynchronous, dual-buffered JSON serialization loop:

```
[State Mutation] ➔ [JSON Map Encode] ➔ [Thread Compute Isolate] ➔ [Write "current_run"]
                                                               └── [Backup to "current_run_backup"]
```

* **`current_run`:** Stores the active, primary serialized JSON string of `RunState`.
* **`current_run_backup`:** A secondary snapshot. If `_loadSavedRun()` throws a JSON decoding error upon startup, the app catches the exception, disk-reads the backup, and restores player states gracefully with zero data loss.
* **Favorite Registry:** Stars and favorites are saved separately into `favourites_v1` string arrays, ensuring a user's starred gear persists independently of active run resets.

---

## 🛰️ 4. Local Multi-Device Co-Op Protocol

Local co-op uses a **zero-payload peer-to-peer broadcast system** implemented inside `MultiplayerSession` and `MultiplayerService`:

* **Socket Networking:** Direct TCP/UDP packet broadcasts over local Wi-Fi or Bluetooth subnets.
* **Payload Serialization:** Run state maps (`main` player, `coop` player, current floor coolness, and floor curse) are serialized to JSON string streams on change.
* **State Reconstruction:** Client devices reconstruct state on-the-fly using `RunState.fromJson()` and trigger `restoreEntireRunState()` in their local provider, syncing inventory screens instantly across companion devices.

---

## 🎨 5. Graphics, Particles & Animation Engine

All custom animations are written in **pure Dart / Flutter canvas layers**, removing the performance overhead of external raster assets:

1. **The Visual Theme Engines (`theme_engines.dart`):**
   * **Drip Engine:** Simulates viscous particle gravity vectors.
   * **Sheen Engine:** Rotates a linear gradient clipping matrix over static headers.
   * **Wobble Engine:** Performs spatial sine/cosine offsets to animate text matrices.
   * **Sequencer Engine:** Rotates a hue-shift matrix dynamically over color coordinates.
2. **Canvas Poof Explosion (`_PoofParticles`):**
   * Uses a custom `AnimationController` and `CustomPainter` to draw 10 trigonometric smoke plumes expanding radially from center:
     $$\text{x} = C + \cos(\theta) \cdot d$$
     $$\text{y} = C + \sin(\theta) \cdot d$$
   * Fades out opacity and scales radius dynamically to construct a crisp, frame-rate independent pixel smoke effect.
3. **Animated Easter Eggs (`_CuriousCatStareWidget`):**
   * Uses an `AnimatedBuilder` to slide the cat sprite across horizontal screen bezel bounds, rotating the layout via custom sinewave offsets:
     $$\text{angle} = \sin(\text{time} \cdot 0.005) \cdot 0.04\text{ rad}$$
     This creates a continuous, life-like curious head wiggle while the cat is on-screen.

---

## 📳 6. Tactile Haptic Framework

Haptics are decoupled from native system defaults and wrapped inside `@/lib/services/haptics.dart` using `HapticFeedback`:
* **`Haptics.light()`:** Triggers quick, micro-vibrations for animated slider snaps and typewriter clicks.
* **`Haptics.selection()`:** Soft feedback for tapping buttons and player avatar portraits.
* **`Haptics.success()`:** Satisfying double-pulse vibration for completing quests, unlocking shop discounts, and acquiring secret curios.

---

## 🎬 7. Video Playback & Animated Wallpapers

The home screen features an animated vortex portal wallpaper (`gungeonmate-animation-02.mp4`) played via the standard `video_player` API:

* **`video_player` (`^2.9.2`):** The core Flutter video API. Backends exist for Android, iOS, macOS, and Web.
* **`video_player_media_kit` (`^2.0.0`):** Drop-in libmpv backend for Windows and Linux. Initialized via `VideoPlayerMediaKit.ensureInitialized(windows: true)` in `main.dart` before `runApp`. No API changes — existing `VideoPlayerController.asset()` calls just work.
* **`AnimatedWallpaperBackground` (`lib/widgets/backgrounds/animated_wallpaper.dart`):** Stateful widget that initializes the video, loops it muted, and falls back to a `_VortexFallbackPainter` (CustomPaint rotating purple rings) if video init fails on any platform.
* **Theme overlay integration:** The wallpaper sits at layer 0.4 in `ThemeOverlay`, always mounted (keeps the video controller warm), visible at 85% opacity when on the home screen.

---

## 🎨 8. Active Run Display Modes (v1.9.62)

The active run screen supports 4 switchable display modes via `RunDisplayMode` enum:

| Mode | Widget | Description |
|------|--------|-------------|
| Classic Scroll | (default PlayerPage scroll) | The original full scroll view. Default. |
| Codex Book | `CodexBookMode` | Leather-and-brass two-page book spread with character locket, interactive GungeonMeters, swipeable gun/item pages. |
| Compact Run | `CompactRunMode` | Tactical HUD — top stat strip, 2-column grid, overflow sheet, gold top-DPS accent bar. |
| Theme Signature | `ThemeSignatureMode` | Adapts entire layout to active theme — lore header, themed stat labels, 14 decorative background painters (embers, frost, sparkles, circuits, paws, moonlight, lightning, etc.). |

**Note:** Matrix mode was removed in v1.9.62. `matrix_mode.dart` and `gungeon_matrix_rain.dart` deleted.

**Switching:** `RunDisplayModeBar` (collapsible pill between header and PageView). Modes apply instantly via `VisualPrefs.setRunDisplayMode()`. No navigation.

**Theme Lore Registry:** `lib/widgets/active_run/modes/theme_lore.dart` — 14 entries (one per visible theme) with lore title, tagline, Gungeon quote, element, decorative style, themed stat labels, and accent glyph.

---

## 📊 9. Interactive GungeonMeter (v1.9.56+)

Custom-painted horizontal fill bar for coolness/curse stats:

* **`GungeonMeter` (`lib/widgets/active_run/gungeon_meter.dart`):** Animated gradient fill (cyan for coolness, oxblood-red for curse). Threshold tick at 10.0. Tap or drag to adjust. Overflow state at curse ≥ 10: pulsing red glow + skull icon + Lord of the Jammed alert. Haptic feedback on threshold cross. `RepaintBoundary` isolated.
* **Threshold:** 10.0 = Lord of the Jammed (curse) / max effective coolness. Provider clamps to -100..100. Visual range 0..15.
* **Locations:** Stats detail screen, Codex Book left page, Theme Signature mode.
