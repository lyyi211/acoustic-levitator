#!/usr/bin/env bash
# Source from any directory; all writable tool state stays inside the project.
LEVITATOR_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PATH="$LEVITATOR_ROOT/.tools:$LEVITATOR_ROOT/.tools/native/usr/bin:$PATH"
export PYTHONPATH="$LEVITATOR_ROOT/.tools/python${PYTHONPATH:+:$PYTHONPATH}"
export PYTHONDONTWRITEBYTECODE=1
export TMPDIR="$LEVITATOR_ROOT/.tools/tmp"
export XDG_CACHE_HOME="$LEVITATOR_ROOT/.tools/cache"
export XDG_CONFIG_HOME="$LEVITATOR_ROOT/.tools/config"
export MPLCONFIGDIR="$LEVITATOR_ROOT/results/.matplotlib"
export ARDUINO_DIRECTORIES_DATA="$LEVITATOR_ROOT/.tools/arduino/data"
export ARDUINO_DIRECTORIES_DOWNLOADS="$LEVITATOR_ROOT/.tools/arduino/downloads"
export ARDUINO_DIRECTORIES_USER="$LEVITATOR_ROOT/.tools/arduino/user"
export LD_LIBRARY_PATH="$LEVITATOR_ROOT/.tools/native/usr/lib/x86_64-linux-gnu:$LEVITATOR_ROOT/.tools/native/usr/lib/x86_64-linux-gnu/pulseaudio:$LEVITATOR_ROOT/.tools/native/usr/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export QT_PLUGIN_PATH="$LEVITATOR_ROOT/.tools/native/usr/lib/x86_64-linux-gnu/qt5/plugins"
export QT_QPA_PLATFORM=offscreen
export SPICE_SCRIPTS="$LEVITATOR_ROOT/.tools/native/usr/share/ngspice/scripts"
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
mkdir -p "$TMPDIR" "$XDG_CACHE_HOME" "$XDG_CONFIG_HOME" "$ARDUINO_DIRECTORIES_DATA" "$ARDUINO_DIRECTORIES_DOWNLOADS" "$ARDUINO_DIRECTORIES_USER"
