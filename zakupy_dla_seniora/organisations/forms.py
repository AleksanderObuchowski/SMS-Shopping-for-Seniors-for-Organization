from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class AddOrganisationForm(FlaskForm):
    name = StringField('Nazwa organizacji', validators=[DataRequired()])
    submit = SubmitField('Dodaj')


class EditOrganisationForm(FlaskForm):
    contact_phone = StringField('Tefefon kontaktowy', validators=[Length(min=9,max=12)])
    contact_email = StringField('Adres email', validators=[Length(min=5,max=100)])
    town = StringField('Miasto', validators=[Length(max=100)])
    postal_code = StringField('Kod pocztowy', validators=[Length(max=10)])
    address = StringField('Ulica i numer', validators=[Length(max=50)])
    website = StringField('Strona internetowa', validators=[Length(max=200)])
    submit = SubmitField('Zapisz')