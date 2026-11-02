@echo off
cd /d "%~dp0"
py src\main.py %*
exit /b %errorlevel%
