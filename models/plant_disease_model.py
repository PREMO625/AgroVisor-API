import tensorflow as tf
import pandas as pd
import numpy as np
from models.base import BaseModel
from PIL import Image
import io

class PlantDiseaseModel(BaseModel):
    def __init__(self, model_path, annotation_path):
        self.model_path = model_path
        self.annotation_path = annotation_path
        self.model = None
        self.class_names = []

    def load(self):
        self.model = tf.keras.models.load_model(self.model_path)
        df = pd.read_csv(self.annotation_path)
        self.class_names = df['class_name'].tolist()

    def preprocess(self, image_bytes):
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        img = np.array(image)
        img = tf.image.resize(img, (224, 224)).numpy()
        img = img.astype('float32') / 255.0
        img = np.expand_dims(img, axis=0)
        return img

    def predict(self, image_bytes):
        img = self.preprocess(image_bytes)
        preds = self.model.predict(img)[0]
        idx = int(np.argmax(preds))
        confidence = float(preds[idx])
        class_name = self.class_names[idx]
        top_3_idx = np.argsort(preds)[-3:][::-1]
        top_3 = [
            {"class_index": int(i), "class_name": self.class_names[i], "confidence": float(preds[i])}
            for i in top_3_idx
        ]
        is_healthy = 'healthy' in class_name.lower() or 'normal' in class_name.lower()
        return {
            "endpoint": "plant-disease",
            "description": "General plant disease classification",
            "prediction": {
                "class_index": idx,
                "class_name": class_name,
                "confidence": confidence,
                "is_healthy": is_healthy
            },
            "top_3_predictions": top_3,
            "model_used": "plant_disease"
        }
