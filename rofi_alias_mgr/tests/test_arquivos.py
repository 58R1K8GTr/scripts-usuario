from pytest import fixture
from unittest.mock import patch, mock_open
from pathlib import Path
from src.arquivos import ler_json, escrever_json


@fixture
def mock_open_file():
    with patch("pathlib.Path.open", mock_open()) as mock:
        yield mock


def test_ler_json(mock_open_file):
    mock_open_file.return_value.read.return_value = '{"aliases": {}}'
    resultado = ler_json(Path("dummy.json"))
    assert resultado == {"aliases": {}}


def test_escrever_json(mock_open_file):
    conteudo = {"aliases": {"test": "value"}}
    escrever_json(conteudo, Path("dummy.json"))
    mock_open_file.assert_called_once_with("w")
