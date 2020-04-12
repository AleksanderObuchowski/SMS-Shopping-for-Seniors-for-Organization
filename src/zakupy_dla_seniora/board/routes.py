from flask import Blueprint, render_template
from flask_login import current_user, login_required

board = Blueprint('board', __name__)


@board.route('/board')
@board.route('/board/<title>')
@login_required
def view(title=None):
    return render_template('board.jinja2', user=current_user, data={'data': []})
