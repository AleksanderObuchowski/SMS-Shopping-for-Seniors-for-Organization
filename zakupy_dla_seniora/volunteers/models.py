from datetime import datetime, timezone
from flask_login import UserMixin, current_user
from zakupy_dla_seniora import db
from flask_babel import _


class Volunteers(db.Model, UserMixin):
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True)
    first_name = db.Column('first_name', db.String(30), nullable=False)
    last_name = db.Column('last_name', db.String(30), nullable=False)
    phone_number = db.Column('phone_number', db.String(12), nullable=False)
    email = db.Column('email', db.String(50), nullable=False, unique=True)
    organisation_id = db.Column('organisation_id', db.Integer, db.ForeignKey('organisations.id', ondelete='CASCADE'),
                                nullable=False)
    town = db.Column('town', db.String(100), nullable=False)
    district = db.Column('district', db.String(100), nullable=False)
    password_hash = db.Column('password_hash', db.String(255), nullable=False)
    created_by = db.Column('created_by', db.ForeignKey('user.id'))
    created_at = db.Column('created_at', db.DateTime)
    is_phone_verified = db.Column('is_phone_verified', db.Boolean, default=False)
    is_active = db.Column('is_active', db.Boolean, default=False)

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

    @classmethod
    def get_all_as_dict(cls, user_org_id=None):
        """
        :param user_org_id:
        :return Volunteer objects as dictionary:
        """
        if user_org_id:
            data = cls.query.filter_by(organisation_id=user_org_id).all()
        else:
            data = cls.query.all()

        return [{
            _('ID'): vol.id,
            _('Username'): vol.username,
            _('First name'): vol.first_name,
            _('Last name'): vol.last_name,
            _('Phone number'): vol.phone_number,
            _('Email'): vol.email,
            _('Organisation'): vol.organisation_id,
            _('Town'): vol.town
        } for vol in data]

    @classmethod
    def get_columns(cls, user_org_id=None):
        return [
            _('ID'),
            _('Username'),
            _('First name'),
            _('Last name'),
            _('Phone number'),
            _('Email'),
            _('Organisation'),
            _('Town')
        ]

    @classmethod
    def get_by_id(cls, volunteer_id):
        """
        Returns volunteer based on current_user. If request is made by superuser, returns any Volunteer. If request
        is made by organisation employee, returns organisation specific Volunteers
        :param volunteer_id:
        :return Volunteer object or None:
        """
        if current_user.is_superuser:
            return cls.query.filter_by(id=volunteer_id).first()
        elif current_user.is_employee:
            return cls.query.filter_by(id=volunteer_id, organisation_id=current_user.organisation_id).first()
        else:
            return cls.query.filter_by(id=current_user.id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
