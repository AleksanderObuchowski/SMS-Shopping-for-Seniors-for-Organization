from flask import Blueprint, request, url_for, redirect, render_template, flash
from flask_login import current_user, login_user, login_required, logout_user
from zakupy_dla_seniora import bcrypt
from zakupy_dla_seniora.auth.forms import LoginForm, RegistrationForm
from zakupy_dla_seniora.auth.functions import admin_role_required
from zakupy_dla_seniora.users.models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
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
            error_message = "Wrong username or password."
            return render_template('forms/login.jinja2', message=error_message, form=form)
    else:
        return render_template('forms/login.jinja2', form=form)


@auth.route('/register-account', methods=['GET', 'POST'])
@admin_role_required
def register_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, organisation=form.organisation.data,
                    password_hash=hashed_password, created_by=current_user.id, is_superuser=form.superuser.data)
        user.save()
        flash('Konto zostało utworzone pomyślnie.', 'success')
        return redirect(url_for('board.view'))
    return render_template('forms/register-account.jinja2', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
