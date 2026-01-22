import streamlit as st
import requests
import pandas as pd
import base64
import matplotlib.pyplot as plt

# ---------------- CONFIG ---------------- #
st.set_page_config(
    page_title="InfernoData",
    page_icon="🔥📊",
    layout="wide"
)

BACKEND_URL = "http://localhost:8000"

st.title("🔥📊 InfernoData")
st.caption("Advanced Dataset Engineering & ML Validation Platform")

# ---------------- SIDEBAR ---------------- #
page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Home",
        "🧪 Dataset Generator",
        "✂️ Dataset Trimmer",
        "🧠 Classification Execution",
        "📉 Regression Execution",
        "🧩 Clustering Execution",
        "🔗 Association Rule Mining"
    ]
)

# ---------------- UTIL ---------------- #
def download_csv(df, name):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    st.markdown(
        f'<a href="data:file/csv;base64,{b64}" download="{name}">⬇️ Download CSV</a>',
        unsafe_allow_html=True
    )

# ---------------- HOME ---------------- #
if page == "🏠 Home":
    st.markdown("""
    ## 🔥 InfernoData
    InfernoData is the dataset engineering layer of ÆTHERIUM.
    All dataset processing and ML validation are executed via
    a centralized backend for scalability and reuse.
    """)

# ---------------- DATASET GENERATOR ---------------- #
elif page == "🧪 Dataset Generator":
    st.header("🧪 Synthetic Dataset Generator")

    rows = st.slider("Rows", 10, 500, 100)
    cols = st.slider("Columns", 2, 10, 4)

    if st.button("🔥 Generate Dataset"):
        response = requests.post(
            f"{BACKEND_URL}/inferno/generate",
            json={"rows": rows, "cols": cols}
        )

        df = pd.DataFrame(response.json()["data"])
        st.dataframe(df.head())
        download_csv(df, "synthetic_dataset.csv")

# ---------------- DATASET TRIMMER ---------------- #
elif page == "✂️ Dataset Trimmer":
    st.header("✂️ Dataset Trimmer")

    file = st.file_uploader("Upload CSV", type=["csv"])
    if file:
        df = pd.read_csv(file)
        st.write("Original Shape:", df.shape)

        cols = st.multiselect("Select Columns", df.columns.tolist())
        rows = st.slider("Rows", 1, len(df), min(100, len(df)))

        if st.button("Trim Dataset"):
            response = requests.post(
                f"{BACKEND_URL}/inferno/trim",
                json={
                    "data": df.to_dict(orient="records"),
                    "columns": cols,
                    "rows": rows
                }
            )

            trimmed = pd.DataFrame(response.json()["data"])
            st.dataframe(trimmed.head())
            download_csv(trimmed, "trimmed_dataset.csv")

# ---------------- CLASSIFICATION ---------------- #
elif page == "🧠 Classification Execution":
    st.header("🧠 Classification Validation")

    file = st.file_uploader("Upload Dataset", type=["csv"])
    if file:
        df = pd.read_csv(file)
        target = st.selectbox("Target Column", df.columns)

        model_type = st.radio("Model", ["LogisticRegression", "DecisionTree"])

        if st.button("Train & Validate"):
            response = requests.post(
                f"{BACKEND_URL}/inferno/classification",
                json={
                    "data": df.to_dict(orient="records"),
                    "target": target,
                    "model": model_type
                }
            )

            st.metric("Accuracy", response.json()["accuracy"])
            st.text(response.json()["report"])

# ---------------- REGRESSION ---------------- #
elif page == "📉 Regression Execution":
    st.header("📉 Regression Validation")

    file = st.file_uploader("Upload Dataset", type=["csv"])
    if file:
        df = pd.read_csv(file)
        target = st.selectbox("Target Column", df.columns)
        model_type = st.radio("Model", ["Linear", "Ridge"])

        if st.button("Train & Validate"):
            response = requests.post(
                f"{BACKEND_URL}/inferno/regression",
                json={
                    "data": df.to_dict(orient="records"),
                    "target": target,
                    "model": model_type
                }
            )

            st.metric("MAE", response.json()["mae"])
            st.metric("MSE", response.json()["mse"])
            st.metric("R2", response.json()["r2"])

# ---------------- CLUSTERING ---------------- #
elif page == "🧩 Clustering Execution":
    st.header("🧩 Clustering Validation")

    file = st.file_uploader("Upload Dataset", type=["csv"])
    if file:
        df = pd.read_csv(file)
        k = st.slider("Clusters", 2, 10, 3)

        if st.button("Run Clustering"):
            response = requests.post(
                f"{BACKEND_URL}/inferno/clustering",
                json={
                    "data": df.to_dict(orient="records"),
                    "k": k
                }
            )

            clustered = pd.DataFrame(response.json()["data"])
            st.dataframe(clustered.head())

# ---------------- ASSOCIATION ---------------- #
elif page == "🔗 Association Rule Mining":
    st.header("🔗 Association Rule Mining")

    file = st.file_uploader("Upload Transaction CSV", type=["csv"])
    if file:
        df = pd.read_csv(file, header=None)

        if st.button("Generate Rules"):
            response = requests.post(
                f"{BACKEND_URL}/inferno/association",
                json={
                    "transactions": df.iloc[:, 0].tolist()
                }
            )

            rules = pd.DataFrame(response.json()["rules"])
            st.dataframe(rules)

