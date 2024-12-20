import argparse
import csv
from bs4 import BeautifulSoup
import re
from datetime import datetime
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')


def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zа-я0-9\s]', '', text)
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('russian') + stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    return " ".join(tokens)


def get_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    if scores['compound'] >= 0.05:
        return "positive"
    elif scores['compound'] <= -0.05:
        return "negative"
    else:
        return "neutral"


def analyze_messages(messages):
    analyzed_messages = []
    for message in messages:
        label = 'other'
        if 'дтп' in preprocess_text(message['text']):
            label = 'disaster'
        elif 'реклама' in preprocess_text(message['text']):
            label = 'advertisement'
        sentiment = get_sentiment(message['text'])
        analyzed_messages.append({
            'Date': message['date'],
            'Semantic tag': sentiment,
            'Label': label
        })
    return analyzed_messages


def load_messages_from_html(input_file):
    messages = []
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
        message_blocks = soup.find_all('div', class_='message')

        current_date = None
        for message_block in message_blocks:
            if 'service' in message_block.get('class', []):
                date_element = message_block.find('div', class_='body details')
                if date_element:
                    date_str = date_element.get_text(strip=True)
                    try:
                        current_date = datetime.strptime(date_str, '%d %B %Y')
                    except ValueError:
                        try:
                            current_date = datetime.strptime(date_str, '%d %b %Y')
                        except ValueError:
                            print(f"Warning: Invalid date format '{date_str}'. Skipping.")
                            current_date = None
                    continue
            elif 'default' in message_block.get('class', []):
                text_element = message_block.find('div', class_='body')
                if text_element and current_date:
                    text_content = text_element.get_text(strip=True)
                    messages.append({'date': current_date.strftime('%Y/%m/%d'), 'text': text_content})
        if not messages:
            print("Error: No messages found in HTML. Check HTML file structure.")
    except Exception as e:
        raise Exception(f"Error loading or parsing HTML: {e}")
    return messages


def create_timeline(analyzed_messages):
    timeline = []
    messages_by_date = {}
    for msg in analyzed_messages:
        if msg['Date'] is not None:
            date_obj = datetime.strptime(msg['Date'], "%Y/%m/%d").date()
            if date_obj not in messages_by_date:
                messages_by_date[date_obj] = []
            messages_by_date[date_obj].append(msg)

    for date_obj, messages in messages_by_date.items():
        semantic_sum = 0
        labels = []
        for msg in messages:
            if msg['Semantic tag'] == "positive":
                semantic_sum += 1
            elif msg['Semantic tag'] == "negative":
                semantic_sum -= 1
            labels.append(msg['Label'])
        most_common_label = Counter(labels).most_common(1)[0][0] if labels else "unknown"

        timeline.append({
            "date": date_obj.strftime("%Y/%m/%d"),
            "semantic_tag": semantic_sum,
            "label": most_common_label
        })

    return timeline


def visualize_timeline(timeline, output_path):
    """
    Визуализирует таймлайн.
    """
    dates = [datetime.strptime(item['date'], "%Y/%m/%d").date() for item in timeline]
    semantic_tags = [item['semantic_tag'] for item in timeline]
    labels = [item["label"] for item in timeline]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(dates, semantic_tags, label="Semantic Tag")

    ax.set_xlabel("Date")
    ax.set_ylabel("Semantic Tag Sum")
    ax.set_title("Timeline Visualization")
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax.tick_params(axis="x", rotation=45)

    # Add labels to the plot
    for i, txt in enumerate(labels):
        ax.annotate(txt, (dates[i], semantic_tags[i]), textcoords="offset points", xytext=(0, 5), ha='center')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close(fig)


def save_to_csv(data, output_file):
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            if data:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            else:
                print("Warning: No data to save")
    except Exception as e:
        raise Exception(f"Error saving to CSV: {e}")


def main():
    parser = argparse.ArgumentParser(description='Telegram News Channel Analyzer')
    parser.add_argument('--input_file', required=True, help='Path to the input HTML file')
    parser.add_argument('--output_file', required=True, help='Path to the output CSV file')
    parser.add_argument('--timeline_output', help='Path to the output timeline CSV file')
    parser.add_argument('--plot_output', help='Path to the output timeline PNG file')

    args = parser.parse_args()

    try:
        messages = load_messages_from_html(args.input_file)
        analyzed_messages = analyze_messages(messages)
        save_to_csv(analyzed_messages, args.output_file)

        if args.timeline_output:
            timeline_data = create_timeline(analyzed_messages)
            save_to_csv(timeline_data, args.timeline_output)

        if args.plot_output and args.timeline_output:
            timeline_data = create_timeline(analyzed_messages)
            visualize_timeline(timeline_data, args.plot_output)

        print("Analysis complete. Check output CSV files.")
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()