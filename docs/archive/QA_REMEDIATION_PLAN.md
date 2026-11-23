# QA Remediation Plan — v3.6.0 Customization/MP Batch

> Produced 2026-11-25 by CORE (Slot 2) after the post-release audit:
> `flutter analyze` 0 issues · `flutter test` 603 pass / 0 fail / 9 skip
> (5 earlier failures confirmed load-flakes). Two parallel deep reviews
> covered every shipped file (`246ddfb..0df69ee`). Slot 4's parallel QA
> sweep already landed fixes for **U-006** (wallpaperImmersive preset
> leak → `VisualPrefs.preserveAppLevel`) and **U-007** (`_AvatarIdle`
> vsync under reduced-motion) — both uncommitted; this plan excludes them.

Each item lists: **files · root cause · fix logic · edge cases · tests**.
Batches are ordered by user-facing severity; each is independently
shippable.

---

## P0 — Correctness (ship first; real user-facing breakage)

### A1. Sidekick can hang forever on "WAITING FOR HOST" — missed `MpStartRun`

- **Files:** `lib/services/mp_session.dart`, `lib/services/mp/mp_sync.dart`,
  `lib/services/mp/mp_handlers.dart`, `lib/screens/mp_connect_screen.dart`
- **Root cause:** `onStartRun` is a single UI callback registered in
  `MpConnectScreen.initState`. `MpStartRun` is whitelisted pre-handshake
  (`mp_sync.dart:287`) so it can be processed before the screen mounts;
  if it lands in the mount gap, `onStartRun == null` and the notification
  is lost forever. No session-level latch, no timeout, no resend.
- **Fix logic:**
  1. In `MpSession`, set `_runStartReceived = true` inside the
     `_sync.onStartRun` closure **before** invoking `onStartRun?.call()`.
     Expose `bool get runStartReceived`.
  2. `MpConnectScreen._awaitingHandshake` becomes
     `session.role == sidekick && !_peerStarted && !session.runStartReceived`.
     `_onPeerStartRun` still sets `_peerStarted` for the immediate path.
  3. Reset `_runStartReceived` on `MpEndRun` receipt and on session
     `cancel()`/new `MpHello` so a stale latch can't leak into a later run.
- **Edge cases:**
  - `MpStartRun` arrives pre-hello, pre-mount, and post-mount — all must
    result in the sidekick entering the run exactly once.
  - Duplicate `MpStartRun` (reconnect replay) — latch is idempotent;
    `_startRunTimer` already guards `runStartMs != 0`.
  - Host taps READY, then link drops before delivery, then reconnects —
    `connectReason == reconnecting` skips the handshake gate; verify the
    run still starts via the restore path, not the latch.
  - End-run → new run in same session: latch must be cleared or the next
    sidekick run auto-enters without confirmation.
- **Tests:**
  - Wire-level: inject `MpStartRun` before screen pump → expect run entry.
  - Session-level: `runStartReceived` flips on message, resets on
    `MpEndRun`.
  - Regression: existing READY→STARTING and sidekick WAITING tests stay
    green.

### A2. `sendStartRun` silently drops when disconnected → pair desyncs

- **Files:** `lib/services/mp/mp_sync.dart:908`,
  `lib/services/mp_session.dart:527`, `lib/screens/mp_connect_screen.dart`
- **Root cause:** `sendStartRun` checks `_link.isConnected` and returns
  silently; `MpSession.sendStartRun` arms `_startRunTimer` *before* the
  send, and the screen sets `_mainConfirmed` before awaiting — Main
  enters the run while the sidekick waits forever.
- **Fix logic:**
  1. `MpSync.sendStartRun` throws `StateError('not connected')` (or
     returns `false`) when `!_link.isConnected`; do not arm the timer on
     failure — move `_startRunTimer()` after a successful send, or have
     `MpSession.sendStartRun` await the send result first.
  2. `MpConnectScreen._confirmAndStart`: `try { await sendStartRun();
     _mainConfirmed = true; } catch { _mainConfirmed = false;
     showSnack/sessionEvents error }` — button re-enables, user can retry.
- **Edge cases:**
  - `isConnected == true` but the underlying write throws mid-send —
    same catch path.
  - Double-tap READY — button disables on first tap (`_mainConfirmed`),
    guard with an `_sending` flag if the await is slow.
  - Peer vanished between splash render and tap — error surfaces instead
    of silent desync.
- **Tests:** mock link disconnected → `sendStartRun` throws; screen shows
  error state and button re-enables; timer not armed on failure.

### A3. No `PopScope` — system back bypasses handshake + leaks session

- **Files:** `lib/screens/mp_connect_screen.dart`
- **Root cause:** only `BottomBackBar.onPressed` calls `session.cancel()`.
  Android system back pops the route: radios keep advertising, phase stays
  `connected`, and on the sidekick path the user lands on `HomeScreen`
  which renders `ActiveRunScreen` (run already started) **without host
  confirmation** — a desynced zombie session.
- **Fix logic:** wrap the Scaffold in
  `PopScope(canPop: false, onPopInvokedWithResult: ...)` routing through
  the same `_cancelAndPop` used by `BottomBackBar`. During the 600ms
  `_buildEntering` beat, back is ignored entirely (the start already
  fired; cancelling would `MpEndRun` the peer's run — see A5).
- **Edge cases:**
  - Back during `connecting`/`discovering` — cancel + pop (current
    BottomBackBar behavior).
  - Back during `connected` splash — cancel sends `MpEndRun`/disconnect;
    verify peer sees the teardown, not a hang.
  - Back during `_buildEntering` — swallowed; verify no pop, no cancel.
  - Back after `_navigatedToRun` — route already gone; no-op.
- **Tests:** `tester.binding.handlePopRoute()` (or page-back simulation)
  at each phase → assert `session.cancel` called / route popped /
  entering-beat swallow.

### A4. `_enterRun`'s delayed `popUntil(isFirst)` can pop foreign routes

- **Files:** `lib/screens/mp_connect_screen.dart:103-116`
- **Fix logic:** the connect route was `pushReplacement`'d, so a single
  `Navigator.pop()` lands on home. Replace `popUntil((r) => r.isFirst)`
  with popping the captured `ModalRoute` (or `pop()` once) guarded by
  `ModalRoute.of(context)?.isCurrent`. Keep the 600ms beat.
- **Edge cases:** user pushes a route over the splash within 600ms
  (currently impossible — splash blocks input — but the predicate must
  not be absolute); widget unmounted mid-delay (already guarded).
- **Tests:** pump 600ms, assert exactly the connect route was removed and
  home remains.

### A5. Back bar live during "ENTERING" beat → accidental `MpEndRun` nuke

- **Files:** `lib/screens/mp_connect_screen.dart:149-154, 619-683`
- **Fix logic:** hide/disable `BottomBackBar` once `_navigatedToRun` is
  true (or during `_buildEntering`); combined with A3's swallow, no path
  sends `MpEndRun` in the transition window.
- **Edge cases:** peer already received `MpStartRun` — their run is
  armed; any local cancel in this window desyncs both players.
- **Tests:** during entering beat, assert back bar absent and system back
  swallowed.

### A6. `_confirmAndStart` unhandled throw → stuck "STARTING…"

- Covered by A2's try/catch. Additional edge: after failure, haptic +
  `sessionEvents` entry so the failure is diagnosable.

### A7. VS splash portrait row overflows at 320dp with long nicknames

- **Files:** `lib/screens/mp_connect_screen.dart:526-561, 921-996`
- **Root cause:** `_Portrait` is an unconstrained `Column` in a `Row`;
  `maxLines:1, ellipsis` never engages without bounded width. Nicknames
  allow 24 chars; at sf≈0.85 the row leaves ~45-90px for two labels.
- **Fix logic:** wrap each `_Portrait` in `Flexible` (or give the label a
  `SizedBox(width: portraitSize * sf)`), so ellipsis actually truncates.
  Consider `FittedBox(scaleDown)` floor ~0.6 for the sub-line.
- **Edge cases:** 24-char nickname both sides; empty peer nickname
  ('Partner' fallback); very long run title chip (already `Flexible`).
- **Tests:** golden or `tester.takeException()` layout test at 320×568
  with max-length nicknames.

### A8. Sidekick "WAITING" has no watchdog or escape hint

- **Files:** `lib/screens/mp_connect_screen.dart`, maybe `mp_handlers.dart`
- **Fix logic:** add a ~20-30s `Timer` armed when the sidekick enters the
  waiting state; on fire, swap the hint text to "Taking long? The host may
  have cancelled — you can back out safely." plus keep the (now
  PopScope-routed) back path. Do **not** auto-cancel; a slow host is
  legitimate. Re-arm/cancel the timer on `runStartReceived`, disconnect,
  or dispose.
- **Edge cases:** timer must not fire after `MpStartRun` lands (cancel on
  latch); must not fire under `_still` differently; reconnect resets it.
- **Tests:** `tester.pump(31s)` → hint text appears; pump `MpStartRun`
  first → timer cancelled, no hint.

### A9. Protocol version not bumped — mixed old/new builds can deadlock

- **Files:** `lib/models/multiplayer_messages.dart:144`,
  `lib/services/mp/mp_sync.dart:426-432`
- **Root cause:** handshake *semantics* changed (sidekick now hard-depends
  on `MpStartRun`; old flow auto-entered on connect) but
  `MpHello.currentProtocolVersion` stayed 3.
- **Fix logic:** bump to 4. The existing version-mismatch path already
  disconnects cleanly — verify it surfaces an error, not a silent drop.
  Document in `VERSION_HISTORY`/changelog that MP cross-version pairing is
  intentionally broken between v3.5.x and v3.6.x+.
- **Edge cases:** v3 peer ↔ v4 peer → clean disconnect + message;
  same-version pairs unaffected; `mp_protocol_v3` test suite updated or
  version-gated.
- **Tests:** protocol tests assert version 4; mismatch test asserts
  disconnect reason.

### A10. Run timer frozen at 0:00 after app-kill restore (pre-existing)

- **Files:** `lib/services/mp/mp_store.dart:77-88`,
  `lib/services/mp_session.dart:488-494`, `mp_handlers.dart:251-262`
- **Root cause:** `runStartMs`/`runAccumMs` only persist on pause; an
  unpaused run killed mid-flight restores zeros and nothing re-arms.
- **Fix logic:** persist run timing inside the existing ~5s
  `_startSaveTimer` (or on `MpStartRun` receipt + periodic); on
  `_onRecoveryRestore`, if a run is active and `runStartMs == 0 &&
  runAccumMs == 0`, re-arm via `_startRunTimer`. Also fix the resume hole:
  `_applyPaused(false)` should arm whenever a run is active, not only when
  time was previously banked.
- **Edge cases:** paused run restore (already banked — don't double-arm);
  clock skew across devices (timer is local-elapsed, fine); run ended
  before kill (don't resurrect); `MpStartRun` arriving while paused (arm
  on unpause).
- **Tests:** simulate kill-restore with active unpaused run → elapsed
  continues; paused → resumes correctly; ended → stays dead.

---

## P1 — Performance

### B1. Liquid tank 12s wrap snap (visible glitch)

- **Files:** `lib/widgets/particles/liquid_tank.dart:53-57, 90-97, 181`
- **Root cause:** `_wave` is a 12s repeating controller; `time =
  _wave.value * 12` sawtooths, but painted sines/bubbles aren't periodic
  in `time` → surface, fill level, and all 22 bubbles teleport every cycle.
- **Fix logic:** keep `_wave` purely as the vsync heartbeat; accumulate
  `time += dt` in `_onTick` using `lastElapsedDuration` (already clamped
  0.001–0.05 for shells). Time becomes monotonic and freezes when the
  ticker is offscreen — consistent with `ParticleField._sw`. `_fill`
  controller unchanged (its 0→1 ramp is genuinely one-shot).
- **Edge cases:** kind switch mid-cycle (fill re-ramps, shells reseed —
  time keeps running, fine); `_still` path keeps fixed `t=41.0`;
  backgrounding the app (ticker stops → time freezes → resume continues,
  no jump); first frame before any tick (`time=0` acceptable).
- **Tests:** expose accumulated time via `@visibleForTesting` getter or
  drive 12+ virtual seconds and assert painter `time` is monotonic;
  golden-diff surface at t≈11.9s vs t≈0.1s shows continuity, not a jump.

### B2. Per-frame shader/path allocation in `_LiquidPainter`

- **Files:** `lib/widgets/particles/liquid_tank.dart:296-370`
- **Fix logic:** hoist the body `LinearGradient` shader (recreated only
  when `size`/`kind` changes via cached `Size`+`kind` key); bubbles share
  one `RadialGradient` shader painted under `canvas.translate` instead of
  22 `createShader` calls; cache the two surface `Path`s? (paths depend on
  `time` — keep, but reuse `Path` objects via `reset()`). Consider dropping
  bubble count 22→16 on `sf < 0.9`.
- **Edge cases:** shader cache invalidation on resize/kind switch;
  `shouldRepaint` still keyed on `time`.
- **Tests:** existing liquid_tank tests stay green; optional frame-time
  smoke test is overkill — rely on code review + profile if needed.

### B3. Double particle system per overlay build (worst battery/jank item)

- **Files:** `lib/widgets/theme_overlay.dart:234, 495`,
  `lib/widgets/particle_engine.dart`
- **Root cause:** `buildBackdropParticleField` is invoked twice — backdrop
  layer + foreground "dust" layer — each a full `ParticleField` with its
  own controller, population, and O(n²) link pass. At COUNT=200 + LINKS
  that's ~2×20k pair checks/frame plus a `LinearGradient`+shader per pair.
- **Fix logic (recommended):** extract the simulation into a shared
  `ParticleSim` (particle list + step function) owned once per overlay;
  the two layers become two `CustomPaint` passes over the same sim with
  different painter params (the dust layer is presumably a subset/slower
  variant — verify intent at `theme_overlay.dart:495` first). Fallback if
  too invasive: spatial-hash the link pass + cap effective link count.
- **Edge cases:** reduceMotion (sim must still freeze both layers);
  item-icon mode (widget-based, separate path — decide whether it also
  duplicates); COUNT slider live-updates; kind/type switching rebuilds.
- **Tests:** `find.byType(ParticleField)` count in overlay tree == 1 (or
  sim shared); existing particle tests green.

### B4. Up to 4 simultaneous `CustomWallpaper` instances in studio

- **Files:** `lib/widgets/backgrounds/custom_wallpaper.dart`,
  `lib/widgets/theme_overlay.dart:295-303`,
  `lib/screens/experience_studio_screen.dart:101,425,1132`
- **Root cause:** studio preview bg + per-LIVE-LOOK panes + the real
  `ThemeOverlay` copy (menuVisible false on pushed routes) — each adds a
  tilt listener and, when immersive, its own 18s zoom controller doing
  full-screen repaint at 60fps. Visually only one is seen.
- **Fix logic:** add a `stillFrame`/`previewStatic` param — LIVE LOOK
  thumbnails and hidden duplicates render one composed frame (they're tiny
  anyway); only the topmost visible instance animates. Simplest robust
  version: a static refcount — first immersive `CustomWallpaper` mounted
  animates, subsequent ones render `t=0.5` static until they become the
  only/visible one. Pick whichever is less code after reading the three
  call sites.
- **Edge cases:** immersive toggled off mid-session; route pop revealing
  the overlay copy (it must resume animating, not stay frozen); reduced
  motion already forces static everywhere.
- **Tests:** mount two wallpapers, assert only one `AnimationController`
  is animating (via `debug` count or ticker count).

### B5. `ItemIconField` rebuilds a widget `Stack` per frame ×2

- **Files:** `lib/widgets/particle_engine.dart:130-185`
- **Fix logic:** optional — paint icons in one `CustomPaint` via
  `canvas.drawImage`/`paintImage` + save/rotate, or accept cost but skip
  the foreground duplicate when `kind == itemIcon`. Lower priority than B3.
- **Edge cases:** `errorBuilder` missing sprites → `SizedBox.shrink`
  (ties to C3 sprite validation); reduced-motion gating gap (callers pass
  `reduceMotion` inconsistently — studio preview doesn't).

---

## P2 — Honesty / persistence / polish

### C1. Unclamped numerics in `VisualPrefs.fromJson` → slider assert crash

- **Files:** `lib/services/theme/theme_flair_prefs.dart:1393-1398`,
  `lib/screens/experience_studio/studio_particles.dart:216`
- **Root cause:** `init()` clamps `particleTypeIndex`, `particleCount`,
  etc.; `fromJson` doesn't — a hand-edited/corrupt/older preset JSON with
  `particleCount: 500` hits `Slider(value:…)`'s `value <= max` assert.
- **Fix logic:** apply the same clamps in `fromJson` (extract a shared
  `_clamp` or clamp at assignment). Cover `particleCount`,
  `particleOpacity`, `particleSizeScale`, `fontSize`,
  `inventoryFontSize`, `particleTypeIndex`, `particleSchemaIndex`,
  `particleItemIcon`, `liquidKindIndex`.
- **Edge cases:** negative, >max, non-int, null, missing keys;
  `particlesEnabled` default mismatch (fromJson `false` vs ctor `true`).
- **Tests:** `fromJson` fuzz — out-of-range values clamp; slider never
  asserts.

### C2. Dead color-override path — schemas silently do nothing

- **Files:** `lib/widgets/theme_overlay.dart:570-579`,
  `lib/widgets/particle_engine.dart:273-277, 549-556`
- **Root cause:** `colorsOverride`/`particleColorSchema`/Unicorn
  `particleColors` are computed but ignored whenever `config != null` —
  which is always in the typed path.
- **Fix logic (decision needed):** either thread the override palette into
  `typedParticleConfig`'s color params, or remove the dead pref/UI so the
  app stops promising behavior. **Recommend wiring it** — the schema row
  exists in the studio and users can pick INFERNO etc.
- **Edge cases:** `themeMatch` schema = no override; custom sprite path
  (color semantics unclear — probably tint); interplay with LOOKS
  `applyParticleLook` (look sets colors; schema would fight it — define
  precedence: explicit look > schema > type default).
- **Tests:** pick schema ≠ themeMatch → rendered colors change (widget
  test on resolved config, not pixels).

### C3. Sprite picker dead-end picks — unverified slug→WEBP paths

- **Files:** `lib/screens/experience_studio/studio_particles.dart:1134-1146`,
  `lib/utils/asset_paths.dart:45-52`, `lib/widgets/particle_engine.dart:172`
- **Root cause:** picker enumerates `guns.json`/`items.json` names and
  derives paths by slug rule without checking the `.webp` exists; a miss
  renders generic icons in the grid, and once picked every
  `Image.asset` hits `errorBuilder → shrink` → invisible particles, no
  feedback. Same risk for stale persisted `particleSpritePath`.
- **Fix logic:** at picker load, intersect the derived list with the
  bundled asset manifest (`AssetManifest` or a generated list); show a
  "N sprites" count; on pick of a path that fails, surface a snackbar.
  On app start / prefs init, validate persisted `particleSpritePath`
  against the manifest — clear + log if missing.
- **Edge cases:** manifest load failure → fall back to current behavior
  (show all); async gap (picker opens before manifest resolves → loading
  state); renamed/culled assets leaving stale prefs.
- **Tests:** manifest-mock test — missing asset excluded from list;
  stale persisted path cleared on init.

### C4. Small persistence gaps

- **Files:** `lib/services/theme/theme_flair_prefs.dart`,
  `lib/services/color_favorites.dart`
- **Items:**
  - `setFontWeightBias` never calls `_persist()` — lost on restart.
  - `fontLetterSpacing` missing from `toJson`/`fromJson` — dropped from
    saved presets.
  - `applyCuration` writes `particlePreset` (dead field) but leaves
    `particleTypeIndex`/`particleItemIcon`/`particleSpritePath` — premade
    themes don't fully reset the particle look. **Decision:** curation
    should clear all three (sprite path especially — a custom sprite
    floating under every premade theme is almost certainly unwanted).
  - `ColorFavorites.setSlot` — two rapid calls persist out of order
    (each writes its own captured list; last `setString` wins on disk).
    Serialize writes or write the latest list.
  - `colorAt` is dead code — remove.
- **Tests:** round-trip tests for the two JSON gaps; curation test
  asserting particle fields reset; favorites rapid-write test.

### C6. PARTICLES summary chip mislabels sprite mode

- **Files:** `lib/screens/experience_studio_screen.dart:2852-2855`
- **Fix:** check `particleSpritePath.isNotEmpty` first → show
  `SPRITE: <name>`; then `particleItemIcon >= 0` → icon label; else type.
- **Tests:** chip text for each of the three modes.

### C7. NaN accelerometer poisons tilt app-wide

- **Files:** `lib/widgets/theme_overlay.dart` (sensor callback ~78-91)
- **Fix:** `if (!tx.isFinite || !ty.isFinite) return;` before clamp —
  `NaN.clamp()` returns NaN, which then NaNs shell positions AND every
  `ParticleField` particle (they fail boundary checks and vanish).
- **Tests:** inject NaN event → tilt unchanged, particles alive.

### C8. Studio `_syncMotion` side effect inside builder + `_still` gaps

- **Files:** `lib/widgets/backgrounds/custom_wallpaper.dart:91-95`,
  `lib/screens/mp_connect_screen.dart` (`_WaitingForHost` frozen dots)
- **Fix:** move wallpaper motion sync to `didChangeDependencies` +
  prefs-listener (not inside `ValueListenableBuilder`); make
  `_WaitingForHost.ctrl` nullable and render a static mid-frame dot row
  under reduced motion.
- **Tests:** toggle immersive off mid-animation → controller stops;
  reduced-motion splash renders static dots.

---

## P3 — Deferred bug list (from AGENTS.md / board)

| Item | Note |
|------|------|
| TIERS test regression (`browse_synergies`) | test-side, needs investigation |
| Synergy-scan recompute-per-build perf | cache scan results per data version |
| Browse row overflow ≤500px | layout test at narrow widths |
| MP first-endpoint mis-pair race | pairing logic, separate session |
| Host-gone hint | UX nicety, pairs with A8 watchdog |
| `�` mojibake in JSONs | encoding sweep, mechanical |
| U-001 white screenshot | re-capture, not an app bug |
| S7 mini-slice in LIVE LOOK | optional masterplan leftover |
| Preview session-seed label | tiny debug aid — helps users describe what they saw in bug reports |

---

## UI/UX review — shipped v3.6.0 features

Overall the batch is strong visually; findings below are polish-level,
not blockers. Severity: **S1** = should fix soon, **S2** = nice to have,
**S3** = optional flourish.

### VS splash + handshake (`mp_connect_screen.dart`)

- **Good:** huge portraits + VS medallion + LINKED chip sells the
  moment; "You are MAIN — confirm to drop both of you in" copy is clear;
  role-aware button vs waiting state.
- **S1 — Sidekick has zero agency.** Only passive "waiting" text + the
  subtle bottom bar as escape. A8's watchdog hint fixes the silence; also
  consider making CANCEL more prominent on the waiting state (secondary
  button, not just the bottom bar).
- **S1 — "STARTING…" lies on failure.** Covered by A2/A6 — after the fix,
  a failed send must visibly revert the button, not sit on STARTING.
- **S2 — No haptic punctuation.** Recommend: selection haptic on READY
  tap, success haptic when LINKED chip appears / when `_buildEntering`
  plays. Cheap, big feel win.
- **S2 — Entering beat shows live back bar** (A5) — during 600ms a stray
  tap nukes both runs. Hide it.
- **S2 — 320dp overflow** (A7) — certain with 24-char nicks.
- **S3 — Versus flourish:** portraits could get a slow opposing drift
  (left drifts left, right drifts right, 8-10px, phase-offset) — sells
  "two sides" more than the current symmetric pulse. Keep subtle;
  reduced-motion already freezes it.

### Player panel (`paradox_player_panel.dart`)

- **Good:** name+tag beside avatar, stats pinned right — reads like a
  versus card now.
- **S2 — Stats legibility floor.** `FittedBox(scaleDown)` has no minimum —
  at 320dp stats can render ~55%. Consider `scaleDown` + a floor: if the
  scaled font would go below ~9px effective, switch to abbreviated labels
  (C/S/SYN already short) or two-line stat column instead of shrinking.
- **S2 — Nickname column fixed at `58*sf`.** 24-char nicks truncate to
  ~"SIDEKICK…". Widening to ~72*sf costs little (avatar+name block still
  < stats zone) — verify at 320dp first.

### Idle avatars (`avatar_frame.dart`)

- **Good:** phase-offset breathing means pairs never sync — nice detail.
- **S2 — TickerMode gating.** `idle: true` is set in 4 places incl.
  `PageView` pages that stay alive offscreen — all tick vsync. Wrap
  `_AvatarIdle`'s repeat in `TickerMode` awareness (or `VisibilityDetector`
  if already a dep) so offscreen avatars freeze.
- Slot 4's U-007 fix (reduced-motion stop) covers the a11y side.

### Studio — LOOKS row + sprite picker (`studio_particles.dart`)

- **Good:** one-tap curated looks with palette dots; mutual exclusion
  keeps UI honest; searchable ANY SPRITE sheet over 500+ assets.
- **S1 — Silent mutual exclusion.** Tapping a TYPE tile clears
  `particleSpritePath` (and vice versa) with no explanation — a user who
  picked a sprite then taps STAR sees particles change but may not
  connect why their sprite "disappeared". Add a transient hint
  ("sprite cleared — types and sprites are exclusive") or a small
  mode-indicator chip showing SPRITE/TYPE/ICONS active.
- **S1 — Dead-end sprite picks** (C3) — unverified paths = invisible
  particles. Fix before users hit it.
- **S2 — No "CUSTOM" state.** After applying a LOOK then nudging a
  slider, `matchesParticleLook` fails → no tile highlighted, no signal
  the look was modified. Add a subtle "CUSTOM" chip at the row's end
  when no look matches — teaches the system.
- **S2 — Sprite picker polish:** show result count, a "currently using:
  X" header, and a NONE/CLEAR row (currently only reachable via other
  tiles).

### Studio — color favorites (`_PaletteColorSheet`)

- **Good:** lives in every palette sheet for free; positional stable
  slots; app-level so presets don't carry them.
- **S2 — Discoverability.** Empty slots at first launch give no hint
  they're long-press-fillable. Add microcopy under the row ("tap to use ·
  hold to save a favorite") or a one-time coach mark.
- **S2 — Double-sheet UX.** Long-press on an empty slot stacks a second
  identical `_PaletteColorSheet` to pick the color — works but odd.
  Consider an inline hue slider strip inside the favorites row instead.
- **S2 — Fixed 478px sheet height** can clip on short/landscape screens —
  switch to `FractionallySizedBox`/max-height constraint.

### Studio — live mocks (COLORS & BG / PANELS)

- **Good:** composite "app slice" repaints all six roles at once;
  panel mock uses resolved `flairFor` — shows the *actual* override
  result, not raw slider values. Exactly the "show me the element"
  idea requested.
- **S2 — Mock could go further:** the element mock is static composition;
  adding the active `liquidKind` as a faint backdrop swatch would preview
  AMBIENCE choices in the same place (currently only visible in LIVE LOOK).

### Wallpaper immersive (`custom_wallpaper.dart` + sheet toggle)

- **Good:** breathing zoom + tilt parallax, scrim frame-locked,
  reduced-motion static frame — all verified.
- **S2 — Label clarity.** "IMMERSIVE" alone may not communicate
  motion+tilt; "IMMERSIVE MOTION" or a subtitle ("slow zoom + tilt
  parallax") in the sheet is clearer.
- **S2 — No preview of effect** in the picker sheet itself — the LIVE
  LOOK pane shows it, but a tiny hint line in the toggle row
  ("subtle zoom · responds to tilt") sets expectations.
- Covered elsewhere: 12s liquid snap (B1), multi-instance waste (B4),
  builder side-effect (C8), app-level pref contract (U-006, done).

### Living preview session (`studio_flow.dart`)

- **Good:** real `ActiveRunScreen` on isolated mock `RunProvider`, random
  loot per open, casino re-roll, RUN/BROWSE dock, nested back pops levels,
  `_mpShield` prevents real-session leakage.
- **S2 — Session seed label.** Masterplan leftover: tiny seed/version
  stamp in the preview chrome ("SEED a3f9") so bug reports can reference
  exactly what was on screen. Cheap, high diagnostic value.
- **S2 — `ItemIconField`/particle preview ignores `reduceMotion`** in
  studio paths (`_ParticlePreview`, LIVE LOOK call
  `buildBackdropParticleField` without the flag) — reduced-motion users
  see animated previews. Pass the flag through.
- **S3 — Preview could demo the liquid tank too** — AMBIENCE changes are
  the least visible in the run preview since the tank sits behind
  content; a peek isn't necessary if LIVE LOOK covers it.

### Cross-cutting UX notes

- **S2 — Haptics coverage is good** (selection on every pick); add the
  two missing punctuation points above (READY, LINKED).
- **S2 — Consistent "active" language:** LOOKS tiles, TYPE tiles, icon
  tiles, liquid chips, immersive toggle all use the same
  primary-tint+border pattern — good. Keep it; the CUSTOM-chip idea
  (LOOKS) extends the language honestly.
- **S3 — Delight budget:** the VS splash is the emotional peak of MP;
  the studio is the craft surface. Don't add more ambient motion to the
  studio — it competes with the content being edited. Current balance is
  right.

---

## Recommended sequencing

1. **Batch A1–A9** (MP handshake hardening + protocol v4 + layout) — one
   focused session; all in `mp_*`/`mp_connect_screen` + tests. Highest
   user-facing risk.
2. **B1 + C7** (liquid snap + NaN guard) — small, visible-quality fixes.
3. **C1 + C3 + C6 + C4** (persistence clamps, sprite validation, chip
   label, JSON gaps) — one "honesty" pass.
4. **B3 + B4** (particle/wallpaper dedupe) — perf pass, needs care.
5. **UX S1/S2 items** — fold into the batches above where they share
   files (A7 layout, LOOKS CUSTOM chip + mutual-exclusion hint, favorites
   discoverability, splash haptics).
6. **P3 deferred bugs** — separate sessions per item.

**Ownership note:** Slot 4's QA sweep has uncommitted fixes in
`avatar_frame.dart`, `theme_flair_prefs.dart`,
`experience_studio_screen.dart`, `custom_wallpaper_test.dart` (U-006,
U-007). Coordinate before touching those files; remaining `_AvatarIdle`
work is TickerMode gating only.

**Version note:** A9's protocol bump + any persisted-pref changes argue
for v3.6.1 (patch) rather than folding silently into v3.6.0 — the
lockstep checklist applies.
