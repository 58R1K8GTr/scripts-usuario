#!/usr/bin/env zsh

# verificando se os arquivos .bash_aliases foram alterados
# se sim, refazer o arquivo com os programas.

# arquivos=("$HOME/.bash_aliases"{,_debian,_arch})

# arquivo_hashes="$(dirname $0)/hashes.txt

if [[ "$ROFI_RETV" -eq 1 ]]; then
	source ~/.bash_aliases
	coproc { eval "$@"; }
else
	cat ~/.config/rofi/alias_data/aliases.txt
fi
