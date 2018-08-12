from marshmallow_sqlalchemy import ModelSchema

from boggle.models.game import Game


class GameSchema(ModelSchema):
    class Meta:
        model = Game


game_schema = GameSchema()
