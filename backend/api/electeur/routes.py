from flask_login import login_user, logout_user, login_required
from .form import ElecteurRegisterForm, ElecteurLoginFrom
from .model import *
from flask import flash, redirect, url_for, render_template, request
from api import db, bcrypt, app

@login_manager.user_loader
def load_user(user_id):
    return Electeur.query.get(int(user_id))

@app.route('/electeur/register', methods=['GET', 'POST'])
def register():
    form = ElecteurRegisterForm()
    electeur = Electeur.query
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        lastname = form.lastname.data
        firstname = form.firstname.data,
        birthday = form.birthday.data,
        cni = form.cni.data,
        email = form.email.data,
        password = hash_password,
        address = form.address.data
        # create a variable to hold the user object
        newbie = Electeur(
            lastname=lastname,
            firstname=firstname,
            birthday=birthday,
            cni=cni,
            email=email,
            password=password,
            address=address,
        )

        db.session.add(newbie)
        flash('Welcome {form.firstname.data} Thank you for registering', 'success')
        db.session.commit()
        return redirect(url_for('dashboard'))
    # return render_template('electeur/register.html', form=form)
    return electeurs_schema.jsonify(electeur)


@app.route('/electeur/login', methods=['GET', 'POST'])
def login():
    form = ElecteurLoginFrom()
    electeur = Electeur.query
    if form.validate_on_submit():
        if electeur and bcrypt.check_password_hash(electeur.password, form.password.data):
            electeur = Electeur.query.filter_by(cni=form.cni.data).first()
            login_user(electeur)
            flash('You are login now!', 'success')
            next_e = request.args.get('next')
            return redirect(next_e or url_for('home'))
        flash('Incorrect email and password', 'danger')
        return redirect(url_for('dashboard'))

    # return render_template('electeur/login.html', form=form)
    return electeur_schema.jsonify(electeur)


@app.route('/electeur/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
