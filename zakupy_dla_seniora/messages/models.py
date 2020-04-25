from sqlalchemy import desc
from zakupy_dla_seniora import db
from datetime import datetime, timezone


class Messages(db.Model):
    __tablename__ = 'messages'
    id = db.Column('id', db.Integer, primary_key=True)
    content = db.Column('content', db.String(500), nullable=False)
    contact_number = db.Column('contact_number', db.String(12), nullable=False)
    location = db.Column('location', db.String(100))
    longtitude = db.Column('longtitude', db.Float(precision=5))
    latitude = db.Column('latitude', db.Float(precision=5))
    volunteer_id = db.Column('volunteer_id', db.Integer, db.ForeignKey('volunteers.id'))
    created_by = db.Column('created_by', db.Integer, db.ForeignKey('volunteers.id'))
    created_at = db.Column('created_at', db.DateTime)
    status = db.Column('status', db.String(60))


    def __init__(self, content, contact_number, location,latitude,longtitude, status, created_by = None ):
        self.content = content
        self.contact_number = contact_number
        self.location = location
        self.latitude = latitude
        self.longtitude = longtitude
        self.status = status
        self.created_at = datetime.now()
        self.created_by = created_by



    def __repr__(self):
        return "Message : ".format(self.content, self.contact_number, self.location, self.status)


    @classmethod
    def get_by_id(cls, id_):
        return cls.query.filter_by(id=id_).first()

    @classmethod
    def get_received(cls):
        return cls.query.filter_by(status='received').all()

    @classmethod
    def get_user_messages(cls,id):
        return cls.query.filter_by(volunteer_id=id).all()

    @classmethod
    def get_by_phone(cls, phone_):
        # first newest
        return cls.query.filter_by(contact_number=phone_).order_by(Messages.created_at.desc())

    def save(self):
        db.session.add(self)
        db.session.commit()