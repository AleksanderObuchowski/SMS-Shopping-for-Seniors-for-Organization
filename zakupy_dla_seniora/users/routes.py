from flask import Blueprint, render_template, flash, redirect, request, url_for, abort
from flask_login import current_user
from flask_babel import _

from zakupy_dla_seniora import bcrypt
from zakupy_dla_seniora.auth.functions import employee_role_required, superuser_role_required
from zakupy_dla_seniora.messages.models import Message
from zakupy_dla_seniora.users.functions import random_password
from zakupy_dla_seniora.users.forms import AddUserForm, EditUserForm
from zakupy_dla_seniora.users.models import User
from zakupy_dla_seniora.organisations.models import Organisation

users = Blueprint('users', __name__, url_prefix='/<lang_code>')


@users.route('/users')
@employee_role_required
def show_all():
    if current_user.is_employee:
        data = User.get_all_for_organisation(current_user.organisation_id)
    else:
        data = User.get_all()
    data_list = [user.to_dict_view_all_users() for user in data]
    [user.update(Organisation=Organisation.get_name_by_id(user['Organisation'])) for user in data_list]
    if 'msg' in request.args:
        return render_template('users/show_users.jinja2', data=data_list, columns=data_list[0].keys(),
                               msg=request.args['msg'])
    return render_template('users/show_users.jinja2', data=data_list, columns=data_list[0].keys())


@users.route('/users/<user_id>')
@employee_role_required
def show(user_id):
    user = User.get_by_id(user_id)
    if not user:
        abort(404)
    return render_template('users/show_users.jinja2', user=user)


@users.route('/profile')
@users.route('/profile/<user_id>')
def profile(user_id=None):
    if not user_id:
        user_id = current_user.id

    messages = Message.get_user_messages(user_id)
    user = User.get_by_id(user_id).to_dict_view_user()
    user[_('Organisation')] = Organisation.get_name_by_id(user[_('Organisation')])
    if not user:
        abort(404)
    return render_template('users/view_user_profile.jinja2', user=user, messages=messages)


@users.route('/user/add', methods=['GET', 'POST'])
@employee_role_required
def add_user():
    if current_user.is_superuser:
        organisations = [
            (org_id, name) for org_id, name in Organisation.query.with_entities(
                Organisation.id, Organisation.name
            ).all()
        ]
    else:
        organisations = [(current_user.organisation_id, Organisation.get_name_by_id(current_user.organisation_id))]
    form = AddUserForm()
    form.organisation.choices = organisations

    if request.method == "POST":
        if not form.organisation.data:
            form.organisation.data = current_user.organisation_id
        if not form.is_superuser.data:
            form.is_superuser.data = 'No'
        if form.validate_on_submit():
            password = random_password()
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user = User(password_hash=hashed_password, created_by=current_user.id, **form.to_dict())
            user.save()
            msg = f"{_('User')} {user.username} {_('has been successfully added')}."
            return redirect(url_for('users.add_user', msg=msg))
        else:
            print(form.errors)
    if 'msg' in request.args:
        return render_template('users/add_user.jinja2', form=form, message=request.args['msg'], success=True)
    return render_template('users/add_user.jinja2', form=form)


@users.route('/user/delete/<user_id>')
@employee_role_required
def delete_user(user_id):
    user = User.get_by_id(user_id)
    msg = f"{_('User')} {user.first_name} {user.last_name} ({user.username}) {_('has been deleted')}."
    user.delete()
    return redirect(url_for('users.show_all', msg=msg))


@users.route('/users/edit', methods=['GET', 'POST'])
@users.route('/users/edit/<user_id>', methods=['GET', 'POST'])
@employee_role_required
def edit_user(user_id):
    user = User.get_by_id(user_id)
    form = EditUserForm(obj=user)
    if form.validate_on_submit() and request.method == "POST":
        user.edit(**form.to_dict())
        user.save()
        msg = _('All changes were successfully saved.')
        return redirect(url_for('users.edit_user', user_id=user.id, msg=msg))
    if 'msg' in request.args:
        return render_template('users/edit_user_profile.jinja2', form=form, user=user, msg=request.args['msg'],
                               success=True)
    return render_template('users/edit_user_profile.jinja2', form=form, user=user)
