from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

from flask_babel import _

class AddOrganisationForm(FlaskForm):
    name = StringField(_('Organisation name'), validators=[DataRequired()])
    submit = SubmitField(_('Add'))


class EditOrganisationForm(FlaskForm):
    contact_phone = StringField(_('Phone number'), validators=[Length(min=9,max=12)])
    contact_email = StringField(_('Email'), validators=[Length(min=5,max=100)])
    town = StringField(_('City'), validators=[Length(max=100)])
    postal_code = StringField(_('ZIP code'), validators=[Length(max=10)])
    address = StringField(_('Street and number'), validators=[Length(max=50)])
    website = StringField(_('Website'), validators=[Length(max=200)])
    submit = SubmitField(_('Save'))