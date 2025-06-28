# API Integration Guide for AgroVisor Backend

## Overview
This guide explains how to integrate the AgroVisor FastAPI backend with any frontend (e.g., Streamlit, React, etc.). It covers all endpoints, request/response formats, authentication (if any), and usage examples. It also provides troubleshooting tips and contact information for backend support.

---

## Base URL

- **Hugging Face Spaces:**
  - `https://premo625-agrivisor-api.hf.space`
- **Local Development:**
  - `http://localhost:7860`

---

## Endpoints

### 1. Health Check
- **GET** `/health`
- **Description:** Returns API status. (Currently returns `{ "status": "ok" }`)
- **Response Example:**
```json
{
  "status": "ok"
}
```

---

### 2. Unified Router Classifier
- **POST** `/predict/unified`
- **Description:** Accepts an image, routes it to the correct model, and returns the prediction.
- **Request:**
  - `multipart/form-data` with key `file` (image file)
- **Response Example:**
```json
{
  "endpoint": "plant-disease",
  "description": "General plant disease classification",
  "prediction": {
    "class_index": 12,
    "class_name": "Tomato___Late_blight",
    "confidence": 0.98,
    "is_healthy": false
  },
  "top_3_predictions": [
    {"class_index": 12, "class_name": "Tomato___Late_blight", "confidence": 0.98},
    {"class_index": 5, "class_name": "Tomato___Early_blight", "confidence": 0.01},
    {"class_index": 2, "class_name": "Tomato___Healthy", "confidence": 0.01}
  ],
  "model_used": "plant_disease",
  "router_info": {
    "router_prediction": "plant_disease",
    "router_confidence": 0.95
  }
}
```

---

### 3. Plant Disease Classifier
- **POST** `/predict/plant-disease`
- **Description:** Specialized plant disease classification.
- **Request:**
  - `multipart/form-data` with key `file` (image file)
- **Response:** Same as above, but without `router_info`.

---

### 4. Paddy Disease Classifier
- **POST** `/predict/paddy-disease`
- **Description:** Specialized paddy/rice disease classification.
- **Request:**
  - `multipart/form-data` with key `file` (image file)
- **Response:** Same as above, but for paddy classes.

---

### 5. Pest Classifier
- **POST** `/predict/pest`
- **Description:** Specialized pest identification.
- **Request:**
  - `multipart/form-data` with key `file` (image file)
- **Response:** Same as above, but for pest classes.

---

## Request Example (Python)

```python
import requests

url = "https://premo625-agrivisor-api.hf.space/predict/unified"
files = {"file": open("your_image.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

---

## Error Handling
- All endpoints return clear error messages and HTTP status codes.
- Common errors:
  - `400 Bad Request`: Invalid or missing file.
  - `503 Service Unavailable`: Model not loaded or server busy.
  - `429 Too Many Requests`: Queue is full.

---

## Frontend Integration Tips
- Always check `/health` before making predictions.
- Use the correct base URL for the environment (local or Hugging Face Spaces).
- For file uploads, use `multipart/form-data` with the key `file`.
- Handle errors gracefully and display user-friendly messages.
- Show prediction confidence and model status in the UI.

---

## Troubleshooting
- If you get connection errors, ensure the API is running and the URL is correct.
- If you get `503` or `429` errors, wait and retry (resource limits may be hit on free tier).
- For unexpected errors, check the API logs or contact backend support.

---

## Backend Support
- For technical support, contact: `backend@yourdomain.com` (replace with actual contact)
- For urgent issues, open an issue on the project repository.

---

## Changelog
- v2.0: Modular backend, lazy loading, LRU caching, queuing, Hugging Face Spaces support.
- v1.0: Initial release.
