import datetime

from flask_login import login_user, logout_user, login_required
from .model import *
from flask import flash, request, jsonify
from api import db, bcrypt, app


@login_manager.user_loader
def load_user(user_id):
    return Electeur.query.get(int(user_id))


@app.route('/electeur/register', methods=["POST"], strict_slashes=False)
def register():
    data = request.get_json()
    hash_password = bcrypt.generate_password_hash(data['password'])
    birth = datetime.strptime(data['birthday'], '%Y-%m-%d')
    lastname = data['lastname']
    firstname = data['firstname']
    birthday = birth
    cni = data['cni']
    email = data['email']
    password = hash_password
    address = data['address']
    electeur = Electeur(lastname=lastname, firstname=firstname,
                        birthday=birthday, cni=cni, email=email,
                        password=password, address=address)
    # Add user to the database
    db.session.add(electeur)
    flash('Thank you for registering', 'success')  # Save
    db.session.commit()
    # Show a success message
    flash("Account Succesfully created", "success")

    return electeur_schema.jsonify(electeur)


@app.route('/electeur/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        try:
            # get the user that exists with the submitted email
            user = Electeur.query.filter_by(cni=Electeur.cni).first()
            # check if the user given email matches the password
            # that is stored for that email
            if user and bcrypt.check_password_hash(user.password, Electeur.password):
                # login the user
                login_user(user)
                # Redirect to the user account
                flash('You are login now!', 'success')
            else:
                flash("Invalid cni or password!", "danger")
        except (Exception,):
            flash("Invalid cni or password!", "danger")

    return jsonify({'message': 'success'})


@app.route('/electeur/logout')
@login_required
def logout():
    logout_user()
