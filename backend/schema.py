from flask_login import UserMixin

from db import db


class User(UserMixin, db.Model):
    id = db.Column(db.String(255), primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), unique=False, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    created_at = db.Column(db.DateTime(), unique=False, nullable=False)
    updated_at = db.Column(db.DateTime(), unique=False, nullable=False)
    comments = db.relationship("Comment")


class Comment(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    user =  db.relationship("User")
    user_id = db.Column(db.String(255), db.ForeignKey("user.id"))
    content = db.Column(db.String(255), unique=False, nullable=False)
    toxic = db.Column(db.Numeric(10, 4), unique=False, nullable=True)
    severe_toxic = db.Column(db.Numeric(10, 4), unique=False, nullable=True)
    obscene = db.Column(db.Numeric(10, 4), unique=False, nullable=True)
    threat = db.Column(db.Numeric(10, 4), unique=False, nullable=True)
    insult = db.Column(db.Numeric(10, 4), unique=False, nullable=True)
    identity_hate = db.Column(db.Numeric(10, 4), unique=False, nullable=True)
    is_censored = db.Column(db.Integer(), unique=False, nullable=True)
    created_at = db.Column(db.DateTime(), unique=False, nullable=False)
    updated_at = db.Column(db.DateTime(), unique=False, nullable=False)
