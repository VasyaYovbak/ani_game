from marshmallow import Schema, fields, validate
from marshmallow.validate import *



class UserSchema(Schema):

    username = fields.String(required=True, validate=Length(min=3, max=15))
    email = fields.Email(required=True, validate=Length(min=8, max=345))
    permission = fields.String(validate=validate.OneOf(["user", "admin"]))
    rating = fields.Integer(validate=validate.Range(min=0, max=5))
    password = fields.String(required=True, validate=[validate.Length(min=6, max=36)], load_only=True)

class AchievementSchema(Schema):

    name = fields.String(required=True, validate=Length(min=3, max=15))
    expirience = fields.Integer(validate=validate.Range(min=0, max=5))
    description = fields.String(validate=validate.Range(min=0, max=120))
