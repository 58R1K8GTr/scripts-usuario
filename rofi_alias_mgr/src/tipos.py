"""Tipos para fazer a tipagem do programa."""


from pathlib import Path
from typing import Iterable, TypedDict
from datetime import datetime


DictStrStrTipo = dict[str, str]
DictStrDictTipo = dict[str, DictStrStrTipo]
JsonTipo = dict[str, DictStrDictTipo]
DataAliasesTipo = Iterable[tuple[Path, str, str]]
ListaDatetimeTipo = list[datetime]


class StatusModificacaoTipo(TypedDict):
    """Tipo de status de modificação de arquivo."""
    arquivos_alterados: bool
    novas_modificacoes: ListaDatetimeTipo
