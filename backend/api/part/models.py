from api import db, ma
from api.electeur.model import Electeur


class Representant(Electeur, db.Model):
    __tablename__ = 'representant'
    vote = db.Column(db.Integer, nullable=True)
    part = db.relationship('Partie', backref='representant',
                           primaryjoin='Representant.id == Partie.representant_id',
                           uselist=False)

    def __repr__(self):
        return '<Representant %r>' % self.vote


class Partie(db.Model):
    __tablename__ = 'partie'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    color = db.Column(db.String(50), unique=False, nullable=False)
    representant_id = db.Column(db.Integer(), db.ForeignKey(Representant.id))  # Foreign key Representant
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return '<part %r>' % self.name


# Representant
class RepresentantSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Representant
        include_fk = True

    id = ma.auto_field()
    lastname = ma.auto_field()
    firstname = ma.auto_field()
    birthday = ma.auto_field()
    cni = ma.auto_field()
    email = ma.auto_field()
    password = ma.auto_field()
    address = ma.auto_field()


representant_schema = RepresentantSchema()
representants_schema = RepresentantSchema(many=True)


# Fiche Electorale
class PartSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Partie
        include_fk = True

    id = ma.auto_field()
    name = ma.auto_field()
    color = ma.auto_field()
    representant_id = ma.auto_field()


part_schema = PartSchema()
parts_schema = PartSchema(many=True)

db.create_all()
