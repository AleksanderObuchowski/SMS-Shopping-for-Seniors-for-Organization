from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import current_user
from flask_babel import _

from zakupy_dla_seniora.auth.functions import superuser_role_required, employee_role_required
from zakupy_dla_seniora.organisations.forms import AddOrganisationForm, EditOrganisationForm
from zakupy_dla_seniora.organisations.models import Organisations
from zakupy_dla_seniora.organisations.functions import get_organisation_name


organisations = Blueprint('organisations', __name__, url_prefix='/<lang_code>')


@organisations.route('/organisation')
@organisations.route('/organisation/<org_id>')
def organisation(org_id=None):
    org = Organisations.get_by_id(org_id).to_dict_view_organisation()
    name = org.pop('Name')
    employees = org.pop('Employees')
    volunteers = org.pop('Volunteers')
    return render_template('view_organisation.jinja2', org=org, name=name, employees=employees,
                           volunteers=volunteers)


@organisations.route('/organisations', methods=['GET'])
@superuser_role_required
def get_all_organisations():
    orgs = Organisations.query.all()
    orgs = [org.to_dict_view_all_organisations() for org in orgs]
    return render_template('all_organisations.jinja2', organisations=orgs, columns=orgs[0].keys())


@organisations.route('/organisation/add', methods=['GET', 'POST'])
@superuser_role_required
def add_organisation():
    form = AddOrganisationForm()
    if request.method == 'POST' and form.validate_on_submit():
        if not Organisations.get_by_name(form.name.data):
            org = Organisations(**form.to_dict(), added_by=current_user.id)
            org.save()
            return redirect(url_for('organisations.add_organisation', msg=f'Organizacja {org.name} została dodana.'))
        else:
            msg = f"{_('Name')} {form.name.data} {_('is already taken.')}."
            return render_template('forms/add_organisation.jinja2', form=form,
                                   msg=msg)
    if 'msg' not in request.args:
        return render_template('forms/add_organisation.jinja2', form=form)
    return render_template('forms/add_organisation.jinja2', form=form,
                           msg=request.args['msg'], success=True)


@organisations.route('/organisation/edit/', methods=['GET', 'POST'])
@organisations.route('/organisation/edit/<org_id>', methods=['GET', 'POST'])
@employee_role_required
def edit_organisation(org_id=None):
    org = Organisations.get_by_id(org_id)
    form = EditOrganisationForm(obj=org)
    if request.method == 'POST' and form.validate_on_submit():
        org.edit(**form.to_dict())
        org.save()
        return redirect(url_for('organisations.edit_organisation', org_id=org_id,
                                msg=_('Changes were successfully saved.')))
    if 'msg' not in request.args:
        return render_template('forms/edit_organisation.jinja2', organisation=org, form=form)
    return render_template('forms/edit_organisation.jinja2', organisation=org, form=form,
                           msg=request.args['msg'], success=True)
