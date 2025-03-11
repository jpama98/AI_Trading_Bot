from flask import Blueprint, jsonify
import requests

api = Blueprint("api", __name__)

def get_crypto_price():
    """Fetch real-time crypto price from an API"""
    try:
        response = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot")
        response.raise_for_status()
        return float(response.json()["data"]["amount"])
    except:
        return None

@api.route("/api/crypto_price")
def crypto_price():
    price = get_crypto_price()
    return jsonify({"crypto_price": price if price else "Error fetching price"})

@api.route("/api/sentiment")
def sentiment():
    sentiment_score = 1  # Replace with actual logic
    return jsonify({"sentiment": sentiment_score})

@api.route("/api/news")
def news():
    latest_news = ["Bitcoin reaches new highs!", "Stock market sees volatility"]
    return jsonify({"news": latest_news})
# # Compare this snippet from Trading_bot_website/app/routes.py:
# from flask import Blueprint, jsonify