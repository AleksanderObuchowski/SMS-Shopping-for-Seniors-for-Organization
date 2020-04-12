from flask import Blueprint, render_template
from zakupy_dla_seniora.auth.functions import admin_role_required
from flask_login import current_user


volunteers = Blueprint('volunteers', __name__)


@volunteers.route('/volunteer/add', methods=['GET', 'POST'])
@admin_role_required
def add_volunteers():
    return render_template('forms/add_volunteer.jinja2', user=current_user)


@volunteers.route('/volunteers')
@admin_role_required
def show_volunteers():
    pass

