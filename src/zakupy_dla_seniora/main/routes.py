from flask import Blueprint, render_template, request
import requests

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/board')
def leaderboard():
    r = requests.get('http://127.0.0.1:5000/board')
    return render_template('board.html', data=r.json())


@main.route('/take_order')
def take():
    r = requests.post('http://127.0.0.1:5000/placing', params=request.args)
    r = requests.get('http://127.0.0.1:5000/board')
    return render_template('board.html', data=r.json())


@main.route('/send_end_placing')
def end():
    r = requests.post('http://127.0.0.1:5000/end_placing', params=request.args)
    r = requests.get('http://127.0.0.1:5000/board')
    return render_template('board.html', data=r.json())


