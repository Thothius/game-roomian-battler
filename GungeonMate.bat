@echo off
title GungeonMate
color 0B
set "FLUTTER=C:\src\flutter\bin\flutter.bat"
set "APP=%~dp0\gungeon_mate"

:MENU
cls
echo ======================================================
echo               G U N G E O N   M A T E
echo ======================================================
echo.
echo   1. Run on Chrome (web)
echo   2. Run on Windows (native)
echo   3. Build Release APK
echo   4. Design Lab  (http://localhost:8619/design-lab/)
echo   5. Emulator Launcher
echo   0. Exit
echo.
set /p CHOICE="Pick: "

if "%CHOICE%"=="1" goto CHROME
if "%CHOICE%"=="2" goto WINDOWS
if "%CHOICE%"=="3" goto APK
if "%CHOICE%"=="4" goto LAB
if "%CHOICE%"=="5" goto EMU
if "%CHOICE%"=="0" exit /b 0
goto MENU

:CHROME
cd /d "%APP%" && call "%FLUTTER%" run -d chrome
goto DONE

:WINDOWS
cd /d "%APP%" && call "%FLUTTER%" run -d windows
goto DONE

:APK
cd /d "%APP%" && call "%FLUTTER%" build apk --release
if errorlevel 1 ( echo BUILD FAILED & goto DONE )
echo Done — APK in gungeon_mate\build\app\outputs\flutter-apk\
goto DONE

:LAB
start "" http://localhost:8619/design-lab/
cd /d "%APP%" && python -m http.server 8619
goto DONE

:EMU
call "%~dp0tools\launch_emulator.bat"
goto DONE

:DONE
echo.
pause
goto MENU
