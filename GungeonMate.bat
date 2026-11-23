@echo off
title GungeonMate
color 0B
set "FLUTTER=C:\src\flutter\bin\flutter.bat"
set "APP=%~dp0\gungeon_mate"
set "RELEASES=%~dp0app-releases"

:MENU
cls
echo ======================================================
echo               G U N G E O N   M A T E
echo ======================================================
echo.
echo   --- RUN (dev mode, hot reload) ---
echo   1. Windows desktop
echo   2. Android  (emulator or USB device)
echo   3. Chrome    (web)
echo.
echo   --- BUILD / INSTALL ---
echo   4. Build release APK  -^> app-releases\
echo   5. Emulator launcher  (boots AVD + installs latest APK)
echo   0. Exit
echo.
set /p CHOICE="Pick: "

if "%CHOICE%"=="1" goto WINDOWS
if "%CHOICE%"=="2" goto ANDROID
if "%CHOICE%"=="3" goto CHROME
if "%CHOICE%"=="4" goto APK
if "%CHOICE%"=="5" goto EMU
if "%CHOICE%"=="0" exit /b 0
goto MENU

:WINDOWS
cd /d "%APP%" && call "%FLUTTER%" run -d windows
goto DONE

:ANDROID
cd /d "%APP%" && call "%FLUTTER%" run -d android
goto DONE

:CHROME
cd /d "%APP%" && call "%FLUTTER%" run -d chrome
goto DONE

:APK
cd /d "%APP%" || goto DONE
:: Pull "version: X.Y.Z+N" out of pubspec for the release filename.
set "VER="
for /f "tokens=2 delims=:" %%v in ('findstr /b /c:"version:" pubspec.yaml') do set "VER=%%v"
set "VER=%VER: =%"
for /f "tokens=1 delims=+" %%a in ("%VER%") do set "VERNAME=%%a"
if "%VERNAME%"=="" set "VERNAME=unknown"

call "%FLUTTER%" build apk --release
if errorlevel 1 ( echo BUILD FAILED & goto DONE )

if not exist "%RELEASES%" mkdir "%RELEASES%"
copy /y "build\app\outputs\flutter-apk\app-release.apk" "%RELEASES%\gungeon-mate-v%VERNAME%.apk" >nul
if errorlevel 1 (
    echo APK built but copy to app-releases failed.
    echo APK is at gungeon_mate\build\app\outputs\flutter-apk\app-release.apk
) else (
    echo Done -^> %RELEASES%\gungeon-mate-v%VERNAME%.apk
)
goto DONE

:EMU
call "%~dp0tools\launch_emulator.bat"
goto DONE

:DONE
echo.
pause
goto MENU
