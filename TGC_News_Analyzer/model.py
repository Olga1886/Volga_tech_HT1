import nltk
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')


class TextClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(preprocessor=self._preprocess_text)
        self.model = MultinomialNB()
        self.classes = ['positive', 'negative', 'neutral', 'economy', 'culture', 'health', 'other', 'sport', 'politics',
                        'disaster', 'entertainment']

    def _preprocess_text(self, text):
        text = text.lower()
        text = re.sub(r'[^a-zа-я0-9\s]', '', text)
        tokens = word_tokenize(text)
        stop_words = set(stopwords.words('russian') + stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]
        return " ".join(tokens)

    def train(self, texts, labels):

        self.vectorizer.fit(texts)
        self.model.fit(self.vectorizer.transform(texts), labels)

    def predict(self, text):
        if not isinstance(text, list):
            text = [text]
        return self.model.predict(self.vectorizer.transform(text))

    def get_semantic_score(self, label):
        if label == 'positive':
            return 1
        elif label == 'negative':
            return -1
        else:
            return 0