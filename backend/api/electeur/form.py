from wtforms import (
    StringField, IntegerField,
    PasswordField, SubmitField, DateField,
    validators, ValidationError
)
from flask_wtf import FlaskForm
from .model import Electeur


class ElecteurRegisterForm(FlaskForm):
    firstname = StringField('First Name: ', [validators.DataRequired()])
    lastname = StringField('Last Name: ', [validators.DataRequired()])
    birthday = DateField('Birthday: ', [validators.DataRequired()])
    cni = IntegerField('CNI: ', [validators.DataRequired()])
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired(),
                                            validators.EqualTo('confirm', message=' Both password must match! ')])
    confirm = PasswordField('Repeat Password: ', [validators.DataRequired()])
    address = StringField('Address: ', [validators.DataRequired()])

    submit = SubmitField('Electeur')

    @staticmethod
    def validate_cni(cni):
        if Electeur.query.filter_by(cni=cni.data).first():
            raise ValidationError("This CNI is already in use!")

    @staticmethod
    def validate_email(email):
        if Electeur.query.filter_by(email=email.data).first():
            raise ValidationError("This email address is already in use!")


class ElecteurLoginFrom(FlaskForm):
    cni = IntegerField('CNI: ', [validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired()])
