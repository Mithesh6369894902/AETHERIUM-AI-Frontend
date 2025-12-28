import streamlit as st

st.set_page_config(
    page_title="Ather AI Hub",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Ather AI Hub")
st.markdown("### One Hub. Multiple AI Engines.")

st.success("If you can see this, Streamlit is running correctly.")

st.markdown("""
### Available Modules (use the sidebar 👈):
- 📊 InfernoData
- ✍️ TextVortex
- 📈 AlphaFlux
- 👁 VisionBlaze
- 🤖 ModelCraft X
""")
