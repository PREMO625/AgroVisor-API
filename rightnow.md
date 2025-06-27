# rightnow.md

## Current Focus
- Phase 3: Modular, Scalable, and Efficient API Backend for Hugging Face Spaces

## Progress Log
- Phase 1: Router classifier API endpoint implemented and integrated with Streamlit app (done)
- Phase 2: Streamlit App & Endpoint Integration Testing completed (all endpoints and UI/UX verified functional, text visibility issues fixed)
- All frontend and backend components are now functional and stable.

## Current Task
- Refactor backend into a modular FastAPI project for Hugging Face Spaces (free tier) and Docker deployment.
- Organize codebase into multiple folders/modules for clarity and maintainability.
- Ensure plug-and-play model architecture (easy model swapping via config files in `models/configs/`).
- Implement lazy loading for models (load only when needed).
- Add LRU model caching with auto-eviction (max 2 models in memory).
- Build request queuing system with queue/model limits.
- Ensure thread safety and handle race conditions.
- Optimize for resource constraints and multi-user scenarios.
- Use Dockerfile to set entrypoint: `uvicorn api.main:app --host 0.0.0.0 --port 7860`.

### Modular Folder Structure
```
AgroVisor-API/
│
├── api/
│   ├── __init__.py
│   ├── main.py
│   └── endpoints/
│       ├── __init__.py
│       ├── plant_disease.py
│       ├── paddy_disease.py
│       ├── pest.py
│       └── unified.py
│
├── models/
│   ├── __init__.py
│   ├── base.py
│   ├── loader.py
│   ├── cache.py
│   └── configs/
│       ├── plant_disease.yaml
│       ├── paddy_disease.yaml
│       ├── pest.yaml
│       └── router.yaml
│
├── queue/
│   ├── __init__.py
│   └── queue_manager.py
│
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   └── helpers.py
│
├── Models/
├── annotations/
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── README.md
└── rightnow.md
```

### Subtasks
- [ ] Refactor codebase into modular structure
- [ ] Implement plug-and-play model loading via configs
- [ ] Add lazy loading for models
- [ ] Implement LRU model caching
- [ ] Build request queuing system
- [ ] Ensure thread safety
- [ ] Optimize for Hugging Face Spaces
- [ ] Test and document the API backend

---

_Current focus: Modular refactor, lazy loading, LRU caching, and Dockerization for Hugging Face Spaces._

(Updated automatically by GitHub Copilot)
