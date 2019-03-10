import logging, json, hashlib
from datetime import datetime
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
# from flask_sqlalchemy.SQL_Alchemy import or_
from sqlalchemy import or_

from . import *
from blueprints import db
from blueprints.cart import Carts
from blueprints.product import Products
from sqlalchemy import in_

bp_cart = Blueprint('cart', __name__)
api = Api(bp_cart)

class CartResource(Resource):

    @jwt_required
    def get(self, cart_id=None):
        user = get_jwt_claims()
        if cart_id == None:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type=int, location='args', default=1)
            parser.add_argument('rp', type=int, location='args', default=5)
            args = parser.parse_args()

            offset = (args['p'] * args['rp']) - args['rp']
            if user["role"] == "buyer":
                query = Carts.query.filter_by(user_id=user['user_id']).all()
            if user["role"] == "seller":
                product = Products.query.filter_by(seller_id = user["user_id"]).all()
                products = []
                for prod in product:
                    products.append(marshal(prod, Products.response_fields)["id"])
                query = Carts.query.filter(Products.id.in_(products))
            rows = []
            for row in query.limit(args['rp']).offset(offset).all():
                rows.append(marshal(row, Carts.response_fields))
            return rows, 200, {'Content-Type': 'application/json'}
        else:
            query = Carts.query.get(cart_id)
            if query is None:
                return {'status': 'NOT_FOUND', 'message': 'Product not found!'}, 404, {'Content-Type': 'application/json'}
            return marshal(query, Carts.response_fields), 200, {'Content-Type': 'application/json'}
    
    @jwt_required
    def post(self):
        role = get_jwt_claims()['role']

        if role == "buyer":
            parser = reqparse.RequestParser()
            parser.add_argument('product_id', location='json', type=int, required=True)
            parser.add_argument('quantity', location='json', type=int, required=True)
            args = parser.parse_args()
            
            prod = Products.query.get(args['product_id'])

            if prod.stock < args["quantity"]:
                return {'status': 'FORBIDDEN', 'message': 'Product stock is below order quantity'}, 403 
                
            buyer_id = get_jwt_claims()['user_id']
            cart = Carts(None, args['product_id'], args['quantity'], buyer_id, "pending")
            db.session.add(cart)
            db.session.commit()
            return marshal(cart, Carts.response_fields), 200, {'Content-Type': 'application/json'}
        return {'status': 'FORBIDDEN', 'message': 'user is not a buyer'}, 403 

    @jwt_required
    def put(self, product_id):
        seller_id = get_jwt_claims()['user_id']
        role = get_jwt_claims()['role']
        query = Products.query.get(product_id)

        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('brand', location='json', required=True)
        parser.add_argument('category', location='json', required=True)
        parser.add_argument('description', location='json', required=True)
        parser.add_argument('stock', location='json', type=int, required=True)
        parser.add_argument('price', location='json', type=float, required=True)
        parser.add_argument('discount', location='json', type=float, required=True)
        parser.add_argument('url_picture', location='json', required=True)
        args = parser.parse_args()

        if role != "seller":
            return {'status': 'FORBIDDEN', 'message': 'user is not a seller'}, 403
        if query is None:
            return {'status': 'NOT_FOUND', 'message': 'Product not found!'}, 404, {'Content-Type': 'application/json'}
        if seller_id != query.seller_id:
            return {'status': 'FORBIDDEN', 'message': 'user is not owner of the product'}, 403
        
        if args['name'] is not None: query.name = args['name']
        if args['brand'] is not None: query.brand = args['brand']
        if args['category'] is not None: query.category = args['category']
        if args['description'] is not None: query.description = args['description']
        if args['stock'] is not None: query.stock = args['stock']
        if args['price'] is not None: query.price = args['price']
        if args['discount'] is not None: query.discount = args['discount']
        if args['url_picture'] is not None: query.url_picture = args['url_picture']

        db.session.commit()
        return marshal(query, Products.response_fields), 200, {'Content-Type': 'application/json'}

    @jwt_required
    def delete(self, product_id):
        seller_id = get_jwt_claims()['user_id']
        role = get_jwt_claims()['role']
        query = Products.query.get(product_id)

        if role != "seller":
            return {'status': 'FORBIDDEN', 'message': 'user is not a seller'}, 403
        if query is None:
            return {'status': 'NOT_FOUND', 'message': 'Product not found!'}, 404, {'Content-Type': 'application/json'}
        if seller_id != query.seller_id:
            return {'status': 'FORBIDDEN', 'message': 'user is not owner of the product'}, 403

        db.session.delete(query)
        db.session.commit()
        return {'status':'SUCCESS','message':'Product %s deleted succesfully' % query.name}, 200, {'Content-Type': 'application/json'}

api.add_resource(CartResource, '/cart', '/cart/<int:cart_id>')