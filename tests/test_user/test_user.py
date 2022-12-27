from models import RegisterUserData, LoginUserData, LogoutUserData, RefreshTokensData, VerifyEmailData, \
    ResetPasswordData

from schemas.schemas import valid_schema, empty_schema, invalid_schema, invalid_field_schema, \
    already_exists_schema, email_verification_valid_schema, email_verification_invalid_schema, \
    email_confirmation_valid_schema, email_confirmation_invalid_schema, reset_password_valid_schema,\
    reset_password_invalid_schema

from methods import Register, Login, Logout, is_refresh_revoked, is_user_added_to_db, RefreshToken, \
    SendEmailConfirmation, SendEmailReset, ConfirmEmail, ResetPassword

import jwt as jwt1
from config import Config
from connection import session
from user_view.models import User


class TestRegistration:

    def test_registration_valid_data(self):
        body = RegisterUserData.valid_data()
        response = Register().register_user(body=body, schema=valid_schema)

        assert response.status_code == 201
        assert response.response_data.get('access_token')
        assert response.response_data.get('refresh_token')
        assert is_user_added_to_db(body)

    def test_registration_already_exist(self):
        body = RegisterUserData.already_registered()
        response = Register().register_user(body=body, schema=already_exists_schema)

        assert response.status_code == 400
        assert response.response_data.get("error") == "User with this email or username is already registered."

    def test_registration_empty_data(self):
        body = RegisterUserData.empty_data()
        response = Register().register_user(body=body, schema=empty_schema)

        assert response.status_code == 400
        assert is_user_added_to_db(body) == False
        assert response.response_data.get("error")

    def test_registration_invalid_data(self):
        body = RegisterUserData.invalid_data()
        response = Register().register_user(body=body, schema=invalid_schema)

        assert response.status_code == 400
        assert response.response_data.get("error")

    def test_registration_digits_in_name(self):
        body = RegisterUserData.digits_name()
        response = Register().register_user(body=body, schema=invalid_schema)

        assert response.status_code == 400
        assert response.response_data.get("error")

    def test_registration_symbols_in_name(self):
        body = RegisterUserData.symbols_name()
        response = Register().register_user(body=body, schema=invalid_schema)

        assert response.status_code == 400
        assert response.response_data.get("error")

    def test_registration_invalid_fields(self):
        body = RegisterUserData.invalid_fields()
        response = Register().register_user(body=body, schema=invalid_field_schema)

        assert response.status_code == 400
        assert response.response_data.get("error")

    def test_registration_empty_fields(self):
        body = RegisterUserData.empty_fields()
        response = Register().register_user(body=body, schema=invalid_field_schema)

        assert response.status_code == 400
        assert response.response_data.get("error")


class TestLogin:

    def test_login_valid_data(self):
        body = LoginUserData.valid_data()
        response = Login().login_user(body=body, schema=valid_schema)

        assert response.status_code == 200
        assert response.response_data.get('access_token')
        assert response.response_data.get('refresh_token')

    def test_login_invalid_email(self):
        body = LoginUserData.invalid_email()
        response = Login().login_user(body=body, schema=invalid_schema)

        assert response.status_code == 400
        assert response.response_data.get('error')

    def test_login_user_dont_exists(self):
        body = LoginUserData.user_dont_exist()
        response = Login().login_user(body=body, schema=invalid_schema)

        assert response.status_code == 400
        assert response.response_data.get('error') == "User with such an email does not exist."

    def test_login_empty_data(self):
        body = LoginUserData.empty_data()
        response = Login().login_user(body=body, schema=empty_schema)

        assert response.status_code == 400
        assert response.response_data.get('error')

    def test_login_invalid_fields(self):
        body = LoginUserData.invalid_fields()
        response = Login().login_user(body=body, schema=invalid_field_schema)

        assert response.status_code == 400
        assert response.response_data.get('error')

    def test_login_empty_fields(self):
        body = LoginUserData.empty_fields()
        response = Login().login_user(body=body, schema=invalid_field_schema)

        assert response.status_code == 400
        assert response.response_data.get('error')


class TestLogout:

    def test_logout_valid_data(self):
        login_body = LoginUserData.valid_data()
        login_response = Login().login_user(body=login_body, schema=valid_schema)

        access_token = login_response.response_data.get('access_token')
        refresh_token = login_response.response_data.get('refresh_token')

        logout_body = {"refresh_token": refresh_token}
        logout_response = Logout().logout_user(body=logout_body, schema=empty_schema, access_token=access_token)

        decoded_refresh = jwt1.decode(refresh_token, Config.SECRET_KEY, algorithms=["HS256"])

        assert is_refresh_revoked(decoded_refresh)
        assert logout_response.status_code == 200

    def test_logout_invalid_tokens(self):

        logout_body = LogoutUserData.invalid_tokens()

        logout_response = Logout().logout_user(body=logout_body,
                                               schema=invalid_schema,
                                               access_token=logout_body['access_token'])

        assert logout_response.status_code == 401
        assert logout_response.response_data.get('msg')

    def test_logout_empty_tokens(self):

        logout_body = LogoutUserData.empty_tokens()

        logout_response = Logout().logout_user(body=logout_body,
                                               schema=empty_schema,
                                               access_token=logout_body['access_token'])

        assert logout_response.status_code == 422
        assert logout_response.response_data.get('msg')

    def test_logout_empty_refresh(self):

        login_body = LoginUserData.valid_data()
        login_response = Login().login_user(body=login_body, schema=valid_schema)

        access_token = login_response.response_data.get('access_token')

        logout_body = {"refresh_token": ""}
        logout_response = Logout().logout_user(body=logout_body, schema=empty_schema, access_token=access_token)

        assert logout_response.status_code == 400
        assert logout_response.response_data.get('error') == "Refresh token is required!"


class TestRefreshTokens:

    def test_refresh_tokens_valid_data(self):

        login_body = LoginUserData.valid_data()
        login_response = Login().login_user(body=login_body, schema=valid_schema)

        refresh_token = login_response.response_data.get('refresh_token')
        refresh_token_new = {"refresh_token": refresh_token}

        refresh_tokens_response = RefreshToken().refresh_token(body=refresh_token_new, schema=valid_schema)

        decoded_refresh = jwt1.decode(refresh_token, Config.SECRET_KEY, algorithms=["HS256"])

        assert is_refresh_revoked(decoded_refresh)
        assert refresh_tokens_response.status_code == 200

    def test_refresh_tokens_empty_data(self):

        refresh_tokens_body = RefreshTokensData.empty_token()
        refresh_tokens_response = RefreshToken().refresh_token(body=refresh_tokens_body, schema=empty_schema)

        assert refresh_tokens_response.status_code == 400
        assert refresh_tokens_response.response_data.get("error") == "This field cannot be empty; please enter a valid " \
                                                                     "refresh_token."

    def test_refresh_tokens_invalid_data(self):

        refresh_tokens_body = RefreshTokensData.invalid_refresh_token()
        refresh_tokens_response = RefreshToken().refresh_token(body=refresh_tokens_body, schema=empty_schema)

        assert refresh_tokens_response.status_code == 422
        assert refresh_tokens_response.response_data.get("msg")

    def test_refresh_tokens_invalid_fields(self):
        refresh_tokens_body = RefreshTokensData.invalid_fields()
        refresh_tokens_response = RefreshToken().refresh_token(body=refresh_tokens_body, schema=empty_schema)

        assert refresh_tokens_response.status_code == 400
        assert refresh_tokens_response.response_data.get("error")

    def test_refresh_tokens_empty_fields(self):
        refresh_tokens_body = RefreshTokensData.empty_fields()
        refresh_tokens_response = RefreshToken().refresh_token(body=refresh_tokens_body, schema=empty_schema)

        assert refresh_tokens_response.status_code == 400
        assert refresh_tokens_response.response_data.get("error")


class TestSendEmailVerification:

    def test_send_email_verification_valid_email(self):

        verify_email_body = VerifyEmailData.valid_email()
        verify_email_response = SendEmailConfirmation().send_email_confirmation(body=verify_email_body,
                                                                   schema=email_verification_valid_schema)

        assert verify_email_response.status_code == 202
        assert verify_email_response.response_data.get("Message")

        url = verify_email_response.response_data.get("url")

        confirm_email_response = ConfirmEmail().confirm_email(url=url, schema=email_confirmation_valid_schema)
        assert confirm_email_response.status_code == 200
        assert confirm_email_response.response_data.get("Message")

    def test_send_email_verification_empty_url(self):

        url = "http://127.0.0.1:5000/confirm/"

        confirm_email_response = ConfirmEmail().confirm_email(url=url, schema=email_confirmation_invalid_schema)
        assert confirm_email_response.status_code == 400
        assert confirm_email_response.response_data.get("error")

    def test_send_email_verification_invalid_url(self):

        url = "http://127.0.0.1:5000/confirm/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9." \
              "eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NjAyODU1NCwianRpIjoiNzliZjQxMTUtYTc4" \
              "YS00Y2Y3LTkxMTEtNjY2MjRlNTYwOGQ4IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOjMsI" \
              "m5iZiI6MTY2NjAyODU1NCwiZXhwIjoxNjY2MDMwMzU0fQ.FugkorrVQTS4wM9bIGfcIReTpMBjlVfaD7pDS3McUm"

        confirm_email_response = ConfirmEmail().confirm_email(url=url, schema=email_confirmation_invalid_schema)
        assert confirm_email_response.status_code == 422
        assert confirm_email_response.response_data.get("msg")

    def test_email_verification_invalid_email(self):

        verify_email_body = VerifyEmailData.invalid_email()
        verify_email_response = SendEmailConfirmation().send_email_confirmation(body=verify_email_body,
                                                                   schema=email_verification_invalid_schema)

        assert verify_email_response.status_code == 400
        assert verify_email_response.response_data.get("error")

    def test_email_verification_empty_email(self):

        verify_email_body = VerifyEmailData.empty_email()
        verify_email_response = SendEmailConfirmation().send_email_confirmation(body=verify_email_body,
                                                                   schema=email_verification_invalid_schema)

        assert verify_email_response.status_code == 400
        assert verify_email_response.response_data.get("error")


class TestSendPasswordReset:

    def test_send_reset_password_valid_email_and_password(self):

        reset_password_body = ResetPasswordData.valid_email()
        reset_password_response = SendEmailReset().send_email_reset(body=reset_password_body,
                                                                   schema=reset_password_valid_schema)

        assert reset_password_response.status_code == 202
        assert reset_password_response.response_data.get("Message")

        url = reset_password_response.response_data.get("url")

        reset_password_2_body = ResetPasswordData.new_password()
        reset_password_2_response = ResetPassword().reset_password(url=url, schema=reset_password_valid_schema,
                                                                   body=reset_password_2_body)
        assert reset_password_2_response.status_code == 200
        assert reset_password_2_response.response_data.get("Message")

    def test_send_reset_password_invalid_password(self):

        reset_password_body = ResetPasswordData.valid_email()
        reset_password_response = SendEmailReset().send_email_reset(body=reset_password_body,
                                                                   schema=reset_password_valid_schema)

        assert reset_password_response.status_code == 202
        assert reset_password_response.response_data.get("Message")

        url = reset_password_response.response_data.get("url")

        reset_password_2_body = ResetPasswordData.new__invalid_password()
        reset_password_2_response = ResetPassword().reset_password(url=url, schema=reset_password_invalid_schema,
                                                                   body=reset_password_2_body)
        assert reset_password_2_response.status_code == 400
        assert reset_password_2_response.response_data.get("error")

    def test_send_reset_password_invalid_email(self):

        reset_password_body = ResetPasswordData.invalid_email()
        reset_password_response = SendEmailReset().send_email_reset(body=reset_password_body,
                                                                   schema=reset_password_invalid_schema)

        assert reset_password_response.status_code == 400
        assert reset_password_response.response_data.get("error")

    def test_send_reset_password_empty_email(self):

        reset_password_body = ResetPasswordData.empty_email()
        reset_password_response = SendEmailReset().send_email_reset(body=reset_password_body,
                                                                   schema=reset_password_invalid_schema)

        assert reset_password_response.status_code == 400
        assert reset_password_response.response_data.get("error")

    def test_send_reset_password_empty_url(self):

        url = "http://127.0.0.1:5000/reset/"

        reset_password_2_body = ResetPasswordData.new__invalid_password()
        reset_password_2_response = ResetPassword().reset_password(url=url, schema=reset_password_invalid_schema,
                                                                   body=reset_password_2_body)
        assert reset_password_2_response.status_code == 400
        assert reset_password_2_response.response_data.get("error")

    def test_send_reset_password_invalid_url(self):

        url = "http://127.0.0.1:5000/reset/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9." \
              "eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NjAyOTMyOCwianRpIjoiNjExYTNiNTgtZW" \
              "Y3Yi00OTIxLTgzMjEtNThiOGQxMWM0YTBjIiwidHlwZSI6InJlZnJlc2giLCJzdWIiO" \
              "jMsIm5iZiI6MTY2NjAyOTMyOCwiZXhwIjoxNjY2MDMxMTI4fQ.L2b8HzjXAUZ_nZq-Pm4AJGv3cMIf_BD__4vsj1ZoV4"

        reset_password_2_body = ResetPasswordData.new__invalid_password()
        reset_password_2_response = ResetPassword().reset_password(url=url, schema=reset_password_invalid_schema,
                                                                   body=reset_password_2_body)
        assert reset_password_2_response.status_code == 422
        assert reset_password_2_response.response_data.get("msg")


def after_test_clear():
    user = session.query(User).filter(User.email == "test").first()
    session.delete(user)
    session.commit()
