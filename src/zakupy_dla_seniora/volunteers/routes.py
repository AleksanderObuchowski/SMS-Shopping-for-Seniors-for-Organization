from flask import Blueprint, url_for, render_template, request, flash
from zakupy_dla_seniora.auth.functions import admin_role_required
from flask_login import current_user
from zakupy_dla_seniora.users.models import User, db
from random import SystemRandom
import string
from sqlalchemy.exc import IntegrityError


volunteers = Blueprint('volunteers', __name__)


@volunteers.route('/volunteer/add', methods=['GET', 'POST'])
@admin_role_required
def add_volunteers():
    fields = [
        ('Imie', 'first_name', 'Jan', 'text'),
        ('Nazwisko', 'last_name', 'Kowalski', 'text'),
        ('Email', 'email', 'jan@kowalski.pl', 'email'),
        ('Telefon', 'phone', '123 456 789', 'tel'),
        ('Lokalizacja', 'localization', 'Gdańsk Zaspa', 'text')
    ]
    if request.method == 'POST':
        form = request.form
        name = form['email']
        pwd_length = 8
        password = ''.join(SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(pwd_length))
        try:
            new_user = User(display_name=name, email=form['email'], password=password, created_by=current_user.id)
            new_user.save()
            return render_template('add_volunteer.jinja2', fields=fields, super_user=current_user.super_user,
                                   message='Użytkownik został dodany.', error=False)
        except IntegrityError:
            db.session.rollback()
            return render_template('add_volunteer.jinja2', fields=fields, super_user=current_user.super_user,
                                   message='Istnieje już użytkownik posługujący się tym adresem email lub numerem '
                                           'telefonu.', error=True)

    return render_template('add_volunteer.jinja2', fields=fields, super_user=current_user.super_user)


@volunteers.route('/volunteers')
@admin_role_required
def show_volunteers():
    pass

