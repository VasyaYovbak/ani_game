from marshmallow import Schema, fields, INCLUDE, ValidationError, pre_load
from marshmallow.validate import Length


class RegisterSchema(Schema):
    username = fields.Str()
    email = fields.Str(validate=Length(min=10))
    password = fields.Str(required=True)

    class Meta:
        fields = ('username', 'email', 'password')


class NewAchievement(Schema):
    name = fields.Str(required=True)
    experience = fields.Int(required=True)
    description = fields.Str(required=True)

    class Meta:
        fields = ('name', 'experience', 'description')


register_schema = RegisterSchema()
newAchievement = NewAchievement()