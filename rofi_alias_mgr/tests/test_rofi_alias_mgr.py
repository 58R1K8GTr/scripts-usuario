import pytest
from unittest.mock import patch
from src.constantes import HOME_ALIASES
from rofi_alias_mgr import verificar_modificacoes, atualizar_arquivos
from datetime import datetime
from zoneinfo import ZoneInfo


ZONA = ZoneInfo('localtime')


@pytest.fixture
def mock_mtime_arquivo():
    with patch("rofi_alias_mgr.mtime_arquivo") as mock:
        yield mock


@pytest.fixture
def mock_ler_json():
    with patch("rofi_alias_mgr.ler_json") as mock:
        yield mock


def test_verificar_modificacoes(mock_mtime_arquivo, mock_ler_json):
    mtimes = [
        "1970-01-01T00:00:01-03:00",
        "1970-01-01T00:00:02-03:00",
        "1970-01-01T00:00:03-03:00"
    ]
    mock_mtime_arquivo.side_effect = map(
        datetime.fromisoformat, mtimes
    )
    mock_ler_json.return_value = {
        "aliases": {
            str(HOME_ALIASES[0]): {"mtime": mtimes[0]},
            str(HOME_ALIASES[1]): {"mtime": mtimes[1]},
            str(HOME_ALIASES[2]): {"mtime": mtimes[2]},
        }
    }

    status = verificar_modificacoes()
    assert status["arquivos_alterados"] is False
    assert len(status["novas_modificacoes"]) == len(HOME_ALIASES)


def test_atualizar_arquivos():
    mock_status = {
        "arquivos_alterados": True,
        "novas_modificacoes": [1, 2, 3],
    }

    with patch("rofi_alias_mgr.escrever_aliases") as mock_escrever_aliases, \
         patch("rofi_alias_mgr.atualizar_hashs") as mock_atualizar_hashs:
        atualizar_arquivos(mock_status)
        mock_escrever_aliases.assert_called_once()
        mock_atualizar_hashs.assert_called_once_with(mock_status["novas_modificacoes"])
