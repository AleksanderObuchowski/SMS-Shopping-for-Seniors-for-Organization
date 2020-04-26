from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email

from flask_babel import _


class AddOrganisationForm(FlaskForm):
    name = StringField(_('Organisation name'), validators=[DataRequired()])
    contact_phone = StringField(_('Phone number'), validators=[DataRequired(message="Proszę podać numer telefonu"),
                                                               Length(min=9, max=12)])
    contact_email = StringField(_('Email'), validators=[DataRequired(), Email()])
    town = StringField(_('City'), validators=[Length(max=100)])
    postal_code = StringField(_('Postal code'), validators=[Length(max=10)])
    address = StringField(_('Address'), validators=[Length(max=100)])
    website = StringField(_('Website'), validators=[Length(max=200)])
    submit = SubmitField(_('Add'))

    def to_dict(self):
        return {
            'name': self.name.data,
            'contact_phone': self.contact_phone.data,
            'contact_email': self.contact_email.data,
            'town': self.town.data,
            'postal_code': self.postal_code.data,
            'address': self.address.data,
            'website': self.website.data,
        }


class EditOrganisationForm(FlaskForm):
    contact_phone = StringField(_('Phone number'), validators=[Length(min=9, max=12)])
    contact_email = StringField(_('Email'), validators=[Length(min=5, max=100)])
    town = StringField(_('City'), validators=[Length(max=100)])
    postal_code = StringField(_('Postal code'), validators=[Length(max=10)])
    address = StringField(_('Street and number'), validators=[Length(max=50)])
    website = StringField(_('Website'), validators=[Length(max=200)])
    submit = SubmitField(_('Save'))

    def to_dict(self):
        return {
            'contact_phone': self.contact_phone.data,
            'contact_email': self.contact_email.data,
            'town': self.town.data,
            'postal_code': self.postal_code.data,
            'address': self.address.data,
            'website': self.website.data,
        }
