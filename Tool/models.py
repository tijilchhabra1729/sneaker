from Tool import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


design = db.Table('design',
                  db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                  db.Column('design_id', db.Integer, db.ForeignKey('designs.id')))

adjective = db.Table('adjective',
                     db.Column('design_id', db.Integer,
                               db.ForeignKey('designs.id')),
                     db.Column('adjective_id', db.Integer, db.ForeignKey('adjectives.id')))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    design_names = db.Column(db.String, default='')

    designs = db.relationship(
        'Design', secondary=design, backref=db.backref('users', lazy='dynamic'))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, name, username, email, password):
        self.email = email
        self.name = name
        self.username = username
        self.password_hash = generate_password_hash(password)


class Design(db.Model):
    __tablename__ = 'designs'
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(64))

    designs = db.relationship(
        'Adjective', secondary=adjective, backref=db.backref('designs', lazy='dynamic'))

    def __init__(self, location):
        self.location = location


class Adjective(db.Model):
    __tablename__ = 'adjectives'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __init__(self, name):
        self.name = name
