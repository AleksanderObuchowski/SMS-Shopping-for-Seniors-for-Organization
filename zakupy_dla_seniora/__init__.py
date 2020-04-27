from flask import abort, Flask, redirect, request, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from zakupy_dla_seniora.config import Config
from flask_babel import Babel
from flask import session
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


def register_blueprints(app):
    from zakupy_dla_seniora.board.routes import board
    app.register_blueprint(board)

    from zakupy_dla_seniora.auth.routes import auth
    app.register_blueprint(auth)

    from zakupy_dla_seniora.volunteers.routes import volunteers
    app.register_blueprint(volunteers)

    from zakupy_dla_seniora.users.routes import users
    app.register_blueprint(users)

    from zakupy_dla_seniora.organisations.routes import organisations
    app.register_blueprint(organisations)

    from zakupy_dla_seniora.landing.routes import landing
    app.register_blueprint(landing)

    from zakupy_dla_seniora.messages.routes import messages
    app.register_blueprint(messages)


def register_error_handlers(app):
    from zakupy_dla_seniora.errors.resources import unauthorized, page_not_found, server_internal
    app.register_error_handler(401, unauthorized)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, server_internal)


def create_app(config_class=Config):
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(Config)
    app.url_map.strict_slashes = False

    # translations
    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        lang = request.path[1:].split('/', 1)[0]
        if lang in app.config['LANGUAGES']:
            return lang
        else:
            return 'en'

    # @babel.localeselector
    # def get_locale():
    #     if request.args.get('lang_code'):
    #         session['lang_code'] = request.args.get('lang_code')
    #     return session.get('lang_code', 'en')

    @app.url_defaults
    def set_language_code(endpoint, values):
        if app.url_map.is_endpoint_expecting(endpoint, 'lang_code'):
            values['lang_code'] = g.lang_code

    @app.url_value_preprocessor
    def get_lang_code(endpoint, values):
        if values is not None:
            g.lang_code = values.pop('lang_code', None)

    @app.before_request
    def ensure_lang_support():
        lang_code = g.get('lang_code')
        if not lang_code:
            g.lang_code = 'en'
        else:
            if lang_code not in app.config['LANGUAGES']:
                if len(g.lang_code) <= 3:
                    g.lang_code = 'en'
                else:
                    g.lang_code = 'en'
                    abort(404)

    register_blueprints(app)
    register_error_handlers(app)
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    return app
