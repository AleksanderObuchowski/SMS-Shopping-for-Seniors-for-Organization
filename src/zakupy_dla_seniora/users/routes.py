from flask import Blueprint, render_template
from flask_login import current_user

users = Blueprint('users', __name__)


@users.route('/profile')
def profile():
    return render_template('view_user_profile.jinja2', user=current_user)
