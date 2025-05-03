"""Programa que auxilia o rofi, facilitando-o."""


from json import dumps

from click import group, option
from rich import print as rich_print

from src.arquivos import ler_json, atualizar_hashs, escrever_aliases
from src.datas import mtime_arquivo, mtime_json
from src.constantes import HOME_ALIASES, ROFI_JSON
from src.tipos import StatusModificacaoTipo
from src.comandos import criar_rodar_daemon, desativar_remover_daemon


ordem = ['verificar', 'atualizar', 'ativar-daemon', 'desativar-daemon']


@group()
def run_rofi_alias_manager() -> None:
    """Verifica e atualiza o arquivo aliases para usar no rofi."""


@run_rofi_alias_manager.command()
@option('-o', '--otimizado', is_flag=True)
def ativar_daemon(otimizado: bool) -> None:
    """Cria e ativa o daemon normal ou otimizado."""
    criar_rodar_daemon(otimizado)


@run_rofi_alias_manager.command()
@option('-o', '--otimizado', is_flag=True)
def desativar_daemon(otimizado: bool) -> None:
    """Ativa ou desativa daemon otimizado."""
    desativar_remover_daemon(otimizado)


@run_rofi_alias_manager.command()
def verificar():
    """Verifica se houve modificações nos arquivos."""
    status = verificar_modificacoes()
    rich_print(f"[green]{dumps(status, indent=4)}[/]")


@run_rofi_alias_manager.command()
@option('-m', '--mostrar', is_flag=True)
def atualizar(mostrar):
    """Atualiza os arquivos de aliases, se necessário."""
    status = verificar_modificacoes()
    if mostrar:
        rich_print(f"[green]{dumps(status, indent=4)}[/]")
    if status["arquivos_alterados"]:
        atualizar_arquivos(status)
        rich_print("[green]Arquivos atualizados com sucesso![/]")
    else:
        rich_print(
            "[yellow]Nenhuma modificação detectada. Nada foi atualizado.[/]"
        )


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
    run_rofi_alias_manager()
