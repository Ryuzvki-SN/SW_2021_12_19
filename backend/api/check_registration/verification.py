from flask import jsonify, make_response
from api import app, db
from api.circonscription.models import Commune, Arrondissement, Departement, Region, commune_schema, \
    arrondissement_schema, departement_schema, region_schema
from api.elector.model import Elector, elector_schema


@app.route("/api/verification/<cni>", methods=["GET"], strict_slashes=False)
def verification(cni):
    checked = []
    user = Elector.query.filter_by(cni=cni).first()

    if not user:
        # returns 401 if user does not exist
        return make_response(
            'User does not exist !!',
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
        )

    bureau = db.session.query(Elector)\
        .filter_by(cni=cni).first()
    br_serializer = elector_schema.dump(bureau)

    commune = db.session.query(Commune).join(Elector)\
        .filter(Commune.id == Elector.commune_id).first()
    com_serializer = commune_schema.dump(commune)

    arrondissement = db.session.query(Arrondissement).join(Commune) \
        .filter(Arrondissement.id == Commune.arrondissement_id) \
        .filter(Commune.id == Elector.commune_id).first()
    arron_serializer = arrondissement_schema.dump(arrondissement)

    departement = db.session.query(Departement).join(Arrondissement)\
        .filter(Departement.id == Arrondissement.departement_id)\
        .filter(Arrondissement.id == Commune.arrondissement_id)\
        .filter(Commune.id == Elector.commune_id).first()
    dep_serializer = departement_schema.dump(departement)

    region = db.session.query(Region).join(Departement)\
        .filter(Region.id == Departement.region_id)\
        .filter(Departement.id == Arrondissement.departement_id)\
        .filter(Arrondissement.id == Commune.arrondissement_id)\
        .filter(Commune.id == Elector.commune_id).first()
    city_serializer = region_schema.dump(region)

    checked.append(
        {
            "Region": city_serializer['name'],   # str(region)
            "Departement": dep_serializer['name'],   # str(departement)
            "Arrondissement": arron_serializer['name'],  # str(arrondissement)
            "Commune": com_serializer['name'],  # str(commune)
            "Adresse": br_serializer['address'],  # str(bureau)
            "Bureau": br_serializer['bureau_id']  # str(bureau)
        }
    )
    return jsonify(checked), 200
