from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import re
import html as html_lib
from dotenv import load_dotenv

# If you're using the Groq client as before, keep it.
# The original file used `from groq import Groq` and `Groq(api_key=...)`.
# Keep that import if you use Groq. If you use another API, adapt below accordingly.
try:
    from groq import Groq
except Exception:
    Groq = None

# Load environment
load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)


# Initialize client if available
_api_key = os.getenv("GROQ_API_KEY", None)
client = Groq(api_key=_api_key) if (Groq is not None and _api_key) else None


SYSTEM_INSTRUCTION = (
    "You are CropIntel, a concise agriculture expert assistant. "
    "Always answer in **2–3 short sentences** unless the user explicitly asks for more detail. "
    "Do NOT emit HTML tags like <br> or <strong>. Use plain text and Markdown for emphasis (e.g. **bold**). "
    "Keep answers focused, helpful, and friendly."
)


def strip_html_tags_and_cleanup(text: str) -> str:
    """Remove HTML tags, unescape HTML entities, normalize whitespace."""
    if not text:
        return text
    # Unescape HTML entities (e.g., &lt; &gt;)
    text = html_lib.unescape(text)

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    # Replace multiple newlines with two newlines, trim whitespace
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()

    return text


def truncate_to_sentences(text: str, max_sentences: int = 3) -> str:
    """Return first up to max_sentences sentences (naive sentence splitter)."""
    if not text:
        return text
    # Split on sentence endings followed by whitespace
    sentences = re.split(r'(?<=[.!?])\s+', text)
    if len(sentences) <= max_sentences:
        return " ".join(s.strip() for s in sentences).strip()
    return " ".join(s.strip() for s in sentences[:max_sentences]).strip()


@app.route("/")
def home():
    # Render the same index.html you already had (ensure it's in templates/ or leave as static)
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    try:
        payload = request.get_json(force=True, silent=True) or {}
        user_message = payload.get("message", "").strip()

        if not user_message:
            return jsonify({"reply": "⚠ CropIntel Error: empty message received. Please type your question."})

        # Build messages for the model — enforce brevity in system prompt
        messages = [
            {"role": "system", "content": SYSTEM_INSTRUCTION},
            {"role": "user", "content": user_message}
        ]

        # If Groq client available, call it (adapt to whichever client you actually use).
        bot_reply_raw = None
        if client is not None:
            # Example call pattern used in your original app.py — keep if compatible
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages
            )
            # Safely extract text
            bot_reply_raw = getattr(completion, "choices", None) and getattr(completion.choices[0].message, "content", None)
            if bot_reply_raw is None:
                # some clients return differently
                bot_reply_raw = completion.choices[0].message.content if hasattr(completion, "choices") else str(completion)
        else:
            # No client available (dev fallback) — create a short canned reply
            bot_reply_raw = "I can't access the AI backend right now. Ask again later or check your API key."

        # 1) Unescape and strip HTML tags (to prevent injected <br><strong> etc.)
        cleaned = strip_html_tags_and_cleanup(bot_reply_raw)

        # 2) Truncate to 2-3 sentences to enforce concision
        short = truncate_to_sentences(cleaned, max_sentences=3)

        # 3) Final safety/format: ensure there is at least some text
        if not short:
            short = "Sorry, I couldn't generate a reply. Please try rephrasing your question."

        # Return plain text (with Markdown allowed)
        return jsonify({"reply": short})

    except Exception as e:
        # Do not return raw exceptions in production; this helps debug while developing.
        return jsonify({"reply": f"⚠ CropIntel Server Error: {str(e)}"}), 500


if __name__ == "__main__":
    # For production use gunicorn or other WSGI server
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
