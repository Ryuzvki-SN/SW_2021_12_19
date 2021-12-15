from api import db, ma
from api.circonscription.models import Commune, Bureau


class Elector(db.Model):
    __tablename__ = 'elector'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    lastname = db.Column(db.String(75), unique=False)
    firstname = db.Column(db.String(75), unique=False)
    birthday = db.Column(db.Date)
    cni = db.Column(db.Integer, unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(200), unique=False)
    address = db.Column(db.String(50), unique=False)

    commune_id = db.Column(db.Integer, db.ForeignKey(Commune.id, ondelete='CASCADE', onupdate='CASCADE'))
    commune = db.relationship('Commune', backref=db.backref('electors', cascade='all,save-update,delete',
                                                            lazy=True),
                              primaryjoin='Commune.id == Elector.commune_id')

    bureau_id = db.Column(db.Integer, db.ForeignKey(Bureau.id, ondelete='CASCADE', onupdate='CASCADE'))
    bureau = db.relationship('Bureau', backref=db.backref('electors', cascade='all,save-update,delete',
                                                          lazy=True),
                             primaryjoin='Bureau.id == Elector.bureau_id')

class ElectorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Elector
        include_fk = True

    public_id = ma.auto_field()
    lastname = ma.auto_field()
    firstname = ma.auto_field()
    birthday = ma.auto_field()
    cni = ma.auto_field()
    email = ma.auto_field()
    password = ma.auto_field()
    address = ma.auto_field()
    commune_id = ma.auto_field()
    bureau_id = ma.auto_field()


elector_schema = ElectorSchema()
electors_schema = ElectorSchema(many=True)

db.create_all()
