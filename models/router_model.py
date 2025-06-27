import tensorflow as tf
import pandas as pd
import numpy as np
from models.base import BaseModel
from PIL import Image
import io

class RouterModel(BaseModel):
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
        # Map router class to model key
        if 'plant' in class_name:
            model_key = 'plant_disease'
        elif 'paddy' in class_name:
            model_key = 'paddy_disease'
        elif 'pest' in class_name:
            model_key = 'pest'
        else:
            model_key = 'plant_disease'
        return {
            "router_prediction": class_name,
            "router_confidence": confidence,
            "model_key": model_key,
            "available_classifiers": self.class_names
        }
