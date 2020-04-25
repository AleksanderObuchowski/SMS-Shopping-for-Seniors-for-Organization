from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_babel import _


class AddMessagesForm(FlaskForm):
    content = StringField(_('Message'), validators=[Length(max=500)])
    contact_number = StringField(_('Phone number'), validators=[Length(max=12)])
    location = StringField(_('Location'), validators=[Length(max=100)])
    status = SelectField(_('Status'), choices=[('Taken'),('Waiting for approval'),('Approved')])
    submit = SubmitField(_('Submit'))


class EditMessagesForm(FlaskForm):
    content = StringField(_('Message'), validators=[Length(max=500)])
    contact_number = StringField(_('Phone number'), validators=[Length(max=12)])
    location = StringField(_('Location'), validators=[Length(max=100)])
    longtitude = FloatField(_('Longitude'))
    latitude = FloatField(_('Latitude'))
    status = SelectField(_('Status'), choices=[('Taken'), ('Waiting for approval'), ('Approved')])
    submit = SubmitField(_('Submit'))