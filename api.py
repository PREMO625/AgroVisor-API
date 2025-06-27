from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
import numpy as np
import cv2
import io
from PIL import Image
import uvicorn
import os
from typing import Dict, Any

# Constants for model
MODEL_PATH = "best_model_cnnv2.keras"

app = FastAPI(title="Plant Disease Classification API",
              description="API for classifying plant diseases from leaf images",
              version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Load model once when the API starts
model = None

# Class names for prediction
class_names = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
    'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 
    'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 
    'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 
    'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 
    'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot',
    'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 
    'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy', 
    'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew', 
    'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 
    'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 
    'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 
    'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

@app.on_event("startup")
async def load_model():
    global model
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")
        raise

def preprocess_image(image_bytes):
    # Convert bytes to image
    image = Image.open(io.BytesIO(image_bytes))
    
    # Convert PIL Image to OpenCV format
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    # Resize and preprocess
    H, W, C = 224, 224, 3
    img = cv2.resize(img, (H, W))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = np.array(img)
    img = img.astype('float32')
    img = img / 255.0
    img = img.reshape(1, H, W, C)
    
    return img

@app.get("/")
async def root():
    return {"message": "Plant Disease Classification API is running. Use /predict endpoint to classify plant diseases."}

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify API status
    """
    try:
        # Check if model is loaded
        if model is None:
            return {
                "status": "error",
                "message": "Model not loaded",
                "is_healthy": False
            }
        
        return {
            "status": "ok",
            "message": "Plant Disease Classification API is running",
            "model_loaded": True,
            "is_healthy": True,
            "supported_plants": len(class_names)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "is_healthy": False
        }

@app.post("/predict")
async def predict(file: UploadFile = File(...)) -> Dict[str, Any]:
    # Read image file
    image_bytes = await file.read()
    
    # Preprocess the image
    img = preprocess_image(image_bytes)
    
    # Make prediction
    predictions = model.predict(img)[0]
    
    # Get the predicted class index and confidence
    predicted_class_index = np.argmax(predictions)
    confidence = float(predictions[predicted_class_index])
    
    # Get the class name
    predicted_class = class_names[predicted_class_index]
    
    # Determine if the plant is healthy or has disease
    is_healthy = "healthy" in predicted_class.lower()
    
    # Prepare response
    response = {
        "filename": file.filename,
        "prediction": {
            "class_index": int(predicted_class_index),
            "class_name": predicted_class,
            "confidence": confidence,
            "is_healthy": is_healthy
        }
    }
    
    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=True)
























