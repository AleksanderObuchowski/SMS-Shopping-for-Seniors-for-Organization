from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from flask_babel import _

from zakupy_dla_seniora import bcrypt
from zakupy_dla_seniora.auth.functions import employee_role_required
from zakupy_dla_seniora.organisations.models import Organisation
from zakupy_dla_seniora.users.functions import random_password
from zakupy_dla_seniora.volunteers.forms import AddVolunteerForm, EditVolunteerForm
from zakupy_dla_seniora.users.models import User

volunteers = Blueprint('volunteers', __name__, url_prefix='/<lang_code>')


@volunteers.route('/volunteer/new', methods=['GET', 'POST'])
@employee_role_required
def add_volunteer():
    """
    Decides whether user is superuser or regular employee. Based on that fills Select Field for organisations with
    possible options. Superuser should be able to add Volunteer to all organisations, where Organisation should
    be able to add Volunteer only to itself.
    If function detects POST request and form is valid, then generates random password for the Volunteer and
    adds the record to database.
    In other case, if method is GET or form is not valid, renders add_volunteer.jinja2 template again.

    TODO Send password through email to a Volunteer with a link to change it.
    """
    if current_user.is_superuser:
        organisations = [
            (org_id, name) for org_id, name in Organisation.query.with_entities(
                Organisation.id, Organisation.name
            ).all()
        ]
    else:
        organisations = [(current_user.organisation_id, Organisation.get_name_by_id(current_user.organisation_id))]

    form = AddVolunteerForm()
    form.organisation.choices = organisations

    if request.method == 'POST' and form.validate_on_submit():
        passwd = random_password()
        ph = bcrypt.generate_password_hash(passwd).decode('utf-8')
        vol = User(username=form.username.data, email=form.email.data, organisation_id=form.organisation.data,
                   password_hash=ph)
        vol.edit_volunteer(**form.to_dict_edit())
        vol.save()
        print("Dodano wolontariusza: ", form.first_name, " ", form.last_name, " Hasło: ", passwd)
        msg = _('The volunteer was successfully created.')
        return redirect(url_for('volunteers.show_all', msg=msg))
    if 'msg' in request.args:
        return render_template('volunteers/add_volunteer.jinja2', form=form, msg=request.args['msg'], success=True)
    return render_template('volunteers/add_volunteer.jinja2', form=form)


@volunteers.route('/volunteers')
@employee_role_required
def show_all():
    """
    For hackathon purposes gets all volunteers in database at once. Not very efficient solution for production.
    TODO Paginate request so it won't take all volunteers at once, rather serve them in "packages"

    :returns All Volunteers for superuser and Organisation specific Volunteers for organisation employee.
    """
    data = User.get_all_volunteers_as_dict()
    if 'msg' in request.args:
        return render_template('volunteers/show_volunteers.jinja2', volunteers=data, columns=data[0].keys(),
                               msg=request.args['msg'])
    return render_template('volunteers/show_volunteers.jinja2', volunteers=data, columns=data[0].keys())


@volunteers.route('/volunteer')
@volunteers.route('/volunteer/<volunteer_id>')
@login_required
def show(volunteer_id=None):
    """
    Show specific volunteer.
    :param volunteer_id:
    :return volunteer profile template or access denied template:
    """
    volunteer = User.get_by_id(volunteer_id)
    if not volunteer:
        abort(404)
    return render_template('volunteers/view_volunteer_profile.jinja2', volunteer=volunteer)


@volunteers.route('/volunteer/edit')
@volunteers.route('/volunteer/edit/<volunteer_id>', methods=["GET", "POST"])
@login_required
def edit(volunteer_id):
    """
    Renders volunteer profile edit page. If volunteer tries to edit other volunteer profile, his own profile is
    rendered instead. If organisation employee tries to edit a profile of volunteer outside his own organisation, an
    error page is returned.
    In other case form is properly rendered, pre-filled with known data. Then saved if properly filled.
    :param volunteer_id:
    :return Volunteer profile edit page or board view on success or 401 on access denied:
    """
    volunteer_id = volunteer_id if volunteer_id else current_user.id
    if not current_user.is_superuser and not current_user.is_employee:
        return redirect(url_for('volunteers.edit', volunteer_id=current_user.id))
    elif current_user.is_employee:
        volunteer = User.get_by_id(volunteer_id)
        if volunteer.organisation_id != current_user.organisation_id or volunteer.is_superuser:
            abort(401)

    # Initially fill form
    volunteer = User.get_by_id(volunteer_id)
    if not volunteer:
        abort(404)

    form = EditVolunteerForm(obj=volunteer)
    if request.method == "POST" and form.validate_on_submit():
        volunteer.edit_volunteer(**form.to_dict())
        volunteer.save()
        msg = _('All changes saved.')
        return redirect(url_for('volunteers.edit', volunteer_id=volunteer.id, msg=msg))
    if 'msg' in request.args:
        return render_template('volunteers/edit_volunteer.jinja2', form=form, volunteer=volunteer,
                               msg=request.args['msg'], success=True)
    return render_template('volunteers/edit_volunteer.jinja2', form=form, volunteer=volunteer)


@volunteers.route('/volunteer/delete/<volunteer_id>')
@employee_role_required
def delete(volunteer_id):
    """
    Deletes given Volunteer based on permissions
    :param volunteer_id:
    :return redirect to board.view:
    """
    volunteer = User.get_by_id(volunteer_id)
    if current_user.is_employee:
        if volunteer.organisation_id != current_user.organisation_id:
            abort(401)

    volunteer.delete()
    msg = f"{_('Volunteer')} {volunteer.username} {_('was successfully deleted')}."
    return redirect(url_for('volunteers.show_all', msg=msg))
