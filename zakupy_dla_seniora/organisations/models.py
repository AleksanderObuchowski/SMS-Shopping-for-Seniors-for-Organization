from datetime import datetime, timezone
from flask_login import current_user
from flask_babel import _

from zakupy_dla_seniora import db
from zakupy_dla_seniora.users.models import User
from zakupy_dla_seniora.volunteers.models import Volunteers


class Organisations(db.Model):
    __tablename__ = 'organisations'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(200), unique=True, nullable=False)
    contact_phone = db.Column('contact_phone', db.String(12))
    contact_email = db.Column('contact_email', db.String(100))
    town = db.Column('town', db.String(100))
    postal_code = db.Column('postal_code', db.String(10))
    address = db.Column('address', db.String(50))
    website = db.Column('website', db.String(200))
    added_by = db.Column('added_by', db.ForeignKey('user.id', ondelete="SET NULL"))
    created_at = db.Column('created_at', db.DateTime)

    employees = db.relationship('User', backref='organisations', cascade='all, delete-orphan', lazy=True,
                                foreign_keys=[User.organisation_id])
    volunteers = db.relationship('Volunteers', backref='organisations', cascade='all, delete-orphan', lazy=True,
                                 foreign_keys=[Volunteers.organisation_id])

    def __init__(self, name, contact_phone=None, contact_email=None, town=None, postal_code=None,
                 address=None, website=None, added_by=None):
        self.name = name
        self.edit(contact_phone=contact_phone, contact_email=contact_email, town=town,
                  postal_code=postal_code, address=address, website=website)
        self.added_by = added_by
        self.created_at = datetime.now(timezone.utc)

    def __repr__(self):
        return f"<Organisation(id={self.id}, name={self.name})>"

    def edit(self, contact_phone=None, contact_email=None, town=None, postal_code=None, address=None, website=None):
        self.contact_phone = contact_phone
        self.contact_email = contact_email
        self.town = town
        self.postal_code = postal_code
        self.address = address
        self.website = website

    def to_dict_view_organisation(self):
        return {
            'Name': self.name,
            _('Phone'): self.contact_phone,
            _('City'): self.town,
            _('Address'): self.address,
            _('Postal code'): self.postal_code,
            _('Website'): self.website,
            _('Created at'): self.created_at,
            'Employees': self.employees,
            'Volunteers': self.volunteers
        }

    def to_dict_view_all_organisations(self):
        return {
            _('ID'): self.id,
            _('Name'): self.name,
            _('Website'): self.website,
            _('Created'): self.created_at,
            _('Employees'): len(self.employees),
            _('Volunteers'): len(self.volunteers)
        }

    @classmethod
    def get_by_id(cls, id_):
        if current_user.is_superuser and id_:
            return cls.query.filter_by(id=id_).first()
        else:
            return cls.query.filter_by(id=current_user.organisation_id).first()

    @classmethod
    def get_name_by_id(cls, id_):
        org = cls.query.filter_by(id=id_).first()
        return org.name

    @classmethod
    def get_id_by_name(cls, name_):
        org = cls.query.filter_by(name=name_).first()
        return org.id

    @classmethod
    def get_by_name(cls, name_):
        return cls.query.filter_by(name=name_).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
