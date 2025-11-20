from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chat():
    user_msg = request.form["msg"].strip().lower()

    # Example responses
    if "hello" in user_msg or "hi" in user_msg:
        reply = "Hi! I am CropIntel 🌾 — your personal agriculture assistant. How can I help you?"
    elif "fertilizer" in user_msg:
        reply = "You can use urea or DAP for better nitrogen and phosphorus balance in soil."
    elif "crop" in user_msg:
        reply = "In this season, wheat and mustard are good rabi crops to sow."
    elif "rain" in user_msg or "drought" in user_msg:
        reply = "During droughts, try drip irrigation and drought-tolerant crops like millets."
    elif "about yourself" in user_msg:
        reply = "I am CropIntel — designed to guide farmers on crops, soil, fertilizers, and disaster management."
    else:
        reply = "I'm still learning 🌱 — please ask about crops, fertilizers, or farming methods."

    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True)
