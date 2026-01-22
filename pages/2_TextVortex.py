import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import io

# ================= CONFIG ================= #
st.set_page_config(
    page_title="TextVortex",
    page_icon="🌪️",
    layout="wide"
)

BACKEND_URL = "http://localhost:8000"

st.title("🌪️ TextVortex — NLP Intelligence Engine (Backend Powered)")

page = st.sidebar.radio(
    "Select Module",
    [
        "🏠 Home",
        "🔠 Tokenization",
        "🛑 Stopwords Removal",
        "🌱 Stemming",
        "🌿 Lemmatization",
        "🔢 N-Grams",
        "🔑 Keyword Extraction",
        "📊 Text Statistics",
        "📈 Text Complexity",
        "☁️ Word Cloud"
    ]
)

# ================= INPUT ================= #
text = st.text_area("✍️ Enter text:", height=200)

def validate():
    if not text.strip():
        st.warning("⚠️ Please enter text.")
        return False
    return True

# ================= HOME ================= #
if page == "🏠 Home":
    st.markdown("""
    **TextVortex** is the NLP intelligence layer of ÆTHERIUM.
    
    All natural language processing operations are executed
    through a centralized backend to ensure scalability,
    reproducibility, and platform independence.
    """)

# ================= TOKENIZATION ================= #
elif page == "🔠 Tokenization" and validate():
    res = requests.post(
        f"{BACKEND_URL}/text/tokenize",
        json={"text": text}
    ).json()

    st.subheader("Word Tokens")
    st.write(res["words"])

    st.subheader("Sentence Tokens")
    st.write(res["sentences"])

# ================= STOPWORDS ================= #
elif page == "🛑 Stopwords Removal" and validate():
    res = requests.post(
        f"{BACKEND_URL}/text/stopwords",
        json={"text": text}
    ).json()
    st.write(res["tokens"])

# ================= STEMMING ================= #
elif page == "🌱 Stemming" and validate():
    res = requests.post(
        f"{BACKEND_URL}/text/stemming",
        json={"text": text}
    ).json()
    st.write(res["tokens"])

# ================= LEMMATIZATION ================= #
elif page == "🌿 Lemmatization" and validate():
    res = requests.post(
        f"{BACKEND_URL}/text/lemmatization",
        json={"text": text}
    ).json()
    st.write(res["tokens"])

# ================= N-GRAMS ================= #
elif page == "🔢 N-Grams" and validate():
    n = st.slider("Select N", 1, 4, 2)
    res = requests.post(
        f"{BACKEND_URL}/text/ngrams",
        json={"text": text, "n": n}
    ).json()
    st.write(res["ngrams"])

# ================= KEYWORDS ================= #
elif page == "🔑 Keyword Extraction" and validate():
    res = requests.post(
        f"{BACKEND_URL}/text/keywords",
        json={"text": text}
    ).json()

    df = pd.DataFrame(res["keywords"])
    st.dataframe(df)

# ================= TEXT STATISTICS ================= #
elif page == "📊 Text Statistics" and validate():
    res = requests.post(
        f"{BACKEND_URL}/text/statistics",
        json={"text": text}
    ).json()
    st.json(res)

# ================= TEXT COMPLEXITY ================= #
elif page == "📈 Text Complexity" and validate():
    res = requests.post(
        f"{BACKEND_URL}/text/complexity",
        json={"text": text}
    ).json()
    st.json(res)

# ================= WORD CLOUD ================= #
elif page == "☁️ Word Cloud" and validate():
    res = requests.post(
        f"{BACKEND_URL}/text/wordcloud",
        json={"text": text}
    )

    img = Image.open(io.BytesIO(res.content))
    st.image(img, caption="Word Cloud", use_column_width=True)


