from flask import Blueprint, request, url_for, redirect, render_template, flash
from flask_login import current_user, login_user, login_required, logout_user
from zakupy_dla_seniora.user_models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.placeholder', title='Is Authenticated'))
    if request.method == 'POST':
        user = User.query.filter_by(display_name=request.form['username']).first()
        print(user)
        print(request.form['password'])
        print(user.check_password(request.form['password']))
        if user and user.check_password(request.form['password']):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.placeholder', title='Logged in'))
        else:
            error_message = "Wrong username or password."
            return render_template('login.html', title='Login', message=error_message)
    return render_template('login.html', title='Login')


@auth.route('/register', methods=['GET', 'POST'])
def register_user():
    error_message = None
    if current_user.is_authenticated:
        return redirect(url_for('main.placeholder', title='Is Authenticated'))
    if request.method == 'POST':
        if request.form['password'] == request.form['password_again']:
            User(
                display_name=request.form['username'],
                email=request.form['email'],
                password=request.form['password']
            ).save()
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('main.placeholder', title='Registered'))
        error_message = 'Passwords do not match'
        return render_template('register.html', title='Register', message=error_message)

    return render_template('register.html', title='Register', message=error_message)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.placeholder', title='Logged out'))

