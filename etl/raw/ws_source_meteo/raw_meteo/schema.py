from datetime import datetime
from pydantic import Json, BaseModel
from typing import Union


class RawMeteoMeta(BaseModel):
    id: int
    data: Union[Json, dict]
    created_at_dttm: datetime

    class Config:
        orm_mode = True
