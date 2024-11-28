import os
import re
from string import punctuation
import pymorphy2
import matplotlib.pyplot as plt
from collections import Counter

morph = pymorphy2.MorphAnalyzer()
stop_words = {"в", "на", "с", "к", "от", "до", "из", "перед", "за", "под", "над", "между", "через", "около", "возле", "рядом", "против", "мимо", "сквозь", "по", "для", "без", "через", "у", "о", "об", "со", "и"}

def preprocess_text(text):
    text = text.lower()
    text = "".join(c for c in text if c not in punctuation)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def create_word_frequency(text):
    words = text.split()
    normalized_words = [morph.parse(word)[0].normal_form for word in words if word not in stop_words]
    return Counter(normalized_words)

def plot_histogram(word_counts, title):
    words, counts = zip(*word_counts.most_common(20))
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts)
    plt.xlabel("Слова")
    plt.ylabel("Частота")
    plt.title(title)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def analyze_reviews(positive_dir, negative_dir):
    positive_reviews = []
    negative_reviews = []

    for filename in os.listdir(positive_dir):
        try:
            with open(os.path.join(positive_dir, filename), 'r', encoding='utf-8') as f:
                text = f.read()
                positive_reviews.append({"text": preprocess_text(text), "sentiment": "positive"})
        except UnicodeDecodeError:
            print(f"Ошибка чтения файла {filename} в директории положительных отзывов.")

    for filename in os.listdir(negative_dir):
        try:
            with open(os.path.join(negative_dir, filename), 'r', encoding='utf-8') as f:
                text = f.read()
                negative_reviews.append({"text": preprocess_text(text), "sentiment": "negative"})
        except UnicodeDecodeError:
            print(f"Ошибка чтения файла {filename} в директории отрицательных отзывов.")

    positive_word_counts = [create_word_frequency(review["text"]) for review in positive_reviews]
    negative_word_counts = [create_word_frequency(review["text"]) for review in negative_reviews]

    for i, counts in enumerate(positive_word_counts):
        plot_histogram(counts, f"Гистограмма для положительного отзыва {i+1}")
    for i, counts in enumerate(negative_word_counts):
        plot_histogram(counts, f"Гистограмма для отрицательного отзыва {i+1}")

    all_positive_words = set().union(*positive_word_counts)
    all_negative_words = set().union(*negative_word_counts)

    only_positive = all_positive_words - all_negative_words
    only_negative = all_negative_words - all_positive_words
    common_words = all_positive_words & all_negative_words

    print("Слова, встречающиеся только в положительных отзывах:", only_positive)
    print("Слова, встречающиеся только в отрицательных отзывах:", only_negative)
    print("Общие слова:", common_words)


positive_reviews_dir = r"C:\Users\Lenovo\PycharmProjects\Volga_tech_HT1\HW4\reviews\positive.txt"
negative_reviews_dir = r"C:\Users\Lenovo\PycharmProjects\Volga_tech_HT1\HW4\reviews\negative.txt"

analyze_reviews(positive_reviews_dir, negative_reviews_dir)

#не выводится ответ, выдает:Traceback (most recent call last):
# File "C:\Users\Lenovo\PycharmProjects\Volga_tech_HT1\HW4\HW4_task.1.py", line 8, in <module>
#    morph = pymorphy2.MorphAnalyzer()
# File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python313\Lib\site-packages\pymorphy2\analyzer.py", line 224, in __init__
#    self._init_units(units)
#    ~~~~~~~~~~~~~~~~^^^^^^^
#  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python313\Lib\site-packages\pymorphy2\analyzer.py", line 235, in _init_units
#    self._units.append((self._bound_unit(unit), False))
#                       ~~~~~~~~~~~~~~~~^^^^^^
#  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python313\Lib\site-packages\pymorphy2\analyzer.py", line 246, in _bound_unit
#    unit = unit.clone()
#  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python313\Lib\site-packages\pymorphy2\units\base.py", line 35, in clone
#    return self.__class__(**self._get_params())
#                           ~~~~~~~~~~~~~~~~^^
#  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python313\Lib\site-packages\pymorphy2\units\base.py", line 76, in _get_params
#    (key, getattr(self, key, None)) for key in self._get_param_names()
#                                               ~~~~~~~~~~~~~~~~~~~~~^^
#  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python313\Lib\site-packages\pymorphy2\units\base.py", line 70, in _get_param_names
#    args, varargs, kw, default = inspect.getargspec(cls.__init__)
#                                 ^^^^^^^^^^^^^^^^^^
# AttributeError: module 'inspect' has no attribute 'getargspec'. Did you mean: 'getargs'?
