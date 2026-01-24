import streamlit as st
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, r2_score

from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC, SVR

# ---------------- STREAMLIT CONFIG ---------------- #
st.set_page_config(
    page_title="ModelCraft-X",
    page_icon="🧬",
    layout="wide"
)

st.title("🧬 ModelCraft-X – AutoML Benchmarking Engine (Frontend Only)")

# ---------------- DATA UPLOAD ---------------- #
uploaded_file = st.file_uploader("Upload CSV Dataset", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("Dataset loaded successfully")
    st.dataframe(df.head(), use_container_width=True)

    target = st.selectbox("Select Target Column", df.columns)

    if st.button("Run ModelCraft-X Benchmark"):

        with st.spinner("Running AutoML benchmarking locally..."):

            data = df.copy()

            # ---------------- PREPROCESSING ---------------- #
            X = data.drop(columns=[target])
            y = data[target]

            # Encode categorical features
            for col in X.select_dtypes(include=["object"]).columns:
                X[col] = LabelEncoder().fit_transform(X[col])

            # Detect problem type
            task_type = "classification" if y.nunique() <= 20 else "regression"

            if task_type == "classification" and y.dtype == "object":
                y = LabelEncoder().fit_transform(y)

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            # ---------------- MODEL ZOO ---------------- #
            if task_type == "classification":
                models = {
                    "Logistic Regression": LogisticRegression(max_iter=1000),
                    "Random Forest": RandomForestClassifier(),
                    "SVM": SVC()
                }
                metric_name = "Accuracy"
                scorer = accuracy_score

            else:
                models = {
                    "Linear Regression": LinearRegression(),
                    "Random Forest Regressor": RandomForestRegressor(),
                    "SVR": SVR()
                }
                metric_name = "R² Score"
                scorer = r2_score

            results = []
            best_score = -np.inf
            best_model = None

            # ---------------- BENCHMARKING ---------------- #
            for name, model in models.items():
                pipeline = Pipeline([
                    ("scaler", StandardScaler()),
                    ("model", model)
                ])

                pipeline.fit(X_train, y_train)
                preds = pipeline.predict(X_test)
                score = scorer(y_test, preds)

                results.append({
                    "Model": name,
                    metric_name: round(score, 4)
                })

                if score > best_score:
                    best_score = score
                    best_model = name

        # ---------------- RESULTS ---------------- #
        st.success("Benchmark completed")

        st.subheader("🏆 Best Model")
        st.write(best_model)

        st.subheader("📊 Benchmark Results")
        st.table(pd.DataFrame(results))

        st.metric(
            label=metric_name,
            value=round(best_score, 4)
        )
