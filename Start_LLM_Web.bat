@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Starting eraMaouEx LLM Web UI...
python -m eraMaouEx_modules.llm.web
pause
