from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import current_user

messages = Blueprint('messages', __name__)

@messages.route('example_name')
def example_name():
    pass