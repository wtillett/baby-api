from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from model.database import DBSession
from model import models


app = FastAPI()

origins = ["http://localhost:5713", "localhost:5173"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your todo list"}
