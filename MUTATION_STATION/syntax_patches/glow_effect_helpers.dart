// =============================================================================
// MUTATION STATION — Reusable Glow Effect Helpers
// Protocol v0.0.5-MUTATION | Archived: 2026-08-18
//
// These helpers extract the common patterns from the 11 GlowEffect
// implementations in particle_engine.dart. They are NOT imported
// anywhere yet — they serve as a reference library for future
// CustomPainter glow work.
//
// To use: copy the specific helper you need into your painter, or
// import this file directly if you need multiple helpers.
// =============================================================================

import 'dart:math' as math;
import 'dart:ui';

/// Smoothstep interpolation — standard GLSL-style easing.
/// Use for lifetime fades, edge fades, and any transition that
/// should feel organic rather than linear.
double smoothstep(double e0, double e1, double x) {
  final t = ((x - e0) / (e1 - e0)).clamp(0.0, 1.0);
  return t * t * (3 - 2 * t);
}

/// Hue-cycling color generator for aurora/rainbow effects.
/// [hueSpeed] is in degrees per second. [phaseOffset] individualizes
/// particles so they don't all cycle in sync.
Color hueCyclingColor(double t, double phaseOffset, double hueSpeed,
    double alpha, {double saturation = 0.7, double lightness = 0.6}) {
  final hue = (t * hueSpeed + phaseOffset) % 360;
  return HSLColor.fromAHSL(alpha, hue, saturation, lightness).toColor();
}

/// Narrow-band hue oscillator for fire/ember effects.
/// Oscillates between [baseHue] and [baseHue + range] degrees.
/// [freq] controls flicker speed (8 = fast fire, 2 = slow candle).
Color flickerHueColor(double t, double phaseOffset, double baseHue,
    double range, double freq, double alpha,
    {double saturation = 0.9, double lightness = 0.5}) {
  final flicker = (math.sin(t * freq + phaseOffset * 10) * 0.5 + 0.5);
  final hue = (baseHue + flicker * range) % 360;
  final flickerAlpha = alpha * (0.4 + flicker * 0.3);
  return HSLColor.fromAHSL(flickerAlpha, hue, saturation, lightness).toColor();
}

/// Dual-oscillator organic breathing size multiplier.
/// Combines a primary and secondary sine wave for non-mechanical pulse.
/// Returns a multiplier centered on 1.0 with ~16% total amplitude.
double organicBreathing(double t, double phaseOffset) {
  return 0.84 +
      0.10 * math.sin(t * 1.5 + phaseOffset * 6) +
      0.06 * math.sin(t * 0.7 + phaseOffset * 3.5);
}

/// RGB-split prism offsets for refraction effects.
/// Returns three (dx, dy) offsets in units of [drawSize].
const List<(double, double)> prismOffsets = [
  (0.5, 0.0),    // red ghost — right
  (-0.3, 0.4),   // green ghost — bottom-left
  (-0.3, -0.4),  // blue ghost — top-left
];

/// Prism RGB colors at standard hue positions (0, 120, 240 degrees).
List<Color> prismColors(double alpha) => [
      HSLColor.fromAHSL(alpha * 0.4, 0, 0.8, 0.5).toColor(),
      HSLColor.fromAHSL(alpha * 0.4, 120, 0.8, 0.5).toColor(),
      HSLColor.fromAHSL(alpha * 0.4, 240, 0.8, 0.5).toColor(),
    ];

/// Plasma ring positions — 3 circles at 120-degree offsets, rotating
/// over time. Returns list of (x, y, radiusScale) tuples.
List<(double, double, double)> plasmaRingPositions(
    double t, double phaseOffset, double drawSize) {
  return List.generate(3, (ring) {
    final angle = t * 2 + phaseOffset * 6 + (ring * 2.094); // 120deg = 2.094 rad
    return (
      math.cos(angle) * drawSize * 0.8,
      math.sin(angle) * drawSize * 0.8,
      drawSize * 0.7,
    );
  });
}

/// Ripple ring parameters — expanding rings that fade as they grow.
/// Returns list of (radius, alpha) tuples for [ringCount] staggered rings.
List<(double, double)> rippleRings(
    double t, double phaseOffset, double drawSize, double baseAlpha,
    {int ringCount = 2, double speed = 1.5, double maxRadius = 3.0}) {
  return List.generate(ringCount, (i) {
    final offset = i / ringCount;
    final phase = (t * speed + phaseOffset + offset) % 1.0;
    final radius = drawSize * (1.5 + phase * maxRadius);
    final alpha = baseAlpha * (1.0 - phase) * 0.4;
    return (radius, alpha);
  });
}

/// MaskFilter blur presets for common glow styles.
class GlowBlur {
  // Soft, even blur — default for most glows
  static MaskFilter soft(double size) =>
      MaskFilter.blur(BlurStyle.normal, size);

  // Tight inner blur — for neon core effects
  static MaskFilter inner(double size) =>
      MaskFilter.blur(BlurStyle.inner, size);

  // Blur + keep shape — for plasma ring effects
  static MaskFilter solid(double size) =>
      MaskFilter.blur(BlurStyle.solid, size);

  // Heavy blur — for smokey/aura effects (0.8-1.2x draw size)
  static MaskFilter heavy(double size) =>
      MaskFilter.blur(BlurStyle.normal, size * 1.2);
}
