from flask import Blueprint, request, url_for, redirect, render_template, flash
from flask_login import current_user, login_user, login_required, logout_user

landing = Blueprint('landing', __name__)

@landing.route('/', methods=['GET'])
def landing_view():
        return render_template('landing.jinja2')