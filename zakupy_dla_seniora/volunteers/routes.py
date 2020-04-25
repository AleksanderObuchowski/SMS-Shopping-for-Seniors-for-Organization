from flask import Blueprint, render_template, request, redirect, url_for
from zakupy_dla_seniora import bcrypt
from zakupy_dla_seniora.auth.functions import employee_role_required
from flask_login import current_user, login_required
from zakupy_dla_seniora.organisations.models import Organisations
from zakupy_dla_seniora.users.functions import random_password
from zakupy_dla_seniora.volunteers.forms import AddVolunteerForm, EditVolunteerForm
from zakupy_dla_seniora.volunteers.models import Volunteers

volunteers = Blueprint('volunteers', __name__)


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
    return render_template('forms/add_volunteer.jinja2', form=form)


@volunteers.route('/volunteers')
@employee_role_required
def show_all():
    """
    For hackathon purposes gets all volunteers in database at once. Not very efficient solution for production.
    TODO Paginate request so it won't take all volunteers at once, rather serve them in "packages"

    :returns All Volunteers for superuser and Organisation specific Volunteers for organisation employee.
    """
    if current_user.is_employee:
        data = Volunteers.get_all_for_organisation(current_user.organisation_id)
    else:
        data = Volunteers.get_all()
    return render_template('show_volunteers.jinja2', data=data)


@volunteers.route('/volunteer/<volunteer_id>')
@login_required
def show(volunteer_id):
    """
    :param volunteer_id:
    :return volunteer profile template or access denied template:
    """
    v = Volunteers.get_by_id(volunteer_id)
    if v:
        return render_template('view_volunteer_profile.jinja2', volunteer=v)
    return render_template('error_pages/access_denied.jinja2')


@volunteers.route('/volunteer/<volunteer_id>/edit', methods=["GET", "POST"])
@login_required
def edit(volunteer_id):
    form = EditVolunteerForm()
    return render_template('forms/edit_volunteer.jinja2', form=form)

# TODO Edit Volunteer, delete Volunteer
