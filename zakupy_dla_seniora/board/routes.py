from flask import Blueprint, render_template
from flask_login import current_user, login_required

from zakupy_dla_seniora.messages.models import Messages


board = Blueprint('board', __name__, url_prefix='/<lang_code>')


@board.route('/board')
@login_required
def view():
    messages = Messages.get_received()
    return render_template('board.jinja2', user=current_user, messages = messages)