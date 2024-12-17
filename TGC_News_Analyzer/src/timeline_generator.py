import pandas as pd
from typing import List, Dict


class TimelineGenerator:
    def __init__(self):
        pass

    def create_timeline(self, messages: List[Dict], labels: List[str], sentiments: List[int]) -> pd.DataFrame:
        df = pd.DataFrame(messages)
        df['label'] = labels
        df['sentiment'] = sentiments
        df['date'] = pd.to_datetime(df['date']).dt.date

        timeline_df = df.groupby('date').agg(
            semantic_tag=pd.NamedAgg(column="sentiment", aggfunc="sum"),
            label=pd.NamedAgg(column="label", aggfunc=lambda x: x.value_counts().index[0]),
        ).reset_index()
        return timeline_df

    def filter_by_category(self, timeline_df: pd.DataFrame, category: str) -> pd.DataFrame:
        return timeline_df[timeline_df['label'] == category]
    