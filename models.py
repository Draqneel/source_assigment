from sqlalchemy import (
    Column,
    Integer, JSON, DateTime, Double
)

from database import Base


class RawMeteo(Base):
    """Source System - ws_source_meteo"""
    __tablename__ = "raw_meteo"

    id = Column(Integer, primary_key=True)
    data = Column(JSON)
    created_at_dttm = Column(DateTime, index=True)


class OdsFactMeteoSnp(Base):
    """
    Contains data from greenhouse meteo sensors
    Builds on RawMeteo
    Source System - ws_source_meteo
    """
    __tablename__ = "fact_meteo_snp"

    # TODO: Add more detail about data fields - doc()
    meteo_created_dttm = Column(DateTime, primary_key=True, index=True)
    external_temperature_c = Column(Double)
    wind_speed_unmuted_m_s = Column(Double)
    wind_speed_m_s = Column(Double)
    wind_direction_degrees = Column(Integer)
    radiation_intensity_unmuted_w_m2 = Column(Integer)
    radiation_intensity_w_m2 = Column(Double)
    standard_radiation_intensity_w_m2 = Column(Integer)
    radiation_sum_j_cm2 = Column(Double)
    radiation_from_plant_w_m2 = Column(Integer)
    precipitation = Column(Integer)
    relative_humidity_perc = Column(Integer)
    moisture_deficit_g_kg = Column(Double)
    moisture_deficit_g_m3 = Column(Double)
    dew_point_temperature_c = Column(Double)
    abs_humidity_g_kg = Column(Double)
    enthalpy_kj_kg = Column(Double)
    enthalpy_kj_m3 = Column(Double)
    atmospheric_pressure_hpa = Column(Integer)
