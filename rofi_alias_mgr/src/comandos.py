"""Executar comandos shell."""


from pathlib import Path
import subprocess

from src.textos import TEXTO_SERVICO_DESFORMATADO, TEXTO_TIMER
from src.arquivos import criar_arquivo, remover_arquivo


local_daemons = Path('~/.config/systemd/user').expanduser()
local_script = Path(__file__).parent.parent / 'rofi_alias_mgr.py'
executavel = Path('~/.local/bin/rofi-alias-mgr').expanduser()
local_daemon = local_daemons / 'rofi_alias_mgr_daemon.service'
local_timer = local_daemons / 'rofi_alias_mgr_daemon.timer'


def criar_rodar_daemon() -> None:
    """Cria e roda o processo daemon."""
    if executavel.exists():
        linha = executavel.name
    else:
        linha = f"/usr/bin/python3 {local_script}"
    texto_servico = TEXTO_SERVICO_DESFORMATADO.format(linha)
    # não sobreescrever caso o daemon estiver rodando
    if not local_timer.exists():
        criar_arquivo(texto_servico, local_daemon)
        criar_arquivo(TEXTO_TIMER, local_timer)
    subprocess.run('systemctl --user daemon-reload'.split(), check=False)
    subprocess.run(
        f"systemctl --user enable --now {local_timer.name}".split(),
        check=False
    )


def desativar_remover_daemon() -> None:
    """Remove e desativa o processo em daemon."""
    desabilitar = f'systemctl --user disable --now {local_timer.name}'.split()
    remover_arquivo(local_daemon)
    remover_arquivo(local_timer)
    subprocess.run(desabilitar, check=False)
    subprocess.run('systemctl --user daemon-reload'.split(), check=False)


# ver o comando final do daemon e por que ele não rodou.
