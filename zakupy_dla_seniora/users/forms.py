from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_babel import _

from zakupy_dla_seniora.users.models import User


class RegistrationForm(FlaskForm):
    username = StringField(_('Username'), validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField(_('Email'), validators=[DataRequired(), Email()])
    organisation = StringField(_('Organisations'), validators=[DataRequired()])
    password = PasswordField(_('Password'), validators=[DataRequired()])
    confirm_password = PasswordField(_('Repeat password'), validators=[DataRequired(), EqualTo('password')])
    superuser = BooleanField(_('Superuser'))
    submit = SubmitField(_('Register'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(_('This user name is already taken. Please choose other one.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(_('This email is already taken. Please choose other one.'))
