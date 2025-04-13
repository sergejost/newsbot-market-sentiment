import feedparser
import time
import csv
import os
from textblob import TextBlob
from termcolor import colored
import threading
from queue import Queue
import platform
from datetime import datetime

# Multiple RSS Feeds (Auto-Switch)
RSS_FEEDS = {
    "Yahoo Finance": "https://feeds.finance.yahoo.com/rss/2.0/headline?s=^DJI,^GSPC,^IXIC&region=US&lang=en-US",
    "CNN Money": "http://rss.cnn.com/rss/money_latest.rss",
    "MarketWatch": "https://www.marketwatch.com/rss/topstories",
}

# Shared queue for news between threads
news_queue = Queue()

# Set to track already seen news titles
seen_titles = set()

# Smart filter thresholds
POSITIVE_THRESHOLD = 0.4
NEGATIVE_THRESHOLD = -0.4

# Overall market sentiment tracking
total_polarity = 0
news_count = 0
previous_cycle_sentiment = 0

# CSV file name
CSV_FILE = "market_sentiment_log.csv"

def fetch_latest_news():
    """Try multiple feeds until we get news."""
    for feed_name, rss_url in RSS_FEEDS.items():
        feed = feedparser.parse(rss_url)
        if len(feed.entries) > 0:
            news_items = []
            for entry in feed.entries:
                title = entry.title
                summary = entry.summary if 'summary' in entry else ''
                news_items.append((feed_name, f"{title}. {summary}"))
            return news_items
        else:
            print(f"⚠️ No news found in {feed_name}, trying next feed...")
    return []

def news_fetcher(interval_seconds=60):
    """Thread 1: Fetch news every X seconds and add to queue."""
    while True:
        # print("\n⏳ Fetching fresh news...")
        news_list = fetch_latest_news()

        for feed_name, news in news_list:
            news_id = feed_name + "::" + news
            if news_id not in seen_titles:
                news_queue.put((feed_name, news))
                seen_titles.add(news_id)

        time.sleep(interval_seconds)

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "Positive", polarity
    elif polarity < -0.1:
        return "Negative", polarity
    else:
        return "Neutral", polarity

def play_sound_alert(sentiment):
    """Play a sound based on sentiment."""
    system = platform.system()

    try:
        if system == "Windows":
            import winsound
            if sentiment == "Positive":
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
            elif sentiment == "Negative":
                winsound.MessageBeep(winsound.MB_ICONHAND)
        elif system == "Darwin":  # MacOS
            if sentiment == "Positive":
                os.system('say "Strong positive news detected"')
            elif sentiment == "Negative":
                os.system('say "Warning, strong negative news"')
        elif system == "Linux":
            if sentiment == "Positive":
                os.system('play -nq -t alsa synth 0.5 sine 440')
            elif sentiment == "Negative":
                os.system('play -nq -t alsa synth 0.5 sine 220')
    except Exception as e:
        print(f"Sound alert failed: {e}")

def print_colored_news(feed_name, news, sentiment, polarity, market_sentiment):
    label = f"[{feed_name}] [{sentiment} {polarity:+.2f}] [Market Sentiment: {market_sentiment:+.2f}]"
    if sentiment == "Positive":
        print(colored(f"{label} {news}", "green"))
    elif sentiment == "Negative":
        print(colored(f"{label} {news}", "red"))
    else:
        print(colored(f"{label} {news}", "yellow"))

def print_cycle_summary(current_sentiment, previous_sentiment):
    delta = current_sentiment - previous_sentiment
    if delta > 0:
        summary = colored(f"📈 Market sentiment improved by {delta:+.2f} points. Current Sentiment: {current_sentiment:+.2f}", "green")
    elif delta < 0:
        summary = colored(f"📉 Market sentiment worsened by {delta:+.2f} points. Current Sentiment: {current_sentiment:+.2f}", "red")
    else:
        summary = colored(f"➖ No change in market sentiment. Current Sentiment: {current_sentiment:+.2f}", "yellow")
    # print("\n" + summary + "\n")
    print("\n" + summary)
    save_sentiment_to_csv(current_sentiment, delta)

def save_sentiment_to_csv(current_sentiment, delta):
    """Save timestamped sentiment data to CSV file."""
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Current Sentiment", "Sentiment Change"])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, f"{current_sentiment:+.4f}", f"{delta:+.4f}"])

def news_analyzer():
    """Thread 2: Continuously analyze and print news from queue."""
    global total_polarity, news_count, previous_cycle_sentiment

    last_summary_time = time.time()

    while True:
        if not news_queue.empty():
            feed_name, news = news_queue.get()
            sentiment, polarity = analyze_sentiment(news)

            # Update overall market sentiment
            total_polarity += polarity
            news_count += 1
            market_sentiment = total_polarity / news_count if news_count else 0

            print_colored_news(feed_name, news, sentiment, polarity, market_sentiment)

            # Smart Filter: Only alert if very strong
            if (sentiment == "Positive" and polarity > POSITIVE_THRESHOLD) or \
               (sentiment == "Negative" and polarity < NEGATIVE_THRESHOLD):
                play_sound_alert(sentiment)

            news_queue.task_done()

        else:
            # Every 60 seconds, print market sentiment summary
            current_time = time.time()
            if current_time - last_summary_time >= 60:
                market_sentiment = total_polarity / news_count if news_count else 0
                print_cycle_summary(market_sentiment, previous_cycle_sentiment)
                previous_cycle_sentiment = market_sentiment
                last_summary_time = current_time

            time.sleep(1)

def main():
    print("🔵 Starting News Monitor with Live Sentiment Tracking and CSV Logging...")

    # Start fetcher thread
    fetch_thread = threading.Thread(target=news_fetcher, daemon=True)
    fetch_thread.start()

    # Start analyzer thread
    analyzer_thread = threading.Thread(target=news_analyzer, daemon=True)
    analyzer_thread.start()

    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping News Monitor...")

if __name__ == "__main__":
    main()
