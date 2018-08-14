from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

from boggle.models.game import Game
from boggle.schemas.board import board_schema


class GameSchema(ModelSchema):
    board = fields.Nested(board_schema)

    class Meta:
        model = Game


game_schema = GameSchema()
