import random
from blueprints import db
from flask_restful import fields


class Carts(db.Model):

    __tablename__ = "product"
    cart_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    buyer_id = db.Column(db.Integer)
    status = db.Column(db.String(10))

    response_fields = {
        'cart_id': fields.Integer,
        'product_id': fields.Integer,
        'quantity': fields.Integer,
        'buyer_id': fields.Integer,
        'status': fields.String,
    }

    def __init__(self, cart_id, product_id, quantity, buyer_id, status):
        self.cart_id = cart_id
        self.product_id = product_id
        self.quantity = quantity
        self.buyer_id = buyer_id
        self.status = status

    def __repr__(self):
        return "<Cart %r>" % self.id
