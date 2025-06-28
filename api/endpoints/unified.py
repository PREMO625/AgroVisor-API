from fastapi import APIRouter, UploadFile, File, HTTPException
from models.loader import ModelLoader
from request_queue.queue_manager import RequestQueue

router = APIRouter(prefix="/predict/unified", tags=["Unified"])

model_loader = ModelLoader(config_dir="models/configs")

# Initialize a global request queue (can be tuned for maxsize)
request_queue = RequestQueue(maxsize=10)

@router.post("")
async def predict_unified(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        # Add request to queue and process in order
        def process_request():
            router_model = model_loader.load_model("router")
            router_result = router_model.predict(image_bytes)
            model_key = router_result.get("model_key", "plant_disease")
            model = model_loader.load_model(model_key)
            result = model.predict(image_bytes)
            return {"filename": file.filename, "router_info": router_result, **result}
        request_queue.add_request(process_request)
        # For simplicity, process immediately after adding (single worker scenario)
        response = request_queue.get_request()()
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
