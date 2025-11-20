from flask import Flask, render_template, request, jsonify
import csv
import difflib

app = Flask(__name__)

# Load Q&A from CSV using | delimiter
def load_data():
    data = {}
    with open("agri_data.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter="|")
        for row in reader:
            if len(row) == 2:
                question, answer = row
                data[question.strip().lower()] = answer.strip()
    return data

qa_data = load_data()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_bot_response():
    user_input = request.form["msg"].strip().lower()

    # Exact match
    if user_input in qa_data:
        return jsonify({"response": qa_data[user_input]})

    # Fuzzy match
    closest = difflib.get_close_matches(user_input, qa_data.keys(), n=1, cutoff=0.6)
    if closest:
        return jsonify({"response": qa_data[closest[0]]})

    return jsonify({"response": "I'm still learning 🌱 — please ask about crops, fertilizers, or farming methods."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
