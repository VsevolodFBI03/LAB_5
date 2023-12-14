from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from __init__ import db
from app.models import CarTaxParam, Region
from .forms import CarTaxParamAddForm, CarTaxParamDeleteForm, CarTaxParamListForm, CarTaxParamUpdateForm

car_2_bp = Blueprint('car_2', __name__)


@car_2_bp.route('/v1/car/tax-param/add', methods=['POST'])
def add_car_tax_param():
    data = request.json
    id = data.get('id')
    city_id = data.get('city_id')
    from_hp_car = data.get('from_hp_car')
    to_hp_car = data.get('to_hp_car')
    start_year = data.get('start_year')
    end_year = data.get('end_year')
    rate = data.get('rate')

    if not id or not city_id or not from_hp_car or not to_hp_car or not start_year or not end_year or not rate:
        return jsonify({'error': 'Missing data in the request'}), 400

    if not Region.query.filter_by(id=city_id).first():
        return jsonify({'error': 'Region does not exist'}), 400

    if CarTaxParam.query.filter_by(
        id=id,
        city_id=city_id,
        from_hp_car=from_hp_car,
        to_hp_car=to_hp_car,
        from_production_year_car=start_year,
        to_production_year_car=end_year
    ).first():
        return jsonify({'error': 'Car tax param already exists for this region and parameters'}), 400

    car_tax_param = CarTaxParam(
        id=id,
        city_id=city_id,
        from_hp_car=from_hp_car,
        to_hp_car=to_hp_car,
        from_production_year_car=start_year,
        to_production_year_car=end_year,
        rate=rate
    )

    db.session.add(car_tax_param)
    db.session.commit()

    return jsonify({'message': 'Car tax param added successfully'}), 200


@car_2_bp.route('/v1/car/tax-param/update', methods=['POST'])
def update_car_tax_param():
    data = request.json
    id = data.get('id')
    city_id = data.get('city_id')
    from_hp_car = data.get('from_hp_car')
    to_hp_car = data.get('to_hp_car')
    start_year = data.get('start_year')
    end_year = data.get('end_year')
    rate = data.get('rate')

    if not id or not city_id or not from_hp_car or not to_hp_car or not start_year or not end_year or not rate:
        return jsonify({'error': 'Missing data in the request'}), 400

    car_tax_param = CarTaxParam.query.get(id)
    if not car_tax_param:
        return jsonify({'error': 'Car tax param not found'}), 400

    if not Region.query.filter_by(id=city_id).first():
        return jsonify({'error': 'Region does not exist'}), 400

    car_tax_param.city_id = city_id
    car_tax_param.from_hp_car = from_hp_car
    car_tax_param.to_hp_car = to_hp_car
    car_tax_param.from_production_year_car = start_year
    car_tax_param.to_production_year_car = end_year
    car_tax_param.rate = rate

    db.session.commit()

    return jsonify({'message': 'Car tax param updated successfully'}), 200


@car_2_bp.route('/v1/car/tax-param/delete', methods=['POST'])
def delete_car_tax_param():
    id = request.json.get('id')

    if not id:
        return jsonify({'error': 'ID is required'}), 400

    car_tax_param = CarTaxParam.query.get(id)
    if not car_tax_param:
        return jsonify({'error': 'Car tax param not found'}), 400

    db.session.delete(car_tax_param)
    db.session.commit()

    return jsonify({'message': 'Car tax param deleted successfully'}), 200


@car_2_bp.route('/v1/car/tax-param/get/all', methods=['GET'])
def get_all_car_tax_params():
    car_tax_params = CarTaxParam.query.all()
    car_tax_params_list = [
        {
            'id': param.id,
            'city_id': param.city_id,
            'min_horsepower': param.from_hp_car,
            'max_horsepower': param.to_hp_car,
            'start_year': param.from_production_year_car,
            'end_year': param.to_production_year_car,
            'tax_rate': param.rate
        }
        for param in car_tax_params
    ]

    return jsonify(car_tax_params_list), 200


@car_2_bp.route('/web/car/tax-param/add', methods=['GET', 'POST'])
def add_car_tax_param_web():
    form = CarTaxParamAddForm()

    if form.validate_on_submit():
        id = form.id.data
        city_id = form.city_id.data
        from_hp_car = form.from_hp_car.data
        to_hp_car = form.to_hp_car.data
        start_year = form.start_year.data
        end_year = form.end_year.data
        rate = form.rate.data

        if CarTaxParam.query.filter_by(
            id=id,
            city_id=city_id,
            from_hp_car=from_hp_car,
            to_hp_car=to_hp_car,
            from_production_year_car=start_year,
            to_production_year_car=end_year
        ).first():
            flash('Такие параметры уже существуют!', 'danger')
        else:
            car_tax_param = CarTaxParam(
                id=id,
                city_id=city_id,
                from_hp_car=from_hp_car,
                to_hp_car=to_hp_car,
                from_production_year_car=start_year,
                to_production_year_car=end_year,
                rate=rate
            )

            db.session.add(car_tax_param)
            db.session.commit()

            flash('Параметры добавлены успешно!', 'success')
            return redirect(url_for('car_2.add_car_tax_param_web'))

    return render_template('tax-param-add.html', form=form)


@car_2_bp.route('/web/car/tax-param/update', methods=['GET', 'POST'])
def update_car_tax_param_web():
    form = CarTaxParamUpdateForm()

    if form.validate_on_submit():
        id = form.id.data
        city_id = form.city_id.data
        from_hp_car = form.from_hp_car.data
        to_hp_car = form.to_hp_car.data
        start_year = form.start_year.data
        end_year = form.end_year.data
        rate = form.rate.data

        car_tax_param = CarTaxParam.query.get(id)
        if not car_tax_param:
            return render_template('tax-param-update.html', form=form, result='Car tax param not found')

        car_tax_param.city_id = city_id
        car_tax_param.from_hp_car = from_hp_car
        car_tax_param.to_hp_car = to_hp_car
        car_tax_param.from_production_year_car = start_year
        car_tax_param.to_production_year_car = end_year
        car_tax_param.rate = rate

        db.session.commit()

        return render_template('tax-param-update.html', form=form, result='Параметры обновлены успешно!')

    return render_template('tax-param-update.html', form=form, result=None)



@car_2_bp.route('/web/car/tax-param/delete', methods=['GET', 'POST'])
def delete_car_tax_param_web():
    form = CarTaxParamDeleteForm()

    if form.validate_on_submit():
        id = form.id.data

        car_tax_param = CarTaxParam.query.get(id)
        if car_tax_param:
            db.session.delete(car_tax_param)
            db.session.commit()
            flash('Параметры удалены успешно!', 'success')
        else:
            flash('Параметры не найдены!', 'danger')

        return redirect(url_for('car_2.delete_car_tax_param_web'))

    return render_template('tax-param-delete.html', form=form)


@car_2_bp.route('/web/car/tax-param/get/all', methods=['GET', 'POST'])
def get_all_car_tax_params_web():
    form = CarTaxParamListForm()

    if form.validate_on_submit():
        car_tax_params = CarTaxParam.query.all()
        car_tax_params_list = [
            {
                'id': param.id,
                'city_id': param.city_id,
                'min_horsepower': param.from_hp_car,
                'max_horsepower': param.to_hp_car,
                'start_year': param.from_production_year_car,
                'end_year': param.to_production_year_car,
                'tax_rate': param.rate
            }
            for param in car_tax_params
        ]

        return render_template('tax-param-list.html', form=form, car_tax_params=car_tax_params_list)

    return render_template('tax-param-list.html', form=form)