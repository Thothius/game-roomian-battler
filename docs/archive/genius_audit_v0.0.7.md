# GungeonMate — Genius-Tier App Audit (Protocol v0.0.7-GENIUS-AUDIT)
> Conducted 2026-08-18 by Coder (Slot 2) on master branch
> All findings verified by direct grep/read of the codebase
> **User decisions locked 2026-08-18 — see below**

---

## Part I: Comprehensive App & Feature Appraisal

### 1. Active Run & Dashboards
**Files:** `lib/widgets/active_run/` (10 files, 200+ GoopText/Text instances)

**Finding:** Stat values (DPS, damage, armor, coolness, curse, ammo, Hegemony Credits) are displayed as **plain `GoopText` widgets that hard-swap on value change**. Zero `AnimatedNumber`, `TweenAnimationBuilder`, or `AnimatedSwitcher` usage in `stat_sheets.dart`, `player_header.dart`, or `summary_tab.dart`.

**Impact:** During frantic combat, the user's eye is not drawn to state changes. A DPS jump from 168 → 240 just flashes the new number with no motion cue.

**Glanceability:** Stats are grouped into dashboards (compact, huntress, junkan) but there's no "Combat Focus Mode" that dims non-essential UI. All telemetry is equally weighted visually.

### 2. Codex & Ammonomicon
**Files:** `lib/screens/codex_screen.dart`, `lib/widgets/codex/ammonomicon_tabs.dart`

**Finding:** Rich offline-first data. The codex is a static reference — no dynamic synergy triggers, no "this item appears in your current run" highlighting, no discovery engine.

### 3. Synergy & Damage Engines
**Files:** `lib/screens/synergies_overview_screen.dart`, `lib/services/damage_calculator.dart`

**Finding:** The synergy tracker shows `status.missing` items (the "needs N" badge) but has **no predictive features**:
- No "shop items that would complete this synergy" scanner
- No "optimal gun swap" recommender
- No historical boss-encounter data integration
- No "partial synergy glow fill" animation as components are acquired

The damage calculator is invaluable but outputs static numbers — no kinetic roll-up animation.

### 4. Multiplayer Co-op Protocol
**Files:** `lib/services/multiplayer_session.dart` (100+ reconnect-related matches)

**Finding:** Multiplayer is **already robust** — this is the app's strongest infrastructure area:
- ✅ Auto-reconnect with exponential backoff (max 30s)
- ✅ Adaptive watchdog (30s → 60s on false positives)
- ✅ Pause/resume with persisted flag
- ✅ Pending-gift tracking (re-send on reconnect, restore on cancel)
- ✅ App lifecycle observer (immediate reconnect on foreground)
- ✅ Persisted session restore on app-kill
- ✅ `peerLikelyGone` detection after 10 attempts
- ✅ `reconnectSuccessNotifier` for "Connection Restored" popup
- ✅ Reconnection Hub for manual PIN re-pair

**Gaps:**
- No synced animated latency indicator (dice roll shows network health)
- No event-log pattern with hash verification (current state-sync could drift on partial drops)
- PIN keypad has no spring-physics feedback

### 5. RepaintBoundary Audit (CRITICAL GAP)
**Count:** 3 RepaintBoundary wrappers for 11 CustomPaint widgets

| CustomPaint widget | Has RepaintBoundary? |
|-------------------|---------------------|
| `particle_engine.dart` (ParticleField) | ✅ Yes |
| `avatar_aura.dart` | ✅ Yes |
| `particles/crimson_drip.dart` | ✅ Yes |
| `home/vortex_lightning.dart` (3 painters) | ❌ NO |
| `home/junk_particle_field.dart` | ❌ NO |
| `theme_overlay.dart` | ❌ NO |
| `periodic_tile.dart` (3 painters) | ❌ NO |
| `backgrounds/gungeon_fall_animation.dart` | ❌ NO |
| `active_run/dice_roll.dart` | ❌ NO |
| `particles/curse_fog.dart` | ❌ NO |
| `particles/touch_particle.dart` | ❌ NO |
| `theme_engines.dart` | ❌ NO |

**8 CustomPaint widgets lack RepaintBoundary.** This means animated regions may trigger full-tree repaints, causing frame drops on lower-end devices.

### 6. State Persistence Integrity
**Files:** `lib/services/app_theme.dart`

**Finding:** No schema version field exists. Enum indices are **clamped** to valid ranges (`particlePresetIdx.clamp(0, ParticlePreset.values.length - 1)`) which prevents crashes but silently maps stale indices to the last valid enum value. Key names include version suffixes (`_v1`, `_v3`) but there's no coordinated migration logic — legacy keys like `_kScaleLegacy` are handled ad-hoc.

**Risk:** When new VisualPrefs fields are added (like the recent `runDisplayMode`), old installs default to `0` (first enum value) silently. No user notification, no migration prompt.

### 7. Particle Engine Safety Limits
**Files:** `lib/widgets/particle_engine.dart`

**Finding:** `ParticleField` has `this.count = 16` default with **no upper clamp**. The O(n²) line-link check has a `ponytail:` comment noting "At count=32 that's 496 pairs — fine. If max count ever increases above ~64, switch to spatial hashing." But nothing prevents a caller from passing `count: 1000`, which would cause 499,500 pair checks per frame.

**No frame-rate throttling** exists. The ticker runs at vsync (60/120Hz) regardless of device capability.

---

## Part II: 5 Genius-Level Creator Questions

### Question 1: Active Run glanceability — how should we optimize for frantic combat?

**Grounded in:** 200+ hard-swap stat texts in `lib/widgets/active_run/`, zero animated numbers, no combat focus mode.

### Question 2: Synergy engine — how to add predictive power without clutter?

**Grounded in:** `synergies_overview_screen.dart` shows `status.missing` but has no shop scanner, no partial-synergy glow, no gun-swap recommender.

### Question 3: Experience Studio — how to elevate from picker to standout feature?

**Grounded in:** Theme picker already has 37 presets, 11 glow effects, 16 schemas, 12 named glow colors, live preview. But no theme sharing, no ambient fragment shaders, no auto-tuner.

### Question 4: Multiplayer — what's the next resilience frontier?

**Grounded in:** Auto-reconnect already robust (backoff, watchdog, pause, lifecycle observer, pending gifts). Gaps: no latency indicator, no event-log hash verification, no PIN keypad spring physics.

### Question 5: Collective Brain — how to structure agent learning without bloat?

**Grounded in:** `MUTATION_STATION/syntax_patches/` already has 2 archived files. No `MEMORIES_AND_SKILLS/` directory exists yet. Memory files are in `C:\Users\saare\.codeium\windsurf\memories\` (100+ .pb files, unstructured).

---

## Part III: User Decisions (Locked 2026-08-18)

| # | Question | Selected Path | Tier |
|---|----------|---------------|------|
| Q1 | Active Run glanceability | **Glowing synergy borders** — CustomPainter glowing borders around active synergy trackers for peripheral awareness | Animation R&D |
| Q2 | Synergy engine expansion | **Synergy Predictor** — Scan player's loadout and highlight shop items that complete hidden synergies | Genius UX |
| Q3 | Experience Studio elevation | **Ambient fragment shaders** — Layer customizable background fragment shaders (digital rain, dark-neon fog) into theme engine | Animation R&D |
| Q4 | Multiplayer + Collective Brain | **RepaintBoundary templates** — Archive modular UI animation templates with pre-tested RepaintBoundary configs (addresses 8 missing wrappers found in audit) | Animation R&D |

### Implementation Priority (proposed)
1. **RepaintBoundary templates** (Q4) — lowest risk, directly addresses the 8 missing wrappers found in audit. Foundation for all other animation work.
2. **Glowing synergy borders** (Q1) — builds on RepaintBoundary foundation. CustomPainter work, reuses particle glow patterns from MUTATION_STATION.
3. **Synergy Predictor** (Q2) — new predictive engine. Requires scanning loadout against synergy database. No UI clutter — highlights existing shop items.
4. **Ambient fragment shaders** (Q3) — most experimental. Requires FragmentShader GLSL work. Highest visual impact but newest territory.
