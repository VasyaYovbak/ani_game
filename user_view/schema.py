from marshmallow import Schema, fields, INCLUDE, ValidationError, pre_load
from marshmallow.validate import Length


class RegisterSchema(Schema):
    username = fields.Str()
    email = fields.Str()
    password = fields.Str(required=True)

    class Meta:
        fields = ('username', 'email', 'password')


class LoginSchema(Schema):
    email = fields.Str()
    password = fields.Str(required=True)

    class Meta:
        fields = ('email', 'password')


register_schema = RegisterSchema()
login_schema = LoginSchema()

# User Achievements
# class NewAchievement(Schema):
#     name = fields.Str(required=True)
#     experience = fields.Int(required=True)
#     description = fields.Str(required=True)
#
#     class Meta:
#         fields = ('name', 'experience', 'description')
# newAchievement = NewAchievement()
