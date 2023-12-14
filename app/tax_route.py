from flask import Blueprint, request, jsonify, render_template
from __init__ import db
from app.models import CarTaxParam, Region
from .forms import CarTaxCalcForm

car_bp = Blueprint('car', __name__)


@car_bp.route('/v1/car/tax/calc', methods=['GET', 'POST'])
def calculate_car_tax():
    form = CarTaxCalcForm()
    result = None

    if form.validate_on_submit():
        city_id = form.city_id.data
        horsepower = form.horsepower.data
        year = form.year.data

        car_tax_param = CarTaxParam.query.filter(
            CarTaxParam.city_id == city_id,
            CarTaxParam.from_hp_car <= horsepower,
            CarTaxParam.from_production_year_car <= year,
            CarTaxParam.to_production_year_car >= year
        ).first()

        if car_tax_param:
            tax = int(car_tax_param.rate) * int(horsepower)
            result = f'Налог: {tax}'
        else:
            result = 'This car tax param found'

    return render_template('index.html', form=form, result=result)


@car_bp.route('/', methods=['GET'])
def index():
    form = CarTaxCalcForm()
    return render_template('index.html', form=form)