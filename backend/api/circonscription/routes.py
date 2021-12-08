from .models import *
from flask import jsonify, request
from api import app, db


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


@app.route("/api/region", methods=["POST"], strict_slashes=False)
def add_region():
    data = request.get_json()
    posted = RegionSchema(only=('name', 'location')).load(data)
    region = Region(**posted)
    db.session.add(region)
    db.session.commit()
    newbie = RegionSchema().dump(region)
    db.session.close()
    return jsonify(newbie), 201


@app.route("/api/region/<id>", methods=["PUT"], strict_slashes=False)
def update_region(id):
    data = request.get_json()
    region = Region.query.get(id)
    if not region:
        return jsonify({"message": "No region found!"}), 404
    region.name = data['name']
    region.location = data['location']
    db.session.commit()
    return region_schema.jsonify(region), 200


@app.route("/api/region/<id>", methods=["DELETE"], strict_slashes=False)
def delete_region(id):
    region = Region.query.filter_by(id=id).first()
    if not region:
        return jsonify({"message": "No city found!"}), 404
    db.session.delete(region)
    db.session.commit()
    return jsonify({"message": "The city has been deleted."}), 200


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


@app.route("/api/departement", methods=["POST"], strict_slashes=False)
def add_department():
    data = request.get_json()
    posted = DepartementSchema(only=('name', 'location', 'region_id')).load(data)
    department = Departement(**posted)
    db.session.add(department)
    db.session.commit()
    newbie = DepartementSchema().dump(department)
    db.session.close()
    return jsonify(newbie), 201


@app.route("/api/departement/<id>", methods=["PUT"], strict_slashes=False)
def update_department(id):
    data = request.get_json()
    department = Departement.query.get(id)
    if not department:
        return jsonify({"message": "No department found!"}), 404
    department.name = data['name']
    department.location = data['location']
    department.region_id = data['region_id']
    db.session.commit()
    return departement_schema.jsonify(department), 200


@app.route("/api/departement/<id>", methods=["DELETE"], strict_slashes=False)
def delete_department(id):
    department = Departement.query.filter_by(id=id).first()
    if not department:
        return jsonify({"message": "No department found!"}), 404
    db.session.delete(department)
    db.session.commit()
    return jsonify({"message": "The department has been deleted."}), 200


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


@app.route("/api/arrondissement", methods=["POST"], strict_slashes=False)
def add_arrondissement():
    data = request.get_json()
    posted = ArrondissementSchema(only=('name', 'location', 'departement_id')).load(data)
    arrondissement = Arrondissement(**posted)
    db.session.add(arrondissement)
    db.session.commit()
    newbie = ArrondissementSchema().dump(arrondissement)
    db.session.close()
    return jsonify(newbie), 201


@app.route("/api/arrondissement/<id>", methods=["PUT"], strict_slashes=False)
def update_arrondissement(id):
    data = request.get_json()
    arrondissement = Arrondissement.query.get(id)
    if not arrondissement:
        return jsonify({"message": "No arrondissement found!"}), 404
    arrondissement.name = data['name']
    arrondissement.location = data['location']
    arrondissement.departement_id = data['departement_id']
    db.session.commit()
    return arrondissement_schema.jsonify(arrondissement), 200


@app.route("/api/arrondissement/<id>", methods=["DELETE"], strict_slashes=False)
def delete_arrondissement(id):
    arrondissement = Arrondissement.query.filter_by(id=id).first()
    if not arrondissement:
        return jsonify({"message": "No arrondissement found!"}), 404
    db.session.delete(arrondissement)
    db.session.commit()
    return jsonify({"message": "The arrondissement has been deleted."}), 200


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


@app.route("/api/commune", methods=["POST"], strict_slashes=False)
def add_commune():
    data = request.get_json()
    posted = CommuneSchema(only=('name', 'location', 'arrondissement_id')).load(data)
    commune = Commune(**posted)
    db.session.add(commune)
    db.session.commit()
    newbie = CommuneSchema().dump(commune)
    db.session.close()
    return jsonify(newbie), 201


@app.route("/api/commune/<id>", methods=["PUT"], strict_slashes=False)
def update_commune(id):
    data = request.get_json()
    commune = Commune.query.get(id)
    if not commune:
        return jsonify({"message": "No commune found!"}), 404
    commune.name = data['name']
    commune.location = data['location']
    commune.arrondissement_id = data['arrondissement_id']
    db.session.commit()
    return commune_schema.jsonify(commune), 200


@app.route("/api/commune/<id>", methods=["DELETE"], strict_slashes=False)
def delete_commune(id):
    commune = Commune.query.filter_by(id=id).first()
    if not commune:
        return jsonify({"message": "No commune found!"}), 404
    db.session.delete(commune)
    db.session.commit()
    return jsonify({"message": "The commune has been deleted."}), 200


# Define a route to fetch the avaialable Bureau

@app.route("/api/bureau", methods=["GET"], strict_slashes=False)
def get_all_bureaux():
    bureau = db.session.query(Bureau).all()
    results = bureaux_schema.dump(bureau)
    db.session.close()
    return jsonify(results), 200


@app.route("/api/bureau/<id>", methods=["GET"], strict_slashes=False)
def get_bureau(id):
    bureau = Bureau.query.get(id)
    if not bureau:
        return jsonify({"message": "No bureau found!"}), 404
    return bureau_schema.jsonify(bureau), 200


@app.route("/api/bureau", methods=["POST"], strict_slashes=False)
def add_bureau():
    data = request.get_json()
    posted = BureauSchema(only=('nombre_inscrit', 'suffrage_valable', 'suffrage_invalide', 'commune_id')) \
        .load(data)
    bureau = Bureau(**posted)
    db.session.add(bureau)
    db.session.commit()
    newbie = BureauSchema().dump(bureau)
    db.session.close()
    return jsonify(newbie), 201


@app.route("/api/bureau/<id>", methods=["PUT"], strict_slashes=False)
def update_bureau(id):
    data = request.get_json()
    bureau = Bureau.query.get(id)
    if not bureau:
        return jsonify({"message": "No bureau found!"}), 404
    bureau.nombre_inscrit = data['nombre_inscrit']
    bureau.suffrage_valable = data['suffrage_valable']
    bureau.suffrage_invalide = data['suffrage_invalide']
    bureau.commune_id = data['commune_id']
    db.session.commit()
    return bureau_schema.jsonify(bureau), 200


@app.route("/api/bureau/<id>", methods=["DELETE"], strict_slashes=False)
def delete_bureau(id):
    bureau = Bureau.query.filter_by(id=id).first()
    if not bureau:
        return jsonify({"message": "No bureau found!"}), 404
    db.session.delete(bureau)
    db.session.commit()
    return jsonify({"message": "The bureau has been deleted."}), 200
