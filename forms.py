from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class CarVinForm(FlaskForm):
    vin = StringField('Введите Vin:', validators=[DataRequired()])
    submit = SubmitField('Получить данные')