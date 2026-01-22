import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="ModelCraft-X", page_icon="🧬", layout="wide")
st.title("🧬 ModelCraft-X – AutoML Benchmarking Engine")

# 🔐 Load secrets
BACKEND_URL = st.secrets["BACKEND_URL"]
API_KEY = st.secrets["API_KEY"]

headers = {"X-API-Key": API_KEY}

# ---------------- DATA UPLOAD ---------------- #
uploaded_file = st.file_uploader("Upload CSV Dataset", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("Dataset loaded successfully")
    st.dataframe(df.head(), use_container_width=True)

    target = st.selectbox("Select Target Column", df.columns)

    if st.button("Run ModelCraft-X Benchmark"):
        payload = {
            "data": df.to_dict(orient="records"),
            "target": target
        }

        with st.spinner("Running AutoML benchmarking..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/modelcraft/benchmark",
                    json=payload,
                    headers=headers,
                    timeout=60  # 🔥 CRITICAL
                )

                if response.status_code == 200:
                    result = response.json()
                    st.success("Benchmark completed")

                    st.subheader("🏆 Best Model")
                    st.write(result.get("best_model", "N/A"))


                    st.subheader("📊 Benchmark Results")
                    st.table(pd.DataFrame(result["benchmark"]))

                    st.metric(
                        result["metric"],
                        result["final_score"]
                    )

                else:
                    st.error(f"Backend error: {response.status_code}")
                    st.text(response.text)

            except requests.exceptions.RequestException as e:
                st.error("Could not connect to ModelCraft-X backend")
                st.text(str(e))


