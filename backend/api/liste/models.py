from api import db, ma
from api.electeur.model import Electeur


class Representant(Electeur):
    __tablename__ = 'representant'

    def __repr__(self):
        return '<Representant %r>' % self.nom

    liste = db.relationship('Liste', backref='representant', uselist=False)


"""Class Liste Electorale"""


class Liste(db.Model):
    __tablename__ = 'liste'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def __repr__(self):
        return '<liste %r>' % self.name

    representant_id = db.Column(db.Integer(), db.ForeignKey(Representant.id))  # Foreign key Representant

# Representant
class RepresentantSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Representant
        include_fk = True

    id = ma.auto_field()
    lastname = ma.auto_field()
    firstname = ma.auto_field()
    CNI = ma.auto_field()
    email = ma.auto_field()
    password = ma.auto_field()
    address = ma.auto_field()
    birth = ma.auto_field()


representant_schema = RepresentantSchema()
representants_schema = RepresentantSchema(many=True)


# Fiche Electorale
class ListeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Liste
        include_fk = True

    id = ma.auto_field()
    name = ma.auto_field()
    representant = ma.auto_field()


liste_schema = ListeSchema()
listes_schema = ListeSchema(many=True)

db.create_all()
