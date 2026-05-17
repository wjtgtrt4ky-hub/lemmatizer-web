from flask import Flask, request, render_template_string, Response
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
    <h1>Web Lemmatizer</h1>

    <form method="post">
        <textarea name="text" rows="10" cols="60">{{ text }}</textarea><br>

<button type="submit" name="action" value="show">Lemmatisieren</button>
<button type="submit" name="action" value="download">Download</button>

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
        action = request.form.get("action", "show")

        doc = nlp(text)

        result = "\n".join(
            f"{token.text}\t{token.lemma_}\t{token.pos_}"
            for token in doc
        )

if action == "download":
    return Response(
        result,
        mimetype="text/plain",
        headers={
            "Content-Disposition": "attachment; filename=lemmatized.txt"
        }
    )

    return render_template_string(HTML, text=text, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
