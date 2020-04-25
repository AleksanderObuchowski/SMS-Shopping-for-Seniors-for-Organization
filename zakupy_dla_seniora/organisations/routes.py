from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import current_user
from zakupy_dla_seniora.auth.functions import superuser_role_required, employee_role_required
from zakupy_dla_seniora.organisations.forms import AddOrganisationForm, EditOrganisationForm
from zakupy_dla_seniora.organisations.models import Organisations
from zakupy_dla_seniora.organisations.functions import get_organisation_name

from flask_babel import _

organisations = Blueprint('organisations', __name__, url_prefix='/<lang_code>')


@organisations.route('/organisation')
def organisation():
    org = Organisations.get_by_id(current_user.organisation_id)
    print(org)
    return render_template('view_organisation.jinja2', org=org)


@organisations.route('/add-new-organisation', methods=['GET', 'POST'])
@superuser_role_required
def add_organisation():
    form = AddOrganisationForm()
    if form.validate_on_submit():
        org = Organisations(name=form.name.data, added_by=current_user.id)
        org.save()
        flash(_('New organisation has been added successfully.'), 'success')
        return redirect(url_for('board.view'))
    return render_template('forms/add_organisation.jinja2', form=form)


@organisations.route('/all-organisations', methods=['GET'])
@superuser_role_required
def get_all_organisations():
    # TODO Optimize query, paginate it (see pagination for SQLAlchemy)
    # TODO Add more organisations management tools (delete, update, create)
    orgs = Organisations.query.all()
    return render_template('all_organisations.jinja2', organisations=orgs)


@organisations.route('/<name>/edit', methods=['GET', 'POST'])
@employee_role_required
def edit_organisation(name):
    org = Organisations.query.filter_by(name=name).first()
    form = EditOrganisationForm()
    if request.method == 'POST' and form.validate_on_submit():
        org.contact_phone = form.contact_phone.data
        org.contact_email = form.contact_email.data
        org.town = form.town.data
        org.postal_code = form.postal_code.data
        org.address = form.address.data
        org.website = form.website.data
        org.save()
        flash(_('Organisation data has been updated successfully'), 'success')
        return redirect(url_for('organisation', name=org.name))
    return render_template('forms/edit_organisation.jinja2', organisation=org, form=form)
