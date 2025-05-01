# rofi-alias-mgr

## Descrição
Programa que faz a verificação se os arquivos .bash_aliases mudaram, caso sim, salva novos aliases comandos no aliases.txt para o rofi poder executá-los.

Esses aliases são atalhos abreviados para executar programas com comandos específivos de maneira rápida, seja no terminal ou no próprio lançador de aplicativos (rofi), e agora com esse programa, será mais rápido a execução desses programas.

## Como criar o executável?
Não é necessário criar o executável, mas se quiser algo mais automático no terminal:
```bash
./criar_executavel_e_mover.sh
```

## Como rodar?
### Sem executável:
`python3 rofi-alias-mgr.py`
### Com executável:
`rofi-alias-mgr`

## Flags:
flag | função
--- | ---
`--help` | obtem ajuda.
`-v (--verificar)` | verifica se houve atualizações.
`-a (--atualizar)` | verifica atualizações e escreve nos arquivos.
`-d (--ativar-daemon)` | cria e ativa o processo daemon no systemd automaticamente.
`-D (--desativar-daemon)` | desativa e remove o processo daemon no systemd automaticamente.

## Informações extras:
### Libs usadas e suas funções no programa:

nome | função
--- | ---
click | Criar o programa como linha de comando (cli).
rich | Colocar cores nas saídas dos prints do programa.
pathlib, hashlib, datetime | Para averiguar se houve mudança nos aliases, escreve-los em outro lugar para o rofi ler e poupar I/O e processamento.
json | Salvar as datas das últimas alterações dos aliases.
poetry | Criar o ambiente virtual para desenvolvimento.
flake8, pylint | Lintagem de código.
mypy | Tipagem no código.
pyinstaller | Gerar um executável
shell script | Otimizar tarefas como gerar e mover o executável.
pytest | Testes automatizados.

