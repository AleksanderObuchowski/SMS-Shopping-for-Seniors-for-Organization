from flask_wtf import FlaskForm
from mongoengine import ValidationError
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email

from zakupy_dla_seniora.users.models import User


class LoginForm(FlaskForm):
    login = StringField('Login lub email', validators=[DataRequired()])
    password = PasswordField('Hasło',  validators=[DataRequired()])
    submit = SubmitField('Zaloguj się')


class RegistrationForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    organisation = StringField('Organizacja', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    confirm_password = PasswordField('Powtórz hasło', validators=[DataRequired(), EqualTo('password')])
    superuser = BooleanField('Superuser')
    submit = SubmitField('Zarejestruj')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ta nazwa użytjownika jest zajęta. Proszę wybrać inną.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Ten aders email jest zajęty. Proszę wybrać inny.')