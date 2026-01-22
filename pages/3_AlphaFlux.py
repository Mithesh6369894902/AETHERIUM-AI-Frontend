import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="AlphaFlux",
    page_icon="🧠📈",
    layout="wide"
)

BACKEND_URL = "http://localhost:8000"

st.title("🧠📈 AlphaFlux")
st.caption("Risk-Aware Stock Trend Forecasting & Decision Intelligence (Backend Powered)")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Controls")

symbol = st.sidebar.text_input("Stock Symbol", "AAPL")
start_date = st.sidebar.date_input("Start Date", datetime(2020, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.today())
forecast_horizon = st.sidebar.slider("Forecast Days", 5, 60, 20)

if st.sidebar.button("🚀 Run Forecast"):

    with st.spinner("Running AlphaFlux workflow..."):
        response = requests.post(
            f"{BACKEND_URL}/workflow/alphaflux/forecast",
            json={
                "symbol": symbol,
                "start_date": str(start_date),
                "end_date": str(end_date),
                "horizon": forecast_horizon
            }
        )

    if response.status_code != 200:
        st.error("Backend error. Please try again.")
        st.stop()

    result = response.json()

    # ---------------- DATA ----------------
    hist_df = pd.DataFrame(result["historical"])
    hist_df["date"] = pd.to_datetime(hist_df["date"])

    forecast_df = pd.DataFrame(result["forecast"])
    forecast_df["date"] = pd.to_datetime(forecast_df["date"])

    # ---------------- VISUALIZATION ----------------
    st.subheader("📊 Price Trend Analysis")

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(hist_df["date"], hist_df["close"], label="Historical Close", color="blue")
    ax.plot(forecast_df["date"], forecast_df["price"], "--", label="Forecast", color="orange")
    ax.set_title(f"{symbol} Price Trend")
    ax.legend()
    st.pyplot(fig)

    # ---------------- METRICS ----------------
    col1, col2, col3 = st.columns(3)

    col1.metric("Recent Avg Price", f"${result['recent_avg']:.2f}")
    col2.metric("Predicted Avg Price", f"${result['future_avg']:.2f}")
    col3.metric("Model Uncertainty (MAE)", f"${result['mae']:.2f}")

    # ---------------- DECISION ----------------
    st.subheader("🧠 Decision Intelligence")

    st.markdown(f"""
    ### **Trading Signal:** {result['signal']}

    - **Risk-adjusted confidence score:** `{result['confidence']:.2f}`
    - **Interpretation:**  
      Recommendation is derived from **trend strength relative to historical prediction error**.
    """)

    # ---------------- TABLE ----------------
    st.subheader("🔮 Forecast Table")
    st.dataframe(forecast_df, use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("⚠️ Educational use only. Not financial advice.")

