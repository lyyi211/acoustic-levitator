@echo off
setlocal
cd /d "%~dp0"
set "TEMP=%~dp0.tools\arduino-1.8.19\portable\tmp"
set "TMP=%TEMP%"
if not exist "%TEMP%" mkdir "%TEMP%"
start "" "%~dp0.tools\arduino-1.8.19\arduino.exe" "%~dp0firmware\acoustic_levitator\acoustic_levitator.ino"
