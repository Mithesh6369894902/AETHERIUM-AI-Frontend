import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="InfernoData",
    page_icon="📊",
    layout="wide"
)

st.title("📊 InfernoData")
st.subheader("Dataset Engineering & ML Data Preparation Engine")

st.markdown("""
InfernoData focuses on **dataset creation, transformation, and ML-ready preparation**  
for **Classification, Regression, Clustering, and Association tasks**.
""")

st.divider()

tab1, tab2, tab3, tab4 = st.tabs([
    "📂 Dataset Generator",
    "📊 Classification",
    "📈 Regression",
    "🧩 Clustering"
])

with tab1:
    st.header("📂 Dataset Generator")
    uploaded = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        st.dataframe(df)
        st.success("Dataset loaded successfully")

with tab2:
    st.header("📊 Classification Dataset Builder")
    st.info("Add your classification dataset logic here")

with tab3:
    st.header("📈 Regression Dataset Builder")
    st.info("Add regression dataset logic here")

with tab4:
    st.header("🧩 Clustering Dataset Builder")
    st.info("Add clustering dataset logic here")
