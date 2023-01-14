from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session
from config import USERNAME, PASSWORD, SERVER, DB


metadata = MetaData()
engine = create_engine(f"mysql+pymysql://{USERNAME}:{PASSWORD}@{SERVER}/{DB}")
session = Session(bind=engine)


