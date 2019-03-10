import logging, json, hashlib
from datetime import datetime
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
from . import *
from blueprints import db

bp_user = Blueprint('user', __name__)
api = Api(bp_user)

class SellerResource(Resource):

    @jwt_required
    def get(self):
        id = get_jwt_claims()['user_id']
        # role = get_jwt_claims()['role']
        query = Users.query.get(id)
        if query is None:
            return {'status': 'NOT_FOUND', 'message': 'User not found!'}, 404, {'Content-Type': 'application/json'}
        if query.role != "seller":
            return {'status': 'FORBIDDEN', 'message': 'user is not a seller'}, 403
        return marshal(query, Users.response_fields), 200, {'Content-Type': 'application/json'}
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_name', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('display_name', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('display_picture', location='json', required=True)
        parser.add_argument('description', location='json', required=True)
        args = parser.parse_args()

        check_users = Users.query.filter_by(user_name = args['user_name']).first()
        if check_users is not None:
            return {'status': 'DUPLICATE_ENTRY', 'message': 'Username %s already exists!' % args['user_name']}, 403, {'Content-Type': 'application/json'}
        
        password = hashlib.md5(args['password'].encode()).hexdigest()
        created_at = datetime.now()
        user = Users(None, args['user_name'], password, args['display_name'], args['email'], args['display_picture'], args['description'], created_at, "active", "seller")
        db.session.add(user)
        db.session.commit()
        return marshal(user, Users.response_fields), 200, {'Content-Type': 'application/json'}

    @jwt_required
    def put(self):
        id = get_jwt_claims()['user_id']
        user_name = get_jwt_claims()['user_name']
        query = Users.query.get(id)

        parser = reqparse.RequestParser()
        parser.add_argument('user_name', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('display_name', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('display_picture', location='json', required=True)
        parser.add_argument('description', location='json', required=True)
        args = parser.parse_args()

        password = hashlib.md5(args['password'].encode()).hexdigest()

        if query is None:
            return {'status': 'NOT_FOUND', 'message': 'User not found!'}, 404, {'Content-Type': 'application/json'}

        if args['user_name'] is not None: 
            check_users = Users.query.filter_by(user_name = args['user_name']).first()
            if check_users is not None and args['user_name'] != user_name:
                return {'status': 'DUPLICATE_ENTRY', 'message': 'Username %s already exists!' % args['user_name']}, 403, {'Content-Type': 'application/json'}
            query.user_name = args['user_name']
        if args['password'] is not None: query.password = password
        if args['display_name'] is not None: query.display_name = args['display_name']
        if args['email'] is not None: query.email = args['email']
        if args['display_picture'] is not None: query.display_picture = args['display_picture']
        if args['description'] is not None: query.description = args['description']

        db.session.commit()
        return marshal(query, Users.response_fields), 200, {'Content-Type': 'application/json'}

    @jwt_required
    def delete(self):
        id = get_jwt_claims()['user_id']
        query = Users.query.get(id)

        if query is None:
            return {'status': 'NOT_FOUND', 'message': 'User not found!'}, 404, {'Content-Type': 'application/json'}
        else:
            db.session.delete(query)
            db.session.commit()
            return {'status':'SUCCESS','message':'User %s deleted succesfully' % query.user_name}, 200, {'Content-Type': 'application/json'}

class BuyerResource(Resource):

    @jwt_required
    def get(self):
        id = get_jwt_claims()['user_id']
        query = Users.query.get(id)
        if query is None:
            return {'status': 'NOT_FOUND', 'message': 'User not found!'}, 404, {'Content-Type': 'application/json'}
        return marshal(query, Users.response_fields), 200, {'Content-Type': 'application/json'}
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_name', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('display_name', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('display_picture', location='json', required=True)
        # parser.add_argument('description', location='json', required=True)
        args = parser.parse_args()

        check_users = Users.query.filter_by(user_name = args['user_name']).first()
        if check_users is not None:
            return {'status': 'DUPLICATE_ENTRY', 'message': 'Username %s already exists!' % args['user_name']}, 403, {'Content-Type': 'application/json'}
        
        password = hashlib.md5(args['password'].encode()).hexdigest()
        created_at = datetime.now()
        user = Users(None, args['user_name'], password, args['display_name'], args['email'], args['display_picture'], "Buyer", created_at, "active", "buyer")
        db.session.add(user)
        db.session.commit()
        return marshal(user, Users.response_fields), 200, {'Content-Type': 'application/json'}

    @jwt_required
    def put(self):
        id = get_jwt_claims()['user_id']
        user_name = get_jwt_claims()['user_name']
        query = Users.query.get(id)

        parser = reqparse.RequestParser()
        parser.add_argument('user_name', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('display_name', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('display_picture', location='json', required=True)
        # parser.add_argument('description', location='json', required=True)
        args = parser.parse_args()

        password = hashlib.md5(args['password'].encode()).hexdigest()

        if query is None:
            return {'status': 'NOT_FOUND', 'message': 'User not found!'}, 404, {'Content-Type': 'application/json'}

        if args['user_name'] is not None: 
            check_users = Users.query.filter_by(user_name = args['user_name']).first()
            if check_users is not None and args['user_name'] != user_name:
                return {'status': 'DUPLICATE_ENTRY', 'message': 'Username %s already exists!' % args['user_name']}, 403, {'Content-Type': 'application/json'}
            query.user_name = args['user_name']
        if args['password'] is not None: query.password = password
        if args['display_name'] is not None: query.display_name = args['display_name']
        if args['email'] is not None: query.email = args['email']
        if args['display_picture'] is not None: query.display_picture = args['display_picture']
        # if args['description'] is not None: query.description = args['description']

        db.session.commit()
        return marshal(query, Users.response_fields), 200, {'Content-Type': 'application/json'}

    @jwt_required
    def delete(self):
        id = get_jwt_claims()['user_id']
        query = Users.query.get(id)

        if query is None:
            return {'status': 'NOT_FOUND', 'message': 'User not found!'}, 404, {'Content-Type': 'application/json'}
        else:
            db.session.delete(query)
            db.session.commit()
            return {'status':'SUCCESS','message':'User %s deleted succesfully' % query.user_name}, 200, {'Content-Type': 'application/json'}

api.add_resource(SellerResource, '/seller')
api.add_resource(BuyerResource, '/buyer')