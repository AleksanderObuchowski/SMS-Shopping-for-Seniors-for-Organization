from datetime import datetime, timezone

from flask_login import UserMixin
from zakupy_dla_seniora import db
from zakupy_dla_seniora.messages.models import Messages

class Volunteers(db.Model, UserMixin):
    __tablename__ = 'volunteers'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(40), nullable=False)
    first_name = db.Column('first_name', db.String(40), nullable=False)
    last_name = db.Column('last_name', db.String(40), nullable=False)
    phone_number = db.Column('phone_number', db.String(12), nullable=False)
    email = db.Column('email', db.String(60), nullable=False)
    organisation_id = db.Column('organisation_id', db.Integer, db.ForeignKey('organisations.id'), nullable=False)
    town = db.Column('town', db.String(100), nullable=False)
    district = db.Column('district', db.String(100), nullable=False)
    password_hash = db.Column('password_hash', db.String(255), nullable=False)
    created_by = db.Column('created_by', db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column('created_at', db.DateTime)
    is_phone_verified = db.Column('is_phone_verified', db.Boolean, default=False)
    is_active = db.Column('is_active', db.Boolean, default=False)

    volunteers_message = db.relationship('Messages', backref='volunteers', cascade='all, delete-orphan', lazy='dynamic', foreign_keys=[Messages.volunteer_id])
    message_creation = db.relationship('Messages', backref='volunteers', cascade='all, delete-orphan', lazy='dynamic', foreign_keys=[
        Messages.created_by])

    def __init__(self, first_name, last_name, phone, email, org_id, town, distr, pass_hash, created_by):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone
        self.email = email
        self.organisation_id = org_id
        self.town = town
        self.district = distr
        self.password_hash = pass_hash
        self.created_by = created_by
        self.created_at = datetime.now(timezone.utc)

    def __repr__(self):
        return "<Volunteer(id='%s', username='%s')>" % (self.id, self.username)

    def set_active(self):
        self.is_active = True
