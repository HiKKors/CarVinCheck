from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

import re

class CarVinForm(FlaskForm):
    vin = StringField('Введите Vin:', validators=[DataRequired()])
    submit = SubmitField('Получить данные')
    
    def validate_vin(self, field):
        vin = field.data.upper()
        
        # Проверка длины
        if len(vin) != 17:
            raise ValidationError("VIN должен содержать 17 символов")
        
        # Проверка на запрещённые символы (I, O, Q)
        if re.search(r'[IOQ]', vin):
            raise ValidationError("VIN не должен содержать буквы I, O, Q")
        
        # Проверка на допустимые символы (A-Z, 0-9)
        if not re.fullmatch(r'^[A-HJ-NPR-Z0-9]{17}$', vin):
            raise ValidationError("VIN может содержать только латинские буквы (кроме I, O, Q) и цифры")
        
        
class CarBodyNumberForm(FlaskForm):
    bodyNumber = StringField("Ведите номер кузова:", validators=[DataRequired()])
    submit = SubmitField('Получить данные')