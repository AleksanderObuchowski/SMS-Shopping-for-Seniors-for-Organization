from flask import Blueprint, render_template
from zakupy_dla_seniora.board.functions import get_min_max_coordinates
from zakupy_dla_seniora.sms_handler.models import Messages

board = Blueprint('board', __name__)


@board.route('/')
@board.route('/board')
def board():
    data = {}
    if data['latitude'] is not None and data['longitude'] is not None and data['radius'] is not None:
        latitude = data['latitude']
        longitude = data['longitude']
        radius = data['radius']

        min_latitude, max_latitude = get_min_max_coordinates(radius, latitude)
        min_longitude, max_longitude = get_min_max_coordinates(radius, longitude)

        messages = Messages.query.filter(
            Messages.message_location_lat > min_latitude,
            Messages.message_location_lat < max_latitude,
            Messages.message_location_lon > min_longitude,
            Messages.message_location_lon < max_longitude,
            Messages.message_status == 'Received'
        ).all()
    else:
        messages = Messages.query.filter(Messages.message_status == 'Received').all()
    messages = [message.prepare_board_view() for message in messages]

    return render_template('board.html', data=messages)


@board.route('/take_order')
def take_order():
    pass