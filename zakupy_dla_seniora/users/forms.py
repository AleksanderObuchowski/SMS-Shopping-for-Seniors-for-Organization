from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_babel import _

from zakupy_dla_seniora.users.models import User


class AddForm(FlaskForm):
    username = StringField(_('Username'), validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField(_('Email'), validators=[DataRequired(), Email()])
    first_name = StringField(_('Name'), validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField(_('Surname'), validators=[DataRequired(), Length(min=2, max=50)])
    phone = StringField(_('Phone number'), validators=[DataRequired(), Length(min=9, max=12)])
    town = StringField(_('City'), validators=[DataRequired(), Length(max=100)])
    organisation = SelectField(_('Organisation'), coerce=int, validators=[DataRequired()])
    position = StringField('Position', validators=[Length(max=100)])
    is_superuser = BooleanField(_('Superuser'))
    submit = SubmitField(_('Register'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(_('This user name is already taken. Please choose other one.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(_('This email is already taken. Please choose other one.'))


class EditForm(FlaskForm):
    username = StringField(_('Username'), validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField(_('Email'), validators=[DataRequired(), Email()])
    first_name = StringField(_('Name'), validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField(_('Surname'), validators=[DataRequired(), Length(min=2, max=50)])
    phone = StringField(_('Phone number'), validators=[DataRequired(), Length(min=9, max=12)])
    town = StringField(_('City'), validators=[DataRequired(), Length(max=100)])
    position = StringField('Position', validators=[DataRequired(), Length(max=100)])
    is_superuser = BooleanField(_('Superuser'))
    submit = SubmitField(_('Register'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(_('This user name is already taken. Please choose other one.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(_('This email is already taken. Please choose other one.'))
