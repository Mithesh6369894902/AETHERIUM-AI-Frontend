import streamlit as st
import requests
from datetime import date

st.set_page_config(page_title="AlphaFlux", page_icon="📈", layout="wide")
st.title("📈 AlphaFlux – Stock Forecasting Engine")

BACKEND_URL = st.secrets["BACKEND_URL"]
API_KEY = st.secrets["API_KEY"]

symbol = st.text_input("Stock Symbol", "AAPL")

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", date(2020, 1, 1))
with col2:
    end_date = st.date_input("End Date", date.today())

horizon = st.slider("Forecast Horizon (days)", 5, 60, 10)

if st.button("Run Forecast"):
    payload = {
        "symbol": symbol,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "horizon": horizon
    }

    try:
        response = requests.post(
            f"{BACKEND_URL}/workflow/alphaflux/forecast",
            json=payload,
            headers={"X-API-Key": API_KEY},
            timeout=60
        )

        if response.status_code == 200:
            data = response.json()

            st.metric("Signal", data["signal"])
            st.metric("Confidence", data["confidence"])
            st.metric("Recent Avg", data["recent_avg"])
            st.metric("Future Avg", data["future_avg"])

            hist = data["historical"]
            fore = data["forecast"]

            if hist and fore:
                import pandas as pd

                hist_df = pd.DataFrame(hist)
                fore_df = pd.DataFrame(fore)

                st.line_chart(
                    {
                        "Historical": hist_df.set_index("date")["price"],
                        "Forecast": fore_df.set_index("date")["price"]
                    }
                )
            else:
                st.warning("No graph data returned from backend")

        else:
            st.error(f"Backend error: {response.status_code}")
            st.text(response.text)

    except Exception as e:
        st.error("Connection failed")
        st.text(str(e))

