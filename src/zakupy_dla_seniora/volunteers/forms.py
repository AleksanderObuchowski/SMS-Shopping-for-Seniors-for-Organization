from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length


class AddVolunteerForm(FlaskForm):
    first_name = StringField('Imie', validators=[Length(max=40)])
    last_name = StringField('Nazwisko', validators=Length(max=40))
    submit = SubmitField('Dodaj')


class EditVolunteerForm(FlaskForm):
    first_name = StringField('Imie', validators=[Length(max=40)])
    last_name = StringField('Nazwisko', validators=Length(max=40))
    phone_number = contact_phone = StringField('Tefefon kontaktowy', validators=[Length(min=9, max=12)])
    email = StringField('Adres email', validators=[Length(min=5, max=100)])
    town = StringField('Miasto', validators=[Length(max=100)])
    district = StringField('Dzielnica', validators=[Length(max=100)])
    submit = SubmitField('Zapisz')