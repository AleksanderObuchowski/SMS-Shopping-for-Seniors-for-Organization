from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_babel import _

class AddMessagesForm(FlaskForm):
    content = TextAreaField(_('Message'), validators=[Length(max=500)])
    contact_number = StringField('Phone Number', validators=[Length(max=12)])
    location = StringField(_('Location'), validators=[Length(max=100)])
    submit = SubmitField(_('Add'))


class EditMessagesForm(FlaskForm):
    content = StringField(_('Message'), validators=[Length(max=500)])
    contact_number = StringField('Phone Number', validators=[Length(max=12)])
    location = StringField(_('Location'), validators=[Length(max=100)])
    longitude = FloatField('Latitude')
    latitude = FloatField('Longitude')
    status = SelectField('Status', choices=[(_('Taken')),('Waiting for approval'),(_('Approved'))])
    submit = SubmitField(_('Save'))