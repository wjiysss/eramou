@echo off
chcp 65001 >nul
title eraMaouEx - Python Version

echo Starting eraMaouEx (Python Version)...
echo.

cd /d "%~dp0"
python eraMaouEx.py

if errorlevel 1 (
    echo.
    echo Error: Failed to start Python version
    echo Make sure Python is installed and in PATH
    pause
)
