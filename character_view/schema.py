from marshmallow import Schema, fields, INCLUDE, ValidationError, pre_load
from marshmallow.validate import Length


class NewCharacter(Schema):
    name = fields.Str(required=True)
    is_alive = fields.Boolean(required=True)
    is_good = fields.Boolean(required=True)
    image = fields.Str(required=True)

    class Meta:
        fields = ('name', 'is_alive', 'is_good', 'image')


character_schema = NewCharacter()
