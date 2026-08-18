# GungeonMate — Technical Reference for All Agents

> **READ THIS BEFORE ANY WORK.** This is the canonical technical reference.
> Every agent must know these facts at all times. No exceptions.
>
> Last updated: 2026-08-18 (v1.9.60)

---

## 1. Repository Architecture

There are **two independent git repositories**:

| Repo | Path | Remote | Tracks |
|------|------|--------|--------|
| **Root** | `X:\apps\GungeonMate` | `https://github.com/Thothius/game-roomian-battler.git` | `AGENTS.md`, `AGENT_STATUS.md`, `docs/`, `MUTATION_STATION/`, `.windsurfrules`, root-level scripts |
| **App** | `X:\apps\GungeonMate\gungeon_mate` | `https://github.com/Thothius/GungeonMate.git` | All `lib/`, `assets/`, `pubspec.yaml`, `test/` |

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
cd X:\apps\GungeonMate\gungeon_mate
git push origin master

# 3. Push the root repo (if root files changed):
cd X:\apps\GungeonMate
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
| **Flutter version** | 3.29.0 (stable, 2025-02-10) |
| **Dart version** | 3.7.0+ |
| **App repo working dir** | `X:\apps\GungeonMate\gungeon_mate` |

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
| `gungeon_mate/lib/screens/main_menu_screen.dart` | Version string in changelog dialog (~line 519) |

**Version format:** `MAJOR.MINOR.PATCH+BUILD` (e.g. `1.9.60+136`). The `+BUILD` number increments with every release. The `PATCH` increments for features/fixes.

**Current version:** `1.9.60+136`

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

## 5. Current App Architecture (v1.9.60)

### Active Run Display Modes

The active run screen supports **5 display modes** via `RunDisplayMode` enum:

| Mode | Enum value | Widget | Description |
|------|------------|--------|-------------|
| Classic Scroll | `classic` | (default scroll view in PlayerPage) | The original full scroll view. Default. |
| Codex Book | `codex` | `CodexBookMode` | Leather-and-brass two-page book spread |
| Compact Run | `compact` | `CompactRunMode` | Tactical HUD, 2-column grid |
| Gungeon Matrix | `matrix` | `MatrixMode` | Purple digital rain background |
| Theme Signature | `signature` | `ThemeSignatureMode` | Adapts to active theme — lore, colors, decorations |

**Routing:** `PlayerPage` checks `VisualPrefs.runDisplayMode` and returns the appropriate mode widget. The `RunDisplayModeBar` (collapsible pill between header and PageView) switches modes instantly.

**Pref key:** `vp.run_display_mode_v2` (v2 because index shifted when `classic` was added as enum value 0).

### Theme System

| Component | Location |
|-----------|----------|
| `AppThemeMode` enum (33 values, 14 visible) | `lib/services/app_theme.dart` |
| `ThemeFlair` (per-theme color palette) | `lib/services/app_theme.dart` |
| `VisualPrefs` (persisted user prefs) | `lib/services/app_theme.dart` |
| `kVisibleThemes` list | `lib/services/app_theme.dart` |
| `ThemeOverlay` (global visual stack) | `lib/widgets/theme_overlay.dart` |
| `ThemeLore` registry (14 entries) | `lib/widgets/active_run/modes/theme_lore.dart` |

**14 visible themes:** Minimalist, Unicorn, Forge Master, Robot's Core, Cat Lady, Moonlit Chamber, Storm Caller, Mr. Robot, Valor of Marines, The Bullet, The Paradox, Gunpowder, Dragunfire, Lich's Domain, Custom.

### VisualPrefs fields (persisted to SharedPreferences)

All fields follow this pattern:
1. Field on `VisualPrefs` class with default
2. `_k<Field>` SharedPreferences key constant
3. Load in `VisualPrefs.init()` 
4. Setter: `VisualPrefs.set<Field>(v)` → `_with()` → `_persist()`
5. `_with()` parameter + assignment

Key fields:
- `runDisplayMode` (RunDisplayMode, default: `classic`)
- `runDisplayModeBarCollapsed` (bool, default: `true`)
- `showModePickerOnNewRun` (bool, default: `false`)
- `depthInventory` (bool, default: `true`)
- `depthTiltIntensity` (double, default: `0.6`)
- `shaderEnabled` (bool, default: `false`)
- `shaderPreset` (ShaderPreset, default: `digitalRain`)

### Video Player

| Component | Package | Platforms |
|-----------|---------|-----------|
| `video_player` | `^2.9.2` | Android, iOS, macOS, Web |
| `video_player_media_kit` | `^2.0.0` | Windows, Linux (libmpv backend) |
| `media_kit_libs_windows_video` | `^1.0.11` | Windows video libs |

**Init:** `VideoPlayerMediaKit.ensureInitialized(windows: true)` in `main.dart` before `runApp`.

**Usage:** `AnimatedWallpaperBackground` widget in `lib/widgets/backgrounds/animated_wallpaper.dart`. Plays `gungeonmate-animation-02.mp4` on the home screen. Falls back to `_VortexFallbackPainter` (CustomPaint) if video init fails.

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

---

## 6. Key File Locations

### Core

| File | Purpose |
|------|---------|
| `lib/main.dart` | App entry point, `VideoPlayerMediaKit.ensureInitialized` |
| `lib/providers/run_provider.dart` | State management (1762 lines) |
| `lib/services/app_theme.dart` | Themes, VisualPrefs, RunDisplayMode enum (3535 lines) |
| `lib/widgets/theme_overlay.dart` | Global visual stack (layers 0-1.0) |
| `lib/screens/home_screen.dart` | Home screen routing (MainMenu vs ActiveRunScreen) |
| `lib/screens/active_run_screen.dart` | Active run screen (903 lines) |
| `lib/widgets/active_run/player_page.dart` | Per-player page with mode routing |

### Active Run Modes

| File | Mode |
|------|------|
| `lib/widgets/active_run/modes/codex_book_mode.dart` | Codex Book |
| `lib/widgets/active_run/modes/compact_run_mode.dart` | Compact Run |
| `lib/widgets/active_run/modes/matrix_mode.dart` | Gungeon Matrix |
| `lib/widgets/active_run/modes/theme_signature_mode.dart` | Theme Signature |
| `lib/widgets/active_run/modes/theme_lore.dart` | ThemeLore registry |
| `lib/widgets/active_run/modes/run_display_mode_bar.dart` | Mode switcher bar |
| `lib/widgets/active_run/modes/mode_picker_onboarding.dart` | Onboarding dialog |

### Graphics

| File | Purpose |
|------|---------|
| `lib/widgets/active_run/gungeon_meter.dart` | Interactive coolness/curse meter |
| `lib/widgets/active_run/depth_tile.dart` | 2.5D perspective inventory tile |
| `lib/widgets/backgrounds/animated_wallpaper.dart` | MP4 video wallpaper + vortex fallback |
| `lib/widgets/backgrounds/gungeon_matrix_rain.dart` | Purple matrix rain CustomPainter |
| `lib/widgets/backgrounds/ambient_shader_layer.dart` | Fragment shader ambient layer |

### Multiplayer

| File | Purpose |
|------|---------|
| `lib/services/multiplayer_session.dart` | MP session, pairing, reconnect (2662 lines) |
| `lib/services/multiplayer_service.dart` | Socket transport |
| `lib/services/paired_partners_store.dart` | Paired partner persistence |
| `lib/models/paired_partner.dart` | Paired partner model |
| `lib/models/multiplayer_messages.dart` | MP message types |

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

**File:** `X:\apps\GungeonMate\AGENT_STATUS.md`

### Slot layout

| Slot | Agent | Specialty |
|------|-------|-----------|
| 1 | XEENU-ANIMATOR | 2.5D, particles, spring physics, RepaintBoundary |
| 2 | Coder-Maintainer-Reworker-Genius | State management, architecture, bug squashing |
| 3 | Planner-Architect-Mockupper | Blueprints, protocol design, wireframing |
| 4 | UNIVERSAL WORKER | General code, docs, cross-slot assistance |

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
2. Read `docs/bug_tracker.md` — check for open bugs
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
   cd X:\apps\GungeonMate\gungeon_mate; git push origin master
   cd X:\apps\GungeonMate; git push origin master
   ```
6. Release slot (AC3)

---

## 11. Dependencies (Key Packages)

| Package | Version | Purpose |
|---------|---------|---------|
| `provider` | ^6.x | State management |
| `video_player` | ^2.9.2 | Video playback API |
| `video_player_media_kit` | ^2.0.0 | Windows/Linux video backend |
| `media_kit_libs_windows_video` | ^1.0.11 | Windows video libs |
| `flutter_animate` | ^4.x | Declarative animations |
| `shared_preferences` | ^2.x | Local persistence |
| `path_provider` | ^2.x | File system paths |

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
