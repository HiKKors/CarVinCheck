import requests
from config import API_KEY
import json
import os
from typing import Dict, Tuple, List
from datetime import datetime

import asyncio
import aiohttp


URL = "https://www.apipoint.ru/api/call"
HEADERS = {
    "Authorization": API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

SOURCES = ['gibdd', 'dtp' ,'restrict', 'wanted', 'fedresurs', 'eaisto', 'pic']

    
async def get_full_car_data_async(vin):
    vin = vin.upper()

    async with aiohttp.ClientSession() as session:
        result = {}
        for source in SOURCES:
            payload = {'sources': source, 'vin': vin}
            response = requests.post(URL, json=payload, headers=HEADERS)
            
            result[source] = response.json()

    return result