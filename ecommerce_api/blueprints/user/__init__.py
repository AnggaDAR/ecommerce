import random
from blueprints import db
from flask_restful import fields


class Users(db.Model):

    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    display_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    display_picture = db.Column(db.Text)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime,)
    status = db.Column(db.String(10))
    role = db.Column(db.String(20))

    response_fields = {
        'user_id': fields.Integer,
        'user_name': fields.String,
        'password': fields.String,
        'display_name': fields.String,
        'email': fields.String,
        'display_picture': fields.String,
        'description': fields.String,
        'created_at': fields.String,
        'status': fields.String,
        'role': fields.String
    }

    token_identity = {
        'user_id': fields.Integer,
        'user_name': fields.String,
        'role': fields.String
    }

    def __init__(self, user_id, user_name, password, display_name, email, display_picture, description, created_at, status, role):

        self.user_id = user_id
        self.user_name = user_name
        self.password = password
        self.display_name = display_name
        self.email = email
        self.display_picture = display_picture
        self.description = description
        self.created_at = created_at
        self.status = status
        self.role = role

    def __repr__(self):
        return "<User %r>" % self.user_id
