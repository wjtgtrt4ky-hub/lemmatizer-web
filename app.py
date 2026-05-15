import spacy
import requests
from flask import Flask, request, render_template_string, Response

last_output = ""

app = Flask(__name__)

HTML = """
<form method="post">
<textarea name="text" rows="10" cols="50">{{ request.form.get('text', '') }}</textarea><br>

<button type="submit" name="action" value="show">Anzeigen</button>
<button type="submit" name="action" value="download">Download</button>

</form>

<pre>{{ result }}</pre>
"""

def process(text):
    response = requests.post(
        "https://web-lemma.onrender.com/lemmatize",
        json={"text": text}
    )

    data = response.json()["result"]

    return data

@app.route("/", methods=["GET", "POST"])
def index():
    global last_output
    result = ""

    if request.method == "POST":
        text = request.form.get("text", "")
        action = request.form.get("action", "show")

        output = process(text)
        last_output = "\n".join(output)

        if action == "download":
            return Response(
                last_output,
                mimetype="text/plain",
                headers={"Content-Disposition": "attachment; filename=tagged.txt"}
            )

        result = last_output

    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run(debug=True)
