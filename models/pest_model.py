import tensorflow as tf
import pandas as pd
import numpy as np
from models.base import BaseModel
from PIL import Image
import io
from keras import backend as K

class PestModel(BaseModel):
    def __init__(self, model_path, annotation_path):
        self.model_path = model_path
        self.annotation_path = annotation_path
        self.model = None
        self.class_names = []

    def focal_loss(self, gamma=2.0, alpha=0.25):
        def focal_loss_fixed(y_true, y_pred):
            y_pred = tf.clip_by_value(y_pred, K.epsilon(), 1. - K.epsilon())
            cross_entropy = -y_true * tf.math.log(y_pred)
            loss = alpha * tf.pow(1 - y_pred, gamma) * cross_entropy
            return tf.reduce_sum(loss, axis=1)
        return focal_loss_fixed

    def load(self):
        self.model = tf.keras.models.load_model(
            self.model_path,
            custom_objects={'focal_loss_fixed': self.focal_loss(gamma=2.0, alpha=0.25)}
        )
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
            "endpoint": "pest",
            "description": "Agricultural pest identification",
            "prediction": {
                "class_index": idx,
                "class_name": class_name,
                "confidence": confidence,
                "is_healthy": is_healthy
            },
            "top_3_predictions": top_3,
            "model_used": "pest"
        }
