from marshmallow.validate import *
from typing import Tuple


def password_check(password:str) -> None:

    password_valid = password.replace(" ", "")

    special_symbols = {'$', '@', '#', '%', '/', '!', '&', '|'}
    password_min_length = 8
    password_max_length = 36

    if not password_min_length <= len(password_valid) <= password_max_length:
        raise ValidationError(
            f"Password length should be between {password_min_length} and {password_max_length} digits.")

    if not contains_digit(password_valid):
        raise ValidationError("Password should contain at least one digit.")

    if not contains_special_char(password_valid, special_symbols):
        raise ValidationError(
            f"Password should have at least one of the symbols: {get_special_symbols_repr(special_symbols)}")


# check if username have digits
def username_check(username: str) -> None:

    username_valid = username.replace(" ", "")

    username_min_length = 3
    username_max_length = 15

    if not username_min_length <= len(username_valid) <= username_max_length:
        raise ValidationError(
            f"Username length should be between {username_min_length} and {username_max_length}.")

    if not username_valid.isalnum():
        raise ValidationError("Username should contain only digits and alphabetic letters!")


def email_check(email: str) -> None:

    email_valid = email.replace(" ", "")

    email_min_length = 3
    email_max_length = 199

    if not email_min_length <= len(email_valid) <= email_max_length:
        raise ValidationError(f"Email length should be between {email_min_length} and {email_max_length} digits.")

    if email_valid.count('@') != 1:
        raise ValidationError("Email is not valid.")


def google_auth_email_check(email: str) -> None:

    email_valid = email.replace(" ", "")

    email_min_length = 3
    email_max_length = 199

    if not email_min_length <= len(email_valid) <= email_max_length:
        raise ValidationError(f"Email length should be between {email_min_length} and {email_max_length} digits.")

    if email_valid.count('@') != 1:
        raise ValidationError("Email is not valid.")

    if email is None:
        raise ValidationError("Email cannot be None")


def google_auth_username_check(username: str) -> None:

    username_valid = username.replace(" ", "")

    username_min_length = 3
    username_max_length = 100

    if not username_min_length <= len(username_valid) <= username_max_length:
        raise ValidationError(
            f"Username length should be between {username_min_length} and {username_max_length}.")


def validate_registration(username: str, password: str, email: str) -> Tuple[None, None, None]:
    return username_check(username), email_check(email), password_check(password)


def validate_google_auth(username: str, email: str) -> Tuple[None, None]:
    return google_auth_username_check(username), google_auth_email_check(email)


def validate_password(password: str) -> None:
    return password_check(password)


def get_special_symbols_repr(special_symbols: set) -> str:
    return ", ".join(list(special_symbols))


def contains_digit(field: str) -> bool:
    return any(char.isdigit() for char in field)


def contains_special_char(field: str, special_chars: set) -> bool:
    return any(char in special_chars for char in field)






# class AchievementSchema(Schema):
#
#     name = fields.String(required=True, validate=Length(min=3, max=15))
#     expirience = fields.Integer(validate=validate.Range(min=0, max=5))
#     description = fields.String(validate=validate.Range(min=0, max=120))

# User Achievements
# class NewAchievement(Schema):
#     name = fields.Str(required=True)
#     experience = fields.Int(required=True)
#     description = fields.Str(required=True)
#
#     class Meta:
#         fields = ('name', 'experience', 'description')
# newAchievement = NewAchievement()


