from flask import render_template


def unauthorized(error):
    return render_template('errors/unauthorized.jinja2')


def page_not_found(error):
    return render_template('errors/page_not_found.jinja2')


def server_internal(error):
    return render_template('errors/server_internal.jinja2')