# Gungeon Fall Animation — Implementation Plan

> **Status:** Planning phase — awaiting approval before implementation
> **Date:** August 2026
> **Author:** Coder (Devin session)

---

## Overview

Add a looping "falling down the Gungeon" animation to the home screen (main menu). A Gungeoneer sprite tumbles endlessly down a hypnotic vortex/portal in the background, referencing the true ending fall sequence of Enter the Gungeon. The character shown is dynamically selected based on the player's last used character, or RNG if no history exists.

---

## Visual Design

### Reference
The true ending of Enter the Gungeon shows the Gungeoneer falling down a bottomless shaft — tumbling, rotating, with the camera pulling back to reveal the depth. This animation captures that moment as an idle background loop.

### Layer Stack (bottom to top)

```
Stack
├── Layer 1: Vortex background (CustomPainter — rotating spiral)
├── Layer 2: Vignette scrim (radial gradient — darkens edges for readability)
├── Layer 3: Falling Gungeoneer sprite (centered, animated)
└── Layer 4: Existing main menu content (title, buttons, etc.)
```

### Vortex Approach — CustomPainter (recommended)

**Why not a video/GIF asset?**
- No vortex/portal asset exists in the project
- Downloading one adds weight (the galaxy MP4 is already 9MB)
- A custom painter is lightweight, themeable, and infinitely scalable

**Implementation: `VortexPainter`**
- Draws N concentric spiral arms (default 6) using `Canvas.drawPath`
- Each arm is a logarithmic spiral: `r = a * e^(b*theta)`
- The entire spiral rotates continuously via an `AnimationController` (repeat, ~20s per revolution)
- Colors: deep purple/violet/indigo gradient — pulled from `ThemeFlair` so it matches the active theme
- Center has a radial gradient "hole" that gets darker toward the middle (the void the character falls into)
- Outer edges fade to transparent so the vortex doesn't clash with the existing galaxy background

**Performance:**
- CustomPainter with `repaint` bound to a single `AnimationController`
- ~6 path draws per frame — trivial for Flutter's canvas
- No texture uploads, no video decode, no GIF frame extraction

### Character Fall Animation

**Sprite source:** `gungeoneerGifPath(name)` → `assets/images/gungeoneers/{slug}.gif`
- These are the in-game animated sprites (1-5KB each, already bundled)
- Fallback: static `.webp` icon via `localGungeoneerIcon(name)`

**flutter_animate effects (looping):**
```dart
Image.asset(spritePath, ...)
  .animate(onPlay: (c) => c.repeat())
  .rotate(  // endless tumble
    begin: 0,
    end: 2 * pi,
    duration: 3.seconds,
    curve: Curves.linear,
  )
  .scale(  // subtle depth pulse — simulates falling closer/farther
    begin: Offset(0.8, 0.8),
    end: Offset(1.1, 1.1),
    duration: 4.seconds,
    curve: Curves.easeInOutSine,
  )
  .moveY(  // slow downward drift + reset (the "fall")
    begin: Offset(0, -20),
    end: Offset(0, 20),
    duration: 6.seconds,
    curve: Curves.easeInOut,
  )
```

**Sprite size:** ~64-80px scaled by `Responsive.factor` — small enough to sit "in the distance" inside the vortex, not dominating the screen.

---

## State & Logic

### `lastPlayedCharacter` — new RunProvider field

**Problem:** No `lastPlayedCharacter` key exists in SharedPreferences. The current run's character is stored in `current_run` but cleared when a run ends.

**Solution:** Add a separate persistent key that survives run end:

```dart
// In RunProvider
static const _kLastPlayedChar = 'last_played_character';
String _lastPlayedCharName = '';
String? get lastPlayedCharName => _lastPlayedCharName.isEmpty ? null : _lastPlayedCharName;
Gungeoneer? get lastPlayedCharacter =>
    _lastPlayedCharName.isEmpty ? null : gungeoneerByName(_lastPlayedCharName);

// Load in loadData() alongside other prefs
_lastPlayedCharName = prefs.getString(_kLastPlayedChar) ?? '';

// Save in startNewRun()
void startNewRun(Gungeoneer character) {
  _runState = RunState(main: _buildPlayerFor(character));
  _saveLastPlayedChar(character.name);  // NEW
  _saveRun();
  notifyListeners();
}

// Also save when MP character is selected (in multiplayer_session.dart
// or multiplayer_lobby_screen.dart — wherever the MP character is picked)
```

**MP hook:** The MP session already persists `mp_last_character`. We can either:
- (a) Read both `last_played_character` and `mp_last_character`, prefer the most recent
- (b) Write `last_played_character` from both SP and MP flows

**Recommended: (b)** — single source of truth. Both `startNewRun()` and the MP character selection write to `last_played_character`.

### Character Selection Logic

```dart
Gungeoneer _pickFallCharacter() {
  // 1. Try last played character
  final last = runProvider.lastPlayedCharacter;
  if (last != null) return last;

  // 2. Fallback: RNG from all gungeoneers
  final all = runProvider.allGungeoneers;
  if (all.isEmpty) return null;  // data not loaded yet
  return all[Random().nextInt(all.length)];
}
```

### RNG Persistence

The RNG fallback should be stable per app session — don't re-roll every rebuild. Pick once in `initState()`, store in a field, reuse for the widget's lifetime. Re-roll on hot restart.

---

## Widget Architecture

### New file: `lib/widgets/backgrounds/gungeon_fall_animation.dart`

```dart
class GungeonFallAnimation extends StatefulWidget {
  final Widget child;  // The main menu content to overlay on top

  const GungeonFallAnimation({super.key, required this.child});
  ...
}

class _GungeonFallAnimationState extends State<GungeonFallAnimation>
    with SingleTickerProviderStateMixin {
  late final AnimationController _vortexCtrl;
  Gungeoneer? _fallingChar;
  String _spritePath = '';

  @override
  void initState() {
    super.initState();
    _vortexCtrl = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 20),
    )..repeat();
    _pickCharacter();
  }

  void _pickCharacter() {
    final p = context.read<RunProvider>();
    final char = p.lastPlayedCharacter ??
        (p.allGungeoneers.isNotEmpty
            ? p.allGungeoneers[Random().nextInt(p.allGungeoneers.length)]
            : null);
    if (char != null) {
      _fallingChar = char;
      _spritePath = gungeoneerGifPath(char.name);
    }
  }

  @override
  Widget build(BuildContext context) {
    final sf = Responsive.factor(context);
    return Stack(
      children: [
        // Layer 1: Vortex
        Positioned.fill(
          child: CustomPaint(
            painter: _VortexPainter(
              progress: _vortexCtrl.value,
              colors: _vortexColors(),
            ),
          ),
        ),
        // Layer 2: Vignette
        Positioned.fill(child: _Vignette()),
        // Layer 3: Falling character
        if (_spritePath.isNotEmpty)
          Center(
            child: SizedBox(
              width: 72 * sf,
              height: 72 * sf,
              child: Image.asset(
                _spritePath,
                fit: BoxFit.contain,
                filterQuality: FilterQuality.none,
                gaplessPlayback: true,
                errorBuilder: (_, __, ___) => SizedBox.shrink(),
              )
              .animate(onPlay: (c) => c.repeat())
              .rotate(begin: 0, end: 2 * pi, duration: 3.seconds)
              .scale(
                begin: Offset(0.8, 0.8),
                end: Offset(1.1, 1.1),
                duration: 4.seconds,
                curve: Curves.easeInOutSine,
              )
              .moveY(
                begin: Offset(0, -20 * sf),
                end: Offset(0, 20 * sf),
                duration: 6.seconds,
                curve: Curves.easeInOut,
              ),
            ),
          ),
        // Layer 4: Main menu content
        widget.child,
      ],
    );
  }
}
```

### VortexPainter

```dart
class _VortexPainter extends CustomPainter {
  final double progress;  // 0.0 to 1.0 from AnimationController
  final List<Color> colors;

  const _VortexPainter({required this.progress, required this.colors});

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final maxRadius = math.max(size.width, size.height) * 0.7;

    // Background radial gradient — the "hole"
    final bgPaint = Paint()
      ..shader = RadialGradient(
        center: Alignment.center,
        colors: [
          colors.first.withOpacity(0.0),
          colors.first.withOpacity(0.15),
          Colors.black.withOpacity(0.4),
        ],
        stops: [0.0, 0.4, 1.0],
      ).createShader(Rect.fromCircle(center: center, radius: maxRadius));
    canvas.drawRect(Offset.zero & size, bgPaint);

    // Spiral arms
    const armCount = 6;
    const turns = 3.0;
    const steps = 60;
    final rotation = progress * 2 * math.pi;

    for (var arm = 0; arm < armCount; arm++) {
      final armOffset = (arm / armCount) * 2 * math.pi;
      final path = Path();
      for (var i = 0; i <= steps; i++) {
        final t = i / steps;
        final theta = t * turns * 2 * math.pi + armOffset + rotation;
        final r = t * maxRadius;
        final x = center.dx + r * math.cos(theta);
        final y = center.dy + r * math.sin(theta);
        if (i == 0) path.moveTo(x, y);
        else path.lineTo(x, y);
      }
      // Color interpolation across arms
      final color = colors[arm % colors.length];
      final paint = Paint()
        ..color = color.withOpacity(0.3)
        ..style = PaintingStyle.stroke
        ..strokeWidth = 2.0
        ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 1.5);
      canvas.drawPath(path, paint);
    }
  }

  @override
  bool shouldRepaint(_VortexPainter old) => old.progress != progress;
}
```

---

## Integration Points

### 1. `main_menu_screen.dart`
Wrap the existing `Stack` content with `GungeonFallAnimation`:
```dart
// Before:
return Scaffold(body: Stack(children: [ ... ]));
// After:
return Scaffold(
  body: GungeonFallAnimation(
    child: Stack(children: [ ... ]),
  ),
);
```

### 2. `RunProvider`
- Add `_lastPlayedCharName` field + `lastPlayedCharacter` getter
- Load in `loadData()`
- Save in `startNewRun()`

### 3. MP character selection
- In `multiplayer_lobby_screen.dart` or `multiplayer_session.dart`, write `last_played_character` when MP character is picked

### 4. `theme_overlay.dart`
- The existing galaxy video background stays — the vortex paints on top of it
- The vortex's transparent edges let the galaxy show through
- Consider lowering galaxy opacity from 0.55 to ~0.35 when the fall animation is active, so the vortex reads clearly

---

## Files to Create/Modify

| File | Action | Description |
|------|--------|-------------|
| `lib/widgets/backgrounds/gungeon_fall_animation.dart` | **CREATE** | Main widget + VortexPainter |
| `lib/screens/main_menu_screen.dart` | MODIFY | Wrap content with GungeonFallAnimation |
| `lib/providers/run_provider.dart` | MODIFY | Add lastPlayedCharacter field + persistence |
| `lib/screens/multiplayer_lobby_screen.dart` | MODIFY | Save lastPlayedCharacter on MP character pick |
| `assets/data/changelog.json` | MODIFY | Add changelog entry |

---

## Edge Cases & Considerations

1. **Data not loaded yet:** `allGungeoneers` is empty during initial load — fall animation shows vortex only (no sprite) until data loads, then picks a character on next build.
2. **Cultist has no GIF:** `the_cultist.gif` exists (1KB) but may be a single-frame GIF. The animated card is a `.webp` (not animated). Fallback to static icon is fine — the rotation/scale animation still applies.
3. **Paradox GIF is 218KB:** Largest sprite — still trivial for `Image.asset`. No optimization needed.
4. **Performance:** VortexPainter runs at 60fps with ~6 path draws. Character GIF decodes natively. Combined cost is negligible compared to the existing galaxy video.
5. **Theme matching:** Vortex colors pulled from `ThemeFlair` — `primary`, `secondary`, `glowPrimary`. On dark themes the vortex is subtle; on neon themes it pops.
6. **Accessibility:** The vortex is purely decorative — `IgnorePointer` wraps it so it never blocks taps. The character sprite is also non-interactive.
7. **Battery:** AnimationController repeats forever. Consider pausing when app is backgrounded (the existing `ThemeOverlay` already handles this pattern via lifecycle observer).

---

## What This Plan Does NOT Include

- No new asset downloads (vortex is custom-painted)
- No changes to the existing galaxy video background system
- No changes to character select screen behavior
- No new dependencies (uses existing `flutter_animate`, `Responsive`, `RunProvider`)
- No version bump (feature addition, not a release)

---

## Open Questions

1. **Should the vortex replace the galaxy video entirely, or layer on top?**
   - Plan assumes layering on top with reduced galaxy opacity. If replacing, we'd skip the galaxy video when the fall animation is active.

2. **Should the character change when the user taps the vortex?**
   - Not in the plan — purely idle animation. Could be a fun easter egg (tap to re-roll character).

3. **Should we show the character name as a subtitle below the sprite?**
   - Not in the plan — keeps the animation subtle and non-distracting from the menu buttons.
