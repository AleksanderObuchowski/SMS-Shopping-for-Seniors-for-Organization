from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import current_user
from zakupy_dla_seniora.messages.forms import AddMessagesForm
from zakupy_dla_seniora.messages.models import Messages
from zakupy_dla_seniora.messages.functions import get_location, conversation
from zakupy_dla_seniora.config import twilio_sid, twilio_auth_token, twilio_phone

from twilio.rest import Client

client = Client(twilio_sid, twilio_auth_token)
messages = Blueprint('messages', __name__, url_prefix='/<lang_code>')


@messages.route('/add_message', methods=['GET', 'POST'], )
def add_message():
    form = AddMessagesForm()
    if request.method == 'POST' and form.validate_on_submit():
        _, lat, lon = get_location(form.location.data, search=False)
        message = Messages(content=form.content.data, contact_number=form.contact_number.data,
                           location=form.location.data,
                           latitude=lat, longitude=lon, status='received', created_by=current_user.id)
        message.save()
        print("Dodano Wiadomość")
        return render_template('messages/add_message.jinja2', form=form, message='Message created successfully!')
    else:
        form = AddMessagesForm()
        return render_template('messages/add_message.jinja2', form=form)


@messages.route('/take_message/<id>', methods=['GET'])
def take_message(id):
    message = Messages.get_by_id(id)
    message.status = 'taken'
    message.volunteer_id = current_user.id
    message.save()
    client.messages.create(
        to=message.contact_number,
        from_=twilio_phone,
        body='Someone volunteered to take your order, please give us detailed location'
    )

    return redirect(url_for('users.profile'))


@messages.route('/end_message/<id>', methods=['GET'])
def end_message(id):
    message = Messages.get_by_id(id)
    message.status = 'waiting for feedback'
    message.save()
    client.messages.create(
        to=message.contact_number,
        from_=twilio_phone,
        body='Volunteer marked your order as finish. Did everything go well? Respond "ok" if yes. If something was wrong tell us about it'
    )

    return redirect(url_for('users.profile'))


@messages.route('/receive_sms', methods=['POST'])
def receive_sms():
    phone_number = request.values['From']
    content = request.values['Body']

    last_message = Messages.get_by_phone(phone_number)
    result, status = conversation(last_message=last_message, content=content, phone_number=phone_number)
    client.messages.create(
        to=phone_number,
        from_=twilio_phone,
        body=result['response']
    )


@messages.route('/error_messages', methods=['GET'])
def error_messages():
    messages = Messages.get_errors()
    return render_template('messages/error_messages.jinja2', messages=messages)
