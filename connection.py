import os

# from sqlalchemy import create_engine, MetaData
# from sqlalchemy.orm import Session
# from config import USERNAME, PASSWORD, SERVER, DB
#
#
# metadata = MetaData()
# engine = create_engine(f"mysql+pymysql://{USERNAME}:{PASSWORD}@{SERVER}/{DB}")
# session = Session(bind=engine)


from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session

CONNECTION_URL = os.getenv("CONNECTION_URL")

metadata = MetaData()
engine = create_engine(CONNECTION_URL)
session = Session(bind=engine)

