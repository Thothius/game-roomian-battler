# GungeonMate — Technical Reference for All Agents

> **READ THIS BEFORE ANY WORK.** This is the canonical technical reference.
> Every agent must know these facts at all times. No exceptions.
>
> Last updated: 2026-10-31 (v3.3.0+162) — **v3.3 delta below supersedes v2-era sections where they conflict.**

---

## 0. v3.x Delta (read first — v2 sections below kept for history)

**Current version:** `3.3.0+162` · **Flutter 3.47.9** / Dart 3.13.7 · **Test suite:** ~477 tests (was 199).

**What's actually current (post-v2.1.0):**

- **Multiplayer (v3 unified).** One co-op protocol on a single Nearby serviceId `mp.v2` — classic and Paradox modes merged (`170e70b`). Paradox is a *character pick* (blank-start inventory), not a mode. `mp_session.dart` facade + `mp/` services (`mp_link`, `mp_sync`, `mp_recovery`, `mp_store`, `mp_foreground_service`, `mp_transport`) + `session/mp_handlers.dart` part file. Screens: `mp_lobby_screen.dart` (3-stage flow: role → gungeoneer → identity w/ host-only RUN TITLE field) + `mp_connect_screen.dart` (themed card shell, per-phase accents). `multiplayer_lobby_screen.dart` deleted. Chat deleted; `paradox/` widgets serve ALL MP (ParadoxBar unified top bar w/ runTitle, ParadoxPlayerPanel ⋮ menu, SurpriseSheet). `MpReconnectBanner` gated by `runBarVisible` (two-bars fix `c5ba8db`).
- **Bottom nav = 3 tabs** (Inventory / Browse / Ammonomicon) + gear sheet in active-run header owns Settings/Quiz/run tools (`49e1f25`..`f46a361`). The v2 "4 tabs + Settings screen" description is stale.
- **Ammonomicon** (renamed from Codex): `ammonomicon_screen.dart` 12-tab picker w/ expandable Chapters/GameModes panels, `ammonomicon_widgets.dart` (part), `ammonomicon_detail_screen.dart`, `widgets/ammonomicon/ammonomicon_tabs.dart`, `synergy_detail_screen.dart`. Data: `chapters.json`, `game_modes.json`, `back_refs.json` all declared+loaded.
- **Item detail** surfaces `ammonomicon_entry` (AmmonomiconCard), wiki sections (guns AND items), and ReferencedBySection back-refs (`1b4400d`).
- **Run title:** `MpSession.runTitle` set from lobby, shown in ParadoxBar + connect chip.
- **Still accurate below:** repo structure (§1), git/push workflow (§2), build commands (§3), release checklist (§4), PowerShell gotchas (§7), board protocol (§8-§10), platform quirks (§12).
- **Stale below:** §5 architecture tables (v2-era — see delta), §6 file locations (line counts/mode tables), §6.5 test counts, version fields throughout.

---

## 1. Repository Architecture

There are **two independent git repositories**:

| Repo | Path | Remote | Tracks |
|------|------|--------|--------|
| **Root** | `X:\GungeonMate` | `https://github.com/Thothius/game-roomian-battler.git` | `AGENTS.md`, `AGENT_STATUS.md`, `docs/`, `.windsurfrules` |
| **App** | `X:\GungeonMate\gungeon_mate` | `https://github.com/Thothius/GungeonMate.git` | All `lib/`, `assets/`, `pubspec.yaml`, `test/` |

**Critical:** `gungeon_mate/` is gitignored in the root repo. The two repos are fully independent. An app-repo worktree does NOT need a root-repo worktree and vice versa.

---

## 2. Git Authentication & Push Workflow

### Credentials

| Tool | Status | Location |
|------|--------|----------|
| **GitHub CLI (`gh`)** | Authenticated as `Thothius` (keyring) | `C:\Program Files\GitHub CLI\gh.exe` |
| **Git Credential Manager** | v2.5.0 installed | Configured via `gh auth setup-git` |
| **SSH keys** | NOT configured | Do not use SSH remotes |
| **HTTPS remotes** | Working with `gh` credential helper | Use HTTPS, not SSH |

### Push procedure (MUST follow exactly)

```powershell
# 1. Ensure gh credential helper is set up (run once per session if push fails):
gh auth setup-git

# 2. Push the app repo:
cd X:\GungeonMate\gungeon_mate
git push origin master

# 3. Push the root repo (if root files changed):
cd X:\GungeonMate
git push origin master
```

### Common push errors

| Error | Cause | Fix |
|-------|-------|-----|
| `could not read Username for 'https://github.com'` | No credential helper | Run `gh auth setup-git` |
| `Permission denied (publickey)` | Remote set to SSH | `git remote set-url origin https://github.com/Thothius/<repo>.git` |
| `gh: command not found` | Not in PATH | Full path: `& 'C:\Program Files\GitHub CLI\gh.exe' auth status` |

### Git config (global)

```
user.name=Kristjan
user.email=saaremets.kristjan@gmail.com
pull.rebase=true
init.defaultbranch=master
core.autocrlf=true
```

---

## 3. Flutter & Build Commands

### Flutter SDK

| Property | Value |
|----------|-------|
| **Flutter path** | `C:\src\flutter\bin\flutter.bat` |
| **Flutter version** | 3.47.9 (stable, 2026-10-30 upgrade) |
| **Dart version** | 3.13.7 |
| **Android toolchain** | Gradle 8.14 · AGP 8.13.0 · Kotlin 2.2.20 · compileSdk 37 · NDK 28.2.13676358 |
| **App repo working dir** | `X:\GungeonMate\gungeon_mate` |

### All agents MUST use the full path to flutter:

```powershell
& 'C:\src\flutter\bin\flutter.bat' <command>
```

**Never** run bare `flutter` — it's not in PATH.

### Essential commands

```powershell
# Analyze (MUST pass before any commit):
& 'C:\src\flutter\bin\flutter.bat' analyze lib/

# Analyze specific files:
& 'C:\src\flutter\bin\flutter.bat' analyze lib/widgets/active_run/modes/theme_signature_mode.dart

# Get dependencies (after pubspec.yaml changes):
& 'C:\src\flutter\bin\flutter.bat' pub get

# Build APK (release):
& 'C:\src\flutter\bin\flutter.bat' build apk --release

# Build Windows (desktop):
& 'C:\src\flutter\bin\flutter.bat' build windows

# Run in debug:
& 'C:\src\flutter\bin\flutter.bat' run
```

### Analyze timeout

`flutter analyze lib/` can take 10-20 seconds. Use `timeout: 280000` (ms) in exec calls. If no output after 10s, it's running in background — use `get_output` with `timeout: 120000`.

---

## 4. Release Checklist (MANDATORY for version bumps)

When bumping the version, ALL of these files must be updated in lockstep:

| File | What to update |
|------|----------------|
| `gungeon_mate/pubspec.yaml` | `version: X.Y.Z+BUILD` |
| `gungeon_mate/lib/utils/asset_paths.dart` | `const String kAppVersion = 'X.Y.Z';` |
| `gungeon_mate/assets/data/changelog.json` | New entry at top of array |
| `gungeon_mate/VERSION_HISTORY.md` | New section at top |
| `gungeon_mate/lib/screens/main_menu_screen.dart` | Imports `kAppVersion` from `asset_paths.dart` — no hardcoded version string |

**Version format:** `MAJOR.MINOR.PATCH+BUILD` (e.g. `2.1.0+150`). The `+BUILD` number increments with every release. The `PATCH` increments for features/fixes.

**Current version:** `2.1.0+150`

### Changelog entry format

```json
{
  "version": "v1.9.XX",
  "title": "Short title",
  "date": "August 2026",
  "items": [
    "FEATURE: ...",
    "FIX: ...",
    "INFRASTRUCTURE: ..."
  ]
}
```

### VERSION_HISTORY entry format

```markdown
## v1.9.XX — Emoji Title (August 2026)
**Build:** XXX

> One-line summary.

### New Features
- **Feature name** — description

### Infrastructure
- `path/to/file.dart` — what changed
```

---

## 5. Current App Architecture (v2.1.0)

### Active Run Display Modes

**Removed in v2.0.2–v2.0.3.** The active run screen previously supported
4 display modes (Classic Scroll, Codex Book, Compact Run, Theme Signature)
via a `RunDisplayMode` enum. All mode widgets, the `RunDisplayModeBar`,
and the `RunDisplayMode` enum itself were deleted in the v2.0.2–v2.0.3
cleanup (`d5dfc9e`). The active run screen now uses a single Classic
Scroll mode rendered by `PlayerPage`. No residual `RunDisplayMode` code
remains in the codebase.

### Theme System

| Component | Location |
|-----------|----------|
| `AppThemeMode` enum | `lib/services/theme/app_theme_modes.dart` (part of app_theme) |
| `ThemeFlair`/`VisualPrefs` | `lib/services/theme/theme_flair_prefs.dart` (part of app_theme) |

| `kVisibleThemes` list (15 active, 12 commented out) | `lib/services/app_theme.dart` |
| `kPickerThemes` list (8 curated with splash graphics) | `lib/services/app_theme.dart` |
| `ThemeOverlay` (global visual stack) | `lib/widgets/theme_overlay.dart` |
| `ThemeLore` registry (14 entries) | **Deleted** (v2.0.2) — was `lib/widgets/active_run/modes/theme_lore.dart` |

**Theme lists:**
- `kPickerThemes` (8 shown in theme picker, all have splash graphics): Unicorn, Forge Master, Moonlit Chamber, The Bullet, The Paradox, Dragunfire, Lich's Domain, Gunpowder.
- `kVisibleThemes` (15 active): Minimalist + 8 picker themes + Robot's Core, Cat Lady, Storm Caller, Mr. Robot, Valor of Marines, Custom.
- 12 themes commented out (no splash graphic yet): The Cultist, The Gunslinger, The Convict, The Hunter, The Pilot, The Rat, Breach Gateway, Lead Lord Keep, Oubliette Pit, Black Powder Mine, Bullet Hell Floor, R&G Department.
- All 14 splash JPGs are 1200×1200 (recompressed from 2048×2048 in v2.1.0).
- `errorBuilder` on all splash `Image.asset` calls falls back to radial gradient if file is missing.

### VisualPrefs fields (persisted to SharedPreferences)

All fields follow this pattern:
1. Field on `VisualPrefs` class with default
2. `_k<Field>` SharedPreferences key constant
3. Load in `VisualPrefs.init()` 
4. Setter: `VisualPrefs.set<Field>(v)` → `_with()` → `_persist()`
5. `_with()` parameter + assignment

Key fields:
- `shaderEnabled` (bool, default: `false`)
- `shaderPreset` (ShaderPreset, default: `digitalRain`)

### Video Player

| Component | Package | Platforms |
|-----------|---------|-----------|
| `video_player` | `^2.9.2` | Android, iOS, macOS, Web |
| `video_player_media_kit` | `^2.0.0` | Windows, Linux (libmpv backend) |
| `media_kit_libs_windows_video` | `^1.0.11` | Windows video libs |

**Init:** `VideoPlayerMediaKit.ensureInitialized(windows: true)` in `main.dart` before `runApp`.

**Usage:** `AnimatedWallpaperBackground` widget in `lib/widgets/backgrounds/animated_wallpaper.dart`. Plays `gungeonmate-animation-02.mp4` on the home screen. Falls back to `_VortexFallbackPainter` (CustomPaint) if video init fails. The unused `wp_anim_01_galaxy.mp4` was deleted in v2.1.0 (8.9MB dead asset).

### GungeonMeter (Interactive Coolness/Curse Meter)

| File | Purpose |
|------|---------|
| `lib/widgets/active_run/gungeon_meter.dart` | Custom-painted horizontal fill bar |
| `lib/screens/stats_detail_screen.dart` | Used in stats detail (replaces LinearProgressIndicator) |
| `lib/widgets/active_run/modes/codex_book_mode.dart` | Used in Codex Book left page |
| `lib/widgets/active_run/modes/theme_signature_mode.dart` | Used in Theme Signature mode |

**Threshold:** 10.0 = Lord of the Jammed (curse) / max effective (coolness). Provider clamps to -100..100. Visual range 0..15.

### Mode Picker Onboarding

| File | Purpose |
|------|---------|
| `lib/widgets/active_run/modes/mode_picker_onboarding.dart` | Fullscreen dialog with animated mode previews |

**Trigger:** Was triggered after `startNewRun` in `character_select_screen.dart`, but user removed the trigger (2026-08-18). `showModePickerOnNewRun` default is now `false`. The dialog widget still exists and can be re-wired if needed.

### Settings Screen (v2.1.0)

| File | Purpose |
|------|---------|
| `lib/screens/settings_screen.dart` | Single-tab layout (SettingsTab only) |
| `lib/widgets/settings/settings_tab.dart` | Settings tab — run tools, dice, MP, data, dev, danger |

**v2.1.0 reorganization:**
- Single tab (Appearance tab deleted — theme selection moved to Experience Studio).
- Sections: RUN TOOLS, DICE (style + roll), MULTIPLAYER (hidden when solo), DATA & STORAGE, DEV TOOLS.
- "Save Run" always visible (was hidden during MP).
- "DEBUG" renamed to "DEV TOOLS".
- Bottom danger actions: END RUN, RESET DATA (full-width).

**Deleted files (v2.0.4–v2.1.0):**
- `lib/widgets/settings/theme_visuals_tab.dart` (Appearance tab, 691 lines)
- `lib/widgets/settings/run_log_screen.dart` (orphaned, 271 lines)
- `lib/widgets/settings/gameplay_tab.dart` (v1.9.62)
- `lib/widgets/settings/run_tab.dart` (v1.9.62)

### Experience Studio (v1.9.61+)

| File | Purpose |
|------|---------|
| `lib/screens/experience_studio_screen.dart` | Theme picker + customization (tabbed, with fullscreen preview) |

**v1.9.61:** 14 theme splash images in `assets/images/themes/splash/`. Each theme card shows its splash as background. `AppThemeMode.splashSlug` getter maps themes to asset slugs. `themeSplashPath()` helper in `asset_paths.dart`.

**v2.1.0:** Splash JPGs recompressed from 2048×2048 to 1200×1200 (45.75MB → 1.51MB total). `errorBuilder` added to all splash Image.asset calls for graceful fallback.

**Redesign complete:** 4-tab picker (Theme / Particles / Typography / Ambiance). Side bookmark button opens fullscreen preview. `_PaletteStep` deleted.

---

## 6. Key File Locations

### Core

| File | Purpose |
|------|---------|
| `lib/main.dart` | App entry point, `VideoPlayerMediaKit.ensureInitialized` |
| `lib/providers/run_provider.dart` | State management (1618 lines) |
| `lib/services/app_theme.dart` | Theme engine hub (479 lines) + `theme/` part files: app_theme_modes (enum+lore), theme_data_tables, theme_flair_prefs, theme_custom_data, theme_store, theme_misc_enums |
| `lib/widgets/theme_overlay.dart` | Global visual stack (layers 0-1.0) |
| `lib/screens/home_screen.dart` | Home screen routing (MainMenu vs ActiveRunScreen) |
| `lib/screens/active_run_screen.dart` | Active run screen (964 lines) |
| `lib/widgets/active_run/player_page.dart` | Per-player page with mode routing |

### Active Run Modes

**Note:** Matrix mode, Codex Book, Compact Run, Theme Signature, RunDisplayModeBar, and ModePickerOnboarding were all deleted in v2.0.2–v2.0.3 cleanup (`d5dfc9e`). The active run screen now uses a single Classic Scroll mode. The `RunDisplayMode` enum and all related VisualPrefs fields were fully removed — no residual code remains.

| File | Status |
|------|--------|
| `lib/widgets/active_run/modes/codex_book_mode.dart` | **Deleted** (v2.0.2) |
| `lib/widgets/active_run/modes/compact_run_mode.dart` | **Deleted** (v2.0.2) |
| `lib/widgets/active_run/modes/theme_signature_mode.dart` | **Deleted** (v2.0.2) |
| `lib/widgets/active_run/modes/theme_lore.dart` | **Deleted** (v2.0.2) |
| `lib/widgets/active_run/modes/run_display_mode_bar.dart` | **Deleted** (v2.0.2) |
| `lib/widgets/active_run/modes/mode_picker_onboarding.dart` | **Deleted** (v2.0.2) |
| `lib/widgets/active_run/depth_tile.dart` | **Deleted** (v2.0.2) |
| `lib/widgets/backgrounds/gungeon_matrix_rain.dart` | **Deleted** (v1.9.62) |

### Graphics

| File | Purpose |
|------|---------|
| `lib/widgets/active_run/gungeon_meter.dart` | Interactive coolness/curse meter |
| `lib/widgets/backgrounds/animated_wallpaper.dart` | MP4 video wallpaper + vortex fallback |

### Multiplayer (v2.0.3 — fully reworked)

The old `multiplayer_session.dart` / `multiplayer_service.dart` / `paired_partner.dart` architecture was replaced in v2.0.2–v2.0.3 with a clean layered design:

| File | Purpose |
|------|---------|
| `lib/services/mp_session.dart` | Thin UI facade + lifecycle coordinator |
| `lib/services/mp/mp_link.dart` | Nearby Connections transport, discovery, advertising, heartbeat |
| `lib/services/mp/mp_sync.dart` | Hello handshake, snapshots, gifts, dice/emotes, shared-state sync |
| `lib/services/mp/mp_recovery.dart` | Reconnect + app-kill restore |
| `lib/services/mp/mp_store.dart` | Persistence of active MP session + run state |
| `lib/services/paired_partners_store.dart` | Nickname persistence only (pairing removed) |
| `lib/models/multiplayer_messages.dart` | MP wire protocol (17 message types) |
| `lib/screens/mp_lobby_screen.dart` | Host/Join lobby — nickname + role selection (no PIN) |
| `lib/screens/mp_connect_screen.dart` | Connecting/connected/error view |
| `lib/widgets/mp_reconnect_banner.dart` | Reconnect status banner |
| `lib/widgets/mp_request_listener.dart` | Gift/request bottom-sheet listener |

**Key changes from v1.x:**
- Pairing system removed entirely (~600 lines dead code purged)
- `AutoConnectModePin` replaces manual endpoint selection
- Main-authoritative shared-state model (Sidekick sends deltas, Main rebroadcasts)
- Heartbeat 5s, reconnect 5s on / 5s off
- `MpEndRun` sent on cancel so peer tears down cleanly
- Connection timeout (45s) prevents infinite spinner
- Discovery loop pauses during connection request (race condition fix)

**Deleted files (v2.0.2):**
- `lib/services/multiplayer_service.dart`
- `lib/services/multiplayer_session.dart`
- `lib/services/mp/mp_pairing.dart`
- `lib/models/paired_partner.dart`
- `lib/screens/multiplayer_lobby_screen.dart`

---

## 6.5. Test Suite (v2.1.0)

199 tests across 15 files, all passing. CI runs on every push via GitHub Actions.

| File | Tests | Coverage |
|------|-------|----------|
| `test/mp_flow_simulation_test.dart` | 5 | MP flow simulation + `_runProvider` desync regression |
| `test/mp_message_test.dart` | 3 | Wire protocol round-trip |
| `test/mp_link_test.dart` | 2 | Endpoint name parsing |
| `test/mp_integration_test.dart` | ~140 | Full MP integration: handshake, snapshots, gifts, reconnect, edge cases |
| `test/mp_recovery_test.dart` | — | MP recovery scenarios |
| `test/mp_reliability_test.dart` | — | MP reliability scenarios |
| `test/run_provider_test.dart` | 2 | State management lifecycle |
| `test/widget/character_select_screen_test.dart` | 2 | Character select rendering |
| `test/widget/codex_screen_test.dart` | 9 | Codex screen rendering + back button |
| `test/widget/home_screen_test.dart` | 3 | Bottom nav tab switching |
| `test/widget/main_menu_test.dart` | — | Main menu rendering |
| `test/widget/mp_lobby_screen_test.dart` | 1 | Lobby UI rendering |
| `test/widget/mp_connect_screen_test.dart` | 3 | Connect screen states |
| `test/widget/settings_screen_test.dart` | 13 | Settings sections, dice, dev tools, danger actions |

**CI workflow:** `.github/workflows/ci.yml` — 3 jobs (analyze, test, build APK) on every push/PR to `master` or `dev`.

**Run tests:**
```powershell
& 'C:\src\flutter\bin\flutter.bat' test
& 'C:\src\flutter\bin\flutter.bat' test --coverage  # generates coverage/lcov.info
```

---

## 7. PowerShell Gotchas

### Heredocs don't work in PowerShell

```powershell
# WRONG — PowerShell doesn't support bash heredocs:
git commit -m "$(cat <<'EOF'
message
EOF
)"

# RIGHT — write to a temp file:
# 1. Use the write tool to create .commit_msg.txt
# 2. git commit -F .commit_msg.txt
# 3. Remove-Item .commit_msg.txt -Force
```

### `$` variables get eaten

PowerShell interprets `$1`, `$2` as shell variables. Never use inline `$` in regex replacements. Write scripts to temp files instead.

### `flutter` not in PATH

Always use the full path: `& 'C:\src\flutter\bin\flutter.bat'`

### Git writes to stderr

`git push` and `git commit` write progress/info to stderr. PowerShell shows this as an error (red text, `NativeCommandError`), but the operation succeeds. Check the exit code and output content, not the color.

---

## 8. Coordination Board

**File:** `X:\GungeonMate\AGENT_STATUS.md`

### Slot layout

| Slot | Agent | Specialty |
|------|-------|-----------|
| 1 | VISUAL | Animations, particles, themes, UI polish, RepaintBoundary |
| 2 | CORE | State management, architecture, bug squashing, blueprints |
| 3 | PARALLEL | Second coder for parallel feature work |
| 4 | SUPPORT | Test infrastructure, docs, cleanup, cross-slot assistance |

### Board fields per slot

- **Status:** `IDLE` / `ACTIVE`
- **Working On:** current task
- **Last Heartbeat:** timestamp
- **Branch:** git branch (if parallel)
- **Session started:** timestamp
- **Last board update:** timestamp
- **Last commit:** SHA + message
- **Files in progress:** files being edited (off-limits to others)
- **Uncommitted changes:** files with uncommitted work

### Session Log

Append a row to the Session Log table at the end of every session with: Agent, Date, Branch, Commit, Task, Files, Status, Next, Watch out for.

---

## 9. Pre-Session Checklist

1. Read `AGENT_STATUS.md` — check all 4 slots
2. Read `docs/USER_BUG_LIST.md` — check for open bugs
3. Read this file (`docs/TECHNICAL_REFERENCE.md`)
4. `git status` — check uncommitted state
5. `git log -5 --oneline` — recent activity
6. Claim a slot (AC1) or verify your existing slot
7. If parallel (2+ agents): create a worktree (AC5d)
8. Run `gh auth setup-git` if you plan to push

---

## 10. Post-Session Checklist

1. Run `flutter analyze lib/` — MUST be clean
2. Commit all work (S7)
3. Update `AGENT_STATUS.md` — set slot to `IDLE`, fill Last commit
4. Append Session Log row
5. Push both repos if changes exist:
   ```powershell
   cd X:\GungeonMate\gungeon_mate; git push origin master
   cd X:\GungeonMate; git push origin master
   ```
6. Release slot (AC3)

---

## 11. Dependencies (Key Packages)

| Package | Version | Purpose |
|---------|---------|---------|
| `provider` | ^6.1.5 | State management |
| `video_player` | ^2.9.2 | Video playback API |
| `video_player_media_kit` | ^2.0.0 | Windows/Linux video backend |
| `media_kit_libs_windows_video` | ^1.0.11 | Windows video libs |
| `flutter_animate` | ^4.x | Declarative animations |
| `shared_preferences` | ^2.2.2 | Local persistence |
| `google_fonts` | ^6.2.1 | Dynamic font loading |
| `nearby_connections` | ^4.3.0 | MP Bluetooth/WiFi Direct transport |
| `path_provider` | ^2.x | File system paths |
| `url_launcher` | ^6.x | External browser links (wiki.gg) |
| `permission_handler` | ^11.4.0 | Runtime permission requests |

**Rule:** Never add a dependency without checking if a stdlib or existing package solution exists first (Ponytail Rules). Prefer packages published >7 days ago. Never use floating ranges (`latest`, `*`).

---

## 12. Known Platform Quirks

| Platform | Quirk | Workaround |
|----------|-------|------------|
| **Windows** | `video_player` has no native backend | `video_player_media_kit` (libmpv) — already added |
| **Windows** | `flutter` not in PATH | Use `& 'C:\src\flutter\bin\flutter.bat'` |
| **All** | Git push fails with "could not read Username" | Run `gh auth setup-git` |
| **All** | PowerShell heredocs fail | Write commit messages to temp files |
| **All** | `git push` shows red error text | Check exit code, not color — stderr is normal |
| **Web** | `nearby_connections` has no web implementation — `MissingPluginException` on load | MP features are native-only. Web builds hang on loading screen if MP init runs before UI mounts. Test MP via widget tests + fake transport, not Playwright. UI-only screens (menu, settings, codex) can be Playwright-tested if the app gets past loading. |
| **Web** | Service worker from prior dev sessions caches old builds | Unregister SW before testing: `navigator.serviceWorker.getRegistrations().then(r => r.forEach(sw => sw.unregister()))` then hard reload. Use a fresh port to avoid SW scope collision. |
