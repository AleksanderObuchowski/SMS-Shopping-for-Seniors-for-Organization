from flask_wtf import FlaskForm
from flask_babel import _

from wtforms import StringField, SelectField, FloatField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError


class AddMessagesForm(FlaskForm):
    content = TextAreaField(_('Message'), validators=[Length(max=500), DataRequired()])
    contact_number = StringField('Phone number', validators=[DataRequired(), Length(min=9, max=12)])
    location = StringField(_('Location'), validators=[Length(max=100), DataRequired()])
    submit = SubmitField(_('Add'))

    def validate_contact_number(self, contact_number):
        check = contact_number.data if contact_number.data[0] != '+' else contact_number[1:]
        if not check.isnumeric():
            raise ValidationError(_('Given phone number is invalid.'))


class EditMessagesForm(FlaskForm):
    content = StringField(_('Message'), validators=[Length(max=500)])
    contact_number = StringField('Phone Number', validators=[Length(max=12)])
    location = StringField(_('Location'), validators=[Length(max=100)])
    longitude = FloatField('Latitude')
    latitude = FloatField('Longitude')
    status = SelectField('Status', choices=[(_('Taken')), (_('Waiting for approval')), (_('Approved'))])
    submit = SubmitField(_('Save'))

    def validate_contact_number(self, contact_number):
        check = contact_number.data if contact_number.data[0] != '+' else contact_number[1:]
        if not check.isnumeric():
            raise ValidationError(_('Given phone number is invalid.'))
