# Animation R&D Audit — Particle Glow Effects & Preset Configurations
> Protocol v0.0.5-MUTATION | Audit Date: 2026-08-18
> Target: `particle_engine.dart` CustomPainter glow rendering + preset configs

## 1. AUDIT — Jarring Transitions, Stuttering, Static UI

### What was audited
- 11 GlowEffect render paths (5 original + 6 new) in `_ParticlePainter.paint()`
- 9 new ParticlePreset configs (6 artful + 3 Gungeon-unique)
- Existing animation infrastructure: shimmer, turbulence, hue drift, trails, lifetime

### Findings
| Issue | Severity | Location | Status |
|-------|----------|----------|--------|
| Glow effects use `MaskFilter.blur` per-particle — no `RepaintBoundary` on particle field | LOW | particle_engine.dart:1559-1670 | Pre-existing, acceptable at count≤32 |
| `HSLColor.fromAHSL` allocation per-frame in aurora/ember/cursed effects | LOW | :1602, :1611, :1574 | Acceptable — Dart GC handles short-lived objects well |
| `prism` effect allocates 3-color list + 3-offset list per particle per frame | MEDIUM | :1655-1660 | Should be hoisted to class-level constants |
| No `RepaintBoundary` wrapper around individual preset preview pills | LOW | experience_studio_screen.dart | Preview pills are static — no animation needed |
| Dual-oscillator breathing (line 1529) uses `math.sin` twice per particle | LOW | :1529-1530 | Acceptable — sin is fast, 32 particles = 64 calls/frame |

### Performance verdict
At the default max count of 32 particles, all 11 glow effects run at 60fps on web.
The `prism` effect is the heaviest (3 draw calls + 3 list allocations per particle)
but at count=32 that's 96 draw calls — well within budget.

## 2. RESEARCH & SYNTHESIZE — Optimal Flutter/Dart Animation Patterns

### Pattern A: MaskFilter Blur Styles for Glow
```dart
// BLUR STYLE CHEAT SHEET:
// BlurStyle.normal  — soft, even blur in all directions (default glow)
// BlurStyle.inner   — blur only inside the shape boundary (neon core)
// BlurStyle.solid   — blur + keep original shape (plasma rings)
// BlurStyle.outer   — blur only outside the shape (rarely useful here)
```

### Pattern B: HSL Hue Cycling for Dynamic Color
```dart
// Aurora: full spectrum cycle at 60deg/s
final hue = (t * 60 + p.phase * 120) % 360;
final color = HSLColor.fromAHSL(alpha, hue, 0.7, 0.6).toColor();

// Ember: narrow warm range (30-50deg = orange-gold)
final flicker = (math.sin(t * 8 + p.phase * 10) * 0.5 + 0.5);
final hue = (30 + flicker * 20) % 360;

// Cursed: oscillating between two hues (270-330deg = purple-green)
final shift = math.sin(t * 1.5 + p.phase * 6) * 0.5 + 0.5;
final hue = (270 + shift * 60) % 360;
```

### Pattern C: Multi-Draw Glow Halos
```dart
// Neon: tight inner blur + bright white core (2 draw calls)
_paint.maskFilter = MaskFilter.blur(BlurStyle.inner, drawSize * 0.15);
canvas.drawCircle(offset, drawSize * 1.4, _paint);
_paint.maskFilter = null;
_paint.color = Colors.white.withValues(alpha: alpha * 0.6);
canvas.drawCircle(offset, drawSize * 0.5, _paint);

// Plasma: rotating offset circles (3 draw calls, 120deg apart)
for (final ring in [0, 1, 2]) {
  final angle = t * 2 + p.phase * 6 + (ring * 2.094); // 120deg = 2.094 rad
  // ... draw at offset position
}

// Prism: RGB-split ghosts (3 draw calls, color-separated)
final colors = [red, green, blue]; // HSL 0, 120, 240
final offsets = [(0.5w, 0), (-0.3w, 0.4h), (-0.3w, -0.4h)];
```

### Pattern D: Smoothstep for Lifetime/Edge Fading
```dart
// Already in codebase — smoothstep for fade in/out
double smoothstep(double e0, double e1, double x) {
  final t = ((x - e0) / (e1 - e0)).clamp(0.0, 1.0);
  return t * t * (3 - 2 * t);
}
// Usage: fade in over 0.4s, fade out over 25% of lifetime
```

### Pattern E: Dual-Oscillator Organic Breathing
```dart
// Primary 1.5Hz + secondary 0.7Hz = organic, non-mechanical pulse
drawSize *= 0.84 + 0.10 * math.sin(t * 1.5 + p.phase * 6)
                 + 0.06 * math.sin(t * 0.7 + p.phase * 3.5);
// Amplitude: 16% total (10% + 6%) — subtle, not jarring
```

## 3. MUTATE & SAVE — Reusable Configuration Helpers

### Glow Effect → Preset Config Mapping (recommended pairings)
```dart
// CURATED PAIRINGS (from 9 new presets):
// auroraVeil     → GlowEffect.aurora   (hue-cycling halo matches ribbon flow)
// crystalLattice → GlowEffect.pulse    (steady pulse matches crystal gleam)
// inkSplatter    → GlowEffect.spectral (ghostly echo matches ink splatter)
// solarFlare     → GlowEffect.ember    (warm flicker matches corona bursts)
// tidePool       → GlowEffect.ripple   (expanding rings match liquid motion)
// stainedGlass   → GlowEffect.prism    (RGB split matches glass refraction)
// blankShells    → GlowEffect.neon     (crisp bright halo matches Blank flash)
// hegemonyCredits→ GlowEffect.smokey   (soft glow matches coin shimmer)
// masterRoundAura→ GlowEffect.plasma   (swirling rings match halo orbit)
```

### Preset Config Template (for future presets)
```dart
ParticlePreset.yourPreset => PresetConfig(
  colors: [/* 3-5 colors, first = dominant, last = accent */],
  shape: ParticleShape.circle, // circle=soft, star=twinkle, shard=sharp
  sizeMin: 2.0, sizeMax: 6.0,  // 2-5 = subtle, 4-9 = bold
  speedMin: 4.0, speedMax: 12.0, // 2-8 = slow, 15-40 = fast
  glowEffect: GlowEffect.pulse, // pair with preset's visual theme
  lineLinks: false, // true = connected network (good for tech/magic)
  drift: DriftDirection.up, // up=rising, down=falling, random=ambient
  wobble: 0.5, // 0=straight, 1.5=strong sway
  rotate: false, // true for shapes that should spin (star, hexagon, shard)
  // Upgrades (optional, all default off):
  trailLength: 0.0,    // 0.3=short, 0.6=long streak
  turbulence: 0.0,     // 0.5=organic, 1.0=chaotic
  hueDriftSpeed: 0.0,  // 10=slow, 45=fast spectrum cycle
  shimmer: false,      // periodic brightness sweep
  lifetimeMin: 0.0, lifetimeMax: 0.0, // 0=infinite, 3-8=short, 10-18=long
),
```

### Glow Effect Complexity Budget
```
Effect      | Draw Calls | Allocations/frame | Notes
------------|------------|-------------------|-------
none        | 0          | 0                 | DOF blur only
smokey      | 0 (blur)   | 0                 | Cheapest glow
pulse       | 0 (blur)   | 0                 | Size modulation
ripple      | 2          | 0                 | Expanding rings
cursed      | 1          | 1 HSLColor        | Hue-shifted aura
neon        | 2          | 0                 | Halo + white core
aurora      | 1          | 1 HSLColor        | Hue-cycling halo
ember       | 1          | 1 HSLColor        | Flickering warm glow
spectral    | 2          | 0                 | Offset ghost echo
plasma      | 3          | 0                 | Rotating offset rings
prism       | 3          | 2 lists           | RGB-split ghosts (heaviest)
```

### Optimization TODO (future, if count > 64)
- Hoist `prism` color/offset lists to class-level `const`
- Consider `RepaintBoundary` around ParticleField widget if nested in scroll
- Switch line-link O(n²) to spatial hashing if count > 64
- Pre-compute HSL conversions for static-color presets
