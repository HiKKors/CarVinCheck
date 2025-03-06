import requests

from flask import Flask, render_template
from forms import CarVinForm
from api_requests import get_car_data

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'  # Защита CSRF


@app.route('/', methods = ["GET", "POST"])
def home():
    form = CarVinForm()
    result = None
    
    if form.validate_on_submit():
        vin = form.vin.data
        status, data = get_car_data(vin)
        result = {"status": status, "data": data}
    
    return render_template('main.html', form = form, result = result)

if __name__ == '__main__':
    app.run(debug=True)