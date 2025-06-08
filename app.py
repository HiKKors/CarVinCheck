import requests
import json

from flask import Flask, render_template
from forms import CarVinForm, CarBodyNumberForm
from api_requests import get_full_car_data_async
import asyncio

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'  # Защита CSRF

@app.route('/', methods=['GET'])
def index():
    vin_form = CarVinForm(prefix='vin')
    body_form = CarBodyNumberForm(prefix='body')
    
    return render_template('main.html', vin_form=vin_form, body_form=body_form, active_form='vin')

@app.route('/check-vin', methods=['POST'])
def check_vin():
    vin_form = CarVinForm(prefix='vin')
    body_form = CarBodyNumberForm(prefix='body')
    
    if vin_form.validate_on_submit():
        data = asyncio.run(get_full_car_data_async(vin_form.vin.data))
        
        return render_results(data, 'vin')
    
    return render_template('main.html', vin_form=vin_form, body_form=body_form, active_form='vin')

@app.route('/check-body', methods=['POST'])
def check_body():
    vin_form = CarVinForm(prefix='vin')
    body_form = CarBodyNumberForm(prefix='body')
    
    if body_form.validate_on_submit():
        data = asyncio.run(get_full_car_data_async(vin_form.vin.data))
        
        return render_results(data, 'vin')
    
    return render_template('main.html', vin_form=vin_form, body_form=body_form, active_form='vin')


def render_results(data, active_form):
    vin_form = CarVinForm(prefix='vin')
    body_form = CarBodyNumberForm(prefix='body')
    
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
    
    photos_list = data['pic']['result'][0]['pic']['imageList']

    return render_template(
        'main.html',
        vin_form=vin_form,
        body_form=body_form,
        active_form=active_form,
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

# @app.route('/', methods = ["GET", "POST"])
# def home():
#     form = CarVinForm()
    
#     if form.validate_on_submit():
#         vin = form.vin.data
#         data = asyncio.run(get_full_car_data_async(vin))
    
    
#         main_car_data = data['gibdd']['result'][0]['gibdd']['vehicle']
#         ownership_periods = data['gibdd']['result'][0]['gibdd']['ownershipPeriod']
        
#         if 'message' in data['eaisto']['result'][0]['eaisto']:
#             TO_data = 'Данные о диагностических картах не найдены'
#         else:
#             TO_data = sorted(
#                 data['eaisto']['result'][0]['eaisto']['records'][0]['previousDcs'], 
#                 key=lambda x: int(x['odometerValue'])
#             )
        
#         damage_transcript = {}
        
#         if data['dtp']['result'][0]['dtp']['records'] == []:
#             dtps = 'ДТП не найдены'
#         else:
#             dtps = data['dtp']['result'][0]['dtp']['records'][0]
#             damage_transcript = dtps['DamageTranscript']
#         dtp_count = data['dtp']['result'][0]['dtp']['count']
        

#         if data['fedresurs']['result'][0] == []:
#             lizing = 'Авто в базе лизинга не найдено'
#         elif 'message' in data['fedresurs']['result'][0]['fedresurs']:
#             lizing = data['fedresurs']['result'][0]['fedresurs']['message']
#         else:
#             lizing = data['fedresurs']['result'][0]['fedresurs']['rez']['data']


#         restrict = data['restrict']['result'][0]['restrict']

#         wanted = {}
#         if 'message' in data['wanted']['result'][0]['wanted']:
#             wanted = data['wanted']['result'][0]['wanted']['message']
#         else: 
#             wanted = data['wanted']['result'][0]['wanted']['records'][0]
        
#         photos_list = set(data['pic']['result'][0]['pic']['imageList'])

#         return render_template(
#             'main.html',
#             form=form,
#             result=main_car_data,
#             ownership_periods=ownership_periods,
#             TO_data=TO_data,
#             dtps=dtps,
#             dtp_count=dtp_count,
#             lizing=lizing,
#             restrict=restrict,
#             wanted=wanted,
#             damage_transcript=damage_transcript,
#             photos_list = photos_list
#         )
    
#     return render_template('main.html', form = form)

if __name__ == '__main__':
    app.run(debug=True)