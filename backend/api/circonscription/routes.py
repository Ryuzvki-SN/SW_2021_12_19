from .models import *
from flask import jsonify, request
from api import app, db
from api.elector.model import Elector

# Define a route to fetch the avaialable Regions

@app.route("/api/region", methods=["GET"], strict_slashes=False)
def get_all_regions():
    region = db.session.query(Region).all()
    results = regions_schema.dump(region)
    db.session.close()
    return jsonify(results), 200


@app.route("/api/region/<id>", methods=["GET"], strict_slashes=False)
def get_region(id):
    region = Region.query.get(id)
    if not region:
        return jsonify({"message": "No region found!"}), 404
    return region_schema.jsonify(region), 200


# Define a route to fetch the avaialable Departements
@app.route("/api/departement", methods=["GET"], strict_slashes=False)
def get_all_departments():
    departement = db.session.query(Departement).all()
    results = departements_schema.dump(departement)
    db.session.close()
    return jsonify(results), 200


@app.route("/api/departement/<id>", methods=["GET"], strict_slashes=False)
def get_departement(id):
    departement = Departement.query.get(id)
    if not departement:
        return jsonify({"message": "No department found!"}), 404
    return departement_schema.jsonify(departement), 200


# Define a route to fetch the avaialable Arrondissements
@app.route("/api/arrondissement", methods=["GET"], strict_slashes=False)
def get_all_arrondissements():
    arrondissement = db.session.query(Arrondissement).all()
    results = arrondissements_schema.dump(arrondissement)
    db.session.close()
    return jsonify(results), 200


@app.route("/api/arrondissement/<id>", methods=["GET"], strict_slashes=False)
def get_arrondissement(id):
    arrondissement = Arrondissement.query.get(id)
    if not arrondissement:
        return jsonify({"message": "No arrondissement found!"}), 404
    return arrondissement_schema.jsonify(arrondissement), 200


# Define a route to fetch the avaialable Communes
@app.route("/api/commune", methods=["GET"], strict_slashes=False)
def get_all_communes():
    commune = db.session.query(Commune).all()
    results = communes_schema.dump(commune)
    db.session.close()
    return jsonify(results), 200


@app.route("/api/commune/<id>", methods=["GET"], strict_slashes=False)
def get_commune(id):
    commune = Commune.query.get(id)
    if not commune:
        return jsonify({"message": "No commune found!"}), 404
    return commune_schema.jsonify(commune), 200


# Define a route to fetch the avaialable Bureaux
@app.route("/api/bureau", methods=["GET"], strict_slashes=False)
def bureaux():
    br = db.session.query(Bureau).all()
    results = bureaux_schema.dump(br)
    db.session.close()
    return jsonify(results), 200


@app.route("/api/bureau/<id>", methods=["GET"], strict_slashes=False)
def bureau(id):
    br = Bureau.query.get(id)
    if not br:
        return jsonify({"message": "No bureau found!"}), 404
    return bureau_schema.jsonify(br), 200


@app.route("/api/bureau/<id>", methods=["PUT"], strict_slashes=False)
def update_bureau(id):
    data = request.get_json()
    br = Bureau.query.get(id)
    # results = db.session.execute("SELECT COUNT(*) FROM elector a "
    #                              "inner join bureau b on b.id = a.bureau_id WHERE bureau_id = '%s';" % br.id)
    # electeurs = results.fetchall()[0][0]

    if not br:
        return jsonify({"message": "No bureau found!"}), 404
    br.electeurs = db.session.query(Elector, Bureau).filter(Bureau.id == Elector.bureau_id).count()
    br.suffrage_valable = data['suffrage_valable']
    br.suffrage_invalide = data['suffrage_invalide']
    if (br.suffrage_valable + br.suffrage_invalide) != br.electeurs:
        return jsonify({"message": "sum suffrage different de nombre inscrit!"}), 404
    br.commune_id = data['commune_id']
    db.session.commit()
    return bureau_schema.jsonify(br), 200
