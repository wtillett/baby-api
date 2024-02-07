from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder


from model.database import DBSession
from model import models


app = FastAPI()

origins = ["http://localhost:5173", "localhost:5173"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/bottles", tags=["bottles"])
async def get_bottles() -> dict:
    db = DBSession()
    try:
        bottles = db.query(models.Bottle).all()
    finally:
        db.close()
    return {"data": jsonable_encoder(bottles)}


@app.post("/bottle", tags=["bottles"])
async def add_bottle(bottle: dict) -> dict:
    # bottles.append(bottle)
    return {"data": {"Bottle added."}}
