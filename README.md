# Agricultural AI System

A comprehensive AI-powered system for plant disease detection, paddy disease classification, and pest identification.

## 🌟 Features

- **Plant Disease Detection**: Identify diseases in 38 different plant classes
- **Paddy Disease Classification**: Specialized classification for 13 rice/paddy diseases
- **Pest Identification**: Recognize 102 different agricultural pest types
- **Unified Interface**: Smart routing system (placeholder implementation)
- **Web API**: RESTful API with comprehensive documentation
- **Frontend Application**: User-friendly Streamlit interface

## 🚀 Quick Start

### Option 1: One-Click Start (Windows)
```bash
# Double-click the batch file
start_system.bat
```

### Option 2: Python Script
```bash
python run_system.py
```

### Option 3: Manual Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start API Server**
   ```bash
   python unified_api.py
   # or
   uvicorn unified_api:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Start Frontend (in another terminal)**
   ```bash
   streamlit run unified_frontend.py
   ```

## 📋 System Requirements

- Python 3.8+
- TensorFlow 2.15.0
- 8GB+ RAM (for model loading)
- Required model files in `Models/` directory
- Annotation files in `annotations/` directory

## 🔗 Access URLs

After starting the system:

- **Frontend Application**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/health
- **Model Information**: http://localhost:8000/models/info

## 📁 Project Structure

```
Backend/
├── unified_api.py              # Main API server
├── unified_frontend.py         # Streamlit frontend
├── run_system.py              # System launcher
├── start_system.bat           # Windows batch launcher
├── requirements.txt           # Python dependencies
├── api.md                     # API documentation
├── README.md                  # This file
├── Models/                    # Model files
│   ├── plant_disease_classifier_cnn.keras
│   ├── paddy_diseases_classifier_cnn.keras
│   └── pest_classifier_effnetB3.keras
└── annotations/               # Class label files
    ├── plant_disease_classifier.csv
    ├── paddy_disease_classifier.csv
    ├── pest_classifier.csv
    └── router_classifier.csv
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/predict/plant-disease` | POST | Plant disease detection |
| `/predict/paddy-disease` | POST | Paddy disease classification |
| `/predict/pest` | POST | Pest identification |
| `/predict/unified` | POST | Unified classification (placeholder) |
| `/health` | GET | System health check |
| `/models/info` | GET | Model information |

## 📊 Model Information

### Plant Disease Classifier
- **Architecture**: CNN
- **Classes**: 38 (Apple, Tomato, Corn, etc.)
- **Input**: 224x224 RGB images

### Paddy Disease Classifier
- **Architecture**: CNN  
- **Classes**: 13 (Rice-specific diseases)
- **Input**: 224x224 RGB images

### Pest Classifier
- **Architecture**: EfficientNetB3
- **Classes**: 102 (Various agricultural pests)
- **Input**: 224x224 RGB images

## 🎯 Usage Examples

### Frontend Usage
1. Open http://localhost:8501
2. Select the appropriate interface
3. Upload an image
4. Click predict to get results

### API Usage (cURL)
```bash
# Plant disease detection
curl -X POST "http://localhost:8000/predict/plant-disease" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@plant_image.jpg"

# Pest identification
curl -X POST "http://localhost:8000/predict/pest" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@pest_image.jpg"
```

### API Usage (Python)
```python
import requests

# Make prediction
with open('plant_image.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:8000/predict/plant-disease', 
        files=files
    )
    result = response.json()
    print(f"Prediction: {result['prediction']['class_name']}")
```

## 🔧 Configuration

### Environment Variables
- `PORT`: API server port (default: 8000)

### Model Paths
Models are expected in the `Models/` directory:
- `plant_disease_classifier_cnn.keras`
- `paddy_diseases_classifier_cnn.keras`
- `pest_classifier_effnetB3.keras`

### Annotation Files
Class labels are loaded from `annotations/` directory:
- `plant_disease_classifier.csv`
- `paddy_disease_classifier.csv`
- `pest_classifier.csv`
- `router_classifier.csv`

## 🚧 Development Status

### ✅ Completed
- Plant disease detection API and frontend
- Paddy disease classification API and frontend
- Pest identification API and frontend
- Comprehensive API documentation
- System launcher and setup scripts

### 🚧 In Progress
- Router classifier model (placeholder implementation)
- Unified interface (waiting for router model)

### 📋 TODO
- Train and integrate router classifier model
- Add batch prediction endpoints
- Implement user authentication
- Add prediction history
- Performance optimization

## 🛠️ Troubleshooting

### Common Issues

1. **Models not loading**
   - Check if model files exist in `Models/` directory
   - Verify file permissions
   - Check available RAM (models require ~2GB each)

2. **API not starting**
   - Ensure port 8000 is not in use
   - Check if all dependencies are installed
   - Verify Python version (3.8+)

3. **Frontend connection issues**
   - Ensure API server is running first
   - Check if port 8501 is available
   - Verify API URL in frontend code

4. **Prediction errors**
   - Check image format (JPG, PNG supported)
   - Verify image is not corrupted
   - Ensure image contains relevant content

### Getting Help

1. Check the API health endpoint: http://localhost:8000/health
2. Review server logs for error messages
3. Verify all required files are present
4. Check the API documentation: http://localhost:8000/docs

## 📄 License

This project is part of an Agricultural Technology Hackathon.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For technical support or questions about the API integration, refer to the comprehensive API documentation in `api.md`.

---

**Version**: 2.0.0  
**Last Updated**: 2024  
**Built with**: FastAPI, Streamlit, TensorFlow