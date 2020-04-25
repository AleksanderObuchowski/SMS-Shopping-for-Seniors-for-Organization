from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import current_user
from zakupy_dla_seniora.messages.forms import AddMessagesForm
from zakupy_dla_seniora.messages.models import Messages
from zakupy_dla_seniora.messages.functions import get_location

messages = Blueprint('messages', __name__)


@messages.route('/add_message', methods=['GET', 'POST'])
def add_message():
    form = AddMessagesForm()
    if request.method == 'POST' and form.validate_on_submit():
        _, lat, lon = get_location(form.location.data, search=False)
        message = Messages(content=form.content.data, contact_number=form.contact_number.data, location=form.location.data,
                           latitude=lat, longtitude=lon,status='received',created_by=current_user.id)
        message.save()
        print("Dodano Wiadomość")
        return render_template('forms/add_message.jinja2', form=form,message='Message created successfully!')
    else:
        form = AddMessagesForm()
        return render_template('forms/add_message.jinja2', form=form)

@messages.route('/take_message/<id>', methods = ['GET'])
def take_message(id):
    message = Messages.get_by_id(id)
    message.status = 'taken'
    message.volunteer_id = current_user.id
    message.save()
    return redirect(url_for('users.profile'))


