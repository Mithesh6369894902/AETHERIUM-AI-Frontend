# ======================================================
# TEXTVORTEX – ZERO-CRASH NLP ENGINE (PRODUCTION SAFE)
# Python 3.13 | Streamlit | Regex NLP Core
# ======================================================

import streamlit as st
import re
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
import textstat

# Optional NLTK (NO TOKENIZERS USED)
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk import pos_tag

# ======================================================
# SAFE NLTK SETUP (NO punkt / no crashes)
# ======================================================
@st.cache_resource
def setup_nltk():
    for r in ["stopwords", "wordnet", "omw-1.4", "averaged_perceptron_tagger"]:
        try:
            nltk.data.find(f"corpora/{r}")
        except LookupError:
            nltk.download(r)

setup_nltk()
STOPWORDS = set(stopwords.words("english"))

# ======================================================
# 🔐 SAFE TOKENIZERS (REGEX-BASED)
# ======================================================
def safe_word_tokenize(text):
    return re.findall(r"\b[a-zA-Z']+\b", text.lower())

def safe_sent_tokenize(text):
    return re.split(r'(?<=[.!?])\s+', text.strip())

# ======================================================
# STREAMLIT CONFIG
# ======================================================
st.set_page_config(
    page_title="TextVortex",
    page_icon="🌪️",
    layout="wide"
)

st.title("🌪️ TextVortex — Future-Proof NLP Intelligence Engine")

page = st.sidebar.radio(
    "Select Module",
    [
        "🏠 Home",
        "🔠 Tokenization",
        "🛑 Stopwords Removal",
        "🏷️ POS Tagging",
        "🌱 Stemming",
        "🌿 Lemmatization",
        "🔢 N-Grams",
        "🔑 Keyword Extraction",
        "📊 Text Statistics",
        "📈 Text Complexity",
        "☁️ Word Cloud"
    ]
)

# ======================================================
# INPUT (USED EVERYWHERE)
# ======================================================
text = st.text_area(
    "✍️ Enter text (works for ALL modules):",
    height=200
)

def validate():
    if not text.strip():
        st.warning("⚠️ Please enter text.")
        return False
    return True

# ======================================================
# HOME
# ======================================================
if page == "🏠 Home":
    st.markdown("""
    **TextVortex** is a next-generation NLP platform built with
    **cloud safety, reproducibility, and research stability** in mind.

    ✔ No tokenizer crashes  
    ✔ Regex-driven NLP core  
    ✔ Python 3.13 compatible  
    ✔ Conference-ready design  
    """)

# ======================================================
# TOKENIZATION
# ======================================================
elif page == "🔠 Tokenization" and validate():
    st.subheader("Word Tokens")
    st.write(safe_word_tokenize(text))

    st.subheader("Sentence Tokens")
    st.write(safe_sent_tokenize(text))

# ======================================================
# STOPWORDS
# ======================================================
elif page == "🛑 Stopwords Removal" and validate():
    tokens = safe_word_tokenize(text)
    st.write([t for t in tokens if t not in STOPWORDS])

# ======================================================
# POS TAGGING
# ======================================================
elif page == "🏷️ POS Tagging" and validate():
    tokens = safe_word_tokenize(text)
    tags = pos_tag(tokens)
    st.dataframe(pd.DataFrame(tags, columns=["Word", "POS"]))

# ======================================================
# STEMMING
# ======================================================
elif page == "🌱 Stemming" and validate():
    stemmer = PorterStemmer()
    st.write([stemmer.stem(w) for w in safe_word_tokenize(text)])

# ======================================================
# LEMMATIZATION
# ======================================================
elif page == "🌿 Lemmatization" and validate():
    lemmatizer = WordNetLemmatizer()
    st.write([lemmatizer.lemmatize(w) for w in safe_word_tokenize(text)])

# ======================================================
# N-GRAMS
# ======================================================
elif page == "🔢 N-Grams" and validate():
    n = st.slider("Select N", 1, 4, 2)
    tokens = safe_word_tokenize(text)
    grams = zip(*[tokens[i:] for i in range(n)])
    st.write([" ".join(g) for g in grams])

# ======================================================
# KEYWORDS
# ======================================================
elif page == "🔑 Keyword Extraction" and validate():
    tokens = [w for w in safe_word_tokenize(text) if w not in STOPWORDS]
    freq = Counter(tokens)
    st.dataframe(pd.DataFrame(freq.items(), columns=["Keyword", "Frequency"])
                 .sort_values("Frequency", ascending=False))

# ======================================================
# TEXT STATISTICS
# ======================================================
elif page == "📊 Text Statistics" and validate():
    st.write({
        "Characters": len(text),
        "Words": len(safe_word_tokenize(text)),
        "Sentences": len(safe_sent_tokenize(text))
    })

# ======================================================
# TEXT COMPLEXITY
# ======================================================
elif page == "📈 Text Complexity" and validate():
    st.write({
        "Flesch Reading Ease": textstat.flesch_reading_ease(text),
        "Flesch-Kincaid Grade": textstat.flesch_kincaid_grade(text),
        "Gunning Fog Index": textstat.gunning_fog(text)
    })

# ======================================================
# WORD CLOUD
# ======================================================
elif page == "☁️ Word Cloud" and validate():
    words = [w for w in safe_word_tokenize(text) if w not in STOPWORDS]
    wc = WordCloud(width=800, height=400, background_color="white").generate(" ".join(words))
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

