from fastapi import APIRouter, UploadFile, File, HTTPException
from models.loader import ModelLoader

router = APIRouter(prefix="/predict/pest", tags=["Pest"])

model_loader = ModelLoader(config_dir="models/configs")

@router.post("")
async def predict_pest(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        model = model_loader.load_model("pest")
        result = model.predict(image_bytes)
        return {"filename": file.filename, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
