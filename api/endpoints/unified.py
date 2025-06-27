from fastapi import APIRouter, UploadFile, File, HTTPException
from models.loader import ModelLoader

router = APIRouter(prefix="/predict/unified", tags=["Unified"])

model_loader = ModelLoader(config_dir="models/configs")

@router.post("")
async def predict_unified(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        router_model = model_loader.load_model("router")
        router_result = router_model.predict(image_bytes)
        # Example: decide which model to use based on router_result
        model_key = router_result.get("model_key", "plant_disease")
        model = model_loader.load_model(model_key)
        result = model.predict(image_bytes)
        return {"filename": file.filename, "router_info": router_result, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
