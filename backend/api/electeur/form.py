from wtforms import (
    StringField, IntegerField,
    PasswordField, SubmitField, DateField,
    validators, ValidationError
)
from flask_wtf import FlaskForm

from .model import Electeur


class ElecteurRegisterForm(FlaskForm):
    firstname = StringField('First Name: ', [validators.DataRequired(),
                                             validators.Length(3, 20, message="Please provide a valid name"),
                                             validators.Regexp("^[A-Za-z][A-Za-z0-9_.]*$", 0,
                                                               "Names must have only letters, " "numbers, dots or "
                                                               "underscores",
                                                               ), ])
    lastname = StringField('Last Name: ', [validators.DataRequired(),
                                           validators.Length(3, 20, message="Please provide a valid name"),
                                           validators.Regexp("^[A-Za-z][A-Za-z0-9_.]*$", 0,
                                                             "Names must have only letters, " "numbers, dots or "
                                                             "underscores",
                                                             ), ])
    birthday = DateField('Birthday: ', [validators.DataRequired()])
    cni = IntegerField('CNI: ', [validators.InputRequired()])
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired(),
                                            validators.EqualTo('confirm', message=' Both password must match! ')])
    confirm = PasswordField('Repeat Password: ', [validators.DataRequired()])
    address = StringField('Address: ', [validators.DataRequired()])

    submit = SubmitField('Electeur')

    def validate_cni(self, cni):
        if Electeur.query.filter_by(cni=cni.data).first():
            raise ValidationError("This CNI is already in use!")

    def validate_email(self, email):
        if Electeur.query.filter_by(email=email.data).first():
            raise ValidationError("This email address is already in use!")


class ElecteurLoginFrom(FlaskForm):
    cni = IntegerField('CNI: ', [validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired()])
