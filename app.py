from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

# ⭐ FIXED ROUTE — must be /ask (NOT /get)
@app.route("/ask", methods=["POST"])
def ask():
    try:
        user_message = request.json.get("message", "")

        if not user_message:
            return jsonify({"reply": "⚠ CropIntel Error: Empty message received."})

        # Groq API call
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are CropIntel, an agriculture expert assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        bot_reply = completion.choices[0].message.content

        # ⭐ MUST RETURN "reply" (your JS expects this)
        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"reply": f"⚠ CropIntel Server Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
