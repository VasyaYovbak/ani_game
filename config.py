from sendgrid import SendGridAPIClient
import os

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
SERVER = os.getenv("SERVER")
DB = os.getenv("DB")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")


class SendGridApi_key:
    API_KEY = os.getenv("API_KEY")

# mysql+pymysql://root:root@127.0.0.1:3306/narutodatabase
