import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="InfernoData", page_icon="🔥", layout="wide")
st.title("🔥 InfernoData – Dataset Engineering Engine")

# 🔐 Load secrets
BACKEND_URL = st.secrets["BACKEND_URL"]
API_KEY = st.secrets["API_KEY"]

headers = {"X-API-Key": API_KEY}

# ---------------- SIDEBAR ---------------- #
mode = st.sidebar.radio(
    "Select Operation",
    [
        "Dataset Generator",
        "Dataset Trimmer",
        "Classification",
        "Regression",
        "Clustering",
        "Association Rules"
    ]
)

# ---------------- DATASET GENERATOR ---------------- #
if mode == "Dataset Generator":
    rows = st.slider("Rows", 10, 500, 100)
    cols = st.slider("Columns", 2, 10, 4)

    if st.button("Generate Dataset"):
        try:
            response = requests.post(
                f"{BACKEND_URL}/inferno/generate",
                json={"rows": rows, "cols": cols},
                headers=headers,
                timeout=60
            )

            if response.status_code == 200:
                df = pd.DataFrame(response.json())
                st.success("Dataset generated")
                st.dataframe(df)
            else:
                st.error(f"Backend error: {response.status_code}")
                st.text(response.text)

        except requests.exceptions.RequestException as e:
            st.error("Could not connect to InfernoData backend")
            st.text(str(e))

# ---------------- DATASET TRIMMER ---------------- #
elif mode == "Dataset Trimmer":
    file = st.file_uploader("Upload CSV", type=["csv"])
    if file and st.button("Trim Dataset"):
        try:
            files = {"file": file}
            response = requests.post(
                f"{BACKEND_URL}/inferno/trim",
                files=files,
                headers=headers,
                timeout=60
            )

            if response.status_code == 200:
                df = pd.DataFrame(response.json())
                st.success("Dataset trimmed")
                st.dataframe(df)
            else:
                st.error(f"Backend error: {response.status_code}")
                st.text(response.text)

        except requests.exceptions.RequestException as e:
            st.error("Connection failed")
            st.text(str(e))

# ---------------- CLASSIFICATION ---------------- #
elif mode == "Classification":
    file = st.file_uploader("Upload CSV", type=["csv"])

    if file:
        df = pd.read_csv(file)
        st.subheader("Dataset Preview")
        st.dataframe(df.head())

        # 🔥 VALID TARGET FILTER
        valid_targets = [
            col for col in df.columns
            if df[col].nunique() <= 10
        ]

        if not valid_targets:
            st.error("No valid classification target found (need categorical column)")
            st.stop()

        target = st.selectbox(
            "Select Target Column (Classification Labels)",
            valid_targets
        )

        st.info("Recommended target: Outcome")

        if st.button("Run Classification"):
            try:
                files = {
                    "file": (
                        file.name,
                        file.getvalue(),
                        file.type
                    )
                }

                response = requests.post(
                    f"{BACKEND_URL}/inferno/classify",
                    files=files,
                    data={"target": target},
                    headers=headers,
                    timeout=60
                )

                if response.status_code == 200:
                    result = response.json()
                    st.success("Classification completed")

                    if "accuracy" in result:
                        st.metric("Accuracy", result["accuracy"])

                    if "report" in result:
                        st.subheader("Classification Report")
                        st.text(result["report"])

                    if "predictions" in result:
                        st.subheader("Sample Predictions")
                        st.write(result["predictions"][:10])

                else:
                    st.error(f"Backend error: {response.status_code}")
                    st.json(response.json())

            except Exception as e:
                st.error("Classification failed")
                st.text(str(e))

# ---------------- REGRESSION ---------------- #
# ---------------- REGRESSION ---------------- #
elif mode == "Regression":
    file = st.file_uploader("Upload CSV", type=["csv"])

    if file:
        # Load dataset locally for column inspection
        df = pd.read_csv(file)

        st.subheader("Dataset Preview")
        st.dataframe(df.head(), use_container_width=True)

        # Filter numeric columns ONLY (regression-safe)
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

        if len(numeric_cols) < 2:
            st.error("Dataset must contain at least 2 numeric columns for regression")
            st.stop()

        target = st.selectbox(
            "Select Target Column (Regression Output)",
            numeric_cols
        )

        st.info(f"Selected target: {target}")

        if st.button("Run Regression"):
            try:
                files = {
                    "file": (
                        file.name,
                        file.getvalue(),
                        file.type
                    )
                }

                response = requests.post(
                    f"{BACKEND_URL}/inferno/regress",
                    files=files,
                    data={"target": target},
                    headers=headers,
                    timeout=60
                )

                if response.status_code == 200:
                    result = response.json()
                    st.success("Regression completed")

                    # ---- ALWAYS SHOW RAW RESULT ----
                    st.subheader("📦 Backend Output")
                    st.json(result)

                    # ---- SMART METRICS ----
                    if "r2" in result:
                        st.metric("R² Score", result["r2"])

                    if "rmse" in result:
                        st.metric("RMSE", result["rmse"])

                    if "mae" in result:
                        st.metric("MAE", result["mae"])

                    if "predictions" in result:
                        st.subheader("Sample Predictions")
                        st.write(result["predictions"][:10])

                    if "y_pred" in result:
                        st.subheader("Sample Predictions")
                        st.write(result["y_pred"][:10])

                else:
                    st.error(f"Backend error: {response.status_code}")
                    st.text(response.text)

            except requests.exceptions.RequestException as e:
                st.error("Could not connect to InfernoData backend")
                st.text(str(e))


# ---------------- CLUSTERING ---------------- #
elif mode == "Clustering":
    file = st.file_uploader("Upload CSV", type=["csv"])
    k = st.slider("Clusters (k)", 2, 10, 3)

    if file and st.button("Run Clustering"):
        try:
            files = {"file": file}
            response = requests.post(
                f"{BACKEND_URL}/inferno/cluster",
                files=files,
                data={"k": k},
                headers=headers,
                timeout=60
            )

            st.json(response.json())

        except requests.exceptions.RequestException as e:
            st.error("Connection failed")
            st.text(str(e))

# ---------------- ASSOCIATION RULES ---------------- #
elif mode == "Association Rules":
    file = st.file_uploader("Upload Transaction CSV", type=["csv"])

    if file and st.button("Run Association Mining"):
        try:
            files = {"file": file}
            response = requests.post(
                f"{BACKEND_URL}/inferno/associate",
                files=files,
                headers=headers,
                timeout=60
            )

            st.json(response.json())

        except requests.exceptions.RequestException as e:
            st.error("Connection failed")
            st.text(str(e))


