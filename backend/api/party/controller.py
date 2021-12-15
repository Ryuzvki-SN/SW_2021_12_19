from api import ma
from api.election.models import Party


class PartySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Party

    name = ma.auto_field()
    color = ma.auto_field()


party_schema = PartySchema(partial=True)
parties_schema = PartySchema(many=True)
