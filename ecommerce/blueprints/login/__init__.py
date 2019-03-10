import logging, json, hashlib
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_claims
# from . import *
# from blueprints import db
from blueprints.user import Users

bp_login = Blueprint('login', __name__)
api = Api(bp_login)

class CreateSellerTokenResources(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_name', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()
        password = hashlib.md5(args['password'].encode()).hexdigest()

        query = Users.query.filter_by(user_name=args['user_name']).filter_by(password=password).first()
        print(query)

        if query is not None:
            # if query.status == "banned":
            #     return {'status': 'FORBIDDEN', 'message': 'user is banned'}, 403
            if query.role != "seller":
                return {'status': 'FORBIDDEN', 'message': 'user is not a seller'}, 403
            token = create_access_token(identity=marshal(query, Users.token_identity))
        else:
            return {'status': 'UNAUTHORIZED', 'message': 'invalid username or password'}, 401
        return {'token': token}, 200

class CreateBuyerTokenResources(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_name', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()
        password = hashlib.md5(args['password'].encode()).hexdigest()

        query = Users.query.filter_by(user_name=args['user_name']).filter_by(password=password).first()
        print(query)

        if query is not None:
            if query.status == "banned":
                return {'status': 'FORBIDDEN', 'message': 'user is banned'}, 403
            if query.role != "buyer":
                return {'status': 'FORBIDDEN', 'message': 'user is not a buyer'}, 403
            token = create_access_token(identity=marshal(query, Users.token_identity))
        else:
            return {'status': 'UNAUTHORIZED', 'message': 'invalid username or password'}, 401
        return {'token': token}, 200

api.add_resource(CreateSellerTokenResources, '/seller/login')
api.add_resource(CreateBuyerTokenResources, '/buyer/login')