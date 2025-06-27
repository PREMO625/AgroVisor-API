from fastapi import FastAPI
from api.endpoints import plant_disease, paddy_disease, pest, unified

app = FastAPI(title="AgroVisor API", description="Modular, scalable backend for Hugging Face Spaces.")

# Include routers from endpoints (to be implemented in each endpoint module)
app.include_router(plant_disease.router)
app.include_router(paddy_disease.router)
app.include_router(pest.router)
app.include_router(unified.router)
