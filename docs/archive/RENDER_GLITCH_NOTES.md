# Render glitch — diagnostic notes

## Symptom

User reports that occasionally the screen renders as a "jumbled mess of
graphics" — fonts, sprites, gradients all visually scrambled — until they
press something to force a relayout, after which the screen renders cleanly.

## Likely causes (most → least probable)

1. **Skia tile cache miss after process suspension.** Android sometimes
   hands the app's `SurfaceView` back with stale GPU texture memory after
   the process was paused for an extended period. The first few frames
   composite garbage textures until the next `markNeedsPaint`. Tapping the
   screen fires a hit-test which schedules a paint, which clears it.

2. **Image decoder cache poisoning.** We render dozens of pixel-art webp
   sprites with `filterQuality.none`. If an `Image.asset` is recreated
   while its `ImageStream` is still being decoded by the engine, the older
   stream's bytes can land in a newer texture slot. Symptom matches:
   correct-looking shapes, wrong textures.

3. **GPU shader compile flicker.** First render of a complex
   `BackdropFilter` / `BlurredImage` after a cold start can fall back to a
   transient solid-colour fill. Less likely here — we don't use
   `BackdropFilter`.

## Mitigations to try (low risk, not done yet)

1. **Force a post-resume repaint.**
   ```dart
   class _Root extends State<Root> with WidgetsBindingObserver {
     @override
     void didChangeAppLifecycleState(AppLifecycleState s) {
       if (s == AppLifecycleState.resumed) {
         WidgetsBinding.instance.addPostFrameCallback((_) {
           setState(() {}); // force a fresh paint
         });
       }
     }
   }
   ```
   Add this once at `MaterialApp` level.

2. **Cache decoded images per name.** Replace `Image.asset(path)` calls in
   `GameIcon` and similar with a `precacheImage` warm-up at app start so
   the engine never serves a half-decoded stream during normal scrolls.

3. **Pin pixel-art textures.** Use `MemoryImage` for the small
   gungeoneer/icon sprites by pre-loading them once into a singleton; this
   sidesteps the asset loader's stream race.

## Reproduction asks

To make a real fix instead of guesses, capture next time it happens:

- Was the app foregrounded from a long pause, or fresh-launched?
- Which screen was visible? (Inventory vs Browse vs Detail)
- Did scrolling or just tapping clear it?
- Android version + device model.

If the user can repro in `flutter run --release` we can attach
`flutter screenshot` mid-glitch and trace from there.
