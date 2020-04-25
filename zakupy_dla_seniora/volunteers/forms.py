from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, ValidationError
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
    organisation = SelectField('Organizacja')
    submit = SubmitField('Zarejestruj')

    @staticmethod
    def validate_email(self, email):
        vol = Volunteers.query.filter_by(email=email.data).first()
        if vol:
            raise ValidationError('Ten adres email jest zajęty.')

    @staticmethod
    def validate_phone_number(self, phone_number):
        vol = Volunteers.query.filter_by(email=phone_number.data).first()
        if vol:
            raise ValidationError('Ten numer telefonu został już zarejestrowany.')


class EditVolunteerForm(FlaskForm):
    first_name = StringField('Imię', validators=[Length(min=2, max=30)])
    last_name = StringField('Nazwisko', validators=[Length(min=2, max=30)])
    phone_number = StringField('Numer telefonu', validators=[Length(min=9, max=12)])
    email = StringField('Adres email', validators=[Email(message="Email jest niepoprawny"), Length(max=50)])
    town = StringField('Miasto', validators=[Length(max=100)])
    district = StringField('Dzielnica', validators=[Length(max=100)])
    organisation = SelectField('Organizacja')
    is_active = BooleanField("Aktywny")
    submit = SubmitField('Zapisz')

    @staticmethod
    def validate_email(self, email):
        vol = Volunteers.query.filter_by(email=email.data).first()
        if vol:
            raise ValidationError('Ten adres email jest zajęty.')

    @staticmethod
    def validate_phone_number(self, phone_number):
        vol = Volunteers.query.filter_by(email=phone_number.data).first()
        if vol:
            raise ValidationError('Ten numer telefonu został już zarejestrowany.')
