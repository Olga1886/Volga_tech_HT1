import os
import re
from string import punctuation
import pymorphy3
import matplotlib.pyplot as plt
from collections import Counter

morph = pymorphy3.MorphAnalyzer()
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
    if not os.path.isdir(positive_dir) or not os.path.isdir(negative_dir):
        raise ValueError("Оба параметра должны быть путями к папкам.")

    positive_reviews = []
    negative_reviews = []

    for filename in os.listdir(positive_dir):
        try:
            file_path = os.path.join(positive_dir, filename)
            if os.path.isfile(file_path):  # Проверка, является ли это файлом
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    positive_reviews.append({"text": preprocess_text(text), "sentiment": "positive"})
        except UnicodeDecodeError:
            print(f"Ошибка чтения файла {filename} в директории положительных отзывов.")

    for filename in os.listdir(negative_dir):
        try:
            file_path = os.path.join(negative_dir, filename)
            if os.path.isfile(file_path):  # Проверка, является ли это файлом
                with open(file_path, 'r', encoding='utf-8') as f:
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

# Пример использования:
positive_reviews_dir = r"C:\Users\Lenovo\PycharmProjects\Volga_tech_HT1\HW4\reviews\positive"
negative_reviews_dir = r"C:\Users\Lenovo\PycharmProjects\Volga_tech_HT1\HW4\reviews\negative"

analyze_reviews(positive_reviews_dir, negative_reviews_dir)
