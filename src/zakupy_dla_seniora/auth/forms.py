from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField('Login lub email', validators=[DataRequired()])
    password = PasswordField('Hasło',  validators=[DataRequired()])
    submit = SubmitField('Zaloguj się')
