ok here are the sqlalchemy code for the day with the help of your hints so how did i do

from sqlalchemy import Column, Integer, String, Boolena
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Pipeline(Base):
    __tablename__ = "pipelines"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    active = Column(Boolena)

active_pipeline = session.query(Pipeline).filter(Pipeline.active == 1).all() what is this doing 

pipeline = session.query(Pipeline).filter(Pipeline.id == 5).one()

new_record = Pipeline(name="daily ETL", active=True)
session.add(new_record)
session.commit()

pipeline = session.query(Pipeline).filter(Pipeline.id == 5).one()
pipeline.active = 0
session.commit()
