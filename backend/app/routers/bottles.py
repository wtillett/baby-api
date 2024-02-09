from datetime import datetime
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from model.models import Bottle
from schemas import BottleInput
from model.database import DBSession

router = APIRouter(prefix="/bottles", tags=["bottles"])


@router.get("/")
async def get_bottles() -> dict:
    db = DBSession()
    try:
        bottles = db.query(Bottle).all()
    finally:
        db.close()
    return {"data": jsonable_encoder(bottles)}


@router.post("/")
async def add_bottle(bottle: BottleInput) -> dict:
    db = DBSession()

    now = datetime.now()

    try:
        new_bottle = Bottle(
            date=f"{now.month}/{now.day}/{str(now.year)[2:]}",
            time=now.strftime("%I:%M %p"),
            amount=bottle.amount,
        )

        db.add(new_bottle)
        db.commit()
        db.refresh(new_bottle)
    finally:
        db.close()

    return {"data": jsonable_encoder(new_bottle)}
