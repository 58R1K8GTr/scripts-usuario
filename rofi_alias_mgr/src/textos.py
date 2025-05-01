"""Textos para serem inseridos em arquivos posteriormente."""


# flake8: noqa: E501


TEXTO_SERVICO_DESFORMATADO = """\
[Unit]
Description=Serviço do rofi-alias-mgr

[Service]
Type=oneshot
ExecStart={} --verificar --atualizar
"""

TEXTO_TIMER = """\
[Unit]
Description=Timer para executar o rofi-alias-mgr a cada 5 horas

[Timer]
OnBootSec=5min
OnUnitActiveSec=5h
Persistent=true

[Install]
WantedBy=timers.target
"""
