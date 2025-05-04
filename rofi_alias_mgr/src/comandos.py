"""Executar comandos shell."""


from pathlib import Path
import subprocess
from time import sleep

from rich import print as rich_print

from src.textos import (
    TEXTO_SERVICO_OPCAO1_DESFORMATADO, TEXTO_TIMER2,
    TEXTO_SERVICO_OPCAO2_DESFORMATADO
)
from src.arquivos import (
    criar_arquivo, remover_arquivo, inotify_instalado
)


pasta_raiz = Path(__file__).parent.parent
local_daemons = Path('~/.config/systemd/user').expanduser()
local_script = pasta_raiz / 'rofi_alias_mgr.py'
executavel = Path('~/.local/bin/rofi-alias-mgr').expanduser()
local_daemon = local_daemons / 'rofi_alias_mgr_daemon.service'
local_timer = local_daemons / 'rofi_alias_mgr_daemon.timer'
if executavel.exists():
    COMANDO = f"{str(executavel)} atualizar"
else:
    COMANDO = f"/usr/bin/python3 {local_script} atualizar"


def criar_rodar_daemon(inotifywait: bool) -> None:
    """Cria e roda o processo daemon."""
    # não sobreescrever caso o daemon estiver rodando
    if local_daemon.exists():
        return rich_print('[red]Daemon existe, remova-o[/]')
    if inotifywait:
        _criar_inotifywait_daemon()
        nome_servico = local_daemon.name
    else:
        _criar_normal_daemon()
        nome_servico = local_timer.name
    subprocess.run('systemctl --user daemon-reload'.split(), check=False)
    sleep(1)
    subprocess.run(
        f"systemctl --user enable --now {nome_servico}".split(),
        check=False
    )


def _criar_inotifywait_daemon() -> None:
    """Cria o daemon que usa o programa inotifywait do inotify-tools."""
    if inotify_instalado():
        texto_servico = TEXTO_SERVICO_OPCAO1_DESFORMATADO.format(COMANDO)
        criar_arquivo(texto_servico, local_daemon)
    else:
        rich_print(
            '[red]Instale o inotify-tools ou semelhante na'
            ' sua distro para funcionar.[/]'
        )


def _criar_normal_daemon() -> None:
    """Cria o daemon que usa esse programa como padrão."""
    texto_servico = TEXTO_SERVICO_OPCAO2_DESFORMATADO.format(COMANDO)
    criar_arquivo(texto_servico, local_daemon)
    criar_arquivo(TEXTO_TIMER2, local_timer)


def desativar_remover_daemon(inotifywait: bool) -> None:
    """Remove e desativa o processo em daemon."""
    nome_servico = local_daemon if inotifywait else local_timer
    desabilitar = f'systemctl --user disable --now {nome_servico.name}'.split()
    sleep(1)
    remover_arquivo(local_daemon)
    if 'timer' in nome_servico.name:
        remover_arquivo(local_timer)
    subprocess.run(desabilitar, check=False)
    sleep(1)
    subprocess.run('systemctl --user daemon-reload'.split(), check=False)
