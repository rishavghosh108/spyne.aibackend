from flask import Blueprint, request
from flask_restful import Resource, Api
from core.apis.decoretor import accept_car_payload, user_authorization_payload
from .Schema import CarSchema
from core.model.car import Car
from core.apis.responses import APIResponse
from core.apis.error_handler import handle_error
from core import db
from core.apis.common import save_image
from flasgger import swag_from

_AddCar = Blueprint("for add new car", __name__)
api = Api(_AddCar)

class AddCar(Resource):

    @swag_from({
        'tags': ['Car'],
        'description': 'Add a new car to the system',
        'parameters': [
            {
                'userauth': 'Authorization',
                'in': 'header',
                'description': 'User authentication token',
                'required': True,
                'type': 'string',
            },
            {
                'name': 'body',
                'in': 'body',
                'description': 'Car details to add a new car',
                'required': True,
                'schema': {
                'type': 'object',
                'properties': {
                    'title': {'type': 'string'},
                    'description': {'type': 'string'},
                    'tags': {'type': 'string'},
                    'price': {'type': 'number', 'format': 'float'},
                    'images': {
                        'type': 'array',
                        'items': {
                            'type': 'string',
                            'format': 'uri',
                        },
                        'maxItems': 10
                    }
                },
                'required': ['title', 'tags', 'description']
            }

            }
        ],
        'responses': {
            200: {
                'description': 'Car added successfully',
                'content': {
                    'application/json': {
                        'example': {"message": "Car added successfully"}
                    }
                }
            },
            400: {
                'description': 'Invalid input',
                'content': {
                    'application/json': {
                        'example': {"error": "Invalid car details"}
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
            }
        }
    })
    @user_authorization_payload
    @accept_car_payload
    def post( user_id, incoming_payload, self):
        data = CarSchema().load(incoming_payload)
        data['user_id'] = user_id
        Car.add(data)
        db.session.commit()
        return APIResponse('{"successful":"car added successfully"}', 200)

api.handle_error = handle_error
api.add_resource(AddCar, "/addcar/")
