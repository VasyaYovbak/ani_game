from marshmallow import Schema, fields, INCLUDE, ValidationError, pre_load
from marshmallow.validate import Length


class NewCharacter(Schema):
    name = fields.Str(required=True)
    image = fields.Str(required=True)

    class Meta:
        fields = ('name', 'image')


character_schema = NewCharacter()
