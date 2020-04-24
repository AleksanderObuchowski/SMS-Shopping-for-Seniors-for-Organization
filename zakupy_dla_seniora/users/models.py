from zakupy_dla_seniora import db, login_manager
from datetime import datetime, timezone
from random import randint
from flask_login import UserMixin


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
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisations.id'), nullable=False)
    town = db.Column('town', db.String(100))
    created_at = db.Column('created_at', db.DateTime)
    created_by = db.Column('created_by', db.ForeignKey('user.id'))
    is_superuser = db.Column('is_superuser', db.Boolean, default=False)
    is_employee = db.Column('is_employee', db.Boolean)
    is_active = db.Column('is_active', db.Boolean, default=False)
    # code_sent = db.Column('code_sent', db.Boolean, default=False)
    # verification_code = db.Column('verification_code', db.Integer)
    # verified = db.Column('verified', db.Boolean, default=False)
    # points = db.Column('points', db.Integer, default=0)
    # placings = db.relationship('Placings', backref='user', cascade='all, delete-orphan', lazy='dynamic')

    def __init__(self, username, email, organisation_id, password_hash, created_by=None, is_superuser=False):
        self.username = username
        self.email = email
        self.organisation_id = organisation_id
        self.password_hash = password_hash
        self.is_superuser = is_superuser
        self.is_employee = not is_superuser
        self.is_active = is_superuser
        self.created_by = created_by
        self.create_date = datetime.now(timezone.utc)
        # self.verification_code = randint(1000, 9999)

    def __repr__(self):
        return "<User(id='%s', username='%s')>" % (self.id, self.username)

    # def as_json(self):
    #     return {
    #         'id': self.id,
    #         'login': self.login,
    #         # 'points': self.points
    #     }

    # def set_phone(self, phone):
    #     self.phone = phone

    @classmethod
    def get_by_id(cls, id_):
        return cls.query.filter_by(id=id_).first()

    @classmethod
    def get_by_username(cls, username_):
        return cls.query.filter_by(username=username_).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

