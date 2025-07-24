# Agricultural AI System (AgroVisor)

A comprehensive AI-powered system for plant disease detection, paddy disease classification, and pest identification. Now available as a live web app and public API!

## 🌟 Features

- **Plant Disease Detection**: Identify diseases in 38 different plant classes
- **Paddy Disease Classification**: Specialized classification for 13 rice/paddy diseases
- **Pest Identification**: Recognize 102 different agricultural pest types
- **Unified Interface**: Smart routing system (auto-selects the right model)
- **Web API**: RESTful API with modular, scalable backend (FastAPI)
- **Frontend Application**: Modern, user-friendly web app (deployed on Vercel)
- **Production-Ready Deployments**: Public API on Hugging Face Spaces, frontend on Vercel

## 🚀 Live Demo & Public API

- **Web App (Frontend):** [https://agrovisor.vercel.app/](https://agrovisor.vercel.app/)
- **API (Hugging Face Spaces):** [https://huggingface.co/spaces/premo625/AgriVisor-API](https://huggingface.co/spaces/premo625/AgriVisor-API)

## 📋 System Requirements

- Python 3.8+
- TensorFlow 2.15.0
- 8GB+ RAM (for model loading)
- Required model files in `Models/` directory
- Annotation files in `annotations/` directory

## 📁 Project Structure

```
AgroVisor-API/
├── api/                  # FastAPI backend (modular endpoints)
│   ├── main.py
│   └── endpoints/
├── models/               # Model loading, configs, cache
│   ├── loader.py
│   ├── cache.py
│   └── configs/
├── utils/                # Logging, helpers
├── request_queue/        # Request queueing, concurrency
├── Models/               # Model files (.keras)
├── annotations/          # Class label files (.csv)
├── frontend_app.py       # (Legacy) Streamlit frontend
├── requirements.txt
├── Dockerfile
├── README.md
└── ...
```

## 🔗 Access URLs

- **Live Web App:** [https://agrovisor.vercel.app/](https://agrovisor.vercel.app/)
- **API (Hugging Face):** [https://huggingface.co/spaces/premo625/AgriVisor-API](https://huggingface.co/spaces/premo625/AgriVisor-API)

## 🔌 API Endpoints

| Endpoint                  | Method | Description                        |
|--------------------------|--------|------------------------------------|
| `/predict/plant-disease` | POST   | Plant disease detection            |
| `/predict/paddy-disease` | POST   | Paddy disease classification       |
| `/predict/pest`          | POST   | Pest identification                |
| `/predict/unified`       | POST   | Unified classification (auto-route)|
| `/health`                | GET    | System health check                |
| `/models/info`           | GET    | Model information                  |

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

### Web App (Recommended)
1. Go to [https://agrovisor.vercel.app/](https://agrovisor.vercel.app/)
2. Select the task (Unified, Plant, Paddy, Pest)
3. Upload an image and get instant results

### API Usage (Python)
```python
import requests

url = "https://premo625-agrivisor-api.hf.space/predict/unified"
files = {"file": open("your_image.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

### API Usage (cURL)
```bash
curl -X POST "https://premo625-agrivisor-api.hf.space/predict/plant-disease" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@plant_image.jpg"
```

## 🔧 Configuration

- **Model files:** Place in `Models/`
- **Annotation files:** Place in `annotations/`
- **Environment:**
  - `PORT` (optional): API server port (default: 7860 on Hugging Face)

## 🚧 Development Status

- ✅ All endpoints and unified interface implemented
- ✅ Modular, scalable backend (FastAPI)
- ✅ Lazy loading, LRU cache, request queueing
- ✅ Hugging Face Spaces deployment (API)
- ✅ Vercel deployment (web app)
- 🚧 Router classifier model (improving)
- 🚧 Batch prediction, user auth, history (planned)

## 🛠️ Troubleshooting

- **API not responding?**
  - Check [API health](https://premo625-agrivisor-api.hf.space/health)
  - If using free tier, wait and retry (resource limits)
- **Model not loading?**
  - Ensure model files are present in `Models/`
- **Frontend not working?**
  - Make sure API is up and reachable from the web app

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of an Agricultural Technology Hackathon.

---

**Version**: 2.1.0  
**Last Updated**: June 2025  
**Built with**: FastAPI, Streamlit, TensorFlow, Vercel, Hugging Face Spaces
