from flask import Blueprint

from .add_car import _AddCar
from .all_cars import _All_Cars
from .delete_car import _Delete_Car
from .veiw_car import _Veiw_car
from .update_details import _UpdateCar

_Cars_Apis=Blueprint('all car related apis', __name__, url_prefix='/car')

_Cars_Apis.register_blueprint(_AddCar)
_Cars_Apis.register_blueprint(_All_Cars)
_Cars_Apis.register_blueprint(_Delete_Car)
_Cars_Apis.register_blueprint(_Veiw_car)
_Cars_Apis.register_blueprint(_UpdateCar)