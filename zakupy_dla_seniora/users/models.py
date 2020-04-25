from datetime import datetime, timezone
from flask_login import UserMixin

from zakupy_dla_seniora import db, login_manager
from zakupy_dla_seniora.volunteers.models import Volunteers
from zakupy_dla_seniora.messages.models import Messages


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('login', db.String(20), unique=True, nullable=False)
    email = db.Column('email', db.String(100), unique=True, nullable=False)
    password_hash = db.Column('password_hash', db.String(255), nullable=False)
    first_name = db.Column('first_name', db.String(50))
    last_name = db.Column('last_name', db.String(50))
    phone = db.Column('phone', db.String(12), unique=True)
    position = db.Column('position', db.String(100))
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisations.id', ondelete='CASCADE'), nullable=False)
    town = db.Column('town', db.String(100))
    created_at = db.Column('created_at', db.DateTime)
    created_by = db.Column('created_by', db.ForeignKey('user.id'))
    is_superuser = db.Column('is_superuser', db.Boolean, default=False)
    is_employee = db.Column('is_employee', db.Boolean)
    is_active = db.Column('is_active', db.Boolean, default=False)

    volunteers_creation = db.relationship('Volunteers', backref='user', cascade='all, delete-orphan', lazy='dynamic',
                                          foreign_keys=[Volunteers.created_by])
    user_creation = db.relationship('User', backref='sub_user', remote_side=id)

    def __init__(self, username, email, organisation_id, password_hash, first_name=None, last_name=None,
                 phone=None, position=None, town=None, created_by=None, is_superuser=False):
        self.username = username
        self.email = email
        self.organisation_id = organisation_id
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.position = position
        self.town = town
        self.is_superuser = is_superuser
        self.is_employee = not is_superuser
        self.is_active = is_superuser
        self.created_by = created_by
        self.create_date = datetime.now(timezone.utc)

    def __repr__(self):
        return f'<User(id={self.id}, username={self.username})>'

    @classmethod
    def get_by_id(cls, id_):
        return cls.query.filter_by(id=id_).first()

    @classmethod
    def get_by_username(cls, username_):
        return cls.query.filter_by(username=username_).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
