import sys
import os

# Add Trading_bot_website to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'Trading_bot_website')))

# Import app safely
try:
    from Trading_bot_website.app.create_app import create_app  # ✅ Use lowercase!
except ImportError:
    print("❌ Module trading_bot_website.app.create_app not found!")
    sys.exit(1)

# Initialize Flask app
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
