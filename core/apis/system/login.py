from flask import Blueprint
from flask_restful import Resource, Api
from core.apis.decoretor import accept_payload
from .Schema import LoginForgetSchema
from core.model.user import User
from core.apis.common import user_authentication_token
from core.apis.responses import APIResponse
import os
from core.apis.error_handler import handle_error
from flasgger import swag_from

_Login = Blueprint("for login api", __name__)
api = Api(_Login)

class Login(Resource):

    @swag_from({
    'tags': ['User'],
    'description': 'User Login API',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'description': 'User Login information',
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['email', 'password']
            },
        }
    ],
    'responses': {
        200: {
            'description': 'Login Successful',
            'content': {
                'application/json': {
                    'example': {"successful":"login successful"}
                }
            }
        },
        400: {
            'description': 'Bad Request, invalid data',
            'content': {
                'application/json': {
                    'example': {"error": "Invalid data"}
                }
            }
        }
    }
    })
    @accept_payload
    def post(incoming_payload, self):
        data = LoginForgetSchema().load(incoming_payload)
        id = User.login(data)
        token = user_authentication_token(data, id)
        message = APIResponse('{"successful":"login successful"}', 200)
        message.headers[os.getenv('user_authorization_header_key')] = token
        
        return message

api.handle_error = handle_error
api.add_resource(Login, "/login/")
