from flask_wtf import FlaskForm
from flask_babel import _

from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError, InputRequired

from zakupy_dla_seniora.users.models import User


class AddVolunteerForm(FlaskForm):
    username = StringField(_('Username'), validators=[DataRequired(), Length(min=2, max=30)])
    first_name = StringField(_('First name'),
                             validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField(_('Last name'), validators=[DataRequired(), Length(min=2, max=30)])
    phone_number = StringField(_('Phone number'), validators=[DataRequired(), Length(min=9, max=12)])
    email = StringField(_('Email'), validators=[DataRequired(), Email(), Length(max=50)])
    town = StringField(_('City'), validators=[DataRequired(), Length(max=100)])
    district = StringField(_('District'), validators=[DataRequired(), Length(max=100)])
    organisation = SelectField(_('Organisation'), coerce=int)
    submit = SubmitField(_('Register'))

    def validate_email(self, email):
        vol = User.query.filter_by(email=email.data).first()
        if vol:
            raise ValidationError(_('This email is already used.'))

    def validate_phone_number(self, phone_number):
        check = phone_number.data if phone_number.data[0] != '+' else phone_number[1:]
        if not check.isnumeric():
            raise ValidationError(_('Given phone number is invalid.'))

    def to_dict_edit(self):
        return {
            'first_name': self.first_name.data,
            'last_name': self.last_name.data,
            'phone': self.phone_number.data,
            'town': self.email.data,
            'district': self.district.data,
        }


class EditVolunteerForm(FlaskForm):
    username = StringField(_('Username'), validators=[Length(max=20)])
    first_name = StringField(_('First name'), validators=[Length(min=2, max=30)])
    last_name = StringField(_('Last name'), validators=[Length(min=2, max=30)])
    phone_number = StringField(_('Phone number'), validators=[Length(min=9, max=12)])
    email = StringField(_('Email'), validators=[Email(), Length(max=50)])
    town = StringField(_('City'), validators=[Length(max=100)])
    district = StringField(_('District'), validators=[Length(max=100)])
    is_active = SelectField(_('Active'), choices=[('Yes', 'Yes'), ('No', 'No')])
    submit = SubmitField(_('Save'))

    def validate_email(self, email):
        vol = User.query.filter_by(email=email.data).first()
        if vol and vol.username != self.username.data:
            raise ValidationError(_('This email is already used.'))

    def validate_phone_number(self, phone_number):
        if phone_number.data != '':
            check = phone_number.data if phone_number.data[0] != '+' else phone_number[1:]
            if not check.isnumeric():
                raise ValidationError(_('Given phone number is invalid.'))

    def to_dict(self):
        return {
            'username': self.username.data,
            'first_name': self.first_name.data,
            'last_name': self.last_name.data,
            'phone': self.phone_number.data,
            'email': self.email.data,
            'town': self.town.data,
            'district': self.district.data,
            'is_active': self.is_active.data == 'Yes'
        }
