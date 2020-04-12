from datetime import datetime, timezone

from zakupy_dla_seniora import db
from zakupy_dla_seniora.users.models import User


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
    added_by = db.Column('added_by', db.ForeignKey('user.id'))
    created_at = db.Column('created_at', db.DateTime)
    employees = db.relationship('User', backref='organisations', cascade='all, delete-orphan', lazy='dynamic',
                                foreign_keys=[User.organisation_id])

    def __init__(self, name, added_by=None):
        self.name = name
        self.added_by = added_by
        self.created_at = datetime.now(timezone.utc)

    def __repr__(self):
        return "<Organisation(id='%s', name='%s')>" % (self.id, self.name)

    @classmethod
    def get_by_id(cls, id_):
        return cls.query.filter_by(id=id_).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
