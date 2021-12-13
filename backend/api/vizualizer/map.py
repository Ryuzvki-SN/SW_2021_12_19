from flask import jsonify
from geojson import Point, Feature, FeatureCollection

from api import app, db
from api.circonscription.models import Region, regions_schema, \
    Departement, Arrondissement, departements_schema, \
    Commune, arrondissements_schema, communes_schema


@app.route("/api/map/region", methods=["GET"], strict_slashes=False)
def regions():
    features = []
    get_regions = db.session.query(Region).filter_by(id=Region.id).all()
    results = regions_schema.dump(get_regions)
    for city in results:
        location = city['location']
        lon, lat = map(float, location.strip('()').split(','))
        point = Point((lat, lon))
        features.append(Feature(geometry=point,
                                properties={"marker-color": "#f73b3b",
                                            "region": city['name'],
                                            "electeurs": city['electeurs'],
                                            "bureaux": city['bureaux'],
                                            "suffrage Valable": city['suffrage_valable'],
                                            "suffrage Invalide": city['suffrage_invalide'],
                                            },
                                id=city['id']))
    feature_collection = FeatureCollection(features)
    return jsonify(feature_collection), 200

@app.route("/api/map/region/<region_id>", methods=["GET"], strict_slashes=False)
def region(region_id):
    features = []
    departements = Departement.query.filter_by(region_id=region_id).all()
    results = departements_schema.dump(departements)
    for dept in results:
        location = dept['location']
        lon, lat = map(float, location.strip('()').split(','))
        point = Point((lat, lon))
        features.append(Feature(geometry=point,
                                properties={"marker-color": "#826fc8",
                                            "departement": dept['name'],
                                            "electeurs": dept['electeurs'],
                                            "bureaux": dept['bureaux'],
                                            "suffrage Valable": dept['suffrage_valable'],
                                            "suffrage Invalide": dept['suffrage_invalide'],
                                            },
                                id=dept['id']))
    feature_collection = FeatureCollection(features)
    return jsonify(feature_collection), 200

@app.route("/api/map/departement/<departement_id>", methods=["GET"], strict_slashes=False)
def departement(departement_id):
    features = []
    arrondissements = Arrondissement.query.filter_by(departement_id=departement_id).all()
    results = arrondissements_schema.dump(arrondissements)
    for arron in results:
        location = arron['location']
        lon, lat = map(float, location.strip('()').split(','))
        point = Point((lat, lon))
        features.append(Feature(geometry=point,
                                properties={"marker-color": "#43dfa4",
                                            "arrondissement": arron['name'],
                                            "electeurs": arron['electeurs'],
                                            "bureaux": arron['bureaux'],
                                            "suffrage Valable": arron['suffrage_valable'],
                                            "suffrage Invalide": arron['suffrage_invalide'],
                                            },
                                id=arron['id']))
    feature_collection = FeatureCollection(features)
    return jsonify(feature_collection), 200

@app.route("/api/map/arrondissement/<arrondissement_id>", methods=["GET"], strict_slashes=False)
def arrondissement(arrondissement_id):
    features = []
    communes = Commune.query.filter_by(arrondissement_id=arrondissement_id).all()
    results = communes_schema.dump(communes)
    for commu in results:
        location = commu['location']
        lon, lat = map(float, location.strip('()').split(','))
        point = Point((lat, lon))
        features.append(Feature(geometry=point,
                                properties={"marker-color": "#c4ce36",
                                            "arrondissement": commu['name'],
                                            "electeurs": commu['electeurs'],
                                            "bureaux": commu['total_bureau'],
                                            "suffrage Valable": commu['suffrage_valable'],
                                            "suffrage Invalide": commu['suffrage_invalide'],
                                            },
                                id=commu['id']))
    feature_collection = FeatureCollection(features)
    return jsonify(feature_collection), 200
