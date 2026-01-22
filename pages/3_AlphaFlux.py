import streamlit as st
import requests
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt

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
                timeout=60
            )

            if response.status_code == 200:
                data = response.json()
                st.success("Forecast generated successfully")

                # ---------------- METRICS ---------------- #
                colA, colB, colC, colD = st.columns(4)
                colA.metric("Signal", data.get("signal", "N/A"))
                colB.metric("Confidence", round(data.get("confidence", 0), 3))
                colC.metric("Recent Avg Price", round(data.get("recent_avg", 0), 2))
                colD.metric("Future Avg Price", round(data.get("future_avg", 0), 2))

                # ---------------- GRAPH ---------------- #
                historical = data.get("historical", [])
                forecast = data.get("forecast", [])

                if historical and forecast:
                    hist_df = pd.DataFrame(historical)
                    fore_df = pd.DataFrame(forecast)

                    fig, ax = plt.subplots(figsize=(12, 5))

                    ax.plot(
                        hist_df["date"],
                        hist_df["price"],
                        label="Historical",
                        color="blue"
                    )

                    ax.plot(
                        fore_df["date"],
                        fore_df["price"],
                        linestyle="--",
                        label="Forecast",
                        color="orange"
                    )

                    ax.set_title(f"{symbol} Price Forecast")
                    ax.set_xlabel("Date")
                    ax.set_ylabel("Price")
                    ax.legend()
                    ax.grid(True)

                    st.pyplot(fig)

                else:
                    st.warning("No graph data returned from backend")

            else:
                st.error(f"Backend error: {response.status_code}")
                st.text(response.text)

        except requests.exceptions.RequestException as e:
            st.error("Could not connect to backend")
            st.text(str(e))

