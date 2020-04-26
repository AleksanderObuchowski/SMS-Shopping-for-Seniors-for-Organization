from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import current_user

from zakupy_dla_seniora import bcrypt
from zakupy_dla_seniora.auth.functions import employee_role_required
from zakupy_dla_seniora.messages.models import Messages
from zakupy_dla_seniora.users.functions import random_password
from zakupy_dla_seniora.users.forms import AddForm, EditForm
from zakupy_dla_seniora.users.models import User
from zakupy_dla_seniora.organisations.models import Organisations
from flask_babel import _

users = Blueprint('users', __name__, url_prefix='/<lang_code>')


@users.route('/profile')
def profile():
    messages = Messages.get_user_messages(current_user.id)
    return render_template('view_user_profile.jinja2', user=current_user, messages = messages)


@users.route('/add_user', methods=['GET', 'POST'])
@employee_role_required
def add_user():
    if current_user.is_superuser:
        organisations = [
            (org_id, name) for org_id, name in Organisations.query.with_entities(
                Organisations.id, Organisations.name
            ).all()
        ]
    else:
        organisations = (current_user.organisation_id, Organisations.get_name_by_id(current_user.id))


    form = EditForm()
    form.organisation.choices = organisations

    if form.validate_on_submit() and request.method == "POST":
        password = random_password()
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        username = form.username.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone = form.phone.data
        town = form.town.data
        position = form.position.data
        organisation_id = form.organisation.data
        is_superuser = form.is_superuser.data if form.is_superuser.data else False

        user = User(username=username, email=email, first_name=first_name, last_name=last_name, phone=phone, town=town, position=position,
                    is_superuser=is_superuser,
                    password_hash=hashed_password, organisation_id=organisation_id,
                    created_by=current_user.id)
        user.save()
        flash(_('Account has been created successfully.'), 'success')
        print("username : {} , password : {}".format(username, password))
        return redirect(url_for('board.view'))
    return render_template('forms/add_user.jinja2', form=form)


@users.route('/users')
@employee_role_required
def show_all():
    if current_user.is_employee:
        data = User.get_all_for_organisation(current_user.organisation_id)
    else:
        data = User.get_all()
    return render_template('show_users.jinja2', data=data)


@users.route('/users/<id>')
@employee_role_required
def show(id):
    if current_user.is_superuser:
        _user = User.get_one(id)
        return render_template('view_user_profile.jinja2', user=_user)
    elif current_user.is_employee:
        _user = User.get_one(id, current_user.organisation_id)
        if not _user:
            error_message = _("There is no such user in your organisation.")
        else:
            return render_template('view_user_profile.jinja2', user=_user)
    else:
        return redirect(url_for('board.view'))



@users.route('/users/<id>/edit', methods=['GET', 'POST'])
@employee_role_required
def edit_user(id):
    form = EditForm()
    _user = User.get_by_id(id)
    if form.validate_on_submit() and request.method == "POST":
        username = form.username.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone = form.phone.data
        town = form.town.data
        position = form.position.data
        is_superuser = form.is_superuser.data if form.is_superuser.data else False

        user = User(username=username, email=email, first_name=first_name, last_name=last_name, phone=phone, town=town, position=position,
                    is_superuser=is_superuser,
                    created_by=current_user.id)
        user.save()
        flash(_('Account has been edited successfully.'), 'success')
        return redirect(url_for('board.view'))

    elif request.method == "GET":
        form.username.data = _user.username
        form.email.data = _user.email
        form.first_name.data = _user.first_name
        form.last_name.data = _user.last_name
        form.phone.data = _user.phone
        form.town.data = _user.town
        form.position.data = _user.position
        form.is_superuser.data = _user.is_superuser

    return render_template('forms/edit_user.jinja2', form=form)



# TODO Add edit user profile form, for superuser add possibility to see all users and manage them
