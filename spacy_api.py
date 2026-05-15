from flask import Flask, request, jsonify
import spacy

app = Flask(__name__)

nlp = spacy.load("de_core_news_sm")

@app.route("/lemmatize", methods=["POST"])
def lemmatize():
    data = request.get_json()
    text = data.get("text", "")

    doc = nlp(text)

    result = [
        {"token": token.text, "lemma": token.lemma_, "pos": token.pos_}
        for token in doc
    ]

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
