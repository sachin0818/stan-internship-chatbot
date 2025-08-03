# app/main.py

from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv  # <-- ADD THIS LINE
from .chatbot import Chatbot
from config import GEMINI_API_KEY

# Load environment variables from .env file
load_dotenv()  # <-- ADD THIS LINE

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Add a check to ensure the API key is loaded
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Make sure it's set in your .env file.")

chatbot = Chatbot(api_key=GEMINI_API_KEY)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_id = data.get("user_id", "default_user")
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    try:
        bot_response = chatbot.generate_response(user_id, user_message)
        return jsonify({"response": bot_response})
    except Exception as e:
        # If anything goes wrong, log it and send an error response
        print(f"An error occurred: {e}")
        return jsonify({"error": "Sorry, I encountered an error."}), 500


if __name__ == '__main__':
    app.run(debug=True)