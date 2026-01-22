import streamlit as st
import requests

BACKEND_URL = st.secrets["BACKEND_URL"]
API_KEY = st.secrets["API_KEY"]

payload = {
    "symbol": symbol,
    "start_date": start_date,
    "end_date": end_date,
    "horizon": horizon
}

response = requests.post(
    f"{BACKEND_URL}/workflow/alphaflux/forecast",
    json=payload,
    headers={
        "X-API-Key": API_KEY
    },
    timeout=60   # 🔥 VERY IMPORTANT
)

if response.status_code == 200:
    data = response.json()
    st.success("Forecast generated")
    st.json(data)
else:
    st.error(f"Error: {response.status_code}")
