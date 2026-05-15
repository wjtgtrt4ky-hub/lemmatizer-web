from flask import Flask, request, jsonify
import spacy

app = Flask(__name__)

nlp = spacy.load("de_core_news_sm")


@app.route("/lemmatize", methods=["POST"])
def lemmatize():
    data = request.get_json(silent=True)

    if not data or "text" not in data:
        return jsonify({"error": "no text provided"}), 400

    text = data["text"]

    doc = nlp(text)

    result = [
        f"{token.text}\t{token.lemma_}\t{token.pos_}"
        for token in doc
    ]

    return jsonify({"result": result})


@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
