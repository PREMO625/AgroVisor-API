from fastapi import APIRouter, UploadFile, File, HTTPException
from models.loader import ModelLoader
from request_queue.queue_manager import RequestQueue

router = APIRouter(prefix="/predict/pest", tags=["Pest"])

model_loader = ModelLoader(config_dir="models/configs")
request_queue = RequestQueue(maxsize=10)

@router.post("")
async def predict_pest(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        def process_request():
            model = model_loader.load_model("pest")
            result = model.predict(image_bytes)
            return {"filename": file.filename, **result}
        request_queue.add_request(process_request)
        response = request_queue.get_request()()
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
