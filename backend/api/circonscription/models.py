from sqlalchemy_utils import aggregated
from api import db, ma

class Region(db.Model):
    __tablename__ = 'region'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    location = db.Column(db.String(255), default='(0,0)')

    @aggregated('departements.arrondissements.communes.bureaux', db.Column(db.Integer))
    def bureaux(self):
        return db.func.count(Bureau.id)

    @aggregated('departements.arrondissements.communes.bureaux', db.Column(db.Integer))
    def electeurs(self):
        return db.func.sum(Bureau.electeurs)

    @aggregated('departements.arrondissements.communes.bureaux', db.Column(db.Integer))
    def suffrage_valable(self):
        return db.func.sum(Bureau.suffrage_valable)

    @aggregated('departements.arrondissements.communes.bureaux', db.Column(db.Integer))
    def suffrage_invalide(self):
        return db.func.sum(Bureau.suffrage_invalide)

    def __repr__(self):
        return '<Region %r>' % self.name


class Departement(db.Model):
    __tablename__ = 'departement'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    location = db.Column(db.String(255), default='(0,0)')
    region_id = db.Column(db.Integer, db.ForeignKey(Region.id, ondelete='CASCADE',
                                                    onupdate='CASCADE'), nullable=False)
    region = db.relationship('Region', backref=db.backref('departements', lazy=True),
                             primaryjoin='Region.id == Departement.region_id')

    @aggregated('arrondissements.communes.bureaux', db.Column(db.Integer))
    def bureaux(self):
        return db.func.count(Bureau.id)

    @aggregated('arrondissements.communes.bureaux', db.Column(db.Integer))
    def electeurs(self):
        return db.func.sum(Bureau.electeurs)

    @aggregated('arrondissements.communes.bureaux', db.Column(db.Integer))
    def suffrage_valable(self):
        return db.func.sum(Bureau.suffrage_valable)

    @aggregated('arrondissements.communes.bureaux', db.Column(db.Integer))
    def suffrage_invalide(self):
        return db.func.sum(Bureau.suffrage_invalide)

    def __repr__(self):
        return '<Departement %r>' % self.name


class Arrondissement(db.Model):
    __tablename__ = 'arrondissement'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    location = db.Column(db.String(255), default='(0,0)')
    departement_id = db.Column(db.Integer, db.ForeignKey(Departement.id, ondelete='CASCADE',
                                                         onupdate='CASCADE'), nullable=False)
    departement = db.relationship('Departement', backref=db.backref('arrondissements', lazy=True),
                                  primaryjoin='Departement.id == Arrondissement.departement_id')

    @aggregated('communes.bureaux', db.Column(db.Integer))
    def bureaux(self):
        return db.func.count(Bureau.id)

    @aggregated('communes.bureaux', db.Column(db.Integer))
    def electeurs(self):
        return db.func.sum(Bureau.electeurs)

    @aggregated('communes.bureaux', db.Column(db.Integer))
    def suffrage_valable(self):
        return db.func.sum(Bureau.suffrage_valable)

    @aggregated('communes.bureaux', db.Column(db.Integer))
    def suffrage_invalide(self):
        return db.func.sum(Bureau.suffrage_invalide)

    def __repr__(self):
        return '<Arrondissement %r>' % self.name


"""Class Commune"""


class Commune(db.Model):
    __tablename__ = 'commune'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    location = db.Column(db.String(255), default='(0,0)')
    arrondissement_id = db.Column(db.Integer, db.ForeignKey(Arrondissement.id, ondelete='CASCADE',
                                                            onupdate='CASCADE'), nullable=False)
    arrondissement = db.relationship('Arrondissement', backref=db.backref('communes', lazy=True),
                                     primaryjoin='Arrondissement.id == Commune.arrondissement_id')

    @aggregated('bureaux.electors', db.Column(db.Integer))
    def total_bureau(self):
        from api.elector.model import Elector
        return db.func.count(Elector.bureau_id)

    @aggregated('electors', db.Column(db.Integer))
    def electeurs(self):
        from api.elector.model import Elector
        return db.func.count(Elector.id)

    @aggregated('bureaux', db.Column(db.Integer))
    def suffrage_valable(self):
        return db.func.sum(Bureau.suffrage_valable)

    @aggregated('bureaux', db.Column(db.Integer))
    def suffrage_invalide(self):
        return db.func.sum(Bureau.suffrage_invalide)

    def __repr__(self):
        return '<Commune %r>' % self.name


class Bureau(db.Model):
    __tablename__ = 'bureau'
    id = db.Column(db.Integer, primary_key=True)
    suffrage_valable = db.Column(db.Integer, nullable=True)
    suffrage_invalide = db.Column(db.Integer, nullable=True)
    commune_id = db.Column(db.Integer, db.ForeignKey(Commune.id, ondelete='CASCADE',
                                                     onupdate='CASCADE'), nullable=False)
    commune = db.relationship('Commune', backref=db.backref('bureaux', cascade='all,save-update,delete'),
                              primaryjoin='Commune.id == Bureau.commune_id')

    @aggregated('electors', db.Column(db.Integer))
    def electeurs(self):
        from api.elector.model import Elector
        return db.func.count(Elector.id)
        # results = db.session.query(Elector, Bureau).filter(Bureau.id == Elector.bureau_id).all()
        # return db.func.count(results)


# Generate marshmallow Schemas from models
# Region
class RegionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Region

    id = ma.auto_field()
    name = ma.auto_field()
    location = ma.auto_field()
    bureaux = ma.auto_field()
    electeurs = ma.auto_field()
    suffrage_valable = ma.auto_field()
    suffrage_invalide = ma.auto_field()


region_schema = RegionSchema(partial=True)
regions_schema = RegionSchema(many=True)


# Departement
class DepartementSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Departement
        include_fk = True

    id = ma.auto_field()
    name = ma.auto_field()
    location = ma.auto_field()
    bureaux = ma.auto_field()
    electeurs = ma.auto_field()
    suffrage_valable = ma.auto_field()
    suffrage_invalide = ma.auto_field()
    region_id = ma.auto_field()


departement_schema = DepartementSchema(partial=True)
departements_schema = DepartementSchema(many=True)


# Arrondissement
class ArrondissementSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Arrondissement
        include_fk = True

    id = ma.auto_field()
    name = ma.auto_field()
    location = ma.auto_field()
    bureaux = ma.auto_field()
    electeurs = ma.auto_field()
    suffrage_valable = ma.auto_field()
    suffrage_invalide = ma.auto_field()
    departement_id = ma.auto_field()


arrondissement_schema = ArrondissementSchema()
arrondissements_schema = ArrondissementSchema(many=True)


# Commune
class CommuneSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Commune
        include_fk = True

    id = ma.auto_field()
    name = ma.auto_field()
    location = ma.auto_field()
    arrondissement_id = ma.auto_field()
    total_bureau = ma.auto_field()
    electeurs = ma.auto_field()
    suffrage_valable = ma.auto_field()
    suffrage_invalide = ma.auto_field()


commune_schema = CommuneSchema()
communes_schema = CommuneSchema(many=True)


# Bureau
class BureauSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Bureau
        include_fk = True

    id = ma.auto_field()
    electeurs = ma.auto_field()
    suffrage_valable = ma.auto_field()
    suffrage_invalide = ma.auto_field()
    commune_id = ma.auto_field()


bureau_schema = BureauSchema()
bureaux_schema = BureauSchema(many=True)

db.create_all()  # Generate table
