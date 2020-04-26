from flask_wtf import FlaskForm
from flask_babel import _

from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField(_('Login or Email'), validators=[DataRequired()])
    password = PasswordField(_('Password'), validators=[DataRequired()])
    submit = SubmitField(_('Save'))
