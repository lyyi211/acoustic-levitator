@echo off
setlocal
cd /d "%~dp0"
start "Acoustic Levitator 3D" wsl.exe --cd "%~dp0" bash -c "source tools/env.sh; export QT_QPA_PLATFORM=xcb; openscad mechanical/levitator_frame.scad"
