import requests

BASE_URL = "http://localhost:8000"

def post(endpoint, payload=None, files=None):
    url = f"{BASE_URL}{endpoint}"
    response = requests.post(url, json=payload, files=files)
    response.raise_for_status()
    return response.json()
