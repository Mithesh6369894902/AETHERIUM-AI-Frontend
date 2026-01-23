import streamlit as st
import numpy as np
import pandas as pd
from datetime import date, timedelta
from sklearn.linear_model import LinearRegression

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="AlphaFlux",
    page_icon="📈",
    layout="wide"
)

st.title("📈 AlphaFlux – Stock Forecasting Engine (Standalone)")
st.caption("Local forecasting demo without backend dependency")

# ---------------- USER INPUT ---------------- #
symbol = st.text_input("Stock Symbol", "AAPL")

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", date(2020, 1, 1))
with col2:
    end_date = st.date_input("End Date", date.today())

horizon = st.slider("Forecast Horizon (days)", 5, 60, 15)

# ---------------- RUN FORECAST ---------------- #
if st.button("Run Forecast"):

    # --------- SYNTHETIC HISTORICAL DATA --------- #
    days = (end_date - start_date).days
    dates = [start_date + timedelta(days=i) for i in range(days)]

    prices = np.cumsum(np.random.randn(days)) + 150

    hist_df = pd.DataFrame({
        "date": dates,
        "price": prices
    })

    # --------- MODEL --------- #
    X = np.arange(len(prices)).reshape(-1, 1)
    y = prices

    model = LinearRegression()
    model.fit(X, y)

    future_X = np.arange(len(prices), len(prices) + horizon).reshape(-1, 1)
    future_prices = model.predict(future_X)

    future_dates = [
        dates[-1] + timedelta(days=i + 1)
        for i in range(horizon)
    ]

    fore_df = pd.DataFrame({
        "date": future_dates,
        "price": future_prices
    })

    # --------- METRICS --------- #
    recent_avg = float(np.mean(y[-10:]))
    future_avg = float(np.mean(future_prices))

    signal = "BUY 📈" if future_avg > recent_avg else "SELL 📉"
    confidence = round(abs(future_avg - recent_avg) / max(recent_avg, 1), 3)

    # ---------------- DISPLAY ---------------- #
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Signal", signal)
    col2.metric("Confidence", confidence)
    col3.metric("Recent Avg Price", round(recent_avg, 2))
    col4.metric("Future Avg Price", round(future_avg, 2))

    st.subheader("📊 Price Forecast Graph")

    chart_df = pd.concat([
        hist_df.assign(type="Historical"),
        fore_df.assign(type="Forecast")
    ])

    chart_df = chart_df.set_index("date")

    st.line_chart(
        {
            "Historical": hist_df.set_index("date")["price"],
            "Forecast": fore_df.set_index("date")["price"]
        }
    )

    st.info(
        "⚠️ This is a standalone demo using synthetic data. "
        "Backend integration can be enabled later."
    )
