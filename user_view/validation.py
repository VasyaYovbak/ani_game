from marshmallow.validate import *


def password_check(password):
    special_symbols = {'$', '@', '#', '%', '/'}

    if len(password) <= 5 or len(password) >= 37:
        raise ValidationError('Password length should be between 6 and 36 digits.')

    if not any(char.isdigit() for char in password):
        raise ValidationError('Password should contain at least one digit.')

    if not any(char in special_symbols for char in password):
        raise ValidationError(
            f"Password should have at least one of the symbols: {get_special_symbols_repr(special_symbols)}")


# check if username have digits
def username_check(username):
    special_symbols = {'$', '@', '#', '%', '/', '^', '~', }

    ans = any(char.isdigit() for char in username)

    if len(username) <= 2 or len(username) >= 33:
        raise ValidationError('Username length should be between 3 and 32 digits.')

    if ans:
        raise ValidationError("Username should contain only letters. Digits are not allowed!")

    if any(char in special_symbols for char in username):
        raise ValidationError(f"{get_special_symbols_repr(special_symbols)} symbols are not allowed.")


def email_check(email):
    if len(email) <= 7 or len(email) >= 346:
        raise ValidationError('Email length should be between 8 and 345 digits.')

    if email.count('@') != 1:
        raise ValidationError('Email is not valid.')


def validate_registration(username, password, email):
    return username_check(username), email_check(email), password_check(password)


def validate_password(password):
    return password_check(password)


def get_special_symbols_repr(special_symbols):
    return ', '.join(list(special_symbols))

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
