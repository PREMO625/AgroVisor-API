import streamlit as st
import requests
from PIL import Image
import io
import time

API_BASE_URL = "http://localhost:7860"

st.set_page_config(page_title="AgroVisor AI System", page_icon="🌱", layout="wide")

st.title("🌱 AgroVisor AI System")
st.markdown("Efficient, modular backend with queuing and resource management.")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose task", [
    "Unified Classification",
    "Plant Disease Detection",
    "Paddy Disease Classification",
    "Pest Identification"
])

# Helper to handle API requests and queue status
def predict(endpoint, file):
    files = {"file": (file.name, file.getvalue(), file.type)}
    try:
        response = requests.post(f"{API_BASE_URL}/predict/{endpoint}", files=files, timeout=60)
        if response.status_code == 200:
            return response.json(), None
        elif response.status_code == 429:
            return None, "Server busy or queue full. Please wait and try again."
        else:
            return None, f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return None, f"Request failed: {e}"

# Main UI logic
def show_predict_ui(endpoint, label):
    st.header(label)
    uploaded_file = st.file_uploader(f"Upload an image for {label.lower()}", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        if st.button(f"Predict {label}"):
            with st.spinner("Processing and waiting in queue if needed..."):
                result, error = predict(endpoint, uploaded_file)
                if error:
                    st.error(error)
                elif result:
                    st.success("Prediction complete!")
                    st.json(result)

if page == "Unified Classification":
    show_predict_ui("unified", "Unified Classification")
elif page == "Plant Disease Detection":
    show_predict_ui("plant-disease", "Plant Disease Detection")
elif page == "Paddy Disease Classification":
    show_predict_ui("paddy-disease", "Paddy Disease Classification")
elif page == "Pest Identification":
    show_predict_ui("pest", "Pest Identification")

st.sidebar.markdown("---")
st.sidebar.info("Backend: FastAPI (modular, lazy loading, LRU cache, queuing)")
