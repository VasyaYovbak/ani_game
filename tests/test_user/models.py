from faker import Faker
import requests

fake = Faker()


class RegisterUserData:

    @staticmethod
    def valid_data():
        username = fake.name()
        email = fake.email()
        password = "Password123@"

        # return {"username": 'test_11_0510', "email": "rxqu3nn_18@gmail.com", "password": 'test_11_0510'}
        return {"username": username, "email": email, "password": password}

    @staticmethod
    def already_registered():
        username = "Roma_first"
        email = "test_login_8@test.com"
        password = "Password123@"

        return {"username": username, "email": email, "password": password}

    @staticmethod
    def empty_data():
        username = ""
        email = ""
        password = ""

        return {"username": username, "email": email, "password": password}

    @staticmethod
    def invalid_data():
        username = "ad"
        email = "advdavaxv"
        password = "12345"

        return {"username": username, "email": email, "password": password}

    @staticmethod
    def digits_name():
        username = "Roma123"
        email = "roma_mail@test.com"
        password = "Password123@"

        return {"username": username, "email": email, "password": password}

    @staticmethod
    def symbols_name():
        username = "Roma@#$"
        email = "roma_mail2@test.com"
        password = "Password123@"

        return {"username": username, "email": email, "password": password}

    @staticmethod
    def invalid_fields():
        username = fake.password()
        email = fake.email()
        password = fake.password()

        return {"username1": username, "email1": email, "password1": password}

    @staticmethod
    def empty_fields():

        username = fake.password()
        email = fake.email()
        password = fake.password()

        return {"": username, "": email, "": password}


class LoginUserData:

    @staticmethod
    def valid_data():
        email = "test_login_8@test.com"
        password = "Password123@"

        return {"email": email, "password": password}

    @staticmethod
    def invalid_email():
        email = "test_login_1@test.com_invalid"
        password = "Password123@_invalid"

        return {"email": email, "password": password}

    @staticmethod
    def user_dont_exist():
        email = "test_login_2@test.com"
        password = "Password123@"

        return {"email": email, "password": password}

    @staticmethod
    def empty_data():
        email = ""
        password = ""

        return {"email": email, "password": password}

    @staticmethod
    def invalid_fields():
        email = fake.email()
        password = fake.password()

        return {"email1": email, "password1": password}

    @staticmethod
    def empty_fields():
        email = fake.email()
        password = fake.password()

        return {"": email, "": password}


class LogoutUserData:

    @staticmethod
    def invalid_tokens():

        access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NTc2ODgyNywianRpIjoi" \
                       "YjFmMGIxYzctOGQ3Yi00MTMzLTk1MjgtYTQ5MzAyZjJjNjdlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NjIsIm5iZiI6" \
                       "MTY2NTc2ODgyNywiZXhwIjoxNjY1NzY5MDA3fQ.xroPELrpl1vE9RlMLuhqfwWhUw9Dp-eEqrcFMjvRJ70"

        refresh_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NTc2ODgyNywianRpIjoiYWEwY" \
                        "mVmYjgtZGYxNi00ZGNmLTg3NTItZTAyYTk2MGE1Njk0IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOjYyLCJuYmYiOjE2NjU3Njg" \
                        "4MjcsImV4cCI6MTY2NTgxMjAyN30.lNR-qeS1NV9yHpukR4bFTbPlpK0VcWiJZfOltSkTdp4"

        return {"access_token": access_token, "refresh_token": refresh_token}

    @staticmethod
    def empty_tokens():

        access_token = ""
        refresh_token = ""

        return {"access_token": access_token, "refresh_token": refresh_token}


class RefreshTokensData:

    @staticmethod
    def empty_token():

        refresh_token = ""
        return {"refresh_token": refresh_token}

    @staticmethod
    def invalid_refresh_token():

        refresh_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NTc3MjQwOSwianRpIjoiZm" \
                        "QwMDhmYTMtYWIzMi00MmQyLThhZTMtMzM2OTkzODllMTRlIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOjYyLCJuYmYiOj" \
                        "E2NjU3NzI0MDksImV4cCI6MTY2NTgxNTYwOX0.b-inApxB-7oTG_Y9BKN9n7c959utYAMrC7VsQe4M6E"

        return {"refresh_token": refresh_token}

    @staticmethod
    def invalid_fields():

        refresh_token = "dsfsefsdfsefsdfsefdsfsefsdfsfesfs"

        return {"refresh_tokens": refresh_token}

    @staticmethod
    def empty_fields():
        refresh_token = ""

        return {"": refresh_token}


class VerifyEmailData:

    @staticmethod
    def valid_email():
        email = "rxqu3nn@gmail.com",
        return {"email": email}

    @staticmethod
    def invalid_email():
        email = "rxqu3nngmail.com"
        return {"email": email}

    @staticmethod
    def empty_email():
        email = ""
        return {"email": email}


class ResetPasswordData:

    @staticmethod
    def valid_email():
        email = "rxqu3nn@gmail.com",
        return {"email": email}

    @staticmethod
    def invalid_email():
        email = "rxqu3nngmail.com"
        return {"email": email}

    @staticmethod
    def empty_email():
        email = ""
        return {"email": email}

    @staticmethod
    def new_password():
        password = "Password123@"
        return {"password": password}

    @staticmethod
    def new__invalid_password():
        password = "Password123"
        return {"password": password}


class ResponseModel:

    def __init__(self, status_code: int, response: dict = None):
        self.status_code = status_code
        self.response_data = response


class Client:
    @staticmethod
    def custom_request(method: str, url, **kwargs):
        return requests.request(method, url, **kwargs)

