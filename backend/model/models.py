from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

import uuid


Base = declarative_base()


class Bottle(Base):

    __tablename__ = "bottles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String)
    time = Column(String)
    amount = Column(String)

    def __repr__(self):
        return f"Bottle (id={self.id}, date={self.date}, time={self.time}, amount={self.amount})"
