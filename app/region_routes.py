from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from __init__ import db
from app.models import Region
from .forms import RegionForm, RegionListForm, RegionDeleteForm, RegionUpdateForm

region_bp = Blueprint('region_bp', __name__)


@region_bp.route('/v1/region/add', methods=['POST'])
def add_region():
    data = request.json
    name = data.get('name')
    id = data.get('id')

    if not name:
        return jsonify({'error': 'Name is required'}), 400

    if not id:
        return jsonify({'error': 'id is required'}), 400

    region = Region.query.filter_by(name=name).first()
    if region:
        return jsonify({'error': 'Region with this name already exists'}), 400

    region_2 = Region.query.filter_by(id=id).first()
    if region_2:
        return jsonify({'error': 'Region with this id already exists'}), 400

    region = Region(id=id, name=name)
    db.session.add(region)
    db.session.commit()

    return jsonify({'message': 'Region added successfully'}), 200


@region_bp.route('/v1/region/update', methods=['POST'])
def update_region():
    data = request.json
    id = data.get('id')
    new_id = data.get('new_id')

    if not id or not new_id:
        return jsonify({'error': 'ID and new_id are required'}), 400

    region = Region.query.get(id)
    if not region:
        return jsonify({'error': 'Region not found'}), 400

    region.id = new_id
    db.session.commit()

    return jsonify({'message': 'Region updated successfully'}), 200


@region_bp.route('/v1/region/delete', methods=['POST'])
def delete_region():
    id = request.json.get('id')

    if not id:
        return jsonify({'error': 'ID is required'}), 400

    region = Region.query.get(id)
    if not region:
        return jsonify({'error': 'Region not found'}), 400

    db.session.delete(region)
    db.session.commit()

    return jsonify({'message': 'Region deleted successfully'}), 200


@region_bp.route('/web/region', methods=['GET'])
def get_region_web():
    form = RegionListForm()
    regions = Region.query.all()
    return render_template('region-list.html', regions=regions, form=form)


@region_bp.route('/web/region/add', methods=['GET', 'POST'])
def add_region_web():
    form = RegionForm()

    if form.validate_on_submit():
        name = form.name.data
        number = form.number.data

        region = Region(name=name, id=number)
        db.session.add(region)
        db.session.commit()

        return render_template('region-add.html', form=form, result='Регион добавлен!')

    return render_template('region-add.html', form=form, result=None)


@region_bp.route('/web/region/update', methods=['GET', 'POST'])
def update_region_web():
    form = RegionUpdateForm()

    if form.validate_on_submit():
        id = form.id.data
        new_id = form.new_id.data

        region = Region.query.get(id)
        if not region:
            flash('Region not found', 'danger')
        else:
            region.id = new_id
            db.session.commit()
            flash('Регион обновлён!', 'success')
            return redirect(url_for('region_bp.update_region_web'))

    return render_template('region-update.html', form=form)


@region_bp.route('/web/region/delete', methods=['GET', 'POST'])
def delete_region_web():
    form = RegionDeleteForm()

    if form.validate_on_submit():
        id = form.id.data

        region = Region.query.get(id)
        if not region:
            flash('Регион не найден', 'danger')
        else:
            db.session.delete(region)
            db.session.commit()
            flash('Регион удалён!', 'success')
            return redirect(url_for('region_bp.delete_region_web'))

    return render_template('region-delete.html', form=form)