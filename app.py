from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

with open("kb.json", "r", encoding="utf-8") as f:
    kb = json.load(f)

@app.route("/api/", methods=["POST"])
def virtual_ta():
    data = request.get_json()
    question = data.get("question", "").lower()

    for item in kb:
        if any(word in question for word in item["keywords"]):
            return jsonify({
                "answer": item["answer"],
                "links": item["links"]
            })
    return jsonify({
        "answer": "Sorry, I don't know that yet.",
        "links": []
    })