import click
import pandas as pd
from src.data_processing import TelegramDataExtractor
from src.text_classification import TextClassifier
from src.timeline_generator import TimelineGenerator
import plotly.graph_objects as go
from plotly.subplots import make_subplots


@click.command()
@click.argument("input_path")
@click.option(
    "--model_type",
    default="tfidf",
    help="Type of classification model (tfidf, zeroshot, topic_classifier)",
)
@click.option(
    "--model_path",
    default=None,
    help="Path to model file or pre-trained model name for zero-shot or topic-classifier",
)
@click.option(
    "--output_csv", default="output.csv", help="Path to save the output CSV file"
)
@click.option("--category", default=None, help="Category to filter timeline")
@click.option("--show_timeline", is_flag=True, default=False, help="Show timeline plot")
@click.option("--labels", default=None, help="Labels for Zero-Shot or topic-classifier separated by comma")
def main(input_path, model_type, model_path, output_csv, category, show_timeline, labels):
    """
    Telegram News Channels Analyzer.
    Analyzes the content of Telegram channel export files (HTML).
    """
    try:
        if model_type in ['zeroshot', 'topic_classifier'] and labels is None:
            raise ValueError("Labels must be provided for Zero-Shot or Topic Classifier model")

        labels = labels.split(',') if labels else None

        extractor = TelegramDataExtractor(input_path)
        messages = extractor.extract_data()

        if not messages:
            print("No messages extracted from input path.")
            return

        texts = [msg["text"] for msg in messages]
        classifier = TextClassifier(model_type=model_type, model_path=model_path)
        labels_predicted = classifier.classify(texts, labels=labels)
        sentiments = classifier.calculate_sentiment(labels_predicted)

        timeline_generator = TimelineGenerator()
        timeline_df = timeline_generator.create_timeline(messages, labels_predicted, sentiments)

        if category:
            filtered_timeline = timeline_generator.filter_by_category(timeline_df, category)
        else:
            filtered_timeline = timeline_df

        filtered_timeline.to_csv(output_csv, index=False)
        print(f"Timeline saved to {output_csv}")

        if show_timeline:
            show_plot(filtered_timeline)

    except Exception as e:
        print(f"An error occurred: {e}")


def show_plot(timeline_df: pd.DataFrame):
    fig = make_subplots(rows=2, cols=1, subplot_titles=('Sentiment', 'Category Distribution'))

    # Create a bar chart for sentiment
    fig.add_trace(go.Bar(x=timeline_df['date'], y=timeline_df['semantic_tag'], name='Sentiment'), row=1, col=1)

    # Create a pie chart for category
    category_counts = timeline_df['label'].value_counts()
    fig.add_trace(go.Pie(labels=category_counts.index, values=category_counts.values, name='Category'), row=2, col=1)

    fig.update_layout(title_text="Timeline Analysis")
    fig.show()


if __name__ == "__main__":
    main()
