from marshmallow import Schema, fields


class CreateRoom(Schema):
    name = fields.Str(required=True)
    is_game_started = fields.Boolean(required=False, default=False)

    class Meta:
        fields = ('name', 'is_game_started')


create_room_schema = CreateRoom()
