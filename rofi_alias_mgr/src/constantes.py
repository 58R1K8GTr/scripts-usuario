"""Contém todas as contantes que devem ser utilizadas no projeto."""


from pathlib import Path

home_encurtada = Path('~')
HOME = home_encurtada.expanduser()
ROFI_DATA = HOME / '.config/rofi/alias_data'
ROFI_JSON = ROFI_DATA / 'data.json'
ROFI_ALIASES = ROFI_DATA / 'aliases.txt'
ALIASES_NAMES = ('.bash_aliases', '.bash_aliases_debian', '.bash_aliases_arch')
HOME_ALIASES = [HOME / alias for alias in ALIASES_NAMES]
HOME_ALIASES_ENCURTADO = [home_encurtada / alias for alias in ALIASES_NAMES]
