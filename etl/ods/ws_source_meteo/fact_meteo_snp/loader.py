from database import Base
from sqlalchemy import inspect
from typing import List
from sqlalchemy.orm import Session
from collections import defaultdict

from models import RawMeteo, OdsFactMeteoSnp


def _prepare_extracted_data(db: Session):
    return db.query(RawMeteo).all()


def _extract_data_by_schema(data: dict, table: Base) -> OdsFactMeteoSnp:
    result_data = defaultdict()
    data = defaultdict(None, data)
    schema = list(map(lambda col: col.key, inspect(table).attrs))

    for row_ls in data['rows']:
        if row_ls[0] in schema:
            result_data[row_ls[0]] = row_ls[1]
    result_data["meteo_created_dttm"] = data["ts"]

    return OdsFactMeteoSnp(**result_data)


def _get_etl_entities(db: Session) -> List[OdsFactMeteoSnp]:
    queried_data = _prepare_extracted_data(db)

    return list(map(lambda column:
                    _extract_data_by_schema(column.data, OdsFactMeteoSnp),
                    queried_data))


def fact_meteo_snp_calculation(db: Session) -> List[OdsFactMeteoSnp]:
    new_entities_list = _get_etl_entities(db)
    db.add_all(new_entities_list)
    db.commit()

    return new_entities_list
