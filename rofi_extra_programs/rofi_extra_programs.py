"""Programa principal "rofi_shell" que auxilia o rofi, facilitando-o."""


from pathlib import Path

from click import echo, command

from src.arquivos import grep_aliases


@command()
def obter_comandos() -> str:
    """Retorna os comandos obtidos pelo arquivo."""
    padrao_arquivo = '.bash_aliases*'
    padrao_regex = r"#gui: .*\n[#.]*alias (.+)="
    local = Path('~').expanduser()
    echo(grep_aliases(local, padrao_arquivo, padrao_regex))


obter_comandos.main()
