from flask import Blueprint

region_bp = Blueprint('region', __name__)
car_bp = Blueprint('car', __name__)
car_2_bp = Blueprint('car_2', __name__)

from app import region_routes, tax_route, tax_param_route


