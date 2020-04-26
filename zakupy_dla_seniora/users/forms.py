from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError, InputRequired
from flask_babel import _

from zakupy_dla_seniora.users.models import User


class AddUserForm(FlaskForm):
    username = StringField(_('Username'), validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField(_('Email'), validators=[DataRequired(), Email()])
    first_name = StringField(_('First name'), validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField(_('Last name'), validators=[DataRequired(), Length(min=2, max=50)])
    phone = StringField(_('Phone number'), validators=[DataRequired(), Length(min=9, max=12)])
    town = StringField(_('City'), validators=[DataRequired(), Length(max=100)])
    organisation = SelectField(_('Organisation'), coerce=int, validators=[DataRequired()])
    position = StringField('Position', validators=[Length(max=100)])
    is_superuser = SelectField('Is superuser', choices=[('No', 'No'), ('Yes', 'Yes')])
    submit = SubmitField(_('Register'))

    def validate_phone(self, phone):
        user = User.query.filter_by(phone=phone.data).first()
        print(user)
        if user:
            raise ValidationError(_('This phone number is already taken. Please choose another one.'))
        check = phone.data if phone.data[0] != '+' else phone[1:]
        if not check.isnumeric():
            raise ValidationError(_('Given phone number is invalid.'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(_('This user name is already taken. Please choose another one.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(_('This email is already taken. Please choose another one.'))

    def to_dict(self):
        return {
            'username': self.username.data,
            'email': self.email.data,
            'first_name': self.first_name.data,
            'last_name': self.last_name.data,
            'phone': self.phone.data,
            'town': self.town.data,
            'organisation_id': self.organisation.data,
            'position': self.position.data,
            'is_superuser': self.is_superuser.data == 'Yes'
        }


class EditUserForm(FlaskForm):
    username = StringField(_('Username'), validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField(_('Email'), validators=[DataRequired(), Email()])
    first_name = StringField(_('First name'), validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField(_('Last name'), validators=[DataRequired(), Length(min=2, max=50)])
    phone = StringField(_('Phone number'), validators=[DataRequired(), Length(min=9, max=12)])
    town = StringField(_('City'), validators=[DataRequired(), Length(max=100)])
    position = StringField('Position', validators=[DataRequired(), Length(max=100)])
    is_superuser = SelectField('Is superuser', validators=[InputRequired()], choices=[('No', 'No'), ('Yes', 'Yes')])
    submit = SubmitField(_('Save changes'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user and user.username != self.username.data:
            raise ValidationError(_('This user name is already taken. Please choose another one.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user and user.email != self.email.data:
            raise ValidationError(_('This email is already taken. Please choose another one.'))

    def to_dict(self):
        return {
            'username': self.username.data,
            'email': self.email.data,
            'first_name': self.first_name.data,
            'last_name': self.last_name.data,
            'phone': self.phone.data,
            'town': self.town.data,
            'position': self.position.data,
            'is_superuser': self.is_superuser.data == 'Yes'
        }
