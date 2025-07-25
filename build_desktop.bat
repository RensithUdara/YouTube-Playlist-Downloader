@echo off
title YouTube Playlist Downloader Pro - Desktop App Builder
cls

echo.
echo ===============================================
echo   YouTube Playlist Downloader Pro
echo   Desktop Application Builder
echo ===============================================
echo.

echo This will create a standalone desktop application that:
echo   * Works without Python installation
echo   * Has a professional icon and name
echo   * Can be distributed to other computers
echo   * Includes all dependencies
echo.

echo Installing required tools...
echo.

REM Install PyInstaller
echo Installing PyInstaller (application builder)...
pip install --upgrade pyinstaller
if %errorlevel% neq 0 (
    echo Failed to install PyInstaller
    pause
    exit /b 1
)

REM Install Pillow for icon creation
echo Installing Pillow (image processing)...
pip install --upgrade Pillow
if %errorlevel% neq 0 (
    echo Failed to install Pillow
    pause
    exit /b 1
)

echo.
echo ===============================================
echo   Creating Application Icons...
echo ===============================================
echo.

REM Create icons
python create_icon.py
if %errorlevel% neq 0 (
    echo Failed to create icons
    pause
    exit /b 1
)

echo.
echo ===============================================
echo   Building Desktop Application...
echo ===============================================
echo.

REM Build the application
python build_desktop_app.py
if %errorlevel% neq 0 (
    echo Failed to build application
    pause
    exit /b 1
)

echo.
echo ===============================================
echo   Desktop Application Created Successfully!
echo ===============================================
echo.
echo Your desktop application is ready!
echo.
echo Files created:
echo   * dist/YouTube Playlist Downloader Pro.exe
echo   * Desktop shortcut (if supported)
echo.
echo You can now:
echo   1. Run the .exe file directly
echo   2. Copy it to other computers
echo   3. Distribute it without Python
echo.

pause
