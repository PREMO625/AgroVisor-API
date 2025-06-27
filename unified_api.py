from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
import numpy as np
import cv2
import io
from PIL import Image
import uvicorn
import os
import pandas as pd
from typing import Dict, Any, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants for models
MODELS_DIR = "Models"
ANNOTATIONS_DIR = "annotations"

MODEL_PATHS = {
    "plant_disease": os.path.join(MODELS_DIR, "plant_disease_classifier_cnn.keras"),
    "paddy_disease": os.path.join(MODELS_DIR, "paddy_diseases_classifier_cnn.keras"),
    "pest": os.path.join(MODELS_DIR, "pest_classifier_effnetB3.keras"),
    "router": os.path.join(MODELS_DIR, "router_classifier_best.keras")
}

ANNOTATION_PATHS = {
    "plant_disease": os.path.join(ANNOTATIONS_DIR, "plant_disease_classifier.csv"),
    "paddy_disease": os.path.join(ANNOTATIONS_DIR, "paddy_disease_classifier.csv"),
    "pest": os.path.join(ANNOTATIONS_DIR, "pest_classifier.csv"),
    "router": os.path.join(ANNOTATIONS_DIR, "router_classifier.csv")
}

app = FastAPI(
    title="Unified Agricultural AI API",
    description="Comprehensive API for plant disease detection, paddy disease classification, and pest identification",
    version="2.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for models and class names
models = {}
class_names = {}

def load_class_names(csv_path: str) -> List[str]:
    """Load class names from CSV annotation file"""
    try:
        df = pd.read_csv(csv_path)
        return df['class_name'].tolist()
    except Exception as e:
        logger.error(f"Error loading class names from {csv_path}: {e}")
        return []

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """Preprocess image for model prediction"""
    try:
        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert PIL Image to numpy array
        img = np.array(image)
        
        # Resize to 224x224
        img = cv2.resize(img, (224, 224))
        
        # Normalize pixel values to [0, 1]
        img = img.astype('float32') / 255.0
        
        # Add batch dimension
        img = np.expand_dims(img, axis=0)
        
        return img
    except Exception as e:
        logger.error(f"Error preprocessing image: {e}")
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")

def load_model_with_compatibility(model_path: str, model_key: str):
    """Load model with compatibility handling for different TensorFlow versions"""
    try:
        # Try loading with current TensorFlow version
        model = tf.keras.models.load_model(model_path)
        logger.info(f"Successfully loaded {model_key} model from {model_path}")
        return model
    except Exception as e:
        logger.error(f"Failed to load {model_key} model with current TensorFlow version: {e}")
        
        # Try loading with compile=False for compatibility
        try:
            model = tf.keras.models.load_model(model_path, compile=False)
            logger.warning(f"Loaded {model_key} model without compilation (compatibility mode)")
            return model
        except Exception as e2:
            logger.error(f"Failed to load {model_key} model even in compatibility mode: {e2}")
            
            # Try loading with custom objects
            try:
                custom_objects = {
                    'batch_shape': None,  # Handle deprecated batch_shape parameter
                }
                model = tf.keras.models.load_model(model_path, custom_objects=custom_objects, compile=False)
                logger.warning(f"Loaded {model_key} model with custom objects (legacy compatibility)")
                return model
            except Exception as e3:
                logger.error(f"All model loading attempts failed for {model_key}: {e3}")
                return None

@app.on_event("startup")
async def load_models():
    """Load all models and class names on startup with enhanced error handling"""
    global models, class_names
    
    logger.info("Starting model and class name loading...")
    
    # Load class names first
    for key, path in ANNOTATION_PATHS.items():
        try:
            if os.path.exists(path):
                class_names[key] = load_class_names(path)
                logger.info(f"✅ Loaded {len(class_names[key])} classes for {key}")
            else:
                logger.warning(f"⚠️ Annotation file not found: {path}")
                class_names[key] = []
        except Exception as e:
            logger.error(f"❌ Error loading class names for {key}: {e}")
            class_names[key] = []
    
    # Load models with enhanced compatibility handling
    successful_models = 0
    total_models = len(MODEL_PATHS)
    
    for key, path in MODEL_PATHS.items():
        if os.path.exists(path):
            logger.info(f"🔄 Attempting to load {key} model...")
            model = load_model_with_compatibility(path, key)
            models[key] = model
            if model is not None:
                successful_models += 1
                logger.info(f"✅ {key} model loaded successfully")
            else:
                logger.error(f"❌ Failed to load {key} model")
        else:
            logger.error(f"❌ Model file not found: {path}")
            models[key] = None
    
    # Summary
    logger.info(f"📊 Model loading summary: {successful_models}/{total_models} models loaded successfully")
    
    if successful_models == 0:
        logger.error("🚨 CRITICAL: No models could be loaded! API will have limited functionality.")
    elif successful_models < total_models:
        logger.warning(f"⚠️ WARNING: Only {successful_models} out of {total_models} models loaded. Some endpoints may not work.")
    else:
        logger.info("🎉 All models loaded successfully!")
    
    logger.info("Model loading process completed!")

def make_prediction(model_key: str, image_bytes: bytes) -> Dict[str, Any]:
    """Make prediction using specified model with enhanced error handling"""
    # Check if model is available
    if model_key not in models or models[model_key] is None:
        error_msg = f"❌ {model_key.replace('_', ' ').title()} model is not available"
        logger.error(error_msg)
        raise HTTPException(
            status_code=503, 
            detail={
                "error": error_msg,
                "suggestion": "The model failed to load during startup. Please check server logs and restart the API.",
                "model_status": "unavailable"
            }
        )
    
    # Check if class names are available
    if model_key not in class_names or not class_names[model_key]:
        error_msg = f"❌ Class names for {model_key.replace('_', ' ').title()} are not available"
        logger.error(error_msg)
        raise HTTPException(
            status_code=503,
            detail={
                "error": error_msg,
                "suggestion": "The annotation file is missing or corrupted. Please check the annotations directory.",
                "model_status": "classes_unavailable"
            }
        )
    
    try:
        # Preprocess image
        img = preprocess_image(image_bytes)
        
        # Make prediction with error handling
        try:
            predictions = models[model_key].predict(img, verbose=0)[0]  # verbose=0 to reduce logs
        except Exception as pred_error:
            logger.error(f"Prediction failed for {model_key}: {pred_error}")
            raise HTTPException(
                status_code=500,
                detail={
                    "error": f"Model prediction failed: {str(pred_error)}",
                    "suggestion": "The model may be corrupted or incompatible. Please retrain or replace the model.",
                    "model_status": "prediction_failed"
                }
            )
        
        # Validate predictions
        if len(predictions) != len(class_names[model_key]):
            logger.error(f"Prediction output size mismatch for {model_key}")
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Model output doesn't match expected class count",
                    "suggestion": "The model and annotation file may be mismatched.",
                    "model_status": "output_mismatch"
                }
            )
        
        # Get top prediction
        predicted_class_index = np.argmax(predictions)
        confidence = float(predictions[predicted_class_index])
        predicted_class = class_names[model_key][predicted_class_index]
        
        # Get top 3 predictions
        top_3_indices = np.argsort(predictions)[-3:][::-1]
        top_3_predictions = [
            {
                "class_index": int(idx),
                "class_name": class_names[model_key][idx],
                "confidence": float(predictions[idx])
            }
            for idx in top_3_indices
        ]
        
        # Determine health status
        is_healthy = any(keyword in predicted_class.lower() for keyword in ['healthy', 'normal', 'good'])
        
        return {
            "prediction": {
                "class_index": int(predicted_class_index),
                "class_name": predicted_class,
                "confidence": confidence,
                "is_healthy": is_healthy
            },
            "top_3_predictions": top_3_predictions,
            "model_used": model_key,
            "model_status": "success"
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error in make_prediction for {model_key}: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": f"Unexpected prediction error: {str(e)}",
                "suggestion": "Please try again or contact support if the issue persists.",
                "model_status": "unexpected_error"
            }
        )

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Unified Agricultural AI API",
        "version": "2.0.0",
        "available_endpoints": [
            "/predict/plant-disease",
            "/predict/paddy-disease", 
            "/predict/pest",
            "/predict/unified"
        ],
        "documentation": "/docs"
    }

@app.get("/health")
async def health_check():
    """Enhanced health check endpoint with detailed status information"""
    model_status = {}
    loaded_count = 0
    
    for key in MODEL_PATHS.keys():
        is_loaded = models.get(key) is not None
        classes_count = len(class_names.get(key, []))
        
        if is_loaded:
            loaded_count += 1
        
        model_status[key] = {
            "loaded": is_loaded,
            "classes_available": classes_count,
            "model_path": MODEL_PATHS[key],
            "annotation_path": ANNOTATION_PATHS.get(key, "N/A"),
            "status": "✅ Ready" if is_loaded and classes_count > 0 else 
                     "⚠️ Model loaded but no classes" if is_loaded else 
                     "❌ Not loaded"
        }
    
    total_models = len(MODEL_PATHS)
    
    # Determine overall system status
    if loaded_count == total_models:
        overall_status = "healthy"
        status_message = "🎉 All systems operational"
    elif loaded_count > 0:
        overall_status = "partial"
        status_message = f"⚠️ Partial functionality ({loaded_count}/{total_models} models loaded)"
    else:
        overall_status = "unhealthy"
        status_message = "❌ No models available - system not functional"
    
    return {
        "status": overall_status,
        "message": status_message,
        "models": model_status,
        "summary": {
            "total_models": total_models,
            "loaded_models": loaded_count,
            "failed_models": total_models - loaded_count,
            "success_rate": f"{(loaded_count/total_models)*100:.1f}%"
        },
        "tensorflow_version": tf.__version__,
        "system_ready": loaded_count > 0
    }

@app.get("/models/info")
async def get_models_info():
    """Get information about all available models"""
    info = {}
    for key in MODEL_PATHS.keys():
        info[key] = {
            "model_path": MODEL_PATHS[key],
            "annotation_path": ANNOTATION_PATHS[key],
            "is_loaded": models.get(key) is not None,
            "num_classes": len(class_names.get(key, [])),
            "classes": class_names.get(key, [])
        }
    
    return {
        "models_info": info,
        "router_classes": class_names.get("router", [])
    }

@app.post("/predict/plant-disease")
async def predict_plant_disease(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Predict plant diseases using the plant disease classifier model
    
    Supports 38 different plant disease classes including various fruits and vegetables
    """
    try:
        image_bytes = await file.read()
        result = make_prediction("plant_disease", image_bytes)
        
        return {
            "filename": file.filename,
            "endpoint": "plant-disease",
            "description": "General plant disease classification",
            **result
        }
    except Exception as e:
        logger.error(f"Error in plant disease prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/paddy-disease")
async def predict_paddy_disease(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Predict paddy/rice diseases using the specialized paddy disease classifier
    
    Supports 13 different paddy disease and pest classes
    """
    try:
        image_bytes = await file.read()
        result = make_prediction("paddy_disease", image_bytes)
        
        return {
            "filename": file.filename,
            "endpoint": "paddy-disease",
            "description": "Specialized paddy/rice disease classification",
            **result
        }
    except Exception as e:
        logger.error(f"Error in paddy disease prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/pest")
async def predict_pest(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Predict agricultural pests using the pest classifier model
    
    Supports 102 different pest classes
    """
    try:
        image_bytes = await file.read()
        result = make_prediction("pest", image_bytes)
        
        return {
            "filename": file.filename,
            "endpoint": "pest",
            "description": "Agricultural pest identification",
            **result
        }
    except Exception as e:
        logger.error(f"Error in pest prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/unified")
async def predict_unified(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Unified prediction endpoint using router classifier
    Automatically determines which specialized model to use
    """
    try:
        image_bytes = await file.read()
        # Predict with router classifier
        if models.get("router") is None:
            raise HTTPException(status_code=503, detail="Router classifier model is not available.")
        img = preprocess_image(image_bytes)
        router_pred = models["router"].predict(img, verbose=0)[0]
        router_idx = int(np.argmax(router_pred))
        router_conf = float(router_pred[router_idx])
        router_classes = class_names.get("router", ["plant_disease", "paddy_disease", "pest"])
        routed_model_key = None
        # Map router class to model key
        if router_classes[router_idx].lower().startswith("plant"):
            routed_model_key = "plant_disease"
        elif router_classes[router_idx].lower().startswith("paddy"):
            routed_model_key = "paddy_disease"
        elif router_classes[router_idx].lower().startswith("pest"):
            routed_model_key = "pest"
        else:
            raise HTTPException(status_code=500, detail="Router classifier returned unknown class.")
        # Predict with routed model
        result = make_prediction(routed_model_key, image_bytes)
        return {
            "filename": file.filename,
            "endpoint": "unified",
            "description": "Unified classification with automatic model routing",
            "router_info": {
                "router_prediction": router_classes[router_idx],
                "router_confidence": router_conf,
                "available_classifiers": router_classes
            },
            **result
        }
    except Exception as e:
        logger.error(f"Error in unified prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/predict/unified/status")
async def unified_status():
    """Get status of unified prediction system"""
    return {
        "status": "placeholder",
        "message": "Router classifier model not yet implemented",
        "available_models": list(MODEL_PATHS.keys()),
        "router_classes": class_names.get("router", []),
        "implementation_needed": "Router classifier model training and integration"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("unified_api:app", host="0.0.0.0", port=port, reload=True)