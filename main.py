import requests

url = "https://www.apipoint.ru/api/call"  # Используем HTTPS
headers = {
    "Authorization": "Bearer kd3yDFfLmP6xP0jwGkGlYBd7eUFn6G9EBwFawZ5Z1194ac7b",  # Ваш токен
    "Content-Type": "application/json",
    "Accept": "application/json"
}
payload = {
    "sources": "number2vin",
    "gosnomer": "С701НО30"
}

response = requests.post(url, json=payload, headers=headers)

print("HTTP Status:", response.status_code)  # Код ответа
print(response.text) 