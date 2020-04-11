from zakupy_dla_seniora import db, login_manager
from datetime import datetime, timezone
from random import randint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String(100), unique=True, nullable=False)
    display_name = db.Column('display_name', db.String(35), unique=True, nullable=False)
    create_date = db.Column('create_date', db.DateTime)
    phone = db.Column('phone', db.String(12), unique=True)
    created_by = db.Column('created_by', db.ForeignKey('user.id'), nullable=True)
    # code_sent = db.Column('code_sent', db.Boolean, default=False)
    # verification_code = db.Column('verification_code', db.Integer)
    # verified = db.Column('verified', db.Boolean, default=False)
    # points = db.Column('points', db.Integer, default=0)

    password_hash = db.Column('password_hash', db.String(255), nullable=False)
    super_user = db.Column('super_user', db.Boolean, default=False)
    # placings = db.relationship('Placings', backref='user', cascade='all, delete-orphan', lazy='dynamic')

    def __init__(self, display_name, email, password, created_by=None, super_user=False):
        self.display_name = display_name
        self.email = email
        self.set_password(password)
        self.super_user = super_user
        self.created_by = created_by

        self.create_date = datetime.now(timezone.utc)
        self.verification_code = randint(1000, 9999)

    def __repr__(self):
        return "<User(id='%s', display_name='%s')>" % (self.id, self.display_name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def as_json(self):
        return {
            'id': self.id,
            'display_name': self.display_name,
            # 'points': self.points
        }

    def set_phone(self, phone):
        self.phone = phone

    @classmethod
    def get_by_id(cls, id_):
        return cls.query.filter_by(id=id_).first()

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(display_name=name).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

