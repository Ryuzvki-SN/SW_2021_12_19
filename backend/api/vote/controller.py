from api import ma
from api.election.models import Vote


class VoteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Vote

    candidate_id = ma.auto_field()
    bureau_id = ma.auto_field()


vote_schema = VoteSchema(partial=True)
votes_schema = VoteSchema(many=True)
