# AgroVisor API Development Rules and Task List

## Rules
- This file is the master reference for all tasks and rules for building the backend API.
- Every update or edit to the project must be preceded by a fresh analysis of the codebase to ensure up-to-date context.
- For each change, an explanation of what will be done and how it will be done must be provided. No implementation will proceed without explicit approval from the user.
- Tasks will only be marked as done after the user explicitly confirms completion.
- All ongoing work, current focus, and progress must be documented in `rightnow.md` to provide a real-time, high-level overview of what is being worked on at any given moment.

## Phase 1: Router Classifier API Endpoint

### Task Description
- Analyze the `Models` folder, focusing on the `router_classifier_best.keras` model.
- Implement the router classifier API endpoint (placeholders already exist).
- The endpoint should:
  - Accept an image from the unified frontend interface.
  - Use the router classifier model to determine which specialized model (paddy, pest, plant disease, etc.) the image should be routed to.
  - Route the image to the correct model endpoint and return the final output.
  - Ensure the endpoint is connected to the Streamlit app as part of the unified interface.

### Status
- [x] Router classifier API endpoint implemented and integrated with Streamlit app (done)

---

## Phase 2: Streamlit App & Endpoint Integration Testing

### Task Description
- Test the entire Streamlit app interface.
- Verify that all API endpoints are correctly integrated and functioning as expected within the app.
- Check the end-to-end flow: ensure images are processed, routed, and results are displayed properly through the unified interface.

### Status
- [x] Phase 2: Streamlit App & Endpoint Integration Testing
    - [x] Manual testing checklist completed
    - [x] All endpoints and UI/UX verified functional
    - [x] All frontend text visibility issues fixed (CSS improved)
    - [x] Marked as done

---

## Phase 3: Modular, Scalable, and Efficient API Backend for Hugging Face Spaces

### Task Description
- Refactor the backend into a modular, maintainable, and scalable FastAPI project, optimized for Hugging Face Spaces (free tier) and Docker deployment.
- Organize the codebase into multiple folders/modules for clarity and maintainability (avoid a single monolithic script).
- Ensure plug-and-play architecture: models can be swapped in/out easily by editing config files in `models/configs/`.
- Implement lazy loading: only load a model into memory when it is actually requested.
- Add a caching mechanism for loaded models, with LRU (Least Recently Used) auto-eviction (max 2 models in memory).
- Build a queuing system for incoming requests, with a limit on the number of models loaded at once.
- Ensure thread safety and handle race conditions for multi-user and concurrent requests.
- Optimize the API for resource constraints and multi-user scenarios typical of Hugging Face Spaces.
- Use Docker for deployment, with a `Dockerfile` that sets the entrypoint to run the API with Uvicorn.

#### Folder Structure
```
AgroVisor-API/
│
├── api/
│   ├── __init__.py
│   ├── main.py                # FastAPI app entrypoint (app instance here)
│   └── endpoints/
│       ├── __init__.py
│       ├── plant_disease.py
│       ├── paddy_disease.py
│       ├── pest.py
│       └── unified.py
│
├── models/
│   ├── __init__.py
│   ├── base.py                # Base model interface/abstract class
│   ├── loader.py              # Plug-and-play loader, lazy loading logic
│   ├── cache.py               # LRU cache with auto-eviction
│   └── configs/
│       ├── plant_disease.yaml
│       ├── paddy_disease.yaml
│       ├── pest.yaml
│       └── router.yaml
│
├── queue/
│   ├── __init__.py
│   └── queue_manager.py       # Request queueing, concurrency, thread safety
│
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   └── helpers.py
│
├── Models/                    # Model files (as before)
├── annotations/               # Annotation files (as before)
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── README.md
└── rightnow.md
```

#### Details
- `models/` handles all model logic: loading, inference, config, caching, and lazy loading.
- `utils/` contains logging and helper utilities used across the project.
- Lazy loading and LRU caching are implemented in `models/loader.py` and `models/cache.py`.
- Only 2 models are kept in memory at once; others are loaded/unloaded as needed.
- Dockerfile sets the entrypoint to `uvicorn api.main:app --host 0.0.0.0 --port 7860` for Hugging Face Spaces compatibility.

#### Subtasks
- [x] Refactor codebase into modular structure (folders, files, configs)
- [x] Implement plug-and-play model loading via configs
- [x] Add lazy loading for models
- [x] Implement model caching with LRU auto-eviction
- [x] Build request queuing system with queue/model limits
- [x] Ensure thread safety and handle race conditions
- [x] Optimize for Hugging Face Spaces (resource usage, multi-user)
- [x] Test and document the API backend

### Status
- [x] Modular, scalable, and efficient API backend implemented and optimized for Hugging Face Spaces (done)

---

## Phase 4: Final Streamlit App & API Integration Testing

### Task Description
- Test the entire Streamlit app interface again after updating the API backend.
- Verify that all endpoints and new backend features (modularity, lazy loading, caching, queuing, etc.) are correctly integrated and functioning as expected.
- Check the end-to-end flow: ensure images are processed, routed, and results are displayed properly through the unified interface with the updated backend.
- Identify and fix any issues that arise from the new backend architecture.

### Status
- [x] Final Streamlit app and API integration tested and verified (done)

---

## Phase 5: Deployment and Optimization on Hugging Face Spaces

### Task Description
- Deploy the API backend to Hugging Face Spaces.
- Test the deployment to ensure the API is running as expected in the Hugging Face environment.
- Monitor for any issues related to performance, resource usage, or multi-user scenarios.
- Optimize the API backend as needed to resolve any issues that arise post-deployment.
- Document the deployment and optimization steps.

### Status
- [ ] API backend deployed and optimized on Hugging Face Spaces (pending user approval)

---

## Phase 6: API Integration Guide for Frontend Engineer

### Task Description
- Create an `api_integration.md` file after the backend is fully completed and deployed.
- Document all API endpoints, request/response formats, authentication (if any), and usage examples.
- Provide clear instructions for integrating the backend API with the frontend (Streamlit or other interfaces).
- Highlight any changes needed in the frontend to support new or updated backend features (e.g., routing, lazy loading, error handling).
- Include troubleshooting tips and contact information for backend support.

### Status
- [ ] API integration guide created and shared with frontend engineer (pending user approval)

---

## Best Practices

### Modular & Scalable API Design
- Organize code into logical modules (e.g., separate files for model loading, prediction, routing, caching, and API endpoints).
- Use configuration files or environment variables for model paths and settings to enable plug-and-play upgrades.
- Avoid monolithic scripts; keep each component focused and testable.

### Hugging Face Spaces Deployment
- Minimize memory usage: only load models on demand (lazy loading).
- Limit the number of models in memory (e.g., max 2) to avoid exceeding resource quotas.
- Monitor resource usage and optimize code for the free tier (CPU, RAM, concurrency limits).
- Use FastAPI for async endpoints and efficient request handling.

### Model Loading, Caching, and Auto-Eviction
- Implement a model cache with LRU (Least Recently Used) eviction policy.
- Unload models that have not been used recently to free up memory.
- Handle model loading errors gracefully and log all loading/unloading events.

### Queuing & Concurrency
- Use a request queue to limit concurrent model loads and predictions.
- Set a queue size limit and return clear errors if the queue is full.
- Ensure thread/process safety when accessing shared resources (models, cache, queue).
- Use async/await and FastAPI background tasks for non-blocking operations.

### Streamlit Integration
- Always check API health before making prediction requests.
- Display clear error messages and loading states in the UI.
- Show model status (loaded/not loaded) and prediction confidence to users.
- Use client-side image resizing to reduce upload size and speed up predictions.

### Error Handling & Logging
- Validate all inputs (file type, size, content) before processing.
- Return user-friendly error messages for all API failures.
- Log all errors, warnings, and important events for debugging and monitoring.

### Security
- Restrict file types and sizes accepted by the API.
- Sanitize all user inputs and filenames.
- Consider rate limiting and authentication for production deployments.

### Testing & Documentation
- Write unit and integration tests for all API endpoints and model logic.
- Document all endpoints, expected inputs/outputs, and error codes.
- Provide clear deployment and troubleshooting instructions.

---

Further tasks and phases will be added here as the project progresses, following the same rules above.