from flask import Flask, request, jsonify, render_template_string, Response
import spacy

app = Flask(__name__)
nlp = spacy.load("de_core_news_sm")

HTML = """
<!doctype html>
<html>
<head>
    <title>Web Lemmatizer</title>
</head>
<body>

<h1>Web Lemmatizer</h1>

<form method="post">
    <textarea name="text" rows="10" cols="60">{{ text }}</textarea><br><br>

    <button type="submit" name="action" value="show">Lemmatisieren</button>
    <button type="submit" name="action" value="download">Download</button>
</form>

<pre>{{ result }}</pre>

</body>
</html>
"""

last_output = ""

@app.route("/", methods=["GET", "POST"])
def index():
    global last_output
    result = ""
    text = ""

    if request.method == "POST":
        text = request.form.get("text", "")
        action = request.form.get("action", "show")

        doc = nlp(text)
        output = [f"{t.text}\t{t.lemma_}\t{t.pos_}" for t in doc]
        last_output = "\n".join(output)

        if action == "download":
            return Response(
                last_output,
                mimetype="text/plain",
                headers={
                    "Content-Disposition": "attachment; filename=tagged.txt"
                }
            )

        result = last_output

    return render_template_string(HTML, result=result, text=text)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
