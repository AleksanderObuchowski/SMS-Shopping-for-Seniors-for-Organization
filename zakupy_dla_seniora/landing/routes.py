from flask import Blueprint, g, redirect, render_template, request, url_for

from zakupy_dla_seniora import config

landing = Blueprint('landing', __name__)


@landing.route('/<lang_code>/', methods=['GET'])
def landing_view():
    return render_template('landing.jinja2')


@landing.route('/', methods=['GET'])
def switch_view():
    local_lang = request.accept_languages.best_match(config.Config.LANGUAGES)
    return redirect(url_for('landing.landing_view', lang_code=local_lang))
