import requests
import json

from flask import Flask, render_template
from forms import CarVinForm
from api_requests import get_full_car_data_async, main
import asyncio

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'  # Защита CSRF


@app.route('/', methods = ["GET", "POST"])
def home():
    form = CarVinForm()
    
    if form.validate_on_submit():
        vin = form.vin.data
        data = asyncio.run(get_full_car_data_async(vin))
    
    
        main_car_data = data['gibdd']['result'][0]['gibdd']['vehicle']
        ownership_periods = data['gibdd']['result'][0]['gibdd']['ownershipPeriod']
        
        if 'message' in data['eaisto']['result'][0]['eaisto']:
            TO_data = 'Данные о диагностических картах не найдены'
        else:
            TO_data = sorted(
                data['eaisto']['result'][0]['eaisto']['records'][0]['previousDcs'], 
                key=lambda x: int(x['odometerValue'])
            )
        
        damage_transcript = {}
        
        if data['dtp']['result'][0]['dtp']['records'] == []:
            dtps = 'ДТП не найдены'
        else:
            dtps = data['dtp']['result'][0]['dtp']['records'][0]
            damage_transcript = dtps['DamageTranscript']
        dtp_count = data['dtp']['result'][0]['dtp']['count']
        

        if data['fedresurs']['result'][0] == []:
            lizing = 'Авто в базе лизинга не найдено'
        elif 'message' in data['fedresurs']['result'][0]['fedresurs']:
            lizing = data['fedresurs']['result'][0]['fedresurs']['message']
        else:
            lizing = data['fedresurs']['result'][0]['fedresurs']['rez']['data']


        restrict = data['restrict']['result'][0]['restrict']

        wanted = {}
        if 'message' in data['wanted']['result'][0]['wanted']:
            wanted = data['wanted']['result'][0]['wanted']['message']
        else: 
            wanted = data['wanted']['result'][0]['wanted']['records'][0]
        
    with open('results.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        photos_list = data[1]['result'][0]['pic']['imagesList']

        return render_template(
            'main.html',
            form=form,
            result=main_car_data,
            ownership_periods=ownership_periods,
            TO_data=TO_data,
            dtps=dtps,
            dtp_count=dtp_count,
            lizing=lizing,
            restrict=restrict,
            wanted=wanted,
            damage_transcript=damage_transcript,
            photos_list = photos_list
        )
    
    return render_template('main.html', form = form)

if __name__ == '__main__':
    app.run(debug=True)