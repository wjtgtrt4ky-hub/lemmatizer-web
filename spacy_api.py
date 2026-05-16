from flask import Flask, request, render_template_string
import spacy

app = Flask(__name__)

nlp = spacy.load("de_core_news_sm")

HTML = """
<!doctype html>
<html>
<head>
    <title>Lemmatizer</title>
</head>
<body>
    <h1>spaCy Lemmatizer</h1>

    <form method="post">
        <textarea name="text" rows="10" cols="60">{{ text }}</textarea><br>
        <button type="submit">Analysieren</button>
    </form>

    {% if result %}
    <h2>Ergebnis</h2>
    <pre>{{ result }}</pre>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    text = ""
    result = ""

    if request.method == "POST":
        text = request.form.get("text", "")
        doc = nlp(text)

        result = "\n".join(
            f"{token.text}\t{token.lemma_}\t{token.pos_}"
            for token in doc
        )

    return render_template_string(HTML, text=text, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
