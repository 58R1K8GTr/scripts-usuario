"""Programa que auxilia o rofi, facilitando-o."""


from rich_click import command, option, echo

from src.arquivos import ler_json, atualizar_hashs, escrever_aliases
from src.datas import mtime_arquivo, mtime_json
from src.constantes import HOME_ALIASES, ROFI_JSON
from src.tipos import StatusModificacaoTipo


@command()
@option('-a', '--atualizar', is_flag=True)
def run_rofi_alias_manager(atualizar) -> None:
    """Verifica e atualiza o arquivo aliases para usar no rofi."""
    status = verificar_modificacoes()
    if atualizar:
        return atualizar_arquivos(status)
    return echo(status)


def atualizar_arquivos(status: StatusModificacaoTipo) -> None:
    """Atualiza os arquivos json e aliases.txt."""
    if status["arquivos_alterados"]:
        escrever_aliases()
        atualizar_hashs(status['novas_modificacoes'])


def verificar_modificacoes() -> StatusModificacaoTipo:
    """Verifica modificações dos arquivos .bash_aliases."""
    novas_modificacoes = list(map(mtime_arquivo, HOME_ALIASES))
    dados_json = ler_json(ROFI_JSON)
    antigas_modificacoes = list(map(mtime_json, dados_json['aliases']))
    arquivos_alterados = any((
        len(antigas_modificacoes) == 0,
        any(
            nova > antiga
            for nova, antiga
            in zip(novas_modificacoes, antigas_modificacoes)
        )
    ))
    status: StatusModificacaoTipo = {
        "arquivos_alterados": arquivos_alterados,
        "novas_modificacoes": novas_modificacoes
    }
    return status


run_rofi_alias_manager.main()
