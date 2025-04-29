"""Gerencia arquivos."""


from re import findall, M
from pathlib import Path
from itertools import chain
from src.tipos import PathStr


def grep(local: PathStr, padrao_arquivo: str, padrao_regex: str) -> str:
    """Retorna nome de aliases de dentro dos arquivos passados."""
    nomes_arquivos = Path(local).glob(padrao_arquivo)
    textos_arquivos = map(
        lambda arquivo: arquivo.read_text(), nomes_arquivos
    )
    aliases = chain(*map(
        lambda texto: findall(padrao_regex, texto, flags=M),
        textos_arquivos
    ))
    return '\n'.join(aliases)
