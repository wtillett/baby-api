import copy
from datetime import datetime
import pytz
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import insert, select
from model.models import Sleep

from model.database import DBSession


router = APIRouter(prefix="/sleeps", tags=["sleeps"])
tz = pytz.timezone("America/Los_Angeles")


@router.get("/all")
async def get_sleeps() -> dict:
    db = DBSession()
    try:
        sleeps = db.query(Sleep).all()
    finally:
        db.close()
    return {"data": jsonable_encoder(sleeps)}


@router.get("/current")
async def get_current_sleep() -> dict:
    db = DBSession()

    try:
        current_sleep = db.query(Sleep).order_by(Sleep.id.desc()).first()

        if not current_sleep:
            raise HTTPException(
                status_code=400,
                detail={
                    "status": "Error 400 - Bad Request",
                    "msg": "No sleeps yet",
                },
            )
    finally:
        db.close()
    return {"data": jsonable_encoder(current_sleep)}


@router.post("/")
async def start_sleep() -> dict:
    db = DBSession()
    now = datetime.now().astimezone(tz)

    try:
        current_sleep = db.query(Sleep).order_by(Sleep.id.desc()).first()

        if current_sleep and not current_sleep.is_finished:
            raise HTTPException(
                status_code=400,
                detail={
                    "status": "Error 400 - Bad Request",
                    "msg": "There is an active sleep",
                },
            )
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
    now = datetime.now().astimezone(tz)

    try:
        current_sleep = db.query(Sleep).order_by(Sleep.id.desc()).first()

        if not current_sleep:
            raise HTTPException(
                status_code=400,
                detail={
                    "status": "Error 400 - Bad Request",
                    "msg": "No sleeps yet",
                },
            )

        if current_sleep.is_finished:
            raise HTTPException(
                status_code=400,
                detail={
                    "status": "Error 400 - Bad Request",
                    "msg": "No current active sleep",
                },
            )

        db.query(Sleep).filter(Sleep.id == current_sleep.id).update(
            {Sleep.end: now, Sleep.is_finished: True}
        )
        db.commit()
        db.refresh(current_sleep)
    finally:
        db.close()

    return {"data": jsonable_encoder(current_sleep)}


@router.delete("/all")
async def delete_sleeps():
    db = DBSession()

    try:
        num_rows_deleted = db.query(Sleep).delete()
        db.commit()
    finally:
        db.close()

    return {"data": {"num_rows_deleted": num_rows_deleted}}


@router.delete("/{sleep_id}")
async def delete_one_sleep(sleep_id: int) -> dict:
    db = DBSession()

    try:
        sleep_to_delete = db.query(Sleep).filter(Sleep.id == sleep_id)

        if not sleep_to_delete:
            raise HTTPException(
                status_code=404,
                detail={
                    "status": "Error 404 - not found",
                    "msg": "Sleep with the provided id not found",
                },
            )

        deleted_sleep = copy.copy(sleep_to_delete)

        sleep_to_delete.delete()

        db.commit()
    finally:
        db.close()

    return {"data": {"msg": "Successfully deleted"}}
