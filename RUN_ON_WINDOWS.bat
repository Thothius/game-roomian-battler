@echo off
title GungeonMate — Launching on Windows Native...
echo =======================================================
echo          GungeonMate — Run on Windows Native
echo =======================================================
cd /d "%~dp0\gungeon_mate"
call flutter run -d windows
pause
