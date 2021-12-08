from sqlalchemy_utils import aggregated
from api import db, ma

"""Class Region"""


class Region(db.Model):
    __tablename__ = 'region'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    location = db.Column(db.String(255),  default='point((0,0))')

    @aggregated('departements', db.Column(db.Integer))
    def bureaux(self):
        return db.func.sum(Departement.bureaux)

    @aggregated('departements', db.Column(db.Integer))
    def electeurs(self):
        return db.func.sum(Departement.electeurs)

    @aggregated('departements', db.Column(db.Integer))
    def suffrage_valable(self):
        return db.func.sum(Departement.suffrage_valable)

    @aggregated('departements', db.Column(db.Integer))
    def suffrage_invalide(self):
        return db.func.sum(Departement.suffrage_invalide)

    def __repr__(self):
        return '<Region %r>' % self.name


"""Class Departement"""


class Departement(db.Model):
    __tablename__ = 'departement'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    location = db.Column(db.String(255),  default='point((0,0))')

    @aggregated('arrondissements', db.Column(db.Integer))
    def bureaux(self):
        return db.func.sum(Arrondissement.bureaux)

    @aggregated('arrondissements', db.Column(db.Integer))
    def electeurs(self):
        return db.func.sum(Arrondissement.electeurs)

    @aggregated('arrondissements', db.Column(db.Integer))
    def suffrage_valable(self):
        return db.func.sum(Arrondissement.suffrage_valable)

    @aggregated('arrondissements', db.Column(db.Integer))
    def suffrage_invalide(self):
        return db.func.sum(Arrondissement.suffrage_invalide)

    def __repr__(self):
        return '<Departement %r>' % self.name

    region_id = db.Column(db.Integer, db.ForeignKey(Region.id), nullable=False)
    region = db.relationship('Region', backref=db.backref('departements', lazy=True))


"""Class Arrondissement"""


class Arrondissement(db.Model):
    __tablename__ = 'arrondissement'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    location = db.Column(db.String(255),  default='point((0,0))')

    @aggregated('communes', db.Column(db.Integer))
    def bureaux(self):
        return db.func.sum(Commune.total_bureau)

    @aggregated('communes', db.Column(db.Integer))
    def electeurs(self):
        return db.func.sum(Commune.electeurs)

    @aggregated('communes', db.Column(db.Integer))
    def suffrage_valable(self):
        return db.func.sum(Commune.suffrage_valable)

    @aggregated('communes', db.Column(db.Integer))
    def suffrage_invalide(self):
        return db.func.sum(Commune.suffrage_invalide)

    def __repr__(self):
        return '<Arrondissement %r>' % self.nom

    departement_id = db.Column(db.Integer, db.ForeignKey(Departement.id), nullable=False)
    departement = db.relationship('Departement', backref=db.backref('arrondissements', lazy=True))


"""Class Commune"""


class Commune(db.Model):
    __tablename__ = 'commune'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    location = db.Column(db.String(255),  default='point((0,0))')

    @aggregated('bureaux', db.Column(db.Integer))
    def total_bureau(self):
        return db.func.count(Bureau.id)

    @aggregated('bureaux', db.Column(db.Integer))
    def electeurs(self):
        return db.func.sum(Bureau.nombre_inscrit)

    @aggregated('bureaux', db.Column(db.Integer))
    def suffrage_valable(self):
        return db.func.sum(Bureau.suffrage_valable)

    @aggregated('bureaux', db.Column(db.Integer))
    def suffrage_invalide(self):
        return db.func.sum(Bureau.suffrage_invalide)

    def __repr__(self):
        return '<Commune %r>' % self.name

    arrondissement_id = db.Column(db.Integer, db.ForeignKey(Arrondissement.id), nullable=False)
    arrondissement = db.relationship('Arrondissement', backref=db.backref('communes', lazy=True))


"""Class Bureau de vote"""


class Bureau(db.Model):
    __tablename__ = 'bureau'
    id = db.Column(db.Integer, primary_key=True)
    nombre_inscrit = db.Column(db.Integer, nullable=False)
    suffrage_valable = db.Column(db.Integer, nullable=True)
    suffrage_invalide = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Bureau %r>' % self.name

    commune_id = db.Column(db.Integer, db.ForeignKey(Commune.id), nullable=False)
    commune = db.relationship('Commune', backref=db.backref('bureaux', lazy=True))


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
    total_bureau = ma.auto_field()
    electeurs = ma.auto_field()
    suffrage_valable = ma.auto_field()
    suffrage_invalide = ma.auto_field()
    arrondissement_id = ma.auto_field()


commune_schema = CommuneSchema()
communes_schema = CommuneSchema(many=True)


# Bureau
class BureauSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Bureau
        include_fk = True

    id = ma.auto_field()
    nombre_inscrit = ma.auto_field()
    suffrage_valable = ma.auto_field()
    suffrage_invalide = ma.auto_field()
    commune_id = ma.auto_field()


bureau_schema = BureauSchema()
bureaux_schema = BureauSchema(many=True)

db.create_all()  # Generate table
