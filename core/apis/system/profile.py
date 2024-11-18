from flask import Blueprint
from flask_restful import Resource, Api
from .Schema import ProfileSchema
from core.model.user import User
from core.apis.decoretor import user_authorization_payload
from core.apis.responses import APIResponse
from core.apis.error_handler import handle_error
from flasgger import swag_from

_Profile = Blueprint("to fatch profile details", __name__)
api = Api(_Profile)

class Profile(Resource):

    @swag_from({
        'tags': ['User'],
        'description': 'Fetch User Profile Details',
        'parameters': [
            {
                'userauth': 'Authorization',
                'in': 'header',
                'description': 'User authentication token',
                'required': True,
                'type': 'string',
            }
        ],
        'responses': {
            200: {
                'description': 'User profile fetched successfully',
                'content': {
                    'application/json': {
                        'example': {
                            'name': 'John Doe',
                            'email': 'john.doe@example.com'
                        }
                    }
                }
            },
            401: {
                'description': 'Unauthorized, invalid token',
                'content': {
                    'application/json': {
                        'example': {"error": "Invalid or missing token"}
                    }
                }
            },
            404: {
                'description': 'User not found',
                'content': {
                    'application/json': {
                        'example': {"error": "User not found"}
                    }
                }
            }
        }
    })
    @user_authorization_payload
    def get( user_id,self):
        user = User.profile(user_id)
        if user:
            message = {"successful": ProfileSchema().dump(user)}
            return APIResponse.respond(message, 200)
        return APIResponse.respond({"error": "User not found"}, 404)

api.handle_error = handle_error
api.add_resource(Profile, "/profile/")
