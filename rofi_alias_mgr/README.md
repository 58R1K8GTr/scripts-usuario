# rofi-alias-mgr

## Descrição
Programa que faz a verificação se os arquivos .bash_aliases mudaram, caso sim, salva novos aliases comandos no aliases.txt para o rofi poder executá-los.

Esses aliases são atalhos abreviados para executar programas com comandos específivos de maneira rápida, seja no terminal ou no próprio lançador de aplicativos (rofi), e agora com esse programa, será mais rápido a execução desses programas.

## Como compilar?
Antes de rodar é necessário compilar. Ele já será movido para o local correto ao término da execução do script.
```bash
./compilar_e_mover.sh
```

## Como rodar?
### compilado:
    - `rofi-alias-mgr --help` obtem ajuda.
    - `rofi-alias-mgr` verifica se houve atualizações.
    - `rofi-alias-mgr -a (--atualizar)` verifica atualizações e escreve nos arquivos.
### não compilado:
    - da mesma forma que acima, porém usando o `python3 rofi-alias-mgr.py`.
