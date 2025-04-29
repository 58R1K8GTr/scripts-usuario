"""Programa principal "rofi_shell" que auxilia o rofi, facilitando-o."""


from pathlib import Path

from src.arquivos import grep

from click import echo, command


@command()
def obter_comandos() -> str:
    """Retorna os comandos obtidos pelo arquivo."""
    padrao_arquivo = '.bash_aliases*'
    padrao_regex = r"^alias (.+)='doas "
    local = Path('~').expanduser()
    echo(grep(local, padrao_arquivo, padrao_regex))


obter_comandos.main()
