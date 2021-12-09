from flask import jsonify
from geojson import Point, Feature, FeatureCollection
from api import app, db
from api.circonscription.models import Region, regions_schema, Departement, departements_schema


@app.route("/api/region/visualizer", methods=["GET"], strict_slashes=False)
def get_all_region_location():
    features = []
    regions = db.session.query(Region).filter_by(location=Region.location).all()
    results = regions_schema.dump(regions)
    for itm1 in results:
        location = itm1['location']
        lng, lat = map(float, location.strip('()').split(','))
        point = Point((lat, lng))
        # dep_loc = itm1['departements']['location']
        # lng_dep, lat_dep = map(float, dep_loc.strip('()').split(','))
        features.append(Feature(geometry=point, properties={"region": itm1['name']}, id=itm1['id'],
                                departements=itm1['departements']['location']))
    feature_collection = FeatureCollection(features)
    return jsonify(feature_collection), 200
