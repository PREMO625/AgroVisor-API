import streamlit as st
import requests
import json
from PIL import Image
import io
import base64

# Configuration
API_BASE_URL = "https://premo625-agrivisor-api.hf.space"

# Page configuration
st.set_page_config(
    page_title="Agricultural AI System",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E8B57;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .sub-header {
        text-align: center;
        color: #4682B4;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4682B4;
        margin: 1rem 0;
        color: #222 !important;
    }
    .success-box {
        background-color: #f0fff0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #32cd32;
        margin: 1rem 0;
        color: #222 !important;
    }
    .warning-box {
        background-color: #fff8dc;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffa500;
        margin: 1rem 0;
        color: #222 !important;
    }
    /* Make all text in the main area and sidebar dark */
    .stApp, .stMarkdown, .stText, .stSelectbox, .stRadio, .stFileUploader, .stSidebar, .st-bb, .st-c3, .st-c4, .st-c5, .st-c6, .st-c7, .st-c8, .st-c9, .st-ca, .st-cb, .st-cc, .st-cd, .st-ce, .st-cf, .st-cg, .st-ch, .st-ci, .st-cj, .st-ck, .st-cl, .st-cm, .st-cn, .st-co, .st-cp, .st-cq, .st-cr, .st-cs, .st-ct, .st-cu, .st-cv, .st-cw, .st-cx, .st-cy, .st-cz {
        color: #222 !important;
    }
    /* Fix button text visibility - make text black */
    .stButton > button {
        color: #000000 !important;
        background-color: #ffffff;
        border: 2px solid #4CAF50;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #4CAF50;
        color: #ffffff !important;
        border-color: #45a049;
    }
    .stButton > button:focus {
        color: #000000 !important;
        background-color: #ffffff;
        border-color: #4CAF50;
        box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.3);
    }
    /* Ensure file uploader text is visible */
    .stFileUploader label {
        color: #000000 !important;
    }
    /* Make sure all text in widgets is visible */
    .stSelectbox label, .stRadio label, .stTextInput label, .stTextArea label, .stNumberInput label, .stSlider label, .stCheckbox label, .stSidebar label {
        color: #222 !important;
    }
    /* Sidebar text color */
    section[data-testid="stSidebar"] * {
        color: #222 !important;
    }
    /* General fix for any white text */
    * {
        text-shadow: none !important;
    }
</style>
""", unsafe_allow_html=True)

def check_api_health():
    """Check if API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200, response.json() if response.status_code == 200 else None
    except:
        return False, None

def make_prediction(endpoint, image_file):
    """Make prediction request to API"""
    try:
        files = {"file": (image_file.name, image_file.getvalue(), image_file.type)}
        response = requests.post(f"{API_BASE_URL}/predict/{endpoint}", files=files, timeout=30)
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"API Error: {response.status_code} - {response.text}"
    except requests.exceptions.Timeout:
        return False, "Request timeout. Please try again."
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to API. Please ensure the API server is running."
    except Exception as e:
        return False, f"Error: {str(e)}"

def display_prediction_results(result):
    """Display prediction results in a formatted way"""
    if not result:
        return
    
    # Main prediction
    prediction = result.get('prediction', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Main Prediction")
        st.markdown(f"**Class:** {prediction.get('class_name', 'N/A')}")
        st.markdown(f"**Confidence:** {prediction.get('confidence', 0):.2%}")
        st.markdown(f"**Health Status:** {'✅ Healthy' if prediction.get('is_healthy', False) else '⚠️ Disease/Pest Detected'}")
    
    with col2:
        st.markdown("### 📊 Model Information")
        st.markdown(f"**Model Used:** {result.get('model_used', 'N/A')}")
        st.markdown(f"**Endpoint:** {result.get('endpoint', 'N/A')}")
        st.markdown(f"**Description:** {result.get('description', 'N/A')}")
    
    # Top 3 predictions
    if 'top_3_predictions' in result:
        st.markdown("### 🏆 Top 3 Predictions")
        for i, pred in enumerate(result['top_3_predictions'], 1):
            st.markdown(f"{i}. **{pred['class_name']}** - {pred['confidence']:.2%}")
    
    # Router information (for unified endpoint)
    if 'router_info' in result:
        st.markdown("### 🔀 Router Information")
        router_info = result['router_info']
        st.markdown(f"**Router Decision:** {router_info.get('router_prediction', 'N/A')}")
        st.markdown(f"**Router Confidence:** {router_info.get('router_confidence', 0):.2%}")
        
        if result.get('note'):
            st.markdown(f"**Note:** {result['note']}")

def main():
    # Header
    st.markdown('<h1 class="main-header">🌱 Agricultural AI System</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Comprehensive Plant Disease Detection, Paddy Disease Classification & Pest Identification</p>', unsafe_allow_html=True)
    
    # Sidebar for navigation
    st.sidebar.title("🔧 Navigation")
    
    # API Health Check
    api_healthy, health_data = check_api_health()
    
    if api_healthy:
        st.sidebar.success("✅ API Connected")
        if health_data:
            loaded_models = health_data.get('loaded_models', 0)
            total_models = health_data.get('total_models', 0)
            st.sidebar.info(f"Models Loaded: {loaded_models}/{total_models}")
    else:
        st.sidebar.error("❌ API Disconnected")
        st.sidebar.warning("Please start the API server first!")
    
    # Page selection
    page = st.sidebar.selectbox(
        "Select Interface",
        [
            "🏠 Home",
            "🔀 Unified Classification",
            "🌿 Plant Disease Detection", 
            "🌾 Paddy Disease Classification",
            "🐛 Pest Identification"
        ]
    )
    
    # Home Page
    if page == "🏠 Home":
        st.markdown("## Welcome to the Agricultural AI System")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="info-box">
                <h3>🌿 Plant Disease Detection</h3>
                <p>Identify diseases in various plants including fruits and vegetables. Supports 38 different disease classes.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="info-box">
                <h3>🌾 Paddy Disease Classification</h3>
                <p>Specialized classification for rice/paddy diseases and pests. Supports 13 specific paddy-related issues.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="info-box">
                <h3>🐛 Pest Identification</h3>
                <p>Comprehensive pest identification system supporting 102 different agricultural pest classes.</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="success-box">
            <h3>🔀 Unified Classification</h3>
            <p>Smart routing system that automatically determines which specialized model to use based on your image. 
            <strong>Note:</strong> Currently in development - uses placeholder routing logic.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # API Status
        if api_healthy and health_data:
            st.markdown("## 📊 System Status")
            
            models_info = health_data.get('models', {})
            
            for model_name, info in models_info.items():
                status = "✅ Loaded" if info['loaded'] else "❌ Not Loaded"
                classes = info['classes_available']
                st.markdown(f"**{model_name.replace('_', ' ').title()}:** {status} ({classes} classes)")
    
    # Unified Classification Page
    elif page == "🔀 Unified Classification":
        st.markdown("## 🔀 Unified Classification System")
        
        st.markdown("""
        <div class="warning-box">
            <h3>⚠️ Development Notice</h3>
            <p>This interface uses a placeholder router system. The actual router classifier model is still in development. 
            Currently, it defaults to plant disease classification for demonstration purposes.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Upload an image and let our AI decide which model to use!")
        
        uploaded_file = st.file_uploader(
            "Choose an image...", 
            type=['jpg', 'jpeg', 'png'],
            key="unified_uploader"
        )
        
        if uploaded_file is not None:
            # Display image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            if st.button("🔍 Analyze with Unified System", key="unified_predict"):
                if not api_healthy:
                    st.error("❌ API is not available. Please start the API server.")
                else:
                    with st.spinner("🤖 AI is analyzing your image and selecting the best model..."):
                        success, result = make_prediction("unified", uploaded_file)
                    
                    if success:
                        st.success("✅ Analysis Complete!")
                        display_prediction_results(result)
                    else:
                        st.error(f"❌ Prediction failed: {result}")
    
    # Plant Disease Detection Page
    elif page == "🌿 Plant Disease Detection":
        st.markdown("## 🌿 Plant Disease Detection")
        st.markdown("Upload an image of a plant leaf to detect diseases in various fruits and vegetables.")
        
        uploaded_file = st.file_uploader(
            "Choose a plant image...", 
            type=['jpg', 'jpeg', 'png'],
            key="plant_uploader"
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Plant Image", use_column_width=True)
            
            if st.button("🔍 Detect Plant Disease", key="plant_predict"):
                if not api_healthy:
                    st.error("❌ API is not available. Please start the API server.")
                else:
                    with st.spinner("🌿 Analyzing plant health..."):
                        success, result = make_prediction("plant-disease", uploaded_file)
                    
                    if success:
                        st.success("✅ Analysis Complete!")
                        display_prediction_results(result)
                    else:
                        st.error(f"❌ Prediction failed: {result}")
    
    # Paddy Disease Classification Page
    elif page == "🌾 Paddy Disease Classification":
        st.markdown("## 🌾 Paddy Disease Classification")
        st.markdown("Specialized classification for rice/paddy diseases and pests.")
        
        uploaded_file = st.file_uploader(
            "Choose a paddy/rice image...", 
            type=['jpg', 'jpeg', 'png'],
            key="paddy_uploader"
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Paddy Image", use_column_width=True)
            
            if st.button("🔍 Classify Paddy Disease", key="paddy_predict"):
                if not api_healthy:
                    st.error("❌ API is not available. Please start the API server.")
                else:
                    with st.spinner("🌾 Analyzing paddy health..."):
                        success, result = make_prediction("paddy-disease", uploaded_file)
                    
                    if success:
                        st.success("✅ Analysis Complete!")
                        display_prediction_results(result)
                    else:
                        st.error(f"❌ Prediction failed: {result}")
    
    # Pest Identification Page
    elif page == "🐛 Pest Identification":
        st.markdown("## 🐛 Pest Identification")
        st.markdown("Identify agricultural pests from images. Supports 102 different pest classes.")
        
        uploaded_file = st.file_uploader(
            "Choose a pest image...", 
            type=['jpg', 'jpeg', 'png'],
            key="pest_uploader"
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Pest Image", use_column_width=True)
            
            if st.button("🔍 Identify Pest", key="pest_predict"):
                if not api_healthy:
                    st.error("❌ API is not available. Please start the API server.")
                else:
                    with st.spinner("🐛 Identifying pest..."):
                        success, result = make_prediction("pest", uploaded_file)
                    
                    if success:
                        st.success("✅ Analysis Complete!")
                        display_prediction_results(result)
                    else:
                        st.error(f"❌ Prediction failed: {result}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>🌱 Agricultural AI System v2.0 | Built with Streamlit & FastAPI</p>
        <p>For technical support, refer to the API documentation</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()