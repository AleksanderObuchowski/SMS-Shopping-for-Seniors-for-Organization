from flask import Blueprint, request, url_for, redirect, render_template, flash
from flask_login import current_user, login_user, login_required, logout_user
from zakupy_dla_seniora.users.models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.placeholder', title='Is Authenticated'))
    fields = [
        ('username', 'Nazwa Użytkownika', 'text'),
        ('password', '******', 'password')
    ]
    if request.method == 'POST':
        form = request.form
        user = User.query.filter_by(display_name=form['username']).first()
        if user and user.check_password(form['password']):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.board', title='Logged in'))
        else:
            error_message = "Wrong username or password."
            return render_template('login.jinja2', title='Login', message=error_message, fields=fields, logged_user = False)
    return render_template('login.jinja2', title='Login', fields=fields, logged_user = False)


@auth.route('/register', methods=['GET', 'POST'])
def register_user():
    error_message = None
    if current_user.is_authenticated:
        return redirect(url_for('main.placeholder', title='Is Authenticated'))
    fields = [
        ('username', 'Nazwa Użytkownika', 'text'),
        ('email', 'jan@kowalski.pl', 'email'),
        ('password', '******', 'password'),
        ('password_again', '******', 'password')
    ]
    if request.method == 'POST':
        form = request.form
        if form['password'] == form['password_again']:
            new_user = User(
                display_name=form['username'],
                email=form['email'],
                password=form['password']
            )
            new_user.save()
            flash('Your account has been created! You are now able to log in', 'success')
            login_user(new_user)
            return redirect(url_for('main.board', title='Registered'))
        error_message = 'Passwords do not match'
        return render_template('login.jinja2', title='Register', message=error_message, fields=fields)

    return render_template('login.jinja2', title='Register', message=error_message, fields=fields)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login', title='Logged out'))
