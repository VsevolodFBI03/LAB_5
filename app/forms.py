from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DecimalField
from wtforms.validators import DataRequired, NumberRange


class RegionForm(FlaskForm):
    name = StringField('Название региона:', validators=[DataRequired()])
    number = IntegerField('Код региона:', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class RegionListForm(FlaskForm):
    pass


class RegionDeleteForm(FlaskForm):
    id = IntegerField('Код региона, который нужно удалить:', validators=[DataRequired()])
    submit = SubmitField('Удалить')


class RegionUpdateForm(FlaskForm):
    id = IntegerField('Код региона, который нужно изменить:', validators=[DataRequired()])
    new_id = IntegerField('Новый код региона:', validators=[DataRequired()])
    submit = SubmitField('Обновить')


class CarTaxParamAddForm(FlaskForm):
    id = IntegerField('ID:', validators=[DataRequired()])
    city_id = IntegerField('Код региона:', validators=[DataRequired()])
    from_hp_car = IntegerField('Мощность (мин):', validators=[DataRequired()])
    to_hp_car = IntegerField('Мощность (макс):', validators=[DataRequired()])
    start_year = IntegerField('Начало производства', validators=[DataRequired()])
    end_year = IntegerField('Конец производства:', validators=[DataRequired()])
    rate = StringField('Налоговая ставка:', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class CarTaxParamDeleteForm(FlaskForm):
    id = IntegerField('ID:', validators=[DataRequired()])
    submit = SubmitField('Удалить')


class CarTaxParamListForm(FlaskForm):
    submit = SubmitField('Обновить')


class CarTaxParamUpdateForm(FlaskForm):
    id = IntegerField('ID', validators=[DataRequired()])
    city_id = IntegerField('Код региона', validators=[DataRequired()])
    from_hp_car = IntegerField('Мощность (мин)', validators=[DataRequired(), NumberRange(min=0)])
    to_hp_car = IntegerField('Мощность (макс)', validators=[DataRequired(), NumberRange(min=0)])
    start_year = IntegerField('Начало производства', validators=[DataRequired()])
    end_year = IntegerField('Конец производства', validators=[DataRequired()])
    rate = DecimalField('Налоговая ставка', validators=[DataRequired()])


class CarTaxCalcForm(FlaskForm):
    city_id = StringField('Код региона', validators=[DataRequired()])
    horsepower = IntegerField('Мощность', validators=[DataRequired()])
    year = IntegerField('Год производства', validators=[DataRequired()])
    submit = SubmitField('Рассчитать налог')
