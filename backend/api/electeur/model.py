from datetime import datetime
from flask_login import UserMixin
from api import db, ma, login_manager

@login_manager.user_loader
def user_loader(user_id):
    return Electeur.query.get(user_id)


class Electeur(db.Model, UserMixin):
    __tablename__ = 'electeur'
    id = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(75), unique=False)
    firstname = db.Column(db.String(75), unique=False)
    birthday = db.Column(db.Date)
    cni = db.Column(db.Integer, unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(200), unique=False)
    address = db.Column(db.String(50), unique=False)
    # bureau_number = db.Column(db.Integer, db.ForeignKey(Bureau.id), nullable=False)
    # bureau = db.relationship('Bureau', backref=db.backref('electeurs', lazy=True))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Electeur %r>' % self.lastname


# Electeur
class ElecteurSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Electeur
        include_fk = True

    id = ma.auto_field()
    lastname = ma.auto_field()
    firstname = ma.auto_field()
    birthday = ma.auto_field()
    cni = ma.auto_field()
    email = ma.auto_field()
    password = ma.auto_field()
    address = ma.auto_field()
    date_created = ma.auto_field()
    date_modified = ma.auto_field()


electeur_schema = ElecteurSchema()
electeurs_schema = ElecteurSchema(many=True)

db.create_all()
