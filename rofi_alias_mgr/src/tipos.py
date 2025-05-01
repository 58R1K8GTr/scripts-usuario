"""Tipos para fazer a tipagem do programa."""


from pathlib import Path
from typing import Iterable, TypedDict


DictStrStrTipo = dict[str, str]
DictStrDictTipo = dict[str, DictStrStrTipo]
JsonTipo = dict[str, DictStrDictTipo]
DataAliasesTipo = Iterable[tuple[Path, str, str]]
ListaDatetimeTipo = Iterable[str]


class StatusModificacaoTipo(TypedDict):
    """Tipo de status de modificação de arquivo."""
    arquivos_alterados: bool
    mtimes: ListaDatetimeTipo
