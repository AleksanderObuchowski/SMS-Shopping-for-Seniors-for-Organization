from datetime import datetime, timezone
from flask_login import UserMixin, current_user
from flask_babel import _

from zakupy_dla_seniora import db, login_manager
# from zakupy_dla_seniora.volunteers.models import Volunteer
from zakupy_dla_seniora.messages.models import Message


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


class User(db.Model, UserMixin):
    __tablename__ = 'users'
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
    district = db.Column('district', db.String(100))
    created_at = db.Column('created_at', db.DateTime)
    created_by = db.Column('created_by', db.ForeignKey('users.id'))
    is_superuser = db.Column('is_superuser', db.Boolean, default=False)
    is_employee = db.Column('is_employee', db.Boolean, default=False)
    is_volunteer = db.Column('is_volunteer', db.Boolean, default=True)
    is_active = db.Column('is_active', db.Boolean, default=False)

    # volunteers_creation = db.relationship('Volunteer', backref='user', cascade='all, delete-orphan', lazy='dynamic',
    #                                       foreign_keys=[User.created_by])
    user_creation = db.relationship('User', backref='sub_user', remote_side=id)

    def __init__(self, username, email, organisation_id, password_hash, district=None, first_name=None, last_name=None,
                 phone=None, position=None, town=None, created_by=None, is_employee=False, is_superuser=False):
        self.edit(username, email, first_name, last_name, phone, town, position, is_superuser)
        self.district = district
        self.organisation_id = organisation_id
        self.password_hash = password_hash
        self.is_employee = is_employee
        self.is_active = is_superuser
        self.created_by = created_by
        self.create_date = datetime.now(timezone.utc)

    def __repr__(self):
        return f'<User(id={self.id}, username={self.username}, super={self.is_superuser}, emp={self.is_employee}, vol={self.is_volunteer})>'

    def edit(self, username, email, first_name, last_name, phone, town, position, is_superuser):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.town = town
        self.position = position
        self.is_superuser = is_superuser

    def edit_volunteer(self, username=None, first_name=None, last_name=None, phone=None, email=None, town=None,
                       district=None, organisation_id=None, is_active=None):
        if username:
            self.username = username
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if phone:
            self.phone = phone
        if email:
            self.email = email
        if town:
            self.town = town
        if district:
            self.district = district
        if organisation_id:
            self.organisation_id = organisation_id
        if is_active:
            self.is_active = is_active

    @classmethod
    def get_all_volunteers_as_dict(cls):
        """
        :return Volunteer objects as dictionary:
        """
        if current_user.is_employee:
            data = cls.query.filter_by(
                organisation_id=current_user.organisation_id,
                is_employee=False,
                is_superuser=False
            ).all()
        else:
            data = cls.query.filter_by(is_employee=False, is_superuser=False).all()

        return [{
            _('ID'): vol.id,
            _('Username'): vol.username,
            _('First name'): vol.first_name,
            _('Last name'): vol.last_name,
            _('Phone number'): vol.phone,
            _('Email'): vol.email,
            _('Organisation'): vol.organisation_id,
            _('Town'): vol.town
        } for vol in data]

    def to_dict_view_user(self):
        return {
            _('Username'): self.username,
            _('First name'): self.first_name,
            _('Last name'): self.last_name,
            _('Email'): self.email,
            _('Phone'): self.phone,
            _('City'): self.town,
            _('Organisation'): self.organisation_id,
            _('Position'): self.position,
            _('Special privileges'): self.is_superuser,
            _('Created by'): self.created_by,
            _('Created at'): self.created_at,
            _('Is active'): self.is_active
        }

    def to_dict_view_all_users(self):
        return {
            _('ID'): self.id,
            _('First name'): self.first_name,
            _('Last name'): self.last_name,
            _('Email'): self.email,
            _('Phone'): self.phone,
            _('City'): self.town,
            _('Organisation'): self.organisation_id,
            _('Position'): self.position,
            _('Special privileges'): self.is_superuser,
            _('Is active'): self.is_active
        }

    @classmethod
    def get_all_for_organisation(cls, user_org_id):
        return cls.query.filter_by(organisation_id=user_org_id).all()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id_):
        if current_user.is_superuser:
            return cls.query.filter_by(id=id_).first()
        elif current_user.is_employee:
            return cls.query.filter_by(id=id_, organisation_id=current_user.organisation_id).first()
        else:
            return cls.query.filter_by(id=current_user.id).first()

    @classmethod
    def get_by_username(cls, username_):
        return cls.query.filter_by(username=username_).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
