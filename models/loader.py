import threading
from .cache import ModelCache
from .base import BaseModel
import yaml
import importlib

class ModelLoader:
    def __init__(self, config_dir, cache_size=2):
        self.config_dir = config_dir
        self.cache = ModelCache(max_size=cache_size)
        self.lock = threading.Lock()

    def load_model(self, model_name):
        with self.lock:
            if model_name in self.cache:
                return self.cache[model_name]
            config_path = f"{self.config_dir}/{model_name}.yaml"
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            module = importlib.import_module(config['module'])
            model_class = getattr(module, config['class'])
            model = model_class(**config.get('params', {}))
            model.load()
            self.cache[model_name] = model
            return model
