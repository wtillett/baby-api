from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Bottle(Base):

    __tablename__ = "bottles"

    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime)
    amount = Column(Integer)

    def __repr__(self):
        return (
            f"Bottle (id={self.id}, date_time={self.date_time}, amount={self.amount})"
        )
