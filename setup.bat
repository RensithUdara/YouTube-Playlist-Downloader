@echo off
title YouTube Playlist Downloader Pro - Setup
cls

echo.
echo ===============================================
echo  YouTube Playlist Downloader Pro - Setup
echo ===============================================
echo.

echo Installing required dependencies...
echo.

REM Install yt-dlp
echo Installing yt-dlp...
pip install --upgrade yt-dlp
if %errorlevel% neq 0 (
    echo Failed to install yt-dlp
    pause
    exit /b 1
)

REM Install customtkinter
echo Installing customtkinter...
pip install --upgrade customtkinter
if %errorlevel% neq 0 (
    echo Failed to install customtkinter
    pause
    exit /b 1
)

echo.
echo ===============================================
echo  Setup completed successfully!
echo ===============================================
echo.
echo You can now run:
echo   * CLI Version: python youtube_Download-cli.py
echo   * GUI Version: python youtube_downloader-gui.py
echo   * Desktop Launcher: python desktop_launcher.py
echo.
echo ===============================================
echo  Optional: Create Desktop Application
echo ===============================================
echo.
echo To create a standalone .exe file that works
echo without Python installation:
echo.
echo   1. Run: build_desktop.bat
echo   2. Or manually: python build_desktop_app.py
echo.
echo This will create a professional desktop application
echo with custom icon and proper Windows integration.
echo.

pause
