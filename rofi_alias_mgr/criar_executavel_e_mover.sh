#!/bin/bash
cd "$(dirname "$0")"
poetry run pyinstaller main.spec
mkdir -p ~/.local/bin 2>/dev/null
mv dist/rofi-alias-mgr ~/.local/bin
