from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import current_user
from flask_babel import _

from zakupy_dla_seniora.messages.forms import AddMessagesForm
from zakupy_dla_seniora.messages.models import Message
from zakupy_dla_seniora.messages.functions import get_location, conversation
from zakupy_dla_seniora.config import twilio_sid, twilio_auth_token, twilio_phone
from zakupy_dla_seniora.auth.functions import employee_role_required

from twilio.rest import Client

client = Client(twilio_sid, twilio_auth_token)
messages = Blueprint('messages', __name__, url_prefix='/<lang_code>')


@messages.route('/message/add', methods=['GET', 'POST'], )
def add_message():
    form = AddMessagesForm()
    if request.method == 'POST' and form.validate_on_submit():
        location, lat, lon = get_location(form.location.data, search=False)
        message = Message(content=form.content.data, contact_number=form.contact_number.data,
                          location=form.location.data,
                          latitude=lat, longitude=lon, status='received', created_by=current_user.id)
        message.save()
        msg = _('Message created successfully.')
        return redirect(url_for('messages.add_message', msg=msg))
    if 'msg' in request.args:
        return render_template('messages/add_message.jinja2', form=form, msg=request.args['msg'], success=True)
    return render_template('messages/add_message.jinja2', form=form)


@messages.route('/message/take/<message_id>', methods=['GET'])
def take_message(message_id):
    message = Message.get_by_id(message_id)
    message.status = 'taken'
    message.user_id = current_user.id
    message.save()
    try:
        client.messages.create(
            to=message.contact_number,
            from_=twilio_phone,
            body='Someone volunteered to take your order, please give us detailed location'
        )
    except:
        pass
    return redirect(url_for('users.profile'))


@messages.route('/message/end/<message_id>', methods=['GET'])
def end_message(message_id):
    message = Message.get_by_id(message_id)
    message.status = 'waiting for feedback'
    message.save()
    client.messages.create(
        to=message.contact_number,
        from_=twilio_phone,
        body='Volunteer marked your order as finish. Did everything go well? Respond "ok" if yes. If something was wrong tell us about it'
    )

    return redirect(url_for('users.profile'))


@messages.route('/sms/receive', methods=['POST'])
def receive_sms():
    phone_number = request.values['From']
    content = request.values['Body']

    last_message = Message.get_by_phone(phone_number)
    result, status = conversation(last_message=last_message, content=content, phone_number=phone_number)
    client.messages.create(
        to=phone_number,
        from_=twilio_phone,
        body=result['response']
    )


@messages.route('/messages/errors', methods=['GET'])
@employee_role_required
def error_messages():
    messages = Message.get_errors()
    return render_template('messages/error_messages.jinja2', messages=messages)
