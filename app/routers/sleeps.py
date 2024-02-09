from datetime import datetime
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy import insert, select
from model.models import Sleep

from model.database import DBSession


router = APIRouter(prefix="/sleeps", tags=["sleeps"])


@router.get("/")
async def get_sleeps() -> dict:
    db = DBSession()
    try:
        sleeps = db.query(Sleep).all()
    finally:
        db.close()
    return {"data": jsonable_encoder(sleeps)}


@router.post("/")
async def start_sleep() -> dict:
    db = DBSession()
    now = datetime.now()

    try:
        new_sleep = Sleep(start=now)

        db.add(new_sleep)
        db.commit()
        db.refresh(new_sleep)
    finally:
        db.close()

    return {"data": jsonable_encoder(new_sleep)}


@router.put("/")
async def end_sleep():
    db = DBSession()
    now = datetime.now()

    try:
        current_sleep = db.query(Sleep).order_by(Sleep.id.desc()).first()
        db.query(Sleep).filter(Sleep.id == current_sleep.id).update(
            {Sleep.end: now, Sleep.is_finished: True}
        )
        db.commit()
        db.refresh(current_sleep)
    finally:
        db.close()

    return {"data": jsonable_encoder(current_sleep)}
