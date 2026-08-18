# GungeonMate — 2026 Animation & Architecture Assessment

> Learned from curated Flutter/Dart library list + 2026 UI/UX trends.
> Assessed against GungeonMate's current codebase on 2026-08-18.

---

## 1. Current Stack Audit

### What GungeonMate already uses (good)
| Library | Version | Usage count | Verdict |
|---------|---------|-------------|---------|
| `provider` | ^6.1.1 | Core state mgmt | Staying — works well, no need to migrate |
| `flutter_animate` | ^4.5.0 | 55 call sites | Gold standard, already in place |
| `sensors_plus` | ^5.0.1 | 1 file (theme_overlay.dart) | Tilt physics — already have it |
| `google_fonts` | ^6.2.1 | Font system | Core to theme picker |
| `shared_preferences` | ^2.2.2 | VisualPrefs persistence | Fine for current scale |
| `video_player` | ^2.9.2 | Animated wallpapers | Already integrated |

### What GungeonMate does NOT use (assessed)
| Library | Verdict | Reasoning |
|---------|---------|-----------|
| `rive` | **Skip** | No .riv assets in pipeline; CustomPainter covers our vector needs |
| `lottie` | **Skip** | No After Effects assets; CustomPainter particles are lighter |
| `flutter_riverpod` | **Skip** | Provider works well at current scale; migration = high risk, low reward |
| `freezed` | **Maybe** | Could help with VisualPrefs/RunState copyWith, but adds build_runner dep |
| `go_router` | **Skip** | App uses Navigator.push pattern throughout; no deep-linking needs |
| `flutter_hooks` | **Skip** | Would require migrating 115 AnimationController sites; not worth it |
| `dio` | **Skip** | App is offline-first; no HTTP client needed |

### Animation infrastructure audit
| Pattern | Count | Status |
|---------|-------|--------|
| `AnimationController` (manual) | 115 | Heavy — many could be `TweenAnimationBuilder` |
| `flutter_animate` (declarative) | 55 | Good — gold standard, expand usage |
| `AnimatedContainer/Switcher/Size` | 47 | Good — implicit animations used well |
| `CustomPainter/CustomPaint` | 25 | Core — particle engine, vortex, auras |
| `RepaintBoundary` | **4 only** | **GAP** — should be 15-20 for perf-critical animations |
| `Transform.translate/scale/rotate` + `Opacity` | 25 | Good — GPU-composited properties |
| Spring physics (`Curves.spring`, `elasticOut`, `bounceOut`) | **0** | **GAP** — no spring physics anywhere |
| `FragmentShader` | 0 | Future — not needed yet, CustomPainter is sufficient |

---

## 2. Key Gaps Identified

### GAP 1: RepaintBoundary underuse (HIGH priority)
Only 4 `RepaintBoundary` wrappers for 25 CustomPainter instances and 115 AnimationControllers. This means animated regions may trigger full-tree repaints.

**Action:** Wrap all CustomPainter-based widgets (ParticleField, vortex, avatar aura, lightning) in RepaintBoundary. Target: 15-20 wrappers.

### GAP 2: No spring physics (MEDIUM priority)
Zero spring-physics curves. All animations use linear or ease curves. The app feels "flash-appear" rather than "organic rebound."

**Action:** Replace `Curves.easeOut` with `Curves.easeOutBack` or `Curves.fastOutSlowIn` for card/button entrances. Consider `SpringSimulation` for drag-release interactions.

### GAP 3: Manual AnimationController overuse (MEDIUM priority)
115 manual AnimationController instances. Many could be replaced with `TweenAnimationBuilder` (implicit) or `flutter_animate` (declarative), eliminating disposal boilerplate.

**Action:** Audit controllers — if a controller doesn't need to be paused/reversed/seeked, replace with implicit animation. Target: reduce to ~60-70 manual controllers.

### GAP 4: No kinetic numerical morphing (LOW priority)
Stat values (DPS, damage, ammo) hard-swap text instead of rolling/animating. The user's eye isn't drawn to state changes.

**Action:** Add an `AnimatedNumber` widget that rolls values on change (like an odometer). Use for DPS, damage, ammo, coolness, curse counters.

---

## 3. 2026 Trends Assessment

### A. Volumetric 2.5D Layering — **Already planned**
The Active Run rework (Slot 3, Design Specialist) includes DepthTile with Z-axis depth and parallax. This trend is being addressed.

### B. Spring-Physics & Inertial Dampening — **GAP (see above)**
No spring curves in the codebase. Should add for card/drawer/button interactions.

### C. Kinetic Numerical Morphing — **GAP (see above)**
No animated number rolling. Should add for stat displays.

### D. Ambient Atmospheric Shaders — **Already strong**
25 CustomPainter instances, 37 particle presets, 11 glow effects, vortex animation, lightning strikes. This is the app's strongest area. The particle engine is production-quality.

### E. GPU-Accelerated Opacity & Transforms — **Good**
25 Transform/Opacity usages. The codebase already follows this pattern well.

### F. FragmentShader — **Future, not now**
No GLSL shaders. CustomPainter is sufficient for current needs. FragmentShader would be over-engineering for a companion app. Revisit if we add CRT distortion or chromatic aberration effects.

---

## 4. Action Plan (Prioritized)

### Immediate (next session)
1. **RepaintBoundary audit** — wrap ParticleField, vortex, avatar aura, lightning in RepaintBoundary. Target: +12 wrappers.
2. **Spring curves** — replace `Curves.easeOut` with `Curves.easeOutBack` in card entrance animations (browse grid, dashboard pills, theme picker).

### Short-term (next week)
3. **AnimatedNumber widget** — create reusable odometer-style number roller for stat displays.
4. **AnimationController reduction** — audit 115 controllers, convert ~50 to implicit animations.

### Long-term (post-release)
5. **freezed evaluation** — assess for VisualPrefs/RunState immutability (adds build_runner).
6. **FragmentShader exploration** — only if we add CRT/aberration effects.

---

## 5. Patterns to Remember

### GPU-composited properties (always animate these)
```dart
// GOOD — GPU-composited, no layout reflow
Transform.translate(offset: ...)
Transform.scale(scale: ...)
Transform.rotate(angle: ...)
Opacity(opacity: ...)

// BAD — CPU-bound, forces re-layout
AnimatedContainer(width: ..., height: ...)
AnimatedPadding(padding: ...)
```

### RepaintBoundary placement
```dart
// Wrap high-frequency animations
RepaintBoundary(
  child: CustomPaint(painter: MyParticlePainter()),
)

// Wrap static content near animations
RepaintBoundary(
  child: StaticHeader(),  // doesn't repaint when particles do
)
```

### Spring physics curves
```dart
// Organic rebound — cards, buttons, drawers
Curves.easeOutBack       // slight overshoot
Curves.fastOutSlowIn     // natural deceleration
Curves.elasticOut        // bouncy spring

// Avoid for UI that should feel precise
Curves.linear            // robotic
Curves.easeInOut         // generic, no character
```

### Declarative animation (flutter_animate)
```dart
// PREFER this over manual AnimationController
widget
  .fadeIn(duration: 300.ms)
  .slideY(begin: 0.1)
  .animate(onPlay: (c) => c.forward());

// Over 55 sites already use this — expand to more
```
