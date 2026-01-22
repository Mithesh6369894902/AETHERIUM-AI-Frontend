import streamlit as st
import pandas as pd
import requests

# -------------------- CONFIG -------------------- #
st.set_page_config(
    page_title="ModelCraft-X",
    page_icon="🧪🧬",
    layout="wide"
)

BACKEND_URL = "http://localhost:8000"

# -------------------- UI HEADER -------------------- #
st.title("🧪🧬 ModelCraft-X")
st.subheader("Cross-Validated AutoML Benchmarking Framework (Backend Powered)")
st.caption("Pipeline-based | Explainable | Reproducible")

# -------------------- DATA UPLOAD -------------------- #
uploaded_file = st.file_uploader("📤 Upload CSV Dataset", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.success("✅ Dataset Loaded Successfully")

    st.write("### 📊 Dataset Preview")
    st.dataframe(data.head(), use_container_width=True)

    # -------------------- TARGET SELECTION -------------------- #
    target_col = st.selectbox("🎯 Select Target Column", data.columns)

    if st.button("🚀 Run AutoML Benchmarking"):

        with st.spinner("⏳ Running backend AutoML benchmarking..."):
            response = requests.post(
                f"{BACKEND_URL}/modelcraft/benchmark",
                json={
                    "data": data.to_dict(orient="records"),
                    "target": target_col
                }
            )

        if response.status_code != 200:
            st.error("❌ Backend error occurred.")
            st.stop()

        result = response.json()

        # -------------------- TASK TYPE -------------------- #
        st.info(f"🧠 Detected Task Type: **{result['task_type'].upper()}**")

        # -------------------- BENCHMARK RESULTS -------------------- #
        st.subheader("📊 Cross-Validated Model Benchmarking")

        benchmark_df = pd.DataFrame(result["benchmark"])
        st.dataframe(benchmark_df, use_container_width=True)

        # -------------------- BEST MODEL -------------------- #
        st.subheader("🏆 Best Model Summary")

        col1, col2 = st.columns(2)
        col1.metric(result["metric"], round(result["final_score"], 4))
        col2.metric("Training Time (sec)", round(result["training_time"], 2))

        st.success(f"✅ Best Model: **{result['best_model']}**")

        # -------------------- EXPERIMENT LOG -------------------- #
        st.subheader("🧾 Experiment Summary")
        st.json(result["experiment_log"])

else:
    st.info("👆 Upload a CSV file to start the AutoML benchmarking process")

