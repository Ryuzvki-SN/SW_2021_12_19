from flask import jsonify
from geojson import Point, Feature, FeatureCollection

from api import app, db
from api.circonscription.models import Region, regions_schema, Departement


@app.route("/api/region/visualizer", methods=["GET"], strict_slashes=False)
def get_data_region():
    features = []
    regions = db.session.query(Region).filter_by(id=Region.id).all()
    results = regions_schema.dump(regions)
    for itm1 in results:
        location = itm1['location']
        lng, lat = map(float, location.strip('()').split(','))
        point = Point((lat, lng))
        features.append(Feature(geometry=point,
                                properties={"region": itm1['name'],
                                            "electeurs": itm1['electeurs'],
                                            "bureaux": itm1['bureaux'],
                                            "suffrage Valable": itm1['suffrage_valable'],
                                            "suffrage Invalide": itm1['suffrage_invalide'],
                                            },
                                id=itm1['id']))
    feature_collection = FeatureCollection(features)
    return jsonify(feature_collection), 200


@app.route("/api/departement/visualizer", methods=["GET"], strict_slashes=False)
def get_data_department():
    features = []
    departement = db.session.query(Departement).filter_by(id=Departement.region_id).all()
    results = regions_schema.dump(departement)
    for itm2 in results:
        location = itm2['location']
        lng, lat = map(float, location.strip('()').split(','))
        point = Point((lat, lng))
        features.append(Feature(geometry=point,
                                properties={"departement": itm2['name'],
                                            "electeurs": itm2['electeurs'],
                                            "bureaux": itm2['bureaux'],
                                            "suffrage Valable": itm2['suffrage_valable'],
                                            "suffrage Invalide": itm2['suffrage_invalide'],
                                            },
                                id=itm2['id']))
    feature_collection = FeatureCollection(features)
    return jsonify(feature_collection), 200
