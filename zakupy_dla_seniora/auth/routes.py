from flask import Blueprint, request, url_for, redirect, render_template
from flask_login import current_user, login_user, login_required, logout_user
from flask_babel import _

from zakupy_dla_seniora import bcrypt
from zakupy_dla_seniora.auth.forms import LoginForm
from zakupy_dla_seniora.users.models import User


auth = Blueprint('auth', __name__, url_prefix='/<lang_code>')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # TODO Add "Login As" field in login template to login as employee or volunteer
    # TODO Bonus feature, save choice in cookies for ease of access
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('board.view'))
    elif request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.login.data).first()
        if not user:
            user = User.query.filter_by(email=form.login.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            if not user.is_active:
                login_user(user, force=True)
                # TODO redirect to change password with next_page
            else:
                login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('board.view'))
        else:
            error_message = _("Wrong username or password.")
            return render_template('auth.jinja2', message=error_message, form=form)
    else:
        return render_template('auth.jinja2', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('landing.landing_view'))


