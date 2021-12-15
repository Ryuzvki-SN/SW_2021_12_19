from datetime import datetime
import timedelta
import uuid
from functools import wraps

import jwt
from flask import request, jsonify, make_response

from api import bcrypt, app
from .model import *


# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')  # http://127.0.0.1:5000/api/electeur?token
        # =eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9
        # .eyJwdWJsaWNfaWQiOiJkNmQ2OTlmMC0yM2YzLTQ3NGEtOGZmNi05ODJkNGFjMDM4ZmEiLCJleHAiOjE2MzkzMTA5OTN9
        # .gU244rqYqsMAxemY17Az58iNPmgIFMqAAkwf8wAulH4

        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = Elector.query.filter_by(public_id=data['public_id']).first()
        except (Exception,):
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/api/elector', methods=['GET'], strict_slashes=False)
@token_required
def electors(current_user):
    users = db.session.query(Elector).all()
    results = electors_schema.dump(users)
    db.session.close()
    return jsonify(results), 200


@app.route('/api/elector/login', methods=['POST'], strict_slashes=False)
def login():
    # creates dictionary of form data
    auth = request.form

    if not auth or not auth.get('cni') or not auth.get('password'):
        # returns 401 if any cni or / and password is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
        )

    user = Elector.query.filter_by(cni=auth.get('cni')).first()

    if not user:
        # returns 401 if user does not exist
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
        )

    if bcrypt.check_password_hash(user.password, auth.get('password')):
        # generates the JWT Token
        token = jwt.encode({
            'public_id': user.public_id,
            'exp': datetime.utcnow() + timedelta.Timedelta(minutes=30)
        }, app.config['SECRET_KEY'])
        return make_response(jsonify({'token': token.decode('UTF-8')}), 201)
    # returns 403 if password is wrong
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
    )


# signup route
@app.route('/api/elector/register', methods=["POST"], strict_slashes=False)
def signup():
    # creates a dictionary of the form data
    data = request.get_json()

    hash_password = bcrypt.generate_password_hash(data['password'])
    birth_format = datetime.strptime(data['birthday'], '%Y-%m-%d')
    lastname = data['lastname']
    firstname = data['firstname']
    birthday = birth_format
    cni = data['cni']
    email = data['email']
    password = hash_password
    address = data['address']
    bureau = data['bureau_id']
    commune = data['commune_id']

    # checking for existing user
    user = Elector.query.filter_by(cni=cni).first()
    if not user:
        # database ORM object
        user = Elector(
            public_id=str(uuid.uuid4()),
            lastname=lastname, firstname=firstname,
            birthday=birthday,
            cni=cni,
            email=email,
            password=password,
            address=address,
            bureau_id=bureau,
            commune_id=commune
        )
        # insert user
        db.session.add(user)
        db.session.commit()

        return make_response('Successfully registered.', 201)
    else:
        # returns 202 if user already exists
        return make_response('User already exists. Please Log in.', 202)
