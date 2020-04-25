from flask_wtf import FlaskForm
from sqlalchemy import create_engine
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from zakupy_dla_seniora.organisations.models import Organisations
from zakupy_dla_seniora.volunteers.models import Volunteers
from flask_babel import _


class AddVolunteerForm(FlaskForm):
    first_name = StringField(_('Name'), validators=[DataRequired(message=_("Please, give name")), Length(min=2, max=30)])
    last_name = StringField(_('Surname'), validators=[DataRequired(message=_("Please, give surname")),
                                                    Length(min=2, max=30)])
    phone_number = StringField(_('Phone number'), validators=[DataRequired(message=_("Please, give phone number")),
                                                             Length(min=9, max=12)])
    email = StringField(_('Email address'), validators=[DataRequired(message=_("Please, give email")),
                                                   Email(message=_("Email is incorrect")), Length(max=50)])
    town = StringField(_('City'), validators=[DataRequired(message=_("Please, give city")), Length(max=100)])
    district = StringField(_('District'), validators=[DataRequired(message=_("Please, give district")), Length(max=100)])
    organisation = StringField(_('Organisation'), validators=[DataRequired(message=_("Please, give name of organisation"))])
    submit = SubmitField(_("Register"))

    @staticmethod
    def validate_email(self, email):
        vol = Volunteers.query.filter_by(email=email.data).first()
        if vol:
            raise ValidationError(message=_("This email address is taken"))
