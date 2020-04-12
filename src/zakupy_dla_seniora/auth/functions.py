from functools import wraps
from flask import current_app, request
from flask_login.config import EXEMPT_METHODS
from flask_login import current_user


def admin_role_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.config.get('LOGIN_DISABLED'):
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        elif not current_user.is_employee and not current_user.is_superuser:
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)

    return decorated_view


def superuser_role_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.config.get('LOGIN_DISABLED'):
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        elif not current_user.is_superuser:
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)

    return decorated_view
