from flask import Blueprint
from flask_restful import Resource, Api
from core.apis.decoretor import user_authorization_payload, accept_payload
from .Schema import CarDeleteSchema, VeiwCarSchema
from core.model.car import Car
from core.apis.responses import APIResponse
from core.apis.error_handler import handle_error
from flasgger import swag_from

_Veiw_car = Blueprint("to view a car", __name__)
api = Api(_Veiw_car)

class GetCarFullDetails(Resource):

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
                'description': 'car details',
                'content': {
                    'application/json': {
                        'example': {"id": "1",
                                    "user_id":"1",
                                    "url_id":"2",
                                    "title":"sedan",
                                    "tags":"favourit",
                                    "description":"i buyed at 20lac",
                                    "images":["url1","url2"]
                                    }
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
        car_view = Car.VeiwCar(data)
        car_object_dump = VeiwCarSchema(many=False).dump(car_view)
        return APIResponse.respond(car_object_dump, 200)

api.handle_error = handle_error
api.add_resource(GetCarFullDetails, "/view/")
