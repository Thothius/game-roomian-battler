# GungeonMate - Technical Architecture & Core Subsystems Summary

GungeonMate is a high-performance, dark-neon companion application for the roguelike game *Enter the Gungeon*. Built with Flutter and Dart, it provides utility calculators, minigame simulators, and interactive branching narrative systems.

---

## 1. System Technology Stack & Core Layers

* **Frontend Framework:** Flutter (Dart) targeting native mobile devices (iOS & Android).
* **State Management:** `ChangeNotifier` with `Provider` for reactive, high-frequency widget rebuild loops.
* **Persistent Storage:** `SharedPreferences` for user custom settings (visual preferences, haptics, quest progression, first encounters).
* **Tactile Feedback:** Low-latency system haptics wrapper (`Haptics`) gating vibration intensity (`off`, `light`, `full`) mapped to tap, selection, success, and warning levels.
* **Visual Engine:** Pure code-driven vector drawings (`CustomPainter`), low-level image codec frame decoders (`ui.instantiateImageCodec`), and high-performance layout slivers preventing squishing.

---

## 2. The Visual & Overlay Subsystem (`ThemeOverlay`)

The app's visual aesthetic relies on a dark-neon space container theme, loaded with dynamic backdrops rendered behind page content routes via a global nested Stack.

### A. Dynamic Ambient Particles
* Renders floating wind motes matching current Gungeon loot-tier themes (Fire Embers, Glacial Frost, Catpaws, Jammed Curses).
* Configurable count, size, opacity, and rotation speed mapped to reactive `VisualPrefs` sliders.

### B. Dynamic Hypnotic Backdrops (Trippy Options)
* Fully replaces the normal particles with full-screen animated GIF backdrops.
* **Low-Level Codec Player (`_HypnoticBg`):** Reads GIF bytes directly from assets (`assets/animations/trippy/`), uses `ui.instantiateImageCodec` to parse individual frame arrays and specific millisecond delays, and caches raw images in RAM.
* **Animation Speed Controls:** Speeds up or slows down playback durations (50% steps, e.g., 0.1x to 4.0x) and applies smooth opacity layers mapped to an experimental visual slider.

---

## 3. NPC Dialogue System (Planned — Not Implemented)

> **Status:** Architecture designed in `docs/npc_view_plan.md`. No code exists yet.
> Previously referenced `animated_chat_bubble.dart`, `vertical_swipe_layout.dart`, `npc_view_screen.dart`, `npc_dialogue.dart`, and `npc_dialogues.json` — all deleted or never created.

The planned system would include:
- Branching dialogue with Gungeon NPCs (Bello, Winchester, etc.)
- Typewriter-style text rendering with haptic feedback
- NPC utility dashboards (price calculators, spawn chances, quest trackers)
- See `docs/npc_view_plan.md` for the full specification.

---

## 4. Codebase File Matrix

* `lib/widgets/theme_overlay.dart` - Global visual route overlay, ambient particle layers, and the low-level custom animated `_HypnoticBg` player.
* `lib/screens/theme_picker_screen.dart` - Theme and custom particles customization options panel, including Hypnotic Backdrop toggles, speed buttons, and opacity slider.
* `lib/screens/codex_screen.dart` - Codex encyclopedia: enemies, bosses, NPCs, objects, pickups browser.
* `lib/screens/active_run_screen.dart` - Central run dashboard with inventory, dashboards, and multiplayer.
* `lib/screens/settings_screen.dart` - Theme, font, and run utility configuration.
