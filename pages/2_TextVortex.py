import streamlit as st
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="TextVortex", page_icon="🌪️", layout="wide")
st.title("🌪️ TextVortex – NLP Intelligence Engine")

# 🔐 Load secrets
BACKEND_URL = st.secrets["BACKEND_URL"]
API_KEY = st.secrets["API_KEY"]

headers = {"X-API-Key": API_KEY}

# ---------------- UI ---------------- #
text = st.text_area("Enter text for analysis", height=200)

operation = st.selectbox(
    "Select NLP Operation",
    [
        "Tokenization",
        "Stopwords Removal",
        "Stemming",
        "Lemmatization",
        "N-Grams",
        "Keyword Extraction",
        "Text Statistics",
        "Text Complexity",
        "Word Cloud"   # ✅ ADDED
    ]
)

# ---------------- ACTION ---------------- #
if st.button("Run TextVortex"):
    if not text.strip():
        st.warning("Please enter text")
        st.stop()

    # -------- WORD CLOUD (FRONTEND VISUALIZATION) -------- #
    if operation == "Word Cloud":
        try:
            response = requests.post(
                f"{BACKEND_URL}/text/keywords",
                json={"text": text},
                headers=headers,
                timeout=60
            )

            if response.status_code == 200:
                keywords = response.json().get("keywords", {})

                if not keywords:
                    st.warning("No keywords returned")
                    st.stop()

                wc = WordCloud(
                    width=800,
                    height=400,
                    background_color="white"
                ).generate_from_frequencies(keywords)

                fig, ax = plt.subplots(figsize=(10, 5))
                ax.imshow(wc, interpolation="bilinear")
                ax.axis("off")

                st.success("Word Cloud generated")
                st.pyplot(fig)

            else:
                st.error(f"Backend error: {response.status_code}")
                st.text(response.text)

        except requests.exceptions.RequestException as e:
            st.error("Could not connect to TextVortex backend")
            st.text(str(e))

    # -------- ALL OTHER NLP OPERATIONS -------- #
    else:
        endpoint_map = {
            "Tokenization": "/text/tokenize",
            "Stopwords Removal": "/text/stopwords",
            "Stemming": "/text/stem",
            "Lemmatization": "/text/lemmatize",
            "N-Grams": "/text/ngrams",
            "Keyword Extraction": "/text/keywords",
            "Text Statistics": "/text/stats",
            "Text Complexity": "/text/complexity"
        }

        endpoint = endpoint_map[operation]

        try:
            response = requests.post(
                f"{BACKEND_URL}{endpoint}",
                json={"text": text},
                headers=headers,
                timeout=60
            )

            if response.status_code == 200:
                st.success("TextVortex processing completed")
                st.json(response.json())
            else:
                st.error(f"Backend error: {response.status_code}")
                st.text(response.text)

        except requests.exceptions.RequestException as e:
            st.error("Could not connect to TextVortex backend")
            st.text(str(e))

