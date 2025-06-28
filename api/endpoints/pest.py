from fastapi import APIRouter, UploadFile, File, HTTPException
from models.loader import ModelLoader
from request_queue.queue_manager import RequestQueue
from queue import Full

router = APIRouter(prefix="/predict/pest", tags=["Pest"])

model_loader = ModelLoader(config_dir="models/configs")
request_queue = RequestQueue(maxsize=10)

@router.post("")
async def predict_pest(file: UploadFile = File(...)):
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded or file is invalid.")
    try:
        image_bytes = await file.read()
        if not image_bytes:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")
        def process_request():
            try:
                model = model_loader.load_model("pest")
            except Exception:
                raise HTTPException(status_code=503, detail="Pest model not loaded or unavailable.")
            result = model.predict(image_bytes)
            return {"filename": file.filename, **result}
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
