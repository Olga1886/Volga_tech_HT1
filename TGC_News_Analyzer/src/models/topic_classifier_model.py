from transformers import pipeline
from typing import List


class TopicClassifierModel:
    def __init__(self, model_path="textattack/bert-base-uncased-QQP"):
        self.classifier = pipeline("text-classification", model=model_path)


    def classify(self, texts: List[str], labels:List[str]=None) -> List[str]:
        results = self.classifier(texts)
        return [result['label'] for result in results]
