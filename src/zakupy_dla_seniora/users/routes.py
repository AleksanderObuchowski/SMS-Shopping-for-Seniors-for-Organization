from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_user, current_user, logout_user, login_required
from zakupy_dla_seniora import bcrypt
from zakupy_dla_seniora.placings.models import Placings
from zakupy_dla_seniora.sms_handler.models import Messages
from zakupy_dla_seniora.users.models import User

users = Blueprint('users', __name__)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.board'))
    if request.method == 'POST':
        user = User.query.filter_by(display_name=request.form['username']).first()
        if user and bcrypt.check_password_hash(user.password_hash, request.form['password']):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.board'))
        else:
            error_message = "Wrong username or password."
            return render_template('login.html', title='Login', message=error_message)
    return render_template('login.html', title='Login')


@users.route('/register', methods=['GET', 'POST'])
def register_user():
    error_message = None
    if current_user.is_authenticated:
        return redirect(url_for('main.board'))
    if request.method == 'POST':
        if request.form['password'] == request.form['password_again']:
            hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        else:
            error_message = 'Passwords not match'
            return render_template('register.html', title='Register', message=error_message)
        User(display_name=request.form['username'], email=request.form['email'], password=hashed_password).save()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', message=error_message)


@users.route('/profile')
@login_required
def profile():
    user = User.query.filter(User.id == current_user.id).first()
    if user:
        placings = Placings.query.filter(Placings.user_id == current_user.id).all()
        data = {
            "name": user.display_name,
            "points": user.points,
            "placings": []
        }
        placings = [placing.prepare_board_view() for placing in placings]
        for placing in placings:
            info = Messages.query.filter(Messages.id == placing['message_id']).first().prepare_profile_view()
            info['placing_status'] = placing['placing_status']
            data['placings'].append(info)
        return render_template('profile.html', data=data)
    else:
        return render_template('error_templates/user_not_found.html')


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.board'))
