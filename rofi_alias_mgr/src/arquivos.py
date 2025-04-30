"""Gerencia arquivos."""


from re import findall, M
from pathlib import Path
from itertools import chain
from hashlib import sha256
from json import load, dump
import sys

from rich_click import echo

from src.tipos import JsonTipo, ListaDatetimeTipo
from src.manipulacao_dados import gerar_dict_alias
from src.constantes import (
    ROFI_DATA, ROFI_ALIASES, HOME_ALIASES,
    HOME_ALIASES_ENCURTADO, ROFI_JSON, HOME
)


def grep_arquivos(
        local: Path, padrao_arquivo: str, padrao_regex: str
) -> str:
    """Retorna nome de aliases de dentro dos arquivos passados."""
    nomes_arquivos = Path(local).glob(padrao_arquivo)
    textos_arquivos = map(
        lambda arquivo: arquivo.read_text(), nomes_arquivos
    )
    try:
        aliases = chain(*map(
            lambda texto: findall(padrao_regex, texto, flags=M),
            textos_arquivos
        ))
        return '\n'.join(aliases)
    except FileNotFoundError as erro:
        echo(f"[red]{erro}[/red]")
        echo(
            '[yellow]Instale os dotfiles primeiro ou crie os '
            'arquivos aliases.[/yellow]'
        )
    except PermissionError as erro:
        echo(f"[red]{erro}[/red]")
    sys.exit(1)


def obter_comandos() -> str:
    """Retorna os aliases filtrados dos arquivos .bash_aliases."""
    padrao_arquivo = '.bash_aliases*'
    padrao_regex = r"#gui: .*\n[#.]*alias (.+)="
    return grep_arquivos(HOME, padrao_arquivo, padrao_regex)


def escrever_json(conteudo: JsonTipo, local: Path) -> None:
    """Salva o conteúdo em um json."""
    try:
        with local.open('r') as arquivo:
            return dump(conteudo, arquivo, indent=4, ensure_ascii=False)
    except PermissionError as erro:
        echo(f"[red]{erro}[/red]")
    sys.exit(1)


def ler_json(local: Path) -> JsonTipo:
    """Retorna o conteúdo de um json."""
    try:
        with local.open('r') as arquivo:
            conteudo: JsonTipo = load(arquivo)
            return conteudo
    except (FileNotFoundError, PermissionError) as erro:
        echo(f"[red]{erro}[/red]")
    sys.exit(1)


def escrever_aliases() -> None:
    """Lê, filtra e escreve os aliases no aliases.txt."""
    ROFI_DATA.mkdir(exist_ok=True)
    ROFI_ALIASES.write_text(obter_comandos(), encoding='utf8')


def hashear_arquivo(local: Path) -> str:
    """Retorna um hask de um arquivo."""
    with local.open('rb') as arquivo:
        quantidade_bytes = 50_000
        item_hash = sha256()
        buffer = arquivo.read(quantidade_bytes)
        while buffer:
            item_hash.update(buffer)
            buffer = arquivo.read(quantidade_bytes)
    return item_hash.hexdigest()


def atualizar_hashs(novas_modificacoes: ListaDatetimeTipo) -> None:
    """Atualiza os hashes no arquivo json."""
    hashs = map(hashear_arquivo, HOME_ALIASES)
    mtimes = map(lambda x: x.isoformat(), novas_modificacoes)
    dict_aliases = gerar_dict_alias(zip(
        HOME_ALIASES_ENCURTADO, mtimes, hashs
    ))
    escrever_json(dict_aliases, ROFI_JSON)
