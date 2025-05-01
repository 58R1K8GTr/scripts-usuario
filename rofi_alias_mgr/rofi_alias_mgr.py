"""Programa que auxilia o rofi, facilitando-o."""


from click import (
    command, option, get_current_context
)
from rich import print as rich_print

from src.arquivos import ler_json, atualizar_hashs, escrever_aliases
from src.datas import mtime_arquivo, mtime_json
from src.constantes import HOME_ALIASES, ROFI_JSON
from src.tipos import StatusModificacaoTipo
from src.comandos import criar_rodar_daemon, desativar_remover_daemon


@command()
@option('-a', '--atualizar', is_flag=True)
@option('-v', '--verificar', is_flag=True)
@option('-d', '--ativar-daemon', is_flag=True)
@option('-D', '--desativar-daemon', is_flag=True)
def run_rofi_alias_manager(
    atualizar, verificar, ativar_daemon, desativar_daemon
) -> None:
    """
    Verifica e atualiza o arquivo aliases para usar no rofi.\n
    IMPORTANTE: necessário flags -va para atualizar!
    """
    erro = False
    match [verificar, atualizar, ativar_daemon, desativar_daemon]:
        case (True, False, _, _):  # verificar
            status = verificar_modificacoes()
            rich_print(f"[green]{status}[/]")
        case (True, True, _, _):  # verificar e atualizar
            status = verificar_modificacoes()
            atualizar_arquivos(status)
            rich_print(f"[green]{status}[/]")
        case (False, True, _, _):
            rich_print('[red]Necessário flags -va para atualizar![/]\n')
            erro = True
        case (_, _, True, False):  # ativar daemon
            criar_rodar_daemon()
        case (_, _, False, True):  # desativar daemon
            desativar_remover_daemon()
        case _:
            erro = True
    if erro:
        contexto = get_current_context()
        rich_print(contexto.get_help())


def atualizar_arquivos(status: StatusModificacaoTipo) -> None:
    """Atualiza os arquivos json e aliases.txt."""
    if status["arquivos_alterados"]:
        escrever_aliases()
        atualizar_hashs(status['mtimes'])


def verificar_modificacoes() -> StatusModificacaoTipo:
    """Verifica modificações dos arquivos .bash_aliases."""
    novas_modificacoes = list(map(mtime_arquivo, HOME_ALIASES))
    dados_json = ler_json(ROFI_JSON)
    aliases = dados_json['aliases']
    antigas_modificacoes = list(map(
        lambda x: mtime_json(aliases[x]['mtime']), aliases
    ))
    arquivos_alterados = any((
        len(antigas_modificacoes) == 0,
        any(
            nova > antiga
            for nova, antiga
            in zip(novas_modificacoes, antigas_modificacoes)
        )
    ))
    mtimes = list(map(lambda x: x.isoformat(), novas_modificacoes))
    status: StatusModificacaoTipo = {
        "arquivos_alterados": arquivos_alterados,
        "mtimes": mtimes
    }
    return status


if __name__ == '__main__':
    run_rofi_alias_manager.main()
