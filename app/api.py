import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from app.routers import bottles
from app.routers import sleeps
from schemas import BottleInput


from model.database import DBSession
from model import models


app = FastAPI()

app.include_router(bottles.router)
app.include_router(sleeps.router)

origins = ["http://localhost:5173", "localhost:5173"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
