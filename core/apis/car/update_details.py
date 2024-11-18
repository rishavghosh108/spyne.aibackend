from flask import Blueprint
from flask_restful import Resource, Api
from core.apis.decoretor import accept_payload, user_authorization_payload
from .Schema import UpdateCarSchema
from core.model.car import Car
from core.apis.responses import APIResponse
from core.apis.error_handler import handle_error
from core import db
from flasgger import swag_from

_UpdateCar = Blueprint("for update car details", __name__)
api = Api(_UpdateCar)

class UpdateCar(Resource):

    @swag_from({
        'tags': ['Car'],
        'description': 'View full details of a car',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'description': 'Car ID for viewing details',
                'required': True,
                'schema':{"id" :"string",
                        "user_id" :"string",
                        "url_id" :"string",
                        "title" : "string",
                        "description" :"string",
                        "tags" : "string",
                        "deleted":"array[indexs of deleted images]"
                        }
            },
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
                'description': 'Car details retrieved successfully',
                'content': {
                    'application/json': {
                        'example': {"message": "Car has been deleted successfully"}
                    }
                }
            },
            400: {
                'description': 'Bad request, invalid data'
            },
            401: {
                'description': 'Unauthorized, invalid token'
            }
        }
    })

    @user_authorization_payload
    @accept_payload
    def post( incoming_payload, user_id,self):
        data = UpdateCarSchema().load(incoming_payload)
        Car.UpdateCarDetails(data)
        db.session.commit()
        return APIResponse('{"successful":"update successfully"}', 200)

api.handle_error = handle_error
api.add_resource(UpdateCar, "/update/")
