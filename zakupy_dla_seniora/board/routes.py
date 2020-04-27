from flask import Blueprint, render_template
from flask_login import current_user, login_required

from zakupy_dla_seniora.messages.models import Message

board = Blueprint('board', __name__, url_prefix='/<lang_code>')


@board.route('/board')
@login_required
def view():
    messages = Message.get_received()
    print(current_user)
    return render_template('board.jinja2', user=current_user, messages=messages)
