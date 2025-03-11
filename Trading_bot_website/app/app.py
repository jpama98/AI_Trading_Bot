from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

PREDICTION_API_URL = "http://127.0.0.1:8000/predict"
COINBASE_API_URL = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
NEWS_API_KEY = "your_news_api_key"

# Home Route
@app.route("/")
def home():
    return "Hello, Flask is running!"


# Fetch Real-Time Crypto Price
@app.route('/crypto_price')
def crypto_price():
    try:
        response = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot")
        response.raise_for_status()
        data = response.json()
        price = data["data"]["amount"]  # Ensure correct JSON parsing
        return jsonify({"price": f"${float(price):,.2f}"})  # Format price correctly
    except Exception as e:
        print(f"⚠ Crypto API Error: {e}")
        return jsonify({"price": "API Error"})




# Fetch Sentiment Score
@app.route('/sentiment_score')
def sentiment_score():
    try:
        response = requests.get(f"{PREDICTION_API_URL}/sentiment")
        response.raise_for_status()
        data = response.json()
        score = data.get("score", "N/A")  # Avoid empty values
        return jsonify({"score": score})
    except Exception as e:
        print(f"⚠ Sentiment API Error: {e}")
        return jsonify({"score": "API Error"})



# Fetch Latest News
@app.route('/latest_news')
def latest_news():
    try:
        news_url = f"https://newsapi.org/v2/everything?q=crypto&apiKey={NEWS_API_KEY}"
        response = requests.get(news_url)
        articles = response.json().get("articles", [])[:5]
        return jsonify({"articles": [{"title": a["title"], "url": a["url"]} for a in articles]})
    except:
        return jsonify({"articles": []})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
