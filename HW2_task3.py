import requests
from bs4 import BeautifulSoup
from typing import List, Optional

def get_wiki_info(keyword: str, max_num_sentences: int = 10, max_sentence_length: int = 10) -> Optional[List[str]]:
    url = "https://simple.wikipedia.org/wiki/" + keyword.replace(" ", "_")

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.RequestException:
        return None


    paragraphs = soup.find_all('p')
    sentences = []
    keyword_sentences = []

    for paragraph in paragraphs:
        text = paragraph.get_text()
        sentences_in_paragraph = text.split('.') #Split by sentences

        for sentence in sentences_in_paragraph:
            sentence = sentence.strip()
            if sentence:
                #Remove punctuation from the end to prevent errors.
                sentence = sentence.rstrip('?!…').replace('...', '.')

                words = sentence.split()
                if len(words) > 0 and words[0].lower() == keyword.lower():
                    if len(words) <= max_sentence_length:
                        keyword_sentences.append(sentence + ".")
                    else:
                        keyword_sentences.append(" ".join(words[:max_sentence_length]) + ".")


    return keyword_sentences[:max_num_sentences]


# Example usage
result = get_wiki_info("Saturn", max_num_sentences=3, max_sentence_length=5)
print(result)

result = get_wiki_info("Python", max_num_sentences=2, max_sentence_length=6)
print(result)