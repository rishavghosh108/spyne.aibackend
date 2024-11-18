from flask import Blueprint, jsonify
from flask_restful import Resource, Api
from core.apis.decoretor import accept_payload
from .Schema import UserDataSchema
from core.apis.common import gen_password
from core.apis.responses import APIResponse
from core.apis.error_handler import handle_error
from core.model.user import User
from core import db
from flasgger import swag_from

_Signup = Blueprint("sign up api", __name__)
api = Api(_Signup)

class Signup(Resource):

    @swag_from({
        'tags': ['User'],
        'description': 'User signup API',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'description': 'User signup information',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string'},
                        'email': {'type': 'string'},
                        'password': {'type': 'string'}
                    },
                    'required': ['name', 'email', 'password']
                },
            }
        ],
        'responses': {
            200: {
                'description': 'Signup Successful',
                'content': {
                    'application/json': {
                        'example': {"successful":"Signup Successful"}
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
    def post( incoming_payload, self):
        data = UserDataSchema().load(incoming_payload)
        data['password'] = gen_password(data['password'])
        User.signup(data)
        db.session.commit()
        return APIResponse('{"successful":"Signup Successful"}', 200)


api.handle_error = handle_error
api.add_resource(Signup, '/signup/')
