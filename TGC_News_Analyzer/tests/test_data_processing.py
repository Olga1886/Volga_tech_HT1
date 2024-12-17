import os
import unittest
from src.data_processing import TelegramDataExtractor
from datetime import datetime


class TestDataExtractor(unittest.TestCase):

    def setUp(self):
        self.example_html = """
            <div class="message default clearfix">
            <div class="message_header">
                <div class="message_date pull_left">
                15 November 2024, 12:00
                </div>
                </div>
                <div class="text">
                First message text.
                </div>
            </div>
            <div class="message default clearfix">
                <div class="message_header">
                    <div class="message_date pull_left">
                        16 Nov 2024, 10:30
                    </div>
                </div>
                    <div class="text">
                        Second message text.
                    </div>
            </div>
            """

        self.example_html_file = "test_example.html"
        with open(self.example_html_file, "w", encoding="utf-8") as f:
            f.write(self.example_html)

    def test_extract_data_from_file(self):
        extractor = TelegramDataExtractor(self.example_html_file)
        messages = extractor.extract_data()
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]['text'], 'First message text.')
        self.assertEqual(messages[1]['text'], 'Second message text.')
        self.assertEqual(messages[0]['date'], datetime(2024, 11, 15, 12, 0))
        self.assertEqual(messages[1]['date'], datetime(2024, 11, 16, 10, 30))

    def test_extract_data_from_folder(self):
        os.makedirs("test_folder", exist_ok=True)
        example_file_1 = "test_folder/example1.html"
        example_file_2 = "test_folder/example2.html"

        with open(example_file_1, "w", encoding="utf-8") as f:
            f.write(self.example_html)
        with open(example_file_2, "w", encoding="utf-8") as f:
            f.write(self.example_html)

        extractor = TelegramDataExtractor("test_folder")
        messages = extractor.extract_data()
        self.assertEqual(len(messages), 4)

        os.remove(example_file_1)
        os.remove(example_file_2)
        os.rmdir("test_folder")

    def tearDown(self):
        os.remove(self.example_html_file)


if __name__ == '__main__':
    unittest.main()
