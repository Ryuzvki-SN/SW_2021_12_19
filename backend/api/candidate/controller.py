from api import ma
from api.election.models import Candidate


class CandidateSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Candidate
        include_fk = True

    party_id = ma.auto_field()


candidate_schema = CandidateSchema(partial=True)
candidates_schema = CandidateSchema(many=True)
