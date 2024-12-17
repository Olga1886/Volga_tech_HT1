import numpy as np
from typing import List
from src.models.tfidf_model import TfidfModel
from src.models.zeroshot_model import ZeroShotModel
from src.models.topic_classifier_model import TopicClassifierModel


class TextClassifier:
    def __init__(self, model_type="tfidf", model_path=None):
        self.model_type = model_type
        self.model = self._load_model(model_type, model_path)


    def _load_model(self, model_type, model_path):
        if model_type == "tfidf":
            return TfidfModel()
        elif model_type == "zeroshot":
            return ZeroShotModel(model_path=model_path)
        elif model_type == "topic_classifier":
            return TopicClassifierModel(model_path=model_path)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")


    def classify(self, texts: List[str], labels: List[str] = None):
        if not texts:
            return []
        if self.model_type == 'zeroshot' or self.model_type == 'topic_classifier':
            if not labels:
                raise ValueError("Labels must be provided for Zero-Shot or Topic Classifier model")
            return self.model.classify(texts, labels)
        elif self.model_type == 'tfidf':
            return self.model.classify(texts)
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")


    def calculate_sentiment(self, labels: List[str]) -> List[int]:
        sentiment_mapping = {
            "POSITIVE": 1,
            "NEUTRAL": 0,
            "NEGATIVE": -1
        }
        return [sentiment_mapping.get(label, 0) for label in labels]
    