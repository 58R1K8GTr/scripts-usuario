#!/usr/bin/env zsh

if [[ "$ROFI_RETV" -eq 1 ]]; then
	source ~/.bash_aliases
	coproc { eval "$@"; }
else
	cat ~/.config/rofi/alias_data/aliases.txt
fi
