@echo off
title GungeonMate — Building Release APK...
echo =======================================================
echo          GungeonMate — Build Release APK
echo =======================================================

cd /d "%~dp0\gungeon_mate"

call C:\src\flutter\bin\flutter.bat build apk --release

if errorlevel 1 (
    echo =======================================================
    echo BUILD FAILED — check errors above
    echo =======================================================
    pause
    exit /b 1
)

:: Parse version from pubspec.yaml (e.g. "version: 0.9.994+46" -> "0.9.994")
for /f "tokens=2 delims=: " %%v in ('findstr /b "version:" pubspec.yaml') do (
    for /f "tokens=1 delims=+" %%w in ("%%v") do set VERSION=%%w
)

set SRC=build\app\outputs\flutter-apk\app-release.apk
set DEST=%~dp0app-releases\gungeon-mate-v%VERSION%.apk

if not exist "%SRC%" (
    echo =======================================================
    echo ERROR — APK not found at expected path:
    echo %SRC%
    echo =======================================================
    pause
    exit /b 1
)

copy /y "%SRC%" "%DEST%" >nul

echo =======================================================
echo Build complete! APK copied to:
echo app-releases\gungeon-mate-v%VERSION%.apk
echo =======================================================
pause
