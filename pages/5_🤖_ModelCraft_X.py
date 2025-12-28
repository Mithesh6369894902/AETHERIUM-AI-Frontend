import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="ModelCraft X",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 ModelCraft X")
st.subheader("Machine Learning Model Builder & Evaluator")

st.markdown("""
ModelCraft X is a **no-code / low-code ML experimentation lab**  
for training, comparing, and validating models.
""")

st.divider()

tab1, tab2, tab3 = st.tabs([
    "📂 Data Loader",
    "⚙ Model Training",
    "📊 Evaluation"
])

with tab1:
    st.header("📂 Dataset Loader")
    file = st.file_uploader("Upload CSV", type=["csv"])
    if file:
        df = pd.read_csv(file)
        st.dataframe(df)

with tab2:
    st.header("⚙ Model Training")
    st.info("Add model selection & training logic here")

with tab3:
    st.header("📊 Model Evaluation")
    st.info("Add accuracy, metrics, plots here")
