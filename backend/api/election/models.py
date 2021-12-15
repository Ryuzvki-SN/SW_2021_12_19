from api import db
from api.elector.model import Elector


class Candidate(Elector):
    __tablename__ = 'candidate'
    id = db.Column(db.Integer, db.ForeignKey('elector.id'), primary_key=True)
    party_id = db.Column(db.Integer, db.ForeignKey('party.id', ondelete='CASCADE'), nullable=False)
    votes = db.relationship('Vote', backref=db.backref('candidate', cascade='all,delete', lazy=True))


class Party(db.Model):
    __tablename__ = 'party'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    color = db.Column(db.String(50), unique=True, nullable=False)
    candidate = db.relationship('Candidate', backref=db.backref('party', cascade='all,delete', lazy=True),
                                uselist=False)


class Vote(db.Model):
    __tablename__ = 'vote'
    id = db.Column(db.Integer, primary_key=True)

    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id', ondelete='CASCADE'), nullable=False)
    bureau_id = db.Column(db.Integer, db.ForeignKey('bureau.id', ondelete='CASCADE'), nullable=False)
    bureau = db.relationship('Bureau', backref=db.backref('votes', cascade='all,delete', lazy=True))


db.create_all()
