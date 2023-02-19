import os

from pathlib import Path

DATA_FILES_ROOT = Path(os.path.dirname(os.path.realpath(__file__))).parent.resolve() / 'data'

WS_SOURCE_METEO_DATA_ROOT = DATA_FILES_ROOT / "may"

