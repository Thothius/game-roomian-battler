---
description: Bump version, update changelog/history, build the release APK, and push to GitHub
---

# GungeonMate Release Build

Run this whenever a set of fixes/features is ready to ship. All paths are
relative to `x:\GungeonMate` unless noted.

> **Agent coordination:** Update your slot in `AGENT_STATUS.md` with the files
> you're modifying (AC2). During the long APK build, update **Last board update**
> so stale detection doesn't fire on you.

## 1. Pick the new version number
Follow semantic bump: patch for bugfixes, minor for features. Increment the
build number (`+N`) every time regardless.

## 2. Bump version in pubspec.yaml
Edit `gungeon_mate/pubspec.yaml`:
```
version: X.Y.Z+N
```

## 3. Add a changelog entry
Prepend a new entry to the top of `gungeon_mate/assets/data/changelog.json`
(newest first). Use a short emoji title and concise bullet items describing
root cause + fix for each change — this is user-facing, shown in the
in-app Changelog dialog.

## 4. Sync VERSION_HISTORY.md
Prepend a matching entry to `gungeon_mate/VERSION_HISTORY.md` with the same
version, APK filename (`gungeon-mate-vX.Y.Z.apk`), build number, and a
Root Cause / Fix breakdown for each item — this is the internal-facing
detailed log.

## 5. Update ALL version strings in main_menu_screen.dart
In `gungeon_mate/lib/screens/main_menu_screen.dart`, search for every `vX.Y.Z`
literal and update them ALL to match the new version:
- The `'Changelog (vX.Y.Z)'` button label string.
- The home screen version `Text` widget (e.g. `'vX.Y.Z'`).
- The changelog dialog header subtitle (e.g. `'vX.Y.Z — Title'`).
Never leave a stale version string in this file.

## 6. Build the release APK
Run non-blocking (release builds take 2-5 min) from
`x:\GungeonMate\gungeon_mate`:
```
C:\src\flutter\bin\flutter.bat build apk --release
```
Poll with `command_status` every 30-60s rather than blocking — blocking
calls on long builds have previously appeared to hang/cancel.

If a previous build is stuck, clear it first:
```
taskkill /f /im dart.exe; taskkill /f /im java.exe
```

## 7. Copy the APK to the releases folder
```
copy "gungeon_mate\build\app\outputs\flutter-apk\app-release.apk" "app-releases\gungeon-mate-vX.Y.Z.apk"
```

## 8. Commit and push
From `x:\GungeonMate\gungeon_mate`:
```
git add -A
git commit -m "vX.Y.Z: <short summary>"
git push origin master
```
Note: PowerShell does not support `&&` as a statement separator — use `;`
or separate commands.

## 9. Confirm
Verify the APK file size looks reasonable (~100-130MB) and that
`git push` reported the new commit hash landed on `origin/master`.
