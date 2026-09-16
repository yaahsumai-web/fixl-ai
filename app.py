import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-3.6-flash"

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

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=f"{SYSTEM_PROMPT}\n\nUser: {message}"
        )
        return jsonify({"reply": response.text or "No response generated."})
    except Exception:
        return jsonify({"error": "Unable to contact the AI service right now."}), 500

if __name__ == "__main__":
    app.run(debug=True)
