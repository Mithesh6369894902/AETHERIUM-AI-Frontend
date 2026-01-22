import requests

BASE_URL = "https://aetherium-ai-backend.onrender.com"

def post(endpoint, payload=None, files=None):
    url = f"{BASE_URL}{endpoint}"
    response = requests.post(url, json=payload, files=files)
    response.raise_for_status()
    return response.json()
