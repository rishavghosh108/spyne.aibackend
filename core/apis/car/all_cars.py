from flask import Blueprint
from flask_restful import Resource, Api
from core.apis.decoretor import user_authorization_payload
from .Schema import CarsSchema
from core.model.car import Car
from core.apis.responses import APIResponse
from core.apis.error_handler import handle_error
from core import db
from flasgger import swag_from

_All_Cars = Blueprint("to get all cars", __name__)
api = Api(_All_Cars)

class GetAllCars(Resource):

    @swag_from({
        'tags': ['Car'],
        'description': 'Get all cars for the authenticated user',
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
                'description': 'List of all cars',
                'content': {
                    'application/json': {
                        'example': [
                            {
                                'title': 'Car 1',
                                'description': 'Description of Car 1',
                                'tags': 'sedan',
                                'images': ['http://example.com/car1.jpg']
                            },
                            {
                                'title': 'Car 2',
                                'description': 'Description of Car 2',
                                'tags': 'SUV',
                                'images': ['http://example.com/car2.jpg']
                            }
                        ]
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
        }
    })
    @user_authorization_payload
    def get( user_id,self,):
        cars = Car.GetAll(user_id)
        cars_object = CarsSchema(many=True).dump(cars)
        return APIResponse.respond(cars_object, 200)

api.handle_error = handle_error
api.add_resource(GetAllCars, "/allcars/")
