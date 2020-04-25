from flask import Blueprint, render_template
from flask_login import current_user, login_required

from zakupy_dla_seniora.messages.models import Messages

board = Blueprint('board', __name__)


@board.route('/board')
@board.route('/board/<title>')
@login_required
def view(title=None):
    messages = Messages.get_received()

    return render_template('board.jinja2', user=current_user, messages = messages)
