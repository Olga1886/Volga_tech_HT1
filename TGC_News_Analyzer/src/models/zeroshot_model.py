from transformers import pipeline
from typing import List
class ZeroShotModel:
    def __init__(self, model_path="facebook/bart-large-mnli"):
        self.classifier = pipeline("zero-shot-classification", model=model_path)


    def classify(self, texts: List[str], labels: List[str]) -> List[str]:
        results = self.classifier(texts, labels, multi_label=False)
        return [result['labels'][0] for result in results]
