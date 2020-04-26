from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from zakupy_dla_seniora import bcrypt
from zakupy_dla_seniora.auth.functions import employee_role_required
from flask_login import current_user, login_required
from zakupy_dla_seniora.organisations.models import Organisations
from zakupy_dla_seniora.users.functions import random_password
from zakupy_dla_seniora.volunteers.forms import AddVolunteerForm, EditVolunteerForm
from zakupy_dla_seniora.volunteers.models import Volunteers

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
            (org_id, name) for org_id, name in Organisations.query.with_entities(
                Organisations.id, Organisations.name
            ).all()
        ]
    else:
        organisations = (current_user.organisation_id, Organisations.get_name_by_id(current_user.id))

    form = AddVolunteerForm()
    form.organisation.choices = organisations
    print(form.organisation.data)
    if request.method == 'POST' and form.validate_on_submit():
        passwd = random_password()
        ph = bcrypt.generate_password_hash(passwd).decode('utf-8')
        vol = Volunteers(first_name=form.first_name.data, last_name=form.last_name.data,
                         phone=form.phone_number.data, email=form.email.data, org_id=form.organisation.data,
                         town=form.town.data, distr=form.district.data, pass_hash=ph,
                         created_by=current_user.id)
        vol.save()
        print("Dodano wolontariusza: ", form.first_name, " ", form.last_name, " Hasło: ", passwd)
        return redirect(url_for('volunteers.show_all'))
    return render_template('volunteers/add_volunteer.jinja2', form=form)


@volunteers.route('/volunteers')
@employee_role_required
def show_all():
    """
    For hackathon purposes gets all volunteers in database at once. Not very efficient solution for production.
    TODO Paginate request so it won't take all volunteers at once, rather serve them in "packages"

    :returns All Volunteers for superuser and Organisation specific Volunteers for organisation employee.
    """
    if current_user.is_employee:
        data = Volunteers.get_all_as_dict(current_user.organisation_id)
    else:
        data = Volunteers.get_all_as_dict()
    columns = Volunteers.get_columns()
    return render_template('volunteers/show_volunteers.jinja2', volunteers=data, columns=columns)


@volunteers.route('/volunteer/<volunteer_id>')
@login_required
def show(volunteer_id):
    """
    Show specific volunteer.
    :param volunteer_id:
    :return volunteer profile template or access denied template:
    """
    v = Volunteers.get_by_id(volunteer_id)
    return render_template('volunteers/view_volunteer_profile.jinja2', volunteer=v)


@volunteers.route('/volunteer/<volunteer_id>/edit', methods=["GET", "POST"])
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
    if not current_user.is_superuser or not current_user.is_employee:
        if volunteer_id != current_user.id:
            return redirect(url_for('volunteers.edit', volunteer_id=current_user.id))
    elif current_user.is_employee:
        v = Volunteers.get_by_id(volunteer_id)
        if v.organisation_id != current_user.organisation_id:
            abort(401)

    # Initially fill form
    v = Volunteers.get_by_id(volunteer_id)
    form = EditVolunteerForm()

    if request.method == "POST" and form.validate_on_submit():
        v.username = form.username.data
        v.first_name = form.first_name.data
        v.last_name = form.last_name.data
        v.phone_number = form.phone_number.data
        v.email = form.email.data
        v.town = form.town.data
        v.district = form.district.data
        v.organisation_id = form.organisation.data
        v.is_active = form.is_active.data
        v.save()
        flash('Użytkownik został dodany!', 'success')
        return redirect(url_for('board.view'))

    elif request.method == "GET":
        form.username.data = v.username
        form.first_name.data = v.first_name
        form.last_name.data = v.last_name
        form.phone_number.data = v.phone_number
        form.email.data = v.email
        form.town.data = v.town
        form.district.data = v.district
        form.organisation.data = v.organisation_id
        form.is_active.data = v.is_active

    return render_template('volunteers/edit_volunteer.jinja2', form=form)


@volunteers.route('/volunteer/<volunteer_id>/delete')
@employee_role_required
def delete(volunteer_id):
    """
    Deletes given Volunteer based on permissions
    :param volunteer_id:
    :return redirect to board.view:
    """
    v = Volunteers.get_by_id(volunteer_id)
    if current_user.is_employee:
        if v.organisation_id != current_user.organisation_id:
            abort(401)

    v.delete()
    flash('Wolontariusz został usunięty z bazy', 'success')
    return redirect(url_for('board.view'))
