# rofi-alias-mgr

## Descrição
Programa que faz a verificação se os arquivos .bash_aliases mudaram, caso sim, salva novos aliases comandos no aliases.txt para o rofi poder executá-los.

Esses aliases são atalhos abreviados para executar programas com comandos específivos de maneira rápida, seja no terminal ou no próprio lançador de aplicativos (rofi), e agora com esse programa, será mais rápido a execução desses programas.

Ele não foi feito para rodar nos scripts do rofi mas sim um auxiliar que filtra os comandos que quero com base em um padrão.

## O que é filtrado pelo comando e jogado no aliases.txt?
Qualquer alias que contenha um comentário na linha acima contendo `# gui:`.

## Como rodar?
### Sem executável:
`python3 rofi-alias-mgr.py`
### Com executável:
`rofi-alias-mgr`
> abaixo está escrito como gerar o executável.

## Subcomandos e suas flags:

comando | função | flag | função
--- | --- | --- | ---
\- | \- | `--help` | obtem ajuda.
verificar | verifica se houve atualizações.
atualizar | verifica atualizações e escreve nos arquivos. | `-m\|--mostrar` | retorna o resultado igual `verificar`.
ativar-daemon | cria e ativa o processo daemon no systemd automaticamente. | `-o\|--otimizado` | ativa o daemon otimizado.
desativar-daemon | desativa e remove o processo daemon no systemd automaticamente. | `-o\|--otimizado` | desativa o daemon otimizado.

>Obs: daemon otimizado só funciona com o inotifywait do inotify-tools (debian e derivados).

## Como criar o executável?
Não é necessário criar o executável, mas se quiser algo mais automático no terminal:
```bash
./criar_executavel_e_mover.sh
```

## Exemplo de arquivo script shell que lê os comandos para o rofi:
arquivo | local
--- | ---
[rofi-shell.sh](arquivos_exemplo/rofi-shell.sh) | `~/.config/rofi/scripts/`

> Obs: Para executar no rofi, leia a documentação do mesmo na seção scripts.


## É necessário o processo em daemon?
O daemon só serve para rodar o processo de atualização automaticamente em background. Caso queira fazer da sua maneira também é possível.

É recomendado algo mais prático como o programa `inotifywait` do pacote `inotify-tools`.

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

### Como eu misturo os arquivos `.desktop` com esses comandos no rofi?
Eu uso um modo chamado _combi_, com ele eu consigo exibir tanto os programas padrões como os meus. Leia a documentação do rofi para tal.