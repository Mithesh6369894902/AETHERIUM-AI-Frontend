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
    target = st.text_input("Target Column")

    if file and target and st.button("Run Classification"):
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

                # ---- SAFE DISPLAY ----
                if "accuracy" in result:
                    st.metric("Accuracy", result["accuracy"])

                if "report" in result:
                    st.subheader("Classification Report")
                    st.text(result["report"])

                if "predictions" in result:
                    st.subheader("Sample Predictions")
                    st.write(result["predictions"][:10])

                else:
                    st.json(result)

            else:
                st.error(f"Backend error: {response.status_code}")
                st.text(response.text)

        except requests.exceptions.RequestException as e:
            st.error("Could not connect to InfernoData backend")
            st.text(str(e))

# ---------------- REGRESSION ---------------- #
elif mode == "Regression":
    file = st.file_uploader("Upload CSV", type=["csv"])
    target = st.text_input("Target Column")

    if file and target and st.button("Run Regression"):
        try:
            files = {"file": file}
            response = requests.post(
                f"{BACKEND_URL}/inferno/regress",
                files=files,
                data={"target": target},
                headers=headers,
                timeout=60
            )

            st.json(response.json())

        except requests.exceptions.RequestException as e:
            st.error("Connection failed")
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


