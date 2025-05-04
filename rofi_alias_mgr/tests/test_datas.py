from unittest.mock import patch
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from src.datas import mtime_arquivo, mtime_json

ZONA = ZoneInfo('America/Sao_Paulo')  # Ajustado para um fuso horário válido


def test_mtime_arquivo():
    with patch("pathlib.Path.stat") as mock_stat:
        mock_stat.return_value.st_mtime = 1633057200
        resultado = mtime_arquivo(Path("dummy.txt"))
        assert resultado == datetime(2021, 10, 1, 0, 0, tzinfo=ZONA)


def test_mtime_json():
    resultado = mtime_json('2021-10-01T00:00:00-03:00')
    assert resultado == datetime(2021, 10, 1, 0, 0, tzinfo=ZONA)
