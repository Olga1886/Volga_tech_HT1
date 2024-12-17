import unittest
import pandas as pd
from src.timeline_generator import TimelineGenerator
from datetime import date, datetime


class TestTimelineGenerator(unittest.TestCase):
    def setUp(self):
        self.messages = [
            {"date": datetime(2024, 11, 15, 12, 0), "text": "Message 1"},
            {"date": datetime(2024, 11, 15, 14, 0), "text": "Message 2"},
            {"date": datetime(2024, 11, 16, 10, 0), "text": "Message 3"},
            {"date": datetime(2024, 11, 17, 11, 0), "text": "Message 4"},
        ]
        self.labels = ["sport", "sport", "disaster", "accident"]
        self.sentiments = [1, 1, -1, -1]
        self.timeline_generator = TimelineGenerator()
        self.timeline_df = self.timeline_generator.create_timeline(self.messages, self.labels, self.sentiments)

    def test_create_timeline(self):
        self.assertEqual(len(self.timeline_df), 3)
        self.assertTrue(all(col in self.timeline_df.columns for col in ["date", "semantic_tag", "label"]))
        self.assertEqual(self.timeline_df.iloc[0]['semantic_tag'], 2)
        self.assertEqual(self.timeline_df.iloc[0]['label'], "sport")
        self.assertEqual(self.timeline_df.iloc[1]['semantic_tag'], -1)
        self.assertEqual(self.timeline_df.iloc[1]['label'], 'disaster')
        self.assertEqual(self.timeline_df.iloc[2]['semantic_tag'], -1)
        self.assertEqual(self.timeline_df.iloc[2]['label'], 'accident')

    def test_filter_by_category(self):
        filtered_df = self.timeline_generator.filter_by_category(self.timeline_df, "sport")
        self.assertEqual(len(filtered_df), 1)
        self.assertEqual(filtered_df.iloc[0]['label'], "sport")

        filtered_df_2 = self.timeline_generator.filter_by_category(self.timeline_df, "accident")
        self.assertEqual(len(filtered_df_2), 1)
        self.assertEqual(filtered_df_2.iloc[0]['label'], 'accident')

        filtered_df_3 = self.timeline_generator.filter_by_category(self.timeline_df, "unknow")
        self.assertTrue(filtered_df_3.empty)


if __name__ == '__main__':
    unittest.main()
