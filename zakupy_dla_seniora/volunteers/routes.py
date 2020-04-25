from flask import Blueprint, render_template, request, redirect, url_for

from zakupy_dla_seniora import bcrypt
from zakupy_dla_seniora.auth.functions import employee_role_required
from flask_login import current_user, login_required
from zakupy_dla_seniora.organisations.models import Organisations
from zakupy_dla_seniora.users.functions import random_password
from zakupy_dla_seniora.volunteers.forms import AddVolunteerForm
from zakupy_dla_seniora.volunteers.models import Volunteers

volunteers = Blueprint('volunteers', __name__)


@volunteers.route('/volunteer/new', methods=['GET', 'POST'])
@employee_role_required
def add_volunteer():
    choices = [Organisations.query.with_entities(Organisations.id, Organisations.name).all()]
    form = AddVolunteerForm()
    form.organisation.choices = choices
    if request.method == 'POST' and form.validate_on_submit():
        if current_user.is_employee:
            org_id = current_user.organisation_id
        elif form.organisation.data:
            org_id = Organisations.get_id_by_name(form.organisation.data)
            if not org_id:
                error_message = "Nie znaleziono takiej organizacji"
                return render_template('forms/add_volunteer.jinja2', form=form, message=error_message)
        else:
            error_message = "Podaj organizację"
            return render_template('forms/add_volunteer.jinja2', form=form, message=error_message)
        passwd = random_password()
        ph = bcrypt.generate_password_hash(passwd).decode('utf-8')
        vol = Volunteers(first_name=form.first_name.data, last_name=form.last_name.data,
                         phone=form.phone_number.data, email=form.email.data, org_id=org_id,
                         town=form.town.data, distr=form.district.data, pass_hash=ph,
                         created_by=current_user.id)
        vol.save()
        print("Dodano wolontariusza: ", form.first_name, " ", form.last_name, " Hasło: ", passwd)
        return redirect(url_for('volunteers.show_all'))
    return render_template('forms/add_volunteer.jinja2', form=form)


# Show volunteers for a given organisation
# For superuser show all volunteers
@volunteers.route('/volunteers')
@employee_role_required
def show_all():
    if current_user.is_employee:
        data = Volunteers.get_all_for_organisation(current_user.organisation_id)
    else:
        data = Volunteers.get_all()
    return render_template('show_volunteers.jinja2', data=data)


# volunteer can only see his profile
# employee can see all volunteers belonging to his organization
# superuser can see all volunteers
@volunteers.route('/volunteers/<id>')
@login_required
def show(id):
    if current_user.is_superuser:
        v = Volunteers.get_one(id)
        return render_template('view_volunteer_profile.jinja2', volunteer=v)
    elif current_user.is_employee:
        v = Volunteers.get_one(id, current_user.organisation_id)
        if not v:
            error_message = "Nie znaleziono wolontariusza w Twojej organizacji."
        else:
            return render_template('view_volunteer_profile.jinja2', volunteer=v)
    else:
        v = Volunteers.get_one(id, current_user.organisation_id)
        if not v:
            return redirect(url_for('board.view'))
        else:
            return render_template('view_volunteer_profile.jinja2', volunteer=v)
