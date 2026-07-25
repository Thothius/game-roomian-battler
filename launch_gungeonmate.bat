@echo off
title GungeonMate - Ultimate High-Performance Emulator Launcher
cls

:: Beautiful cyan color scheme for Gungeon aesthetics
color 0B

echo ======================================================================
echo  [+][+][+]   G U N G E O N   M A T E   C O M P A N I O N   [+][+][+]
echo  [+][+][+]       OPTIMIZED EMULATOR LAUNCHER (v1.7.2)      [+][+][+]
echo ======================================================================
echo.

:: Detect SDK Path based on your screen captures
set "SDK_PATH=C:\Users\saare\AppData\Local\Android\Sdk"
if not exist "%SDK_PATH%" (
    set "SDK_PATH=%LOCALAPPDATA%\Android\Sdk"
)
if not exist "%SDK_PATH%" (
    echo [ERROR] Android SDK not found in %LOCALAPPDATA%\Android\Sdk
    echo Please make sure Android Studio is installed and SDK is configured.
    pause
    exit /b 1
)

set "EMULATOR=%SDK_PATH%\emulator\emulator.exe"
set "ADB=%SDK_PATH%\platform-tools\adb.exe"

echo [INFO] Android SDK detected at: %SDK_PATH%
echo [INFO] Emulator Tool: %EMULATOR%
echo [INFO] ADB Tool: %ADB%
echo.

:: Detect the newest APK in the entire workspace using PowerShell
echo [INFO] Scanning workspace for the latest compiled GungeonMate APK...
set "FINAL_APK="
for /f "delims=" %%i in ('powershell -NoProfile -Command "Get-ChildItem -Path 'X:\GungeonMate' -Filter *.apk -Recurse -ErrorAction SilentlyContinue ^| Sort-Object LastWriteTime -Descending ^| Select-Object -First 1 -ExpandProperty FullName"') do (
    set "FINAL_APK=%%i"
)

if "%FINAL_APK%"=="" (
    echo [ERROR] No APK file found in the workspace!
    echo Please build your APK first with "flutter build apk" or place an APK in gungeon_mate/builds/
    pause
    exit /b 1
)

echo [SUCCESS] Latest APK found:
echo          %FINAL_APK%
echo.

:: Check if an emulator is already running
echo [INFO] Checking if an Android device/emulator is already active...
set "DEVICE_READY=0"
for /f "tokens=1,2" %%a in ('"%ADB%" devices') do (
    if "%%b"=="device" (
        echo [INFO] Active device/emulator detected: %%a
        set "DEVICE_READY=1"
        goto :install_app
    )
)

:: No running device, start emulator
echo [INFO] No running device detected. Starting optimized Android emulator...

:: Find the best emulator available using a memory-only PowerShell selection
set "AVD_NAME="
for /f "delims=" %%a in ('powershell -NoProfile -Command "if (Test-Path '%EMULATOR%') { $avds = & '%EMULATOR%' -list-avds; if ($avds -contains 'Medium_Phone_API_36.1') { 'Medium_Phone_API_36.1' } else { $avds[0] } }"') do (
    set "AVD_NAME=%%a"
)

if "%AVD_NAME%"=="" (
    echo [ERROR] No Android Virtual Devices found!
    echo Please open Android Studio's Device Manager and create an emulator first.
    pause
    exit /b 1
)

echo [LAUNCH] Starting AVD: %AVD_NAME% with Maximum Performance settings...
echo          - hardware graphics acceleration (host GPU)
echo          - Windows Hypervisor Platform (WHPX) acceleration
echo          - 4 CPU Cores & 3GB RAM allocated
echo          - Disabled boot animations for fast startup
echo.

:: Launch the emulator asynchronously and return prompt
start "GungeonMate Emulator" "%EMULATOR%" -avd "%AVD_NAME%" -gpu host -accel on -no-boot-anim -cores 4 -memory 3072 -dns-server 8.8.8.8

echo [WAIT] Waiting for the emulator to finish booting...
echo        This usually takes 15-45 seconds. Please stand by...

:wait_loop
timeout /t 3 /nobreak >nul
"%ADB%" shell getprop sys.boot_completed > "%temp%\boot_status.txt" 2>&1
set /p BOOT_STATUS=<"%temp%\boot_status.txt"

if "%BOOT_STATUS%"=="1" (
    echo.
    echo [SUCCESS] Emulator is fully booted and responsive!
    goto :install_app
) else (
    <nul set /p =.
    goto :wait_loop
)

:install_app
echo.
echo [INSTALL] Installing GungeonMate onto the emulator...
echo           Package: com.gungeonmate.gungeon_mate
"%ADB%" install -r "%FINAL_APK%"
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install the APK onto the emulator.
    echo Make sure the emulator is active and unlocked.
    pause
    exit /b 1
)
echo [SUCCESS] App installed successfully!
echo.

echo [LAUNCH] Starting GungeonMate (MainActivity)...
"%ADB%" shell am start -n com.gungeonmate.gungeon_mate/com.gungeonmate.gungeon_mate.MainActivity
if %errorlevel% neq 0 (
    echo [ERROR] Failed to launch the application.
    pause
    exit /b 1
)

echo ======================================================================
echo   [🎉 SUCCESS] GUNGEONMATE IS LIVE ON THE SIMULATOR!
echo ======================================================================
echo   💡 PRO-TIP FOR 5X SPEED IMPROVEMENTS:
echo   To speed up the emulator and compiler dramatically, go to:
echo   Windows Security -> Virus & threat protection -> Manage settings 
echo   -> Exclusions (Add or remove exclusions) -> Add folder
echo   And select these two folders:
echo   1. %SDK_PATH%
echo   2. X:\GungeonMate
echo ======================================================================
echo.
echo Press any key to close this launcher shell...
pause >nul
