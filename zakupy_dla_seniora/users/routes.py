from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user

from zakupy_dla_seniora import bcrypt
from zakupy_dla_seniora.auth.functions import employee_role_required
from zakupy_dla_seniora.organisations.models import Organisations
from zakupy_dla_seniora.users.forms import RegistrationForm
from zakupy_dla_seniora.users.models import User
from zakupy_dla_seniora.messages.models import Messages
users = Blueprint('users', __name__)


@users.route('/profile')
def profile():
    messages = Messages.get_user_messages(current_user.id)
    return render_template('view_user_profile.jinja2', user=current_user, messages = messages)


@users.route('/register-account', methods=['GET', 'POST'])
@employee_role_required
def register_user():
    form = RegistrationForm()
    form.organisation.choices = [
        (org_id, name) for org_id, name in Organisations.query.with_entities(Organisations.id, Organisations.name).all()
    ]

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, organisation_id=form.organisation.data,
                    password_hash=hashed_password, created_by=current_user.id, is_superuser=form.superuser.data)
        user.save()
        flash('Konto zostało utworzone pomyślnie.', 'success')
        return redirect(url_for('board.view'))
    return render_template('forms/register-account.jinja2', form=form)

# TODO Add edit user profile form, for superuser add possibility to see all users and manage them
