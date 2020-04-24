from flask_wtf import FlaskForm
from sqlalchemy import create_engine
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from zakupy_dla_seniora.organisations.models import Organisations
from zakupy_dla_seniora.volunteers.models import Volunteers


class AddVolunteerForm(FlaskForm):
    first_name = StringField('Imię', validators=[DataRequired(message="Proszę podać imię"), Length(min=2, max=30)])
    last_name = StringField('Nazwisko', validators=[DataRequired(message="Proszę podać nazwisko"),
                                                    Length(min=2, max=30)])
    phone_number = StringField('Numer telefonu', validators=[DataRequired(message="Proszę podać numer tlefonu"),
                                                             Length(min=9, max=12)])
    email = StringField('Adres email', validators=[DataRequired(message="Proszę podać email"),
                                                   Email(message="Email jest niepoprawny"), Length(max=50)])
    town = StringField('Miasto', validators=[DataRequired(message="Proszę podać miasto"), Length(max=100)])
    district = StringField('Dzielnica', validators=[DataRequired(message="Proszę podać dzielnicę"), Length(max=100)])
    organisation = StringField('Organizacja', validators=[DataRequired(message="Proszę podać nazwę organizacji")])
    submit = SubmitField('Zarejestruj')

    @staticmethod
    def validate_email(self, email):
        vol = Volunteers.query.filter_by(email=email.data).first()
        if vol:
            raise ValidationError('Ten adres email jest zajęty.')
