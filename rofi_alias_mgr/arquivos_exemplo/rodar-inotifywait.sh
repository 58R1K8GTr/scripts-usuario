#!/bin/bash
cd "$(dirname "$0")"

if [ "$1" = 'executavel' ]; then
    comando='rofi-alias-mgr atualizar'
else
    comando="python3 ../rofi_alias_mgr.py atualizar"
fi

inotifywait -m -e close_write ~/.bash_aliases* | while read caminho evento;
    do $comando;
done