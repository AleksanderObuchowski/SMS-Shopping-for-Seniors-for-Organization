from flask import Blueprint, render_template
from flask_login import current_user, login_required

main = Blueprint('main', __name__)


@main.route('/<title>')
def placeholder(title):
    return render_template('placeholder.jinja2', title=title)


@main.route('/board')
@login_required
def board():
    return render_template('newboard.jinja2', super_user=current_user.super_user)
