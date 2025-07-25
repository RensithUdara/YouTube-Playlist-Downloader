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
echo.

pause
