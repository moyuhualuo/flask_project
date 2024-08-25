from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True, default=1)

    like_count = db.Column(db.Integer, default=0)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    time = db.Column(db.String(20), nullable=False)


class Web(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_type = db.Column(db.String(20))
    link_url = db.Column(db.String(255))
    link_name = db.Column(db.String(255))
    description = db.Column(db.Text)


class Md_test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(20))
    author = db.Column(db.String(20))
    content = db.Column(db.Text, nullable=False)
    is_published = db.Column(db.Boolean, default=False)
