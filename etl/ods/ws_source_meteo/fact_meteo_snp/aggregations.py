from sqlalchemy.sql import text
from typing import Any
from sqlalchemy.orm import Session

from models import OdsFactMeteoSnp
from tools import row_data_to_dict


def latest(db: Session) -> OdsFactMeteoSnp:
    sql_query = text("""
    SELECT *
    FROM fact_meteo_snp
    WHERE meteo_created_dttm = (SELECT MAX(meteo_created_dttm) FROM fact_meteo_snp);
    """)

    return db.query(OdsFactMeteoSnp).from_statement(sql_query).first()


def last_days_avg(db: Session, days_cnt: int) -> dict:
    sql_query = text("""
    SELECT
      AVG(external_temperature_c)               AS external_temperature_c_avg
    , AVG(wind_speed_unmuted_m_s)               AS wind_speed_unmuted_m_s_avg
    , AVG(wind_speed_m_s)                       AS wind_speed_m_s_avg
    , AVG(wind_direction_degrees)               AS wind_direction_degrees_avg
    , AVG(radiation_intensity_unmuted_w_m2)     AS radiation_intensity_unmuted_w_m2_avg
    , AVG(radiation_intensity_w_m2)             AS radiation_intensity_w_m2_avg
    , AVG(standard_radiation_intensity_w_m2)    AS standard_radiation_intensity_w_m2_avg
    , AVG(radiation_sum_j_cm2)                  AS radiation_sum_j_cm2_avg
    , AVG(radiation_from_plant_w_m2)            AS radiation_from_plant_w_m2_avg
    , AVG(precipitation)                        AS precipitation_avg
    , AVG(relative_humidity_perc)               AS relative_humidity_perc_avg
    , AVG(moisture_deficit_g_kg)                 AS moisture_deficit_g_kg_avg
    , AVG(moisture_deficit_g_m3)                 AS moisture_deficit_g_m3_avg
    , AVG(dew_point_temperature_c)              AS dew_point_temperature_c_avg
    , AVG(abs_humidity_g_kg)                    AS abs_humidity_g_kg_avg
    , AVG(enthalpy_kj_kg)                       AS enthalpy_kj_kg_avg
    , AVG(enthalpy_kj_m3)                       AS enthalpy_kj_m3_avg
    , AVG(atmospheric_pressure_hpa)             AS atmospheric_pressure_hpa_avg
    FROM fact_meteo_snp
    --WHERE meteo_created_dttm BETWEEN (NOW() - interval ':days_cnt day') AND NOW()
    WHERE meteo_created_dttm BETWEEN (DATE '2021-05-04' - interval ':days_cnt day') AND DATE '2021-05-04'
    """).bindparams(days_cnt=days_cnt)

    return dict(zip(db.execute(sql_query).keys(), db.execute(sql_query).fetchone()))


def last_week_avg_trunked(db: Session) -> dict:
    sql_query = text("""
    SELECT
      DATE(meteo_created_dttm)                  AS dttm
    , AVG(external_temperature_c)               AS external_temperature_c_avg
    , AVG(wind_speed_unmuted_m_s)               AS wind_speed_unmuted_m_s_avg
    , AVG(wind_speed_m_s)                       AS wind_speed_m_s_avg
    , AVG(wind_direction_degrees)               AS wind_direction_degrees_avg
    , AVG(radiation_intensity_unmuted_w_m2)     AS radiation_intensity_unmuted_w_m2_avg
    , AVG(radiation_intensity_w_m2)             AS radiation_intensity_w_m2_avg
    , AVG(standard_radiation_intensity_w_m2)    AS standard_radiation_intensity_w_m2_avg
    , AVG(radiation_sum_j_cm2)                  AS radiation_sum_j_cm2_avg
    , AVG(radiation_from_plant_w_m2)            AS radiation_from_plant_w_m2_avg
    , AVG(precipitation)                        AS precipitation_avg
    , AVG(relative_humidity_perc)               AS relative_humidity_perc_avg
    , AVG(moisture_deficit_g_kg)                 AS moisture_deficit_g_kg_avg
    , AVG(moisture_deficit_g_m3)                 AS moisture_deficit_g_m3_avg
    , AVG(dew_point_temperature_c)              AS dew_point_temperature_c_avg
    , AVG(abs_humidity_g_kg)                    AS abs_humidity_g_kg_avg
    , AVG(enthalpy_kj_kg)                       AS enthalpy_kj_kg_avg
    , AVG(enthalpy_kj_m3)                       AS enthalpy_kj_m3_avg
    , AVG(atmospheric_pressure_hpa)             AS atmospheric_pressure_hpa_avg
    FROM fact_meteo_snp
    -- WHERE meteo_created_dttm BETWEEN (NOW() - interval ':days_cnt day') AND NOW()
    WHERE meteo_created_dttm BETWEEN (DATE '2021-05-04' - interval ':days_cnt day') AND DATE '2021-05-04'
    GROUP BY dttm, date_trunc('day', meteo_created_dttm)
    """).bindparams(days_cnt=7)

    return row_data_to_dict(db.execute(sql_query).keys(), db.execute(sql_query).fetchall())


def last_day_changes_fifteen_min(db: Session, min_count: int) -> dict:
    sql_query = text("""
       SELECT
          date_trunc('hour', meteo_created_dttm) +
          (((date_part('minute', meteo_created_dttm)::integer / :min_count ::integer) * :min_count ::integer)
          || ' minutes')::interval                  AS dttm
        , AVG(external_temperature_c)               AS external_temperature_c_avg
        , AVG(wind_speed_unmuted_m_s)               AS wind_speed_unmuted_m_s_avg
        , AVG(wind_speed_m_s)                       AS wind_speed_m_s_avg
        , AVG(wind_direction_degrees)               AS wind_direction_degrees_avg
        , AVG(radiation_intensity_unmuted_w_m2)     AS radiation_intensity_unmuted_w_m2_avg
        , AVG(radiation_intensity_w_m2)             AS radiation_intensity_w_m2_avg
        , AVG(standard_radiation_intensity_w_m2)    AS standard_radiation_intensity_w_m2_avg
        , AVG(radiation_sum_j_cm2)                  AS radiation_sum_j_cm2_avg
        , AVG(radiation_from_plant_w_m2)            AS radiation_from_plant_w_m2_avg
        , AVG(precipitation)                        AS precipitation_avg
        , AVG(relative_humidity_perc)               AS relative_humidity_perc_avg
        , AVG(moisture_deficit_g_kg)                 AS moisture_deficit_g_kg_avg
        , AVG(moisture_deficit_g_m3)                 AS moisture_deficit_g_m3_avg
        , AVG(dew_point_temperature_c)              AS dew_point_temperature_c_avg
        , AVG(abs_humidity_g_kg)                    AS abs_humidity_g_kg_avg
        , AVG(enthalpy_kj_kg)                       AS enthalpy_kj_kg_avg
        , AVG(enthalpy_kj_m3)                       AS enthalpy_kj_m3_avg
        , AVG(atmospheric_pressure_hpa)             AS atmospheric_pressure_hpa_avg
    FROM fact_meteo_snp
    -- WHERE meteo_created_dttm BETWEEN (NOW() - interval ':days_cnt day') AND NOW()
    WHERE meteo_created_dttm BETWEEN (DATE '2021-05-04' - interval ':days_cnt day') AND DATE '2021-05-04'
    GROUP BY dttm
    ORDER BY dttm
        """).bindparams(days_cnt=1, min_count=min_count)

    return row_data_to_dict(db.execute(sql_query).keys(), db.execute(sql_query).fetchall())
