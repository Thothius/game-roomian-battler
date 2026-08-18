# Adversarial Penetration Test & Stress Evaluation
> Protocol: v0.0.7-GENIUS-AUDIT (adversarial mode)
> Conducted by: Slot 2 — Coder-Maintainer-Reworker-Genius
> Date: 2026-08-18
> Method: grep-verified findings against actual codebase, not speculation

---

## Part I: State Architecture Race Conditions

### CRITICAL: notifyListeners() storm in RunProvider

**Finding:** `run_provider.dart` has **60 `notifyListeners()` calls** — many fire after every single async setter completes. There is no batching, no debounce, no `_isNotifying` guard.

**Attack vector:** Rapid-fire UI interactions (e.g. tapping Robot Armor +1, +1, +1 in quick succession) each trigger:
1. `setRobotArmor(armor)` → async `prefs.setInt()` → `notifyListeners()`
2. `setRobotArmor(armor+1)` → async `prefs.setInt()` → `notifyListeners()`
3. `setRobotArmor(armor+2)` → async `prefs.setInt()` → `notifyListeners()`

Each call is async with no mutual exclusion. The three `prefs.setInt()` calls can interleave, and the last one to complete wins — but `notifyListeners()` fires 3 times, causing 3 rebuilds for what should be 1 state change.

**Severity:** MEDIUM — causes excess rebuilds and potential visual flicker, but data integrity is OK because SharedPreferences writes are serialized internally by the platform.

**Hardening:** Add a batch/debounce pattern:
```dart
bool _notifyScheduled = false;
void _scheduleNotify() {
  if (_notifyScheduled) return;
  _notifyScheduled = true;
  SchedulerBinding.instance.addPostFrameCallback((_) {
    _notifyScheduled = false;
    notifyListeners();
  });
}
```
Then replace bare `notifyListeners()` in async setters with `_scheduleNotify()`.

### HIGH: Async setters fire-and-forget — no await at call sites

**Finding:** Every `setRobot*`, `setHuntress*`, `setGunderfury*` etc. is `Future<void>` but callers don't await them. Example: `setRobotArmor(5)` is called without `await`, so the UI proceeds assuming the write completed.

**Attack vector:** If the user navigates away immediately after changing a stat, the async `prefs.setInt()` may not complete before the widget tree disposes. The data is lost silently.

**Severity:** LOW-MEDIUM — SharedPreferences writes are fast (<5ms) and the window is tiny, but it's a real data-loss path on app-kill during the await.

**Hardening:** Either (a) await at call sites, or (b) accept the risk and document it. Option (a) is cleaner but requires changing every caller. Option (b) is the pragmatic choice — the window is <5ms.

### MEDIUM: No write coalescing for _saveRun()

**Finding:** `_saveRun()` is called 20+ times across the file. It does `jsonEncode(_runState.toJson())` + `prefs.setString('current_run', encoded)` every time. If the user adds 3 items in quick succession, that's 3 full JSON serializations + 3 disk writes.

**Attack vector:** On a complex run state (10 guns, 20 items, shrines, coolness, curse), each `_saveRun()` could be 2-5KB of JSON. Three rapid calls = 3 serializations that could stutter on low-end devices.

**Severity:** LOW — JSON encode of 5KB is <1ms on modern devices, but could matter on older Android.

**Hardening:** Add a write debounce — collect changes for 500ms then write once:
```dart
Timer? _saveDebounce;
void _saveRun() {
  _saveDebounce?.cancel();
  _saveDebounce = Timer(const Duration(milliseconds: 500), () async {
    // actual save logic
  });
}
```

---

## Part II: Git Workflow Edge Cases

### CRITICAL: Nested dual-repo structure is a trap

**Finding:** `X:\apps\GungeonMate\` is a git repo (remote: `game-roomian-battler.git`) that **gitignores** `gungeon_mate/`. Inside `gungeon_mate/` is a **separate git repo** (remote: `GungeonMate.git`). They have no submodule link.

**Attack vectors:**
1. **Agent commits to wrong repo:** I already hit this twice this session — committed MUTATION_STATION to the root repo when it should have been in gungeon_mate, and had to cherry-pick between branches.
2. **Branch confusion:** `git checkout master` in the root repo does NOT switch gungeon_mate's branch. An agent could think they're on master but be on a feature branch in the nested repo.
3. **AC5 branch rules don't specify which repo:** "Create branch: `git checkout -b slot2-coder/feature`" — but which repo? If the agent is editing `lib/` files, it's gungeon_mate. If editing `docs/` or `AGENTS.md`, it's the root repo. Both need branches.
4. **Pre-session sync (AC5b) only pulls one repo:** `git pull origin master` in root doesn't sync gungeon_mate.

**Severity:** HIGH — this has already caused real merge confusion this session.

**Hardening:** Add to AC5:
> **Nested repo awareness:** This workspace has two git repos:
> - **Root repo** (`X:\apps\GungeonMate\`): tracks `AGENTS.md`, `AGENT_STATUS.md`, `docs/`, `MUTATION_STATION/`. Remote: `game-roomian-battler.git`.
> - **App repo** (`X:\apps\GungeonMate\gungeon_mate\`): tracks all `lib/`, `assets/`, `pubspec.yaml`. Remote: `GungeonMate.git`.
> - Before branching, identify which repo your changes touch. If both, branch in both.
> - Pre-session sync (AC5b) must pull BOTH repos: `git pull` in root AND in gungeon_mate.

### MEDIUM: Slot 3's unmerged branch is a drift hazard

**Finding:** `coder/active-run-rework` branch in gungeon_mate has Phase 1 committed (`4e5940b`) but NOT merged to master. Master has advanced with particle engine work (`e7eefbb`), animation assessment (`5f23c6e`), genius audit (`e275534`), and protocol changes.

**Attack vector:** When Slot 3 resumes and tries to merge, `coder/active-run-rework` will be behind master by 5+ commits. The rebase could conflict on `app_theme.dart` (both branches modified it) and `experience_studio_screen.dart` (Slot 3 marked it off-limits but master advanced it).

**Severity:** MEDIUM — the conflict is resolvable but will require careful manual merge.

**Hardening:** Add to AC5:
> **Unmerged feature branches must rebase within 24h of master advancing.** If your branch is behind master by more than 3 commits, rebase before continuing work. This prevents accumulation of merge debt.

---

## Part III: Multi-Agent Workflow Friction

### MEDIUM: Shared Core file coordination has no timeout

**Finding:** The protocol v0.0.2 proposal (now locked) adds `app_theme.dart`, `particle_engine.dart`, `run_provider.dart`, `theme_overlay.dart` as Shared Core files requiring announced intent. But there's no timeout — an agent can claim `app_theme.dart` and hold it indefinitely.

**Attack vector:** Slot 1 claims `app_theme.dart` for a 2-hour animation task. Slot 2 needs to add a VisualPrefs field for a new feature. Slot 2 is blocked for the entire duration with no recourse.

**Severity:** MEDIUM — real friction in a 4-slot setup.

**Hardening:** Add to AC7:
> **Shared Core claims auto-expire after 1 hour of heartbeat staleness.** If the claiming agent's heartbeat is >1h old, the file is considered unclaimed and another agent can claim it (with a board note).

### LOW: Slot 4 (Universal Worker) has no domain boundary

**Finding:** The four-slot roster defines Slot 4 as "can step into any domain" but doesn't specify what files it can touch. This creates ambiguity vs. the Coder domain ownership rules.

**Severity:** LOW — hasn't caused issues yet because Slot 4 hasn't been used.

**Hardening:** Add to the roster:
> **Slot 4 file scope:** Universal Worker can touch any file NOT listed in another slot's "Files in progress" or in the Shared Core section. For Shared Core files, Slot 4 follows the same AC7 claim protocol as other slots.

---

## Part IV: Hardening Steps (Prioritized)

### Immediate (this session)
1. **Document the nested dual-repo structure in AC5** — prevents the #1 source of git confusion
2. **Add rebase-within-24h rule for unmerged branches** — prevents merge debt accumulation

### Short-term (next few sessions)
3. **Add notifyListeners() batching to RunProvider** — eliminates the 60-call rebuild storm
4. **Add Shared Core claim timeout (1h heartbeat staleness)** — prevents indefinite file locks
5. **Add Slot 4 file scope clarification** — removes domain ambiguity

### Long-term (post-release)
6. **Add _saveRun() write debounce** — coalesces rapid saves into single disk writes
7. **Consider SharedPreferences write queue** — guarantees write ordering for rapid-fire stat changes

---

## Part V: Advanced Implementation Candidates (assessed 2026-08-18)

Extracted from external framework suggestions, filtered against actual codebase gaps.

### High-impact (do soon)
1. **Selector partitioning in RunProvider** — wrap high-frequency display widgets (ammo, armor, coolness, curse counters) in `Selector<RunProvider, T>` so they only rebuild when their specific slice changes. Directly addresses the 60-notifyListeners storm. Highest-impact performance fix available.
2. **Spring-damped scale responses** — replace `Curves.easeInOut` with `Curves.easeOutBack` (card entrances), `Curves.elasticOut` (playful bounces), `Curves.fastOutSlowIn` (drawers) in touch interactions. Audit found zero spring curves — this is the #1 tactile feel gap.
3. **Schema migration parser** — add `_kSchemaVersion` int to SharedPreferences + boot-time upgrade path. Prevents silent enum remapping when new VisualPrefs/RunProvider fields are added. Real gap found in audit.

### Medium-impact (do when complex feature warrants it)
4. **DAG task mapping** — for multi-file features like Device Pairing (Task 21), decompose into a markdown DAG with upstream prerequisites and downstream side effects before coding. Not for every task — only features touching 4+ files.
5. **Decision Log** — lightweight `docs/decision_log.md` recording architectural choices + discarded alternatives (e.g. "chose Provider over Riverpod because..."). Not a master plan, just a "why X over Y" reference for future sessions.

### Skipped (assessed and rejected)
- Immutable state snapshotting — massive refactor, Ponytail says current Provider + Selectors covers it
- Shader pre-warming — no shaders exist yet, premature
- Zero-cloud contract — already enforced by design
- Automated static guardrails — already have /bughunt-proof, /frame-audit, /state-audit commands
- master_plan.md — explicitly rejected in protocol v0.0.2

---

## Part VI: Rendering & Design System Assessment (2026-08-18)

Assessed 20+ external suggestions against actual codebase. Findings:

### Already implemented (no action needed)
- Zero-allocation particle pooling — `_respawnParticle` mutates existing objects in-place, no per-frame allocation
- V-Sync frame lock — particle engine uses `SingleTickerProviderStateMixin` + vsync-driven `AnimationController`
- Haptic-synced visual pulses — `haptics.dart` service + `HapticFeedback` calls in dashboards (BUG-053)
- BackdropFilter avoidance — vortex explicitly uses `ImageFiltered` over `BackdropFilter` (documented in `vortex_config.dart`)
- Opacity leaf-level — all 14 `Opacity()` usages are on individual icons/containers, not wrapping large subtrees
- Flavor-title presets — 37 particle presets + 11 glows + 16 schemas + 12 named glow colors already exist
- Intelligent fallback — `app_theme.dart` migrates stale themes to `kVisibleThemes.first`, enum indices clamped
- Granular override as diff — VisualPrefs stores individual fields in SharedPreferences (is a diff patch)
- 48dp touch targets — BUG-051 fixed sub-minimum targets, BUG-052 added tooltips

### Useful — log for future implementation
6. **Double-buffered painter offscreen rasterization** — cache static particle background layers onto `ui.Picture`, composite only dynamic sprites per frame. Relevant for the 8 missing RepaintBoundary wrappers.
7. **Surface hierarchy (3 tiers)** — formalize `SurfaceTier.base/floating/overlay` enum with mapped container colors. Low effort, real consistency gain. Currently `0xFF1E1E22` is used ad-hoc.
8. **One-click preset reset in Experience Studio** — verify a "reset to defaults" button exists; add if missing. Small win.
9. **Boss Encounter HUD** — new `RunDisplayMode` that auto-triggers on boss rooms, strips non-essential clutter, expands DPS/armor/weapon into large high-visibility nodes with pulsing neon warning borders. Best new view mode idea — genuinely useful during actual gameplay. Requires boss detection input from user.
10. **Minimalist Peripheral HUD ("Ghost Glass")** — corner-only ultra-thin semi-transparent indicators that flare on critical events (low health, item trigger). Pairs with Combat Focus Mode (Q1).
11. **Compact Combat Bar** — single-line ticker mode for peripheral glanceability during heavy bullet-hell. Pairs with Combat Focus Mode (Q1).

### Skipped (assessed and rejected)
- Subpixel text snap — Flutter handles this; manual intervention fights the framework
- GPU color matrix tinting — no shaders exist, premature
- 8pt harmonic grid — massive refactor of every spacing constant for no user-visible benefit
- Polymorphic pill-button-tab engine — abstraction nobody asked for (Ponytail #1)
- Theme-linked layout tokens — low priority, current ThemeFlair covers colors adequately
- Unified typography scaling — over-engineering, google_fonts + ThemeFlair sufficient
- Speedrun & Split Timer — requires floor timing infrastructure we don't have, niche audience
