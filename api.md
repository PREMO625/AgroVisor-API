# Agricultural AI API Documentation

## Overview

The Unified Agricultural AI API provides comprehensive plant disease detection, paddy disease classification, and pest identification services. This API is built with FastAPI and offers four main prediction endpoints along with utility endpoints for health checking and model information.

**Base URL:** `http://localhost:8000` (development)  
**API Version:** 2.0.0  
**Documentation:** Available at `/docs` (Swagger UI) and `/redoc` (ReDoc)

## Table of Contents

1. [Quick Start](#quick-start)
2. [Authentication](#authentication)
3. [Endpoints Overview](#endpoints-overview)
4. [Prediction Endpoints](#prediction-endpoints)
5. [Utility Endpoints](#utility-endpoints)
6. [Request/Response Formats](#requestresponse-formats)
7. [Error Handling](#error-handling)
8. [Code Examples](#code-examples)
9. [Model Information](#model-information)
10. [Best Practices](#best-practices)

## Quick Start

### 1. Start the API Server
```bash
python unified_api.py
```
The API will be available at `http://localhost:8000`

### 2. Test API Health
```bash
curl http://localhost:8000/health
```

### 3. Make a Prediction
```bash
curl -X POST "http://localhost:8000/predict/plant-disease" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_image.jpg"
```

## Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

## Endpoints Overview

| Endpoint | Method | Purpose | Status |
|----------|--------|---------|--------|
| `/` | GET | API information | ✅ Active |
| `/health` | GET | Health check | ✅ Active |
| `/models/info` | GET | Model information | ✅ Active |
| `/predict/plant-disease` | POST | Plant disease detection | ✅ Active |
| `/predict/paddy-disease` | POST | Paddy disease classification | ✅ Active |
| `/predict/pest` | POST | Pest identification | ✅ Active |
| `/predict/unified` | POST | Unified classification | 🚧 Placeholder |
| `/predict/unified/status` | GET | Unified system status | ✅ Active |

## Prediction Endpoints

### 1. Plant Disease Detection

**Endpoint:** `POST /predict/plant-disease`

**Description:** Detects diseases in various plants including fruits and vegetables using a CNN model trained on 38 different disease classes.

**Supported Plants:** Apple, Blueberry, Cherry, Corn, Grape, Orange, Peach, Pepper, Potato, Raspberry, Soybean, Squash, Strawberry, Tomato

**Request:**
```http
POST /predict/plant-disease
Content-Type: multipart/form-data

file: [image file]
```

**Response:**
```json
{
  "filename": "plant_leaf.jpg",
  "endpoint": "plant-disease",
  "description": "General plant disease classification",
  "prediction": {
    "class_index": 3,
    "class_name": "Apple___healthy",
    "confidence": 0.95,
    "is_healthy": true
  },
  "top_3_predictions": [
    {
      "class_index": 3,
      "class_name": "Apple___healthy",
      "confidence": 0.95
    },
    {
      "class_index": 0,
      "class_name": "Apple___Apple_scab",
      "confidence": 0.03
    },
    {
      "class_index": 1,
      "class_name": "Apple___Black_rot",
      "confidence": 0.02
    }
  ],
  "model_used": "plant_disease"
}
```

### 2. Paddy Disease Classification

**Endpoint:** `POST /predict/paddy-disease`

**Description:** Specialized classification for rice/paddy diseases and pests using a CNN model trained on 13 paddy-specific classes.

**Supported Classes:** bacterial_leaf_blight, bacterial_leaf_streak, bacterial_panicle_blight, black_stem_borer, blast, brown_spot, downy_mildew, hispa, leaf_roller, normal, tungro, white_stem_borer, yellow_stem_borer

**Request:**
```http
POST /predict/paddy-disease
Content-Type: multipart/form-data

file: [image file]
```

**Response:**
```json
{
  "filename": "paddy_leaf.jpg",
  "endpoint": "paddy-disease",
  "description": "Specialized paddy/rice disease classification",
  "prediction": {
    "class_index": 9,
    "class_name": "normal",
    "confidence": 0.88,
    "is_healthy": true
  },
  "top_3_predictions": [
    {
      "class_index": 9,
      "class_name": "normal",
      "confidence": 0.88
    },
    {
      "class_index": 5,
      "class_name": "brown_spot",
      "confidence": 0.07
    },
    {
      "class_index": 4,
      "class_name": "blast",
      "confidence": 0.03
    }
  ],
  "model_used": "paddy_disease"
}
```

### 3. Pest Identification

**Endpoint:** `POST /predict/pest`

**Description:** Identifies agricultural pests using an EfficientNetB3 model trained on 102 different pest classes.

**Request:**
```http
POST /predict/pest
Content-Type: multipart/form-data

file: [image file]
```

**Response:**
```json
{
  "filename": "pest_image.jpg",
  "endpoint": "pest",
  "description": "Agricultural pest identification",
  "prediction": {
    "class_index": 7,
    "class_name": "brown plant hopper",
    "confidence": 0.92,
    "is_healthy": false
  },
  "top_3_predictions": [
    {
      "class_index": 7,
      "class_name": "brown plant hopper",
      "confidence": 0.92
    },
    {
      "class_index": 8,
      "class_name": "white backed plant hopper",
      "confidence": 0.05
    },
    {
      "class_index": 9,
      "class_name": "small brown plant hopper",
      "confidence": 0.02
    }
  ],
  "model_used": "pest"
}
```

### 4. Unified Classification (Placeholder)

**Endpoint:** `POST /predict/unified`

**Description:** Unified prediction endpoint that automatically determines which specialized model to use. Currently uses placeholder logic.

**Status:** 🚧 **PLACEHOLDER IMPLEMENTATION** - Router classifier model needed

**Request:**
```http
POST /predict/unified
Content-Type: multipart/form-data

file: [image file]
```

**Response:**
```json
{
  "filename": "sample_image.jpg",
  "endpoint": "unified",
  "description": "Unified classification with automatic model routing",
  "router_info": {
    "router_prediction": "plant_disease_classifier",
    "router_confidence": 0.85,
    "available_classifiers": [
      "plant_disease_classifier",
      "paddy_disease_classifier", 
      "pest_classifier"
    ]
  },
  "note": "This is a placeholder implementation. Router classifier model needed for full functionality.",
  "prediction": {
    "class_index": 3,
    "class_name": "Apple___healthy",
    "confidence": 0.95,
    "is_healthy": true
  },
  "top_3_predictions": [...],
  "model_used": "plant_disease"
}
```

## Utility Endpoints

### Health Check

**Endpoint:** `GET /health`

**Description:** Check API and model status

**Response:**
```json
{
  "status": "healthy",
  "models": {
    "plant_disease": {
      "loaded": true,
      "classes_available": 38
    },
    "paddy_disease": {
      "loaded": true,
      "classes_available": 13
    },
    "pest": {
      "loaded": true,
      "classes_available": 102
    }
  },
  "total_models": 3,
  "loaded_models": 3
}
```

### Model Information

**Endpoint:** `GET /models/info`

**Description:** Get detailed information about all models

**Response:**
```json
{
  "models_info": {
    "plant_disease": {
      "model_path": "Models/plant_disease_classifier_cnn.keras",
      "annotation_path": "annotations/plant_disease_classifier.csv",
      "is_loaded": true,
      "num_classes": 38,
      "classes": ["Apple___Apple_scab", "Apple___Black_rot", ...]
    },
    "paddy_disease": {
      "model_path": "Models/paddy_diseases_classifier_cnn.keras",
      "annotation_path": "annotations/paddy_disease_classifier.csv",
      "is_loaded": true,
      "num_classes": 13,
      "classes": ["bacterial_leaf_blight", "bacterial_leaf_streak", ...]
    },
    "pest": {
      "model_path": "Models/pest_classifier_effnetB3.keras",
      "annotation_path": "annotations/pest_classifier.csv",
      "is_loaded": true,
      "num_classes": 102,
      "classes": ["rice leaf roller", "rice leaf caterpillar", ...]
    }
  },
  "router_classes": [
    "plant_disease_classifier",
    "paddy_disease_classifier",
    "pest_classifier"
  ]
}
```

### Unified System Status

**Endpoint:** `GET /predict/unified/status`

**Description:** Get status of unified prediction system

**Response:**
```json
{
  "status": "placeholder",
  "message": "Router classifier model not yet implemented",
  "available_models": ["plant_disease", "paddy_disease", "pest"],
  "router_classes": [
    "plant_disease_classifier",
    "paddy_disease_classifier", 
    "pest_classifier"
  ],
  "implementation_needed": "Router classifier model training and integration"
}
```

## Request/Response Formats

### Image Upload Requirements

- **Supported formats:** JPG, JPEG, PNG
- **Recommended size:** Any size (will be resized to 224x224)
- **Max file size:** No explicit limit (reasonable sizes recommended)
- **Color space:** RGB (will be converted if necessary)

### Standard Response Structure

All prediction endpoints return responses with this structure:

```json
{
  "filename": "string",           // Original filename
  "endpoint": "string",           // Endpoint used
  "description": "string",        // Endpoint description
  "prediction": {
    "class_index": "integer",     // Predicted class index
    "class_name": "string",       // Predicted class name
    "confidence": "float",        // Confidence score (0-1)
    "is_healthy": "boolean"       // Health status
  },
  "top_3_predictions": [          // Top 3 predictions
    {
      "class_index": "integer",
      "class_name": "string", 
      "confidence": "float"
    }
  ],
  "model_used": "string"          // Model identifier
}
```

## Error Handling

### HTTP Status Codes

- `200` - Success
- `400` - Bad Request (invalid image, etc.)
- `422` - Validation Error
- `500` - Internal Server Error (model loading issues, etc.)

### Error Response Format

```json
{
  "detail": "Error description"
}
```

### Common Errors

1. **Model Not Loaded**
   ```json
   {
     "detail": "plant_disease model not available"
   }
   ```

2. **Invalid Image Format**
   ```json
   {
     "detail": "Error processing image: cannot identify image file"
   }
   ```

3. **Missing File**
   ```json
   {
     "detail": "Field required"
   }
   ```

## Code Examples

### JavaScript/Fetch API

```javascript
async function predictPlantDisease(imageFile) {
  const formData = new FormData();
  formData.append('file', imageFile);
  
  try {
    const response = await fetch('http://localhost:8000/predict/plant-disease', {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const result = await response.json();
    console.log('Prediction:', result);
    return result;
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}

// Usage
const fileInput = document.getElementById('imageInput');
const file = fileInput.files[0];
predictPlantDisease(file).then(result => {
  console.log(`Predicted: ${result.prediction.class_name} (${(result.prediction.confidence * 100).toFixed(1)}%)`);
});
```

### Python/Requests

```python
import requests

def predict_pest(image_path):
    url = "http://localhost:8000/predict/pest"
    
    with open(image_path, 'rb') as image_file:
        files = {'file': image_file}
        response = requests.post(url, files=files)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

# Usage
try:
    result = predict_pest("pest_image.jpg")
    print(f"Predicted: {result['prediction']['class_name']}")
    print(f"Confidence: {result['prediction']['confidence']:.2%}")
except Exception as e:
    print(f"Error: {e}")
```

### React Component Example

```jsx
import React, { useState } from 'react';

const PlantDiseasePredictor = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileSelect = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handlePredict = async () => {
    if (!selectedFile) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://localhost:8000/predict/plant-disease', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        setPrediction(result);
      } else {
        console.error('Prediction failed');
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input type="file" accept="image/*" onChange={handleFileSelect} />
      <button onClick={handlePredict} disabled={!selectedFile || loading}>
        {loading ? 'Analyzing...' : 'Predict Disease'}
      </button>
      
      {prediction && (
        <div>
          <h3>Prediction Results:</h3>
          <p>Class: {prediction.prediction.class_name}</p>
          <p>Confidence: {(prediction.prediction.confidence * 100).toFixed(1)}%</p>
          <p>Status: {prediction.prediction.is_healthy ? 'Healthy' : 'Disease Detected'}</p>
        </div>
      )}
    </div>
  );
};

export default PlantDiseasePredictor;
```

## Model Information

### Plant Disease Classifier
- **Model:** CNN (Convolutional Neural Network)
- **Classes:** 38
- **Input Size:** 224x224x3
- **Supported Plants:** Apple, Blueberry, Cherry, Corn, Grape, Orange, Peach, Pepper, Potato, Raspberry, Soybean, Squash, Strawberry, Tomato

### Paddy Disease Classifier  
- **Model:** CNN (Convolutional Neural Network)
- **Classes:** 13
- **Input Size:** 224x224x3
- **Focus:** Rice/Paddy specific diseases and pests

### Pest Classifier
- **Model:** EfficientNetB3
- **Classes:** 102
- **Input Size:** 224x224x3
- **Focus:** Agricultural pest identification

### Router Classifier (Planned)
- **Status:** Not yet implemented
- **Purpose:** Automatically route images to appropriate specialized models
- **Classes:** 3 (plant_disease_classifier, paddy_disease_classifier, pest_classifier)

## Best Practices

### 1. Image Quality
- Use clear, well-lit images
- Focus on the affected area (leaf, pest, etc.)
- Avoid blurry or heavily distorted images
- Ensure good contrast

### 2. Error Handling
- Always check HTTP status codes
- Implement retry logic for network failures
- Handle model loading errors gracefully
- Provide user-friendly error messages

### 3. Performance
- Resize large images client-side before upload
- Implement loading states for better UX
- Consider caching results for identical images
- Use appropriate timeouts for requests

### 4. Security
- Validate file types client-side
- Implement file size limits
- Sanitize filenames if storing them
- Consider rate limiting for production

### 5. User Experience
- Show prediction confidence levels
- Display top 3 predictions for context
- Provide clear health status indicators
- Include model information for transparency

## CORS Configuration

The API is configured with permissive CORS settings for development:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Note:** For production, configure CORS more restrictively by specifying allowed origins.

## Deployment Notes

### Development
```bash
python unified_api.py
```

### Production
```bash
uvicorn unified_api:app --host 0.0.0.0 --port 8000
```

### Docker (Example)
```dockerfile
FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "unified_api:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Support and Troubleshooting

### Common Issues

1. **Models not loading:** Check if model files exist in the Models directory
2. **API not starting:** Verify all dependencies are installed
3. **Prediction errors:** Ensure image format is supported
4. **CORS errors:** Check if API server is running and accessible

### Getting Help

- Check the interactive API documentation at `/docs`
- Review the health endpoint for system status
- Check server logs for detailed error information

---

**API Version:** 2.0.0  
**Last Updated:** 2024  
**Maintained by:** Agricultural AI Team