from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session

from config import SERVER, USERNAME, PASSWORD, DB

metadata = MetaData()
# engine = create_engine(f"mysql+pymysql://{USERNAME}:{PASSWORD}@{SERVER}/{DB}")
engine = create_engine("ibm_db_sa://jzg20410:DHYw385kfnn4K4bq@2d46b6b4-cbf6-40eb-bbce-6251e6ba0300.bs2io90l08kqb1od8lcg.databases.appdomain.cloud:32328/bludb?security=SSL")
session = Session(bind=engine)


