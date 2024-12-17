import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from typing import List


class TfidfModel:
    def __init__(self):
        self.model = make_pipeline(TfidfVectorizer(), MultinomialNB())
        self.labels = ["POSITIVE", "NEUTRAL", "NEGATIVE"]
        self.training_data = [
                "This is a great day!",
                "I am feeling good.",
                "The weather is nice.",
                "I'm feeling okay today.",
                "It is a normal day.",
                "I am neutral about it.",
                "I am feeling bad.",
                "This is terrible!",
                "I'm very sad today."
            ]
        self.training_labels = [
                "POSITIVE",
                "POSITIVE",
                "POSITIVE",
                "NEUTRAL",
                "NEUTRAL",
                "NEUTRAL",
                "NEGATIVE",
                "NEGATIVE",
                "NEGATIVE",
            ]
        self.model.fit(self.training_data, self.training_labels)


    def classify(self, texts: List[str]) -> List[str]:
        return self.model.predict(texts).tolist()
