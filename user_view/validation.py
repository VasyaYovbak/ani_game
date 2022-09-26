from marshmallow import Schema, fields, validate
from marshmallow.validate import *


class RegisterSchema(Schema):

    username = fields.String(required=True, validate=Length(min=3, max=15))
    email = fields.Email(required=True, validate=Length(min=8, max=345))
    password = fields.String(required=True, validate=[validate.Length(min=6, max=36)], load_only=True)


class LoginSchema(Schema):

    email = fields.Email(required=True, validate=Length(min=8, max=345))
    password = fields.String(required=True, validate=[validate.Length(min=6, max=36)], load_only=True)


class ResetSchema(Schema):
    password = fields.String(required=True, validate=[validate.Length(min=6, max=36)], load_only=True)


class PasswordValidation():

    @staticmethod
    def password_check(self):
        SpecialSym = ['$', '@', '#', '%', '/']
        val = True

        if not any(char.isdigit() for char in self):
            print('Password should have at least one numeral')
            val = False

        if not any(char.isupper() for char in self):
            print('Password should have at least one uppercase letter')
            val = False

        if not any(char.islower() for char in self):
            print('Password should have at least one lowercase letter')
            val = False

        if not any(char in SpecialSym for char in self):
            print('Password should have at least one of the symbols $@#')
            val = False

        if not val:
            print("Your password is shit like my python knowledge")

        return val

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



registration_schema = RegisterSchema()
login_schema = LoginSchema()
reset_schema = ResetSchema()

