import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(page_title="VisionBlaze", page_icon="📷", layout="wide")
st.title("📷 VisionBlaze – Computer Vision Engine")

# 🔐 Load secrets
BACKEND_URL = st.secrets["BACKEND_URL"]
API_KEY = st.secrets["API_KEY"]

# ---------------- IMAGE UPLOAD ---------------- #
uploaded_file = st.file_uploader(
    "Upload an image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:
    st.image(uploaded_file, caption="Original Image", use_container_width=True)

    t1 = st.slider("Lower Threshold", 0, 255, 80)
    t2 = st.slider("Upper Threshold", 0, 255, 180)

    if st.button("Run Edge Detection"):
        with st.spinner("Processing image with VisionBlaze..."):
            try:
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                }

                response = requests.post(
                    f"{BACKEND_URL}/vision/edges",
                    files=files,
                    headers={"X-API-Key": API_KEY},
                    timeout=60  # 🔥 CRITICAL
                )

                if response.status_code == 200:
                    img = Image.open(io.BytesIO(response.content))
                    st.success("Edge detection successful")
                    st.image(img, caption="Processed Image", use_container_width=True)

                else:
                    st.error(f"Backend error: {response.status_code}")
                    st.text(response.text)

            except requests.exceptions.RequestException as e:
                st.error("Could not connect to VisionBlaze backend")
                st.text(str(e))

