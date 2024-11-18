from core import app
import os
from flask_cors import CORS
from flasgger import Swagger

from core.apis.system import _System_Apis
from core.apis.car import _Cars_Apis

app.register_blueprint(_System_Apis)
app.register_blueprint(_Cars_Apis)


from flask import Blueprint, jsonify
from flask_restful import Resource, Api
from core.apis.decoretor import accept_payload
from core.apis.system.Schema import UserDataSchema
from core.apis.common import gen_password
from core.apis.responses import APIResponse
from core.apis.error_handler import handle_error
from core.model.user import User
from core import db
from flasgger import swag_from

CORS(
    app,
    resources={r"*": {"origins": "*"}},
    methods=['POST', 'GET', 'OPTIONS'],
    expose_headers=['Content-Type', 'Access-Control-Allow-Origin', os.getenv('user_authorization_header_key')],
    allow_headers=['Content-Type', 'Access-Control-Allow-Origin', os.getenv('user_authorization_header_key')],
)


app.config['SWAGGER'] = {
    'title': 'My API',
    'uiversion': 3,
    'specs': [
        {
            'endpoint': 'apispec',
            'route': '/apispec.json',  # Path where apispec.json will be served
            'rule_filter': lambda rule: True,  # Include all routes
            'model_filter': lambda tag: True,  # Include all models
        }
    ],
    'swagger_ui': True,
    'specs_route': '/apidocs'
}


swagger = Swagger(app)
