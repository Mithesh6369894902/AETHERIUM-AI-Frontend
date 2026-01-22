import streamlit as st
import requests
from PIL import Image
import io
import time

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Vision Blaze+",
    page_icon="📷⚡",
    layout="wide"
)

BACKEND_URL = "http://localhost:8000"

st.title("📷⚡ Vision Blaze+ : Interactive Computer Vision Platform (Backend Powered)")

# ---------------- SESSION STATE ----------------
if "image_file" not in st.session_state:
    st.session_state.image_file = None

if "log" not in st.session_state:
    st.session_state.log = []

def log_operation(name):
    st.session_state.log.append({
        "operation": name,
        "timestamp": time.strftime("%H:%M:%S")
    })

# ---------------- SIDEBAR ----------------
menu = st.sidebar.radio(
    "🔬 Vision Operations",
    [
        "Upload Image",
        "Edge Analysis",
        "Contrast Enhancement",
        "Saliency Mapping",
        "Segmentation",
        "Operation Log"
    ]
)

# ---------------- IMAGE UPLOAD ----------------
if menu == "Upload Image":
    file = st.file_uploader("📤 Upload Image", ["png", "jpg", "jpeg"])
    if file:
        st.session_state.image_file = file
        log_operation("Image Uploaded")
        st.success("Image loaded successfully")
        st.image(Image.open(file), use_container_width=True)

# ---------------- EDGE ANALYSIS ----------------
elif menu == "Edge Analysis" and st.session_state.image_file:
    t1 = st.slider("Lower Threshold", 0, 255, 80)
    t2 = st.slider("Upper Threshold", 0, 255, 180)

    if st.button("Run Edge Detection"):
        res = requests.post(
            f"{BACKEND_URL}/vision/edges",
            files={"file": st.session_state.image_file},
            data={"t1": t1, "t2": t2}
        )

        log_operation("Edge Detection (Canny)")
        img = Image.open(io.BytesIO(res.content))
        st.image(img, caption="Edge Output", use_container_width=True)

# ---------------- CONTRAST ENHANCEMENT ----------------
elif menu == "Contrast Enhancement" and st.session_state.image_file:
    if st.button("Enhance Contrast"):
        res = requests.post(
            f"{BACKEND_URL}/vision/contrast",
            files={"file": st.session_state.image_file}
        )

        log_operation("Histogram Equalization")
        img = Image.open(io.BytesIO(res.content))
        st.image(img, caption="Enhanced Image", use_container_width=True)

# ---------------- SALIENCY ----------------
elif menu == "Saliency Mapping" and st.session_state.image_file:
    if st.button("Generate Saliency Map"):
        res = requests.post(
            f"{BACKEND_URL}/vision/saliency",
            files={"file": st.session_state.image_file}
        )

        log_operation("Saliency Mapping")
        img = Image.open(io.BytesIO(res.content))
        st.image(img, caption="Saliency Map", use_container_width=True)

# ---------------- SEGMENTATION ----------------
elif menu == "Segmentation" and st.session_state.image_file:
    if st.button("Run Segmentation"):
        res = requests.post(
            f"{BACKEND_URL}/vision/segmentation",
            files={"file": st.session_state.image_file}
        )

        log_operation("GrabCut Segmentation")
        img = Image.open(io.BytesIO(res.content))
        st.image(img, caption="Segmented Output", use_container_width=True)

# ---------------- LOG ----------------
elif menu == "Operation Log":
    st.subheader("🧾 Experiment Log")
    if st.session_state.log:
        st.table(st.session_state.log)
    else:
        st.info("No operations recorded yet")

# ---------------- FALLBACK ----------------
elif not st.session_state.image_file:
    st.info("⬅ Upload an image to begin")

