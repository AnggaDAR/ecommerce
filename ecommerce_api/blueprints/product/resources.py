import logging, json, hashlib
from datetime import datetime
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
# from flask_sqlalchemy.SQL_Alchemy import or_
from sqlalchemy import or_

from . import *
from blueprints import db
from blueprints.product import Products

bp_product = Blueprint('product', __name__)
api = Api(bp_product)

class ProductResource(Resource):

    def get(self, product_id=None):
        if product_id == None:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type=int, location='args', default=1)
            parser.add_argument('rp', type=int, location='args', default=5)
            parser.add_argument('category', location='args')
            parser.add_argument('brand', location='args')
            parser.add_argument('q', location='args')
            args = parser.parse_args()

            offset = (args['p'] * args['rp']) - args['rp']

            query = Products.query
            if args['q'] is not None:
                query = query.filter(or_(Products.name.like("%"+args['q']+"%"), Products.category.like("%"+args['q']+"%"), Products.brand.like("%"+args['q']+"%"), Products.description.like("%"+args['q']+"%")))
            if args['category'] is not None:
                query = query.filter_by(category=args['category'])
            if args['brand'] is not None:
                query = query.filter_by(brand=args['brand'])
            rows = []
            for row in query.limit(args['rp']).offset(offset).all():
                rows.append(marshal(row, Products.response_fields))
            return rows, 200, {'Content-Type': 'application/json'}
        else:
            query = Products.query.get(product_id)
            if query is None:
                return {'status': 'NOT_FOUND', 'message': 'Product not found!'}, 404, {'Content-Type': 'application/json'}
            return marshal(query, Products.response_fields), 200, {'Content-Type': 'application/json'}
    
    @jwt_required
    def post(self):
        seller_id = get_jwt_claims()['user_id']
        role = get_jwt_claims()['role']
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
        if role == "seller":
            product = Products(None, args['name'], args['brand'], args['category'], args['description'], args['stock'], args['price'], args['discount'], args['url_picture'], seller_id)
            db.session.add(product)
            db.session.commit()
            return marshal(product, Products.response_fields), 200, {'Content-Type': 'application/json'}
        return {'status': 'FORBIDDEN', 'message': 'user is not a seller'}, 403 

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

api.add_resource(ProductResource, '/product', '/product/<int:product_id>')