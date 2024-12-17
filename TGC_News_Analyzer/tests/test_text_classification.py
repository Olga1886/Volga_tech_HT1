import unittest
from src.text_classification import TextClassifier


class TestTextClassifier(unittest.TestCase):
    def test_tfidf_classification(self):
        classifier = TextClassifier(model_type="tfidf")
        texts = ["This is a great day!", "I am feeling bad."]
        labels = classifier.classify(texts)
        self.assertEqual(len(labels), 2)
        self.assertTrue(labels[0] in ["POSITIVE", "NEUTRAL", "NEGATIVE"])
        self.assertTrue(labels[1] in ["POSITIVE", "NEUTRAL", "NEGATIVE"])

    def test_zeroshot_classification(self):
        classifier = TextClassifier(model_type="zeroshot")
        texts = ["This is about sports", "This is a disaster"]
        labels = ["sport", "disaster"]
        predicted_labels = classifier.classify(texts, labels=labels)
        self.assertEqual(len(predicted_labels), 2)
        self.assertTrue(predicted_labels[0] in labels)
        self.assertTrue(predicted_labels[1] in labels)

    def test_topic_classifier(self):
        classifier = TextClassifier(model_type="topic_classifier")
        texts = ["This is about sports", "This is a disaster"]
        predicted_labels = classifier.classify(texts)
        self.assertEqual(len(predicted_labels), 2)

    def test_calculate_sentiment(self):
        classifier = TextClassifier(model_type="tfidf")
        labels = ["POSITIVE", "NEUTRAL", "NEGATIVE", "UNKNOWN"]
        sentiments = classifier.calculate_sentiment(labels)
        self.assertEqual(sentiments, [1, 0, -1, 0])


if __name__ == '__main__':
    unittest.main()
