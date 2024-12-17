import os
import re
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict
from src.utils import parse_date


class TelegramDataExtractor:
    def __init__(self, input_path):
        self.input_path = input_path
        self.messages = []

    def _parse_html_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

        messages = []
        for message_div in soup.find_all('div', class_='message'):
            date_span = message_div.find('div', class_='message_date')
            if not date_span:
                continue
            date_str = date_span.text.strip()
            date = parse_date(date_str)

            text_div = message_div.find('div', class_='text')
            if not text_div:
                continue
            message_text = text_div.text.strip()
            messages.append({"date": date, "text": message_text})
        return messages

    def extract_data(self) -> List[Dict]:
        """Extracts data from HTML files."""

        if os.path.isdir(self.input_path):
            for filename in os.listdir(self.input_path):
                if filename.endswith(".html"):
                    file_path = os.path.join(self.input_path, filename)
                    self.messages.extend(self._parse_html_file(file_path))
        elif os.path.isfile(self.input_path) and self.input_path.endswith(".html"):
            self.messages = self._parse_html_file(self.input_path)
        else:
            raise ValueError("Input path must be a directory or html file")

        return self.messages
