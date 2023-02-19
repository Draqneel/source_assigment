from datetime import datetime
from pydantic import (
    BaseModel,
    Json,
)
from typing import Union


class OdsFactMeteoSnpMeta(BaseModel):
    meteo_created_dttm: datetime
    external_temperature_c: float
    wind_speed_unmuted_m_s: float
    wind_speed_m_s: float
    wind_direction_degrees: int
    radiation_intensity_unmuted_w_m2: float
    radiation_intensity_w_m2: float
    standard_radiation_intensity_w_m2: int
    radiation_sum_j_cm2: float
    radiation_from_plant_w_m2: int
    precipitation: int
    relative_humidity_perc: int
    moisture_deficit_g_kg: float
    moisture_deficit_g_m3: float
    dew_point_temperature_c: float
    abs_humidity_g_kg: float
    enthalpy_kj_kg: float
    enthalpy_kj_m3: float
    atmospheric_pressure_hpa: int

    class Config:
        orm_mode = True
