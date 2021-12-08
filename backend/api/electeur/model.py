from datetime import datetime
from flask_login import UserMixin
from api import db, ma, login_manager
from api.circonscription.models import Bureau


@login_manager.user_loader
def user_loader(user_id):
    return Electeur.query.get(user_id)


class Electeur(db.Model, UserMixin):
    __tablename__ = 'electeur'
    id = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(75), unique=False)
    firstname = db.Column(db.String(75), unique=False)
    CNI = db.Column(db.Integer, unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(200), unique=False)
    address = db.Column(db.String(50), unique=False)
    birth = db.Column(db.DateTime, default=datetime.utcnow)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Electeur %r>' % self.lastname

    bureau = db.Column(db.Integer, db.ForeignKey(Bureau.id), nullable=False)
    bureau_electeur = db.relationship('Bureau', backref=db.backref('electeurs', lazy=True))


# Electeur
class ElecteurSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Electeur
        include_fk = True

    id = ma.auto_field()
    lastname = ma.auto_field()
    firstname = ma.auto_field()
    CNI = ma.auto_field()
    email = ma.auto_field()
    password = ma.auto_field()
    address = ma.auto_field()
    birth = ma.auto_field()
    bureau = ma.auto_field()
    date_created = ma.auto_field()
    date_modified = ma.auto_field()


electeur_schema = ElecteurSchema()
electeurs_schema = ElecteurSchema(many=True)

db.create_all()
