"""Gerenciar estruturas de dados."""


from src.tipos import DataAliasesTipo, JsonTipo


# refatorar pois há algo faltando. (dica: Path)
def gerar_dict_alias(dados: DataAliasesTipo) -> JsonTipo:
    """Retorna um dicionário no formato adequado para salvamento."""
    return {
        "aliases": {
            str(local): {'mtime': hora, 'hash': str_hash}
            for local, hora, str_hash in dados
        }
    }
