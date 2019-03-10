from flask import Flask, request, url_for, Blueprint
from flask_restful import Resource, Api, reqparse #, abort
from time import strftime
from datetime import timedelta
import json, logging
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager


# initiate flask-restful instance
app = Flask(__name__)
#############
# DB Config #
#############
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/ecommerce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

##############
# JWT Config #
##############
app.config['JWT_SECRET_KEY'] = 'ThisIsMyECommerce'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return identity

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

api = Api(app, catch_all_404s=True)

@app.after_request
def after_request(response):
    if request.method == 'GET':
        app.logger.warning("REQUEST LOG\t%s", 
        json.dumps({'request': request.args.to_dict(),
            'response': json.loads(response.data.decode('utf-8'))
            })
        )
    else:
        app.logger.warning("REQUEST LOG\t%s",
        json.dumps({
            'request': request.get_json(),
            'response': json.loads(response.data.decode('utf-8'))
            })
        )
    return response

from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from . import *
from blueprints import db
            
# Call Blueprint
# from blueprints.penerbit.resources import bp_penerbit
from blueprints.user.resources import bp_user
# from blueprints.public.resources import bp_public
# from blueprints.internal.resources import bp_internal
from blueprints.login import bp_login

# app.register_blueprint(bp_penerbit, url_prefix='/penerbit')
app.register_blueprint(bp_user)
# app.register_blueprint(bp_public, url_prefix='/public')
# app.register_blueprint(bp_internal, url_prefix='/internal')
app.register_blueprint(bp_login)
db.create_all()

@app.route('/')
def index():
    return "<h1> Hello : This main route </h1>"
