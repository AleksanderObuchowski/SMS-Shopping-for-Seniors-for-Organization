from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from zakupy_dla_seniora.config import Config

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


def create_app(config_class=Config):
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(Config)

    register_blueprints(app)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    return app
