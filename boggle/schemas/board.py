from marshmallow_sqlalchemy import ModelSchema

from boggle.models.board import Board


class BoardSchema(ModelSchema):
    class Meta:
        model = Board


board_schema = BoardSchema()
