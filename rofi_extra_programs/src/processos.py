"""Gerencia a execução de novos processos."""
# arquivo descartável, não necessário.

import subprocess


def processo_shell(comando: str) -> None:
    """Executa um processo em paralelo no shell."""
    dev_null = subprocess.DEVNULL
    subprocess.run(
        ['/bin/bash', '-ic', f'{comando} &'],
        check=False,
        start_new_session=True,
        stdin=dev_null,
        # stdout=dev_null,
        stderr=dev_null,
    )
