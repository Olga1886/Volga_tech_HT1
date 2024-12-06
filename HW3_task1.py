import json
import os

def read_data(path):
    data = open(path, 'rt', encoding='UTF-8').read()
    return data.split('\n')

# Задание 1:Напишите программу, которая переберет все слова и занесет их в словарь (назвать его можете как угодно).
# Увеличивайте счётчик при добавлении каждого нового слова, чтобы посчитать сколько раз это слово встречается в тексте.


def word_dictionary(data) -> dict:
    frequency_dic = {}
    for word in data:
        if word not in frequency_dic:
            frequency_dic[word] = 1
            continue
        if word in frequency_dic:
            frequency_dic[word] += 1
    return frequency_dic


def split_to_chapters(data):
    # Разбиваем текст на главы
    deliminators_indicis = [i for i, e in enumerate(data) if e == '[new chapter]']
    start = 0
    chapters = []
    for index in deliminators_indicis:
        chapter_context = data[start + 1:index]
        chapters.append(chapter_context)
        start = index
    last_chapter = data[start + 1:]
    chapters.append(last_chapter)
    return chapters


def create_chapters_dicts(data):
    deliminators_indicis = [i for i, e in enumerate(data[1:]) if e == '[new chapter]']
    start = 0
    chapter_frequencies = []
    for index in deliminators_indicis:
        chapter_context = data[start + 1:index]
        chapter_frequency = word_dictionary(chapter_context)
        chapter_frequencies.append(chapter_frequency)
        start = index
    last_chapter = data[start +1:]
    chapter_frequency = word_dictionary(last_chapter)
    chapter_frequencies.append(chapter_frequency)
    return chapter_frequencies

# Пример:
file_path = "war_peace.txt"
data = read_data(file_path)
word_frequencies = word_dictionary(data)
print(word_frequencies)

# Вывод результатов:
print(json.dumps(word_frequencies, indent=4, ensure_ascii=False))

# Задание 2: Напишите программу, которая посчитает chapter frequency для заданного слова target_word.
#     chapter_freq = number_of_chapters_with_target_word / number_of_chapters
#     number_of_chapters_with_target_word - общее количество глав
#     number_of_chapters - количество глав, в которых встречается target_word

def chapter_frequency(path: str, target_word: str) -> float:
    data = read_data(path)
    chapter_frequencies = create_chapters_dicts(data)

    number_of_chapters = len(chapter_frequencies)
    number_of_chapters_with_target_word = 0

    for chapter_dict in chapter_frequencies:
        if target_word.lower() in chapter_dict:
            number_of_chapters_with_target_word += 1

    if number_of_chapters == 0:
        return 0.0

    chapter_freq = number_of_chapters_with_target_word / number_of_chapters
    return chapter_freq

# Пример:
file_path = "war_peace.txt"
target_word = "война"
chapter_freq = chapter_frequency(file_path, target_word)
print(f"Chapter frequency for '{target_word}': {chapter_freq}")

# Задание 3: Напишите программу, которая выведет частоту употребления заданного слова target_word в заданной главе target_chapter.
#     tf = количество раз, когда слово target_word встречается в тексте главы / количество всех слов в тексте главы

def term_frequency(target_word: str, target_chapter_idx: int, chapters: list) -> float: #Изменено: chapters - list
    if 0 <= target_chapter_idx < len(chapters):
        chapter_dict = chapters[target_chapter_idx]
        total_words = sum(chapter_dict.values())
        count_target_word = chapter_dict.get(target_word.lower(), 0)

        if total_words > 0:
            tf = count_target_word / total_words
            return tf
        else:
            return 0.0
    else:
        return 0.0


#Пример:
chapters = create_chapters_dicts(read_data("war_peace.txt")) # chapters = list
target_word = "мир"
target_chapter_idx = 170 #заменить на нужный индекс
tf = term_frequency(target_word, target_chapter_idx, chapters)
print(f"Term frequency for '{target_word}' in chapter {target_chapter_idx}: {tf}")

print(f"Term frequency for 'лес' in chapter 25: {tf}")

# Задание 4: Напишите программу, которая выведет значение tf*idf для заданного слова target_word в заданной главе target_chapter.
#     https://en.wikipedia.org/wiki/Tf%E2%80%93idf
#
#     tf_idf = tf*idf = term frequency * inverse document frequency
#     tf — это частотность термина, которая измеряет, насколько часто термин встречается в документе.
#     idf — это обратная документная частотность термина. Она измеряет непосредственно важность термина во всём множестве документов.

import math
from collections import Counter

def get_tf_idf(data, target_word: str, target_chapter: int) -> float:
    # Разделение документа на главы
    chapter_texts = split_to_chapters(data)  # создание списка глав
    chapter_text = chapter_texts[target_chapter]
    print(chapter_text)
    total_words = len(chapter_text)
    term_count = chapter_text.count(target_word.lower())
    if total_words > 0:
        tf = term_count / total_words
    else:
        tf = 0.0
    total_chapters = len(chapter_texts)
    doc_count = sum(1 for chapter in chapter_texts if target_word.lower() in chapter)
    if doc_count > 0:
        idf = math.log(total_chapters / doc_count)
    else:
        idf = 0.0
    tf_idf = tf * idf
    return tf_idf

# Пример использования:
file_path = "war_peace.txt"
data = read_data(file_path)
target_word = "князь"
target_chapter = 95
tf_idf_score = get_tf_idf(file_path, target_word, target_chapter)


print(f"TF-IDF for '{target_word}' in chapter {target_chapter}: {tf_idf_score}")

# Вывод TF-IDF для других слов и глав:
#print(f"TF-IDF for 'свет' in chapter 20: {get_tf_idf(file_path, 'свет', 20)}")
#print(f"TF-IDF for 'Пьер' in chapter 20: {get_tf_idf(file_path, 'Пьер', 20)}")
#print(f"TF-IDF for 'дуб' in chapter 110: {get_tf_idf(file_path, 'дуб', 110)}")

#для корректной работы вызова функции в последнем задании необходимо поставить # перед другими примерами в задачах
