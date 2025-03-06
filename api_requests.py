import requests
from config import API_KEY

def get_car_data(vin):
    vin = vin.upper()
    
    url = "https://www.apipoint.ru/api/call"  # Используем HTTPS
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "sources": "gibdd",
        "vin": vin
    }

    response = requests.post(url, json=payload, headers=headers)
    
    return response.status_code, response.json()