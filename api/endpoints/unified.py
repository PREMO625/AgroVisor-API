from fastapi import APIRouter, UploadFile, File, HTTPException
from models.loader import ModelLoader
from request_queue.queue_manager import RequestQueue
from queue import Full

router = APIRouter(prefix="/predict/unified", tags=["Unified"])

model_loader = ModelLoader(config_dir="models/configs")

# Initialize a global request queue (can be tuned for maxsize)
request_queue = RequestQueue(maxsize=10)

@router.post("")
async def predict_unified(file: UploadFile = File(...)):
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded or file is invalid.")
    try:
        image_bytes = await file.read()
        if not image_bytes:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")
        def process_request():
            try:
                router_model = model_loader.load_model("router")
            except Exception:
                raise HTTPException(status_code=503, detail="Router model not loaded or unavailable.")
            router_result = router_model.predict(image_bytes)
            model_key = router_result.get("model_key", "plant_disease")
            try:
                model = model_loader.load_model(model_key)
            except Exception:
                raise HTTPException(status_code=503, detail=f"Model '{model_key}' not loaded or unavailable.")
            result = model.predict(image_bytes)
            return {"filename": file.filename, "router_info": router_result, **result}
        try:
            request_queue.add_request(process_request)
        except Full:
            raise HTTPException(status_code=429, detail="Request queue is full. Please try again later.")
        response = request_queue.get_request()()
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
