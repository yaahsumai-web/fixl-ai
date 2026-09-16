
import os
import logging

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai

load_dotenv()

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-3.6-flash"

client = None

if API_KEY:
    client = genai.Client(api_key=API_KEY)
else:
    logging.error("GEMINI_API_KEY is missing")


with open("chatbot_config.txt", "r", encoding="utf-8") as file:
    SYSTEM_PROMPT = file.read()


@app.get("/")
def home():
    return render_template("index.html", bot_name="FixItAI")


@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"error": "Please enter a message."}), 400

    if client is None:
        logging.error("Gemini client is not initialized")
        return jsonify({
            "error": "Gemini API key is missing in Render Environment."
        }), 500

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=f"{SYSTEM_PROMPT}\n\nUser: {message}"
        )

        return jsonify({
            "reply": response.text or "No response generated."
        })

    except Exception as error:
        logging.exception("Gemini API request failed")

        return jsonify({
            "error": "Gemini API request failed. Check Render logs."
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
