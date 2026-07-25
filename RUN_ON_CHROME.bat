@echo off
title GungeonMate — Launching on Chrome...
echo =======================================================
echo          GungeonMate — Run on Chrome Desktop
echo =======================================================
cd /d "%~dp0\gungeon_mate"
call flutter run -d chrome
pause
