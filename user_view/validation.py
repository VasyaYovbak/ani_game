from typing import Tuple

from marshmallow.validate import *


def password_check(password: str) -> None:
    special_symbols = {'$', '@', '#', '%', '/', '!', '&', '|'}
    password_min_length = 8
    password_max_length = 36

    if not password_min_length <= len(password) <= password_max_length:
        raise ValidationError(
            f"Password length should be between {password_min_length} and {password_max_length} digits.")

    if not contains_digit(password):
        raise ValidationError("Password should contain at least one digit.")

    if not contains_special_char(password, special_symbols):
        raise ValidationError(
            f"Password should have at least one of the symbols: {get_special_symbols_repr(special_symbols)}")


def username_check(username: str) -> None:
    username_min_length = 3
    username_max_length = 15

    if not username_min_length <= len(username) <= username_max_length:
        raise ValidationError(
            f"Username length should be between {username_min_length} and {username_max_length}.")

    if not username.isalnum():
        raise ValidationError("Username should contain only digits and alphabetic letters!")


def email_check(email: str) -> None:
    email_min_length = 3
    email_max_length = 199

    if not email_min_length <= len(email) <= email_max_length:
        raise ValidationError(f"Email length should be between {email_min_length} and {email_max_length} digits.")

    if email.count('@') != 1:
        raise ValidationError("Email is not valid.")


def validate_registration(username: str, password: str, email: str) -> Tuple[None, None, None]:
    return username_check(username), email_check(email), password_check(password)


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
