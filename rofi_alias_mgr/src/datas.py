"""Gerencia datas."""


from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import sys

from rich_click import echo


REGIAO = ZoneInfo('localtime')


def mtime_arquivo(arquivo: Path) -> datetime:
    """Retorna a datetime formatada da última modificação do arquivo."""
    try:
        tempo = arquivo.stat().st_mtime
        return datetime.fromtimestamp(tempo, REGIAO)
    except FileNotFoundError as erro:
        echo(erro)
        echo(
            '[red]Instale os dotfiles primeiro ou crie '
            'arquivos aliases.[/red]'
        )
    sys.exit(1)


def mtime_json(data: str) -> datetime:
    """Retorna a datetime da data como string."""
    return datetime.fromisoformat(data)
