import os
import time
import logging
import requests
import schedule
import tweepy
import pandas as pd
import sqlite3
from textblob import TextBlob
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("trades.log", encoding="utf-8"),  # Log to file
        logging.StreamHandler()  # Log to console
    ]
)

# API Keys
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Initialize Twitter API
client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)

# Initialize SQLite database
conn = sqlite3.connect("trading_bot.db")
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS price_history (
    timestamp DATETIME,
    symbol TEXT,
    price REAL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS trades (
    timestamp DATETIME,
    action TEXT,
    symbol TEXT,
    price REAL,
    sentiment_score REAL
)
""")
conn.commit()

# ==============================
# FETCH STOCK & CRYPTO PRICES
# ==============================
def get_stock_price(symbol):
    """Fetch latest stock price from Alpaca API"""
    try:
        headers = {
            "APCA-API-KEY-ID": ALPACA_API_KEY,
            "APCA-API-SECRET-KEY": ALPACA_SECRET_KEY
        }
        response = requests.get(
            f"https://data.alpaca.markets/v2/stocks/{symbol}/quotes/latest",
            headers=headers, timeout=10
        )
        response.raise_for_status()
        return response.json().get("quote", {}).get("askprice", None)
    except Exception as e:
        logging.error(f"Error fetching stock price for {symbol}: {e}")
        return None

def get_crypto_price():
    """Fetch latest crypto price (BTC-USD) from Coinbase API"""
    try:
        response = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot", timeout=10)
        response.raise_for_status()
        return float(response.json()["data"]["amount"])
    except Exception as e:
        logging.error(f"Error fetching crypto price: {e}")
        return None

# ==============================
# FETCH LATEST FINANCIAL NEWS
# ==============================
def get_latest_news(query="stock market"):
    """Fetch latest financial news from NewsAPI"""
    try:
        url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json().get("articles", [])[:5]  # Return top 5 articles
    except Exception as e:
        logging.error(f"Error fetching news: {e}")
        return []

# ==============================
# ANALYZE TWEET SENTIMENT
# ==============================
def analyze_tweet_sentiment():
    """Analyze sentiment of recent tweets on Bitcoin using TextBlob"""
    try:
        tweets = client.search_recent_tweets(query="Bitcoin OR BTC OR crypto", max_results=100)
        sentiment_scores = [TextBlob(tweet.text).sentiment.polarity for tweet in tweets.data]
        return sum(sentiment_scores) / len(sentiment_scores)  # Average sentiment score
    except Exception as e:
        logging.error(f"Error analyzing Twitter sentiment: {e}")
        return 0

# ==============================
# TELEGRAM ALERT FUNCTION
# ==============================
def send_telegram_alert(message):
    """Send alerts to Telegram when a trade is executed"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    
    try:
        requests.post(url, json=payload, timeout=5)
        logging.info(f"📢 Telegram alert sent: {message}")
    except Exception as e:
        logging.error(f"⚠️ Failed to send Telegram alert: {e}")

# ==============================
# TRADING LOGIC WITH MOVING AVERAGE STRATEGY
# ==============================
price_history = []  # Stores past prices to calculate moving average

def trade_logic():
    """Execute trading strategy based on sentiment & price movements"""
    
    sentiment_score = analyze_tweet_sentiment()
    logging.info(f"🧠 Sentiment Score: {sentiment_score}")

    # Fetch the latest price BEFORE using it
    current_price = get_crypto_price()
    
    if not current_price:
        logging.error("API is down. Skipping prediction.")
        return

    # Store latest price in history
    price_history.append(current_price)
    if len(price_history) > 5:
        price_history.pop(0)  # Keep only last 5 prices

    # Calculate moving average
    moving_avg = sum(price_history) / len(price_history)
    threshold = moving_avg * 0.02  # 2% threshold for price movement

    # Save price to database
    cursor.execute("INSERT INTO price_history (timestamp, symbol, price) VALUES (datetime('now'), 'BTC', ?)", (current_price,))
    conn.commit()

    # Execute trade logic
    if sentiment_score > 0 and current_price > moving_avg + threshold:
        action = "BUY"
        logging.info(f"✅ {action} Signal Triggered at ${current_price}")
        send_telegram_alert(f"✅ {action} Signal Triggered at ${current_price}")
    elif sentiment_score < 0 and current_price < moving_avg - threshold:
        action = "SELL"
        logging.info(f"❌ {action} Signal Triggered at ${current_price}")
        send_telegram_alert(f"❌ {action} Signal Triggered at ${current_price}")
    else:
        action = None
        logging.info("⏳ No trade executed. Conditions not met.")

    # Save trade to database
    if action:
        cursor.execute("""
        INSERT INTO trades (timestamp, action, symbol, price, sentiment_score)
        VALUES (datetime('now'), ?, 'BTC', ?, ?)
        """, (action, current_price, sentiment_score))
        conn.commit()

# ==============================
# AUTO-TRADING LOOP
# ==============================
schedule.every(1).minutes.do(trade_logic)

logging.info("🚀 Bot is now running. Checking trades every 1 minute...")

while True:
    schedule.run_pending()
    time.sleep(10)