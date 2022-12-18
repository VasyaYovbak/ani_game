from marshmallow.validate import *


def password_check(password):
    Special_Symbols = ['$', '@', '#', '%', '/']

    if len(password) <= 5 or len(password) >= 37:
        raise ValidationError('Password length should be between 6 and 36 digits')

    if not any(char.isdigit() for char in password):
        raise ValidationError('Password should have at least one numeral')

    if not any(char.isupper() for char in password):
        raise ValidationError('Password should have at least one uppercase letter')

    if not any(char.islower() for char in password):
        raise ValidationError('Password should have at least one lowercase letter')

    if not any(char in Special_Symbols for char in password):
        raise ValidationError('Password should have at least one of the symbols: $, @, #, %, /')


# check if username have digits
def username_check(username):
    Special_Symbols = {'$', '@', '#', '%', '/', '^', '~', }

    ans = any(char.isdigit() for char in username)

    if len(username) <= 2 or len(username) >= 33:
        raise ValidationError('Username length should be between 3 and 32 digits')

    if ans:
        raise ValidationError("Username should have only letters, digits are not allowed.")

    if any(char in Special_Symbols for char in username):
        raise ValidationError('This symbols are not allowed.')


def email_check(email):
    if len(email) <= 7 or len(email) >= 346:
        raise ValidationError('Email length should be between 8 and 345 digits')

    if email.count('@') != 1:
        raise ValidationError('Email is not valid')

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
