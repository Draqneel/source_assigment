import models
import logging as log

from sqlalchemy.orm import Session
from database import engine
from fastapi import FastAPI, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from etl.raw.ws_source_meteo.raw_meteo.loader import raw_meteo_calculation

from etl.ods.ws_source_meteo.fact_meteo_snp.schema import OdsFactMeteoSnpMeta
from etl.ods.ws_source_meteo.fact_meteo_snp.loader import fact_meteo_snp_calculation
from etl.ods.ws_source_meteo.fact_meteo_snp.aggregations import (
    latest,
    last_days_avg,
    last_week_avg_trunked,
    last_day_changes_fifteen_min,
)


from database import get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

log.basicConfig(
    filename="web_server.log",
    level=log.DEBUG,
    format="%(asctime)s.%(msecs)d: %(levelname)s\t%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

"""
In the future, we need to use AirFlow (or something similar) for schedule ETL.
In target architecture we should use: 
 1. raw_meteo_recalculation_endpoint
 2. fact_meteo_snp_recalculation_endpoint
ONLY for full tables recalculation, regular calculations should use the CTL table.
"""


@app.get('/raw/ws_source_meteo/raw_meteo/recalculation')
def raw_meteo_recalculation_endpoint(db: Session = Depends(get_db)) -> JSONResponse:
    # TODO: Access only for staff members with WRITE rights
    try:
        raw_meteo_calculation(db)
        return JSONResponse(content=None)
    except Exception as e:
        log.error(f"*** Error in raw_meteo_recalculation_endpoint '{str(e)}'. Sent 500.")
        return JSONResponse(content=None, status_code=500)


@app.get('/ods/ws_source_meteo/fact_meteo_snp/recalculation')
def fact_meteo_snp_recalculation_endpoint(db: Session = Depends(get_db)) -> JSONResponse:
    # TODO: Access only for staff members with WRITE rights
    try:
        fact_meteo_snp_calculation(db)
        return JSONResponse(content=None)
    except Exception as e:
        log.error(f"*** Error in fact_meteo_snp_recalculation_endpoint '{str(e)}'. Sent 500.")
        return JSONResponse(content=None, status_code=500)


@app.get('/weather_conditions/latest',
         response_model=OdsFactMeteoSnpMeta)
def weather_conditions_latest_endpoint(db: Session = Depends(get_db)) -> JSONResponse:
    try:
        return JSONResponse(content=jsonable_encoder(latest(db)))
    except Exception as e:
        log.error(f"*** Error in *_latest_endpoint '{str(e)}'. Sent 500.")
        return JSONResponse(content=None, status_code=500)


@app.get('/weather_conditions/last_day_avg')
def weather_conditions_last_day_avg_endpoint(db: Session = Depends(get_db)) -> JSONResponse:
    try:
        return JSONResponse(content=jsonable_encoder(last_days_avg(db, 1)))
    except Exception as e:
        log.error(f"*** Error in *_last_day_avg_endpoint '{str(e)}'. Sent 500.")
        return JSONResponse(content=None, status_code=500)


@app.get('/weather_conditions/last_week_avg')
def weather_conditions_last_week_avg_endpoint(db: Session = Depends(get_db)) -> JSONResponse:
    try:
        return JSONResponse(content=jsonable_encoder(last_days_avg(db, 7)))
    except Exception as e:
        log.error(f"*** Error in *_last_week_avg_endpoint '{str(e)}'. Sent 500.")
        return JSONResponse(content=None, status_code=500)


@app.get('/weather_conditions/last_week_avg_trunked')
def weather_conditions_last_week_avg_trunked_endpoint(db: Session = Depends(get_db)) -> JSONResponse:
    try:
        return JSONResponse(content=jsonable_encoder(last_week_avg_trunked(db)))
    except Exception as e:
        log.error(f"*** Error in *_last_week_avg_trunked_endpoint '{str(e)}'. Sent 500.")
        return JSONResponse(content=None, status_code=500)


@app.get('/weather_conditions/last_day_changes_fifteen_min')
def weather_conditions_last_day_changes_fifteen_min(db: Session = Depends(get_db)) -> JSONResponse:
    try:
        return JSONResponse(content=jsonable_encoder(last_day_changes_fifteen_min(db, 15)))
    except Exception as e:
        log.error(f"*** Error in *_last_day_changes_fifteen_min '{str(e)}'. Sent 500.")
        return JSONResponse(content=None, status_code=500)
