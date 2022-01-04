from flask import make_response, jsonify, request

from api import app, db
from api.circonscription.models import Region, Departement, Arrondissement, Commune, region_schema, \
    departement_schema, arrondissement_schema, commune_schema
from api.elector.model import Elector, elector_schema


@app.route("/api/bureau/change/request/<cni>", methods=["GET", "POST"], strict_slashes=False)
def change_request(cni):
    user = Elector.query.filter_by(cni=cni).first()

    if not user:
        # returns 401 if bureau does not exist
        return make_response(
            'Elector does not exist !!',
            404,
            {'WWW-Authenticate': 'Basic realm ="Elector does not exist !!"'}
        )
    old_inf = []
    name_query = db.session.query(Elector.lastname, Elector.firstname).filter_by(cni=cni).first()
    name = elector_schema.dump(name_query)

    circonscription = []

    region_query = db.session.query(Region).join(Departement) \
        .filter(Region.id == Departement.region_id) \
        .filter(Departement.id == Arrondissement.departement_id) \
        .filter(Arrondissement.id == Commune.arrondissement_id) \
        .filter(Commune.id == Elector.commune_id).first()
    region = region_schema.dump(region_query)

    departement_query = db.session.query(Departement).join(Arrondissement) \
        .filter(Departement.id == Arrondissement.departement_id) \
        .filter(Arrondissement.id == Commune.arrondissement_id) \
        .filter(Commune.id == Elector.commune_id).first()
    departement = departement_schema.dump(departement_query)

    arrondissement_query = db.session.query(Arrondissement).join(Commune) \
        .filter(Arrondissement.id == Commune.arrondissement_id) \
        .filter(Commune.id == Elector.commune_id).first()
    arrondissement = arrondissement_schema.dump(arrondissement_query)

    commune_query = db.session.query(Commune).join(Elector) \
        .filter(Commune.id == Elector.commune_id).first()
    commune = commune_schema.dump(commune_query)

    elector = elector_schema.dump(user)

    circonscription.append(
        {
            "Region": region['name'],  # str(region)
            "Departement": departement['name'],  # str(departement)
            "Arrondissement": arrondissement['name'],  # str(arrondissement)
            "Commune": commune['name'],  # str(commune)
            "Adresse": elector['address'],  # str(bureau)
            "Bureau": elector['bureau_id']  # str(bureau)
        }
    )

    old_inf.append(
        {
            "Objet": "old Information",
            "Name": name,
            "Circonscription": circonscription
        }
    )

    new_inf = []
    data = request.get_json()

    new_region = data['region']
    # new_department = data['department']
    # new_arron = data['arrondissement']
    # new_commune = data['commune']

    new_inf.append(
        {
            "Region": new_region,
            # "Department": new_department,
            # "Arrondissement": new_arron,
            # "Commune": new_commune,
            "Objet": "New Information"
        }
    )

    return jsonify(new_inf)

