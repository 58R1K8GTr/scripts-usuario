"""Textos em geral."""


# flake8: noqa: E501


TEXTO_SERVICO_OPCAO1_DESFORMATADO = """\
[Unit]
Description=Serviço do rofi-alias-mgr

[Service]
ExecStart=inotifywait -m -e close_write ~/.bash_aliases* | while read caminho evento; do {}; done
Restart=always

[Install]
WantedBy=default.target
"""

TEXTO_SERVICO_OPCAO2_DESFORMATADO = """\
[Unit]
Description=Serviço do rofi-alias-mgr

[Service]
Type=oneshot
ExecStart={}
"""

TEXTO_TIMER2 = """\
[Unit]
Description=Timer para executar o rofi-alias-mgr a cada 5 horas

[Timer]
OnBootSec=5min
OnUnitActiveSec=5h
Persistent=true

[Install]
WantedBy=timers.target
"""
