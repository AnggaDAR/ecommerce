import random
from blueprints import db
from flask_restful import fields


class Products(db.Model):

    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))
    brand = db.Column(db.String(200))
    category = db.Column(db.String(200))
    description = db.Column(db.Text)
    stock = db.Column(db.Integer)
    price = db.Column(db.Float)
    discount = db.Column(db.Float)
    url_picture = db.Column(db.String(255))
    seller_id = db.Column(db.Integer)

    response_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'brand': fields.String,
        'category': fields.String,
        'description': fields.String,
        'stock': fields.Integer,
        'price': fields.Float,
        'discount': fields.Float,
        'url_picture': fields.String,
        'seller_id': fields.Integer,
    }

    def __init__(self, id, name, brand, category, description, stock, price, discount, url_picture, seller_id):
        self.id = id
        self.name = name
        self.brand = brand
        self.category = category
        self.description = description
        self.stock = stock
        self.price = price
        self.discount = discount
        self.url_picture = url_picture
        self.seller_id = seller_id

    def __repr__(self):
        return "<Product %r>" % self.id
