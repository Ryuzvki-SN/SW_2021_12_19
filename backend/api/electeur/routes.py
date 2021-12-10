from flask_login import login_user, logout_user

from .form import ElecteurRegisterForm, ElecteurLoginFrom
from .model import *
from flask import flash, redirect, url_for, render_template, request
from api import db, bcrypt, app


@app.route('/electeur/register', methods=['GET', 'POST'])
def electeur_register():
    form = ElecteurRegisterForm()
    electeur = Electeur.query
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        electeur.lastname = form.lastname.data
        electeur.firstname = form.firstname.data,
        electeur.birthday = form.birthday.data,
        electeur.cni = form.cni.data,
        electeur.email = form.email.data,
        electeur.password = hash_password,
        electeur.address = form.address.data

        db.session.add(electeur)
        flash('Welcome {form.firstname.data} Thank you for registering', 'success')
        db.session.commit()
        return redirect(url_for('login'))
    # return render_template('electeur/register.html', form=form)
    return electeurs_schema.jsonify(electeur)


@app.route('/electeur/login', methods=['GET', 'POST'])
def electeur_login():
    form = ElecteurLoginFrom()
    user = Electeur.query.filter_by(cni=form.cni.data).first()
    if form.validate_on_submit():
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You are login now!', 'success')
            next_e = request.args.get('next')
            return redirect(next_e or url_for('home'))
        flash('Incorrect email and password', 'danger')
        return redirect(url_for('electeur_login'))

    # return render_template('electeur/login.html', form=form)
    return electeur_schema.jsonify(user)


@app.route('/electeur/logout')
def electeur_logout():
    logout_user()
    return redirect(url_for('home'))
