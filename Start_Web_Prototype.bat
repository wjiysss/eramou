@echo off
chcp 65001 >nul
title eraMaouEx Browser Prototype

cd /d "%~dp0"
python web-prototype\server.py
