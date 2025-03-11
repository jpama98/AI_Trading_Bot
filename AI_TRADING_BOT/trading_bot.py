import os
import requests
import tweepy
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twitter API setup
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN, wait_on_rate_limit=True)

print(os.getenv("TWITTER_BEARER_TOKEN"))

# Fetch crypto price
def get_crypto_price():
    try:
        response = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot", timeout=10)
        response.raise_for_status()
        return float(response.json()["data"]["amount"])
    except Exception as e:
        print(f"Error fetching crypto price: {e}")
        return None

# Fetch latest news
def get_latest_news(query="stock market"):
    try:
        url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&apiKey={os.getenv('NEWS_API_KEY')}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()["articles"][:5]  # Return top 5 articles
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

# Analyze tweet sentiment
def analyze_tweet_sentiment():
    try:
        tweets = client.search_recent_tweets(query="Bitcoin OR BTC OR crypto", max_results=5)
        return sum(1 if tweet.text.startswith("Positive") else -1 for tweet in tweets.data)  # Placeholder logic
    except Exception as e:
        print(f"Error analyzing Twitter sentiment: {e}")
        return 0