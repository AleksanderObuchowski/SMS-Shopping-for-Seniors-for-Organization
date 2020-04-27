from flask import render_template


def unauthorized(error):
    return render_template('errors/unauthorized.jinja2', error=str(error))


def page_not_found(error):
    return render_template('errors/page_not_found.jinja2', error=str(error))


def server_internal(error):
    return render_template('errors/server_internal.jinja2', error=str(error))
