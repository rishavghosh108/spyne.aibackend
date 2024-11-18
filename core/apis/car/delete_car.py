from flask import Blueprint
from flask_restful import Resource, Api
from core.apis.decoretor import user_authorization_payload, accept_payload
from .Schema import CarDeleteSchema
from core.model.car import Car
from core.model.images import CarImages
from core.apis.responses import APIResponse
from core.apis.error_handler import handle_error
from core import db
from flasgger import swag_from

_Delete_Car = Blueprint("to delete a car", __name__)
api = Api(_Delete_Car)

class DeleteCar(Resource):

    @swag_from({
        'tags': ['Car'],
        'description': 'Delete a car from the system based on provided car data',
        'parameters': [
            {
                'in': 'body',
                'description': 'Car data required to delete a car (e.g., car ID)',
                'required': True,
                'schema': {
                    "id":"string",
                    "user_id":"string",
                    "url_id":"string"
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
                'description': 'Car deleted successfully',
                'content': {
                    'application/json': {
                        'example': {"message": "Car has been deleted successfully"}
                    }
                }
            },
            400: {
                'description': 'Bad request, invalid data',
                'content': {
                    'application/json': {
                        'example': {"error": "Invalid car data"}
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
    @accept_payload
    def post( incoming_payload, user_id,self):
        data = CarDeleteSchema().load(incoming_payload)
        Car.Delete(data)
        db.session.commit()
        return APIResponse('{"successful":"car has been deleted"}', 200)

api.handle_error = handle_error
api.add_resource(DeleteCar, "/delete/")
