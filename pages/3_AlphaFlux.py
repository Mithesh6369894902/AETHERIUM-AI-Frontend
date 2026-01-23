import streamlit as st
import requests
from datetime import date

st.set_page_config(page_title="AlphaFlux", page_icon="📈", layout="wide")

st.title("📈 AlphaFlux – Stock Forecasting Engine")

# 🔐 Load secrets
BACKEND_URL = st.secrets["BACKEND_URL"]
API_KEY = st.secrets["API_KEY"]

# ---------------- UI INPUTS ---------------- #
symbol = st.text_input("Stock Symbol", value="AAPL")

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", value=date(2020, 1, 1))
with col2:
    end_date = st.date_input("End Date", value=date.today())

horizon = st.slider("Forecast Horizon (days)", 5, 60, 10)

# ---------------- ACTION ---------------- #
if st.button("Run Forecast"):
    payload = {
        "symbol": symbol,
        "start_date": str(start_date),
        "end_date": str(end_date),
        "horizon": horizon
    }

    with st.spinner("Contacting AlphaFlux engine..."):
        try:
            response = requests.post(
                f"{BACKEND_URL}/workflow/alphaflux/forecast",
                json=payload,
                headers={"X-API-Key": API_KEY},
                timeout=60   # IMPORTANT for Render
            )

            if response.status_code == 200:
                data = response.json()
                st.success("Forecast generated successfully")

                st.metric("Signal", data["signal"])
                st.metric("Confidence", data["confidence"])
                st.metric("Recent Avg Price", data["recent_avg"])
                st.metric("Future Avg Price", data["future_avg"])

            else:
                st.error(f"Backend error: {response.status_code}")
                st.text(response.text)

        except requests.exceptions.RequestException as e:
            st.error("Could not connect to backend")
            st.text(str(e))
