from typing import List
from pathlib import Path
from datetime import datetime
from sqlalchemy.orm import Session

from configs.etl_conf import WS_SOURCE_METEO_DATA_ROOT
from models import RawMeteo
from tools import json_to_dict


def _get_all_data_paths(root_path: Path = WS_SOURCE_METEO_DATA_ROOT) -> List[Path]:
    res = []
    for data_dir in root_path.iterdir():
        res.extend(list(data_dir.glob('**/*.json')))
    return res


def raw_meteo_calculation(db: Session) -> List[RawMeteo]:
    all_data = [json_to_dict(json_path) for json_path in _get_all_data_paths()]

    new_entities = list(map(
        lambda json_dict: RawMeteo(data=json_dict, created_at_dttm=datetime.now()),
        all_data
    ))

    db.add_all(new_entities)
    db.commit()

    return new_entities