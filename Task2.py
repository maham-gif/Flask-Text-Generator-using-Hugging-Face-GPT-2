from flask import Flask, request, render_template_string
from transformers import pipeline

app = Flask(__name__)

# Load a better lightweight open-source text generation model
generator = pipeline("text-generation", model="gpt2")

# HTML template with a form for input and a place to display the generated text
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Text Generator</title>
</head>
<body>
    <h1>Text Generator</h1>
    <form method="POST">
        <label for="text">Enter a prompt:</label><br>
        <textarea name="text" rows="5" cols="50" required></textarea><br>
        <input type="submit" value="Generate">
    </form>
    {% if generated_text %}
        <h2>Generated Text:</h2>
        <p>{{ generated_text }}</p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def generate_text():
    generated_text = None
    if request.method == "POST":
        prompt = request.form.get("text", "").strip()
        if prompt:
            result = generator(prompt, max_length=100, num_return_sequences=1)
            generated_text = result[0]['generated_text']
    return render_template_string(html_template, generated_text=generated_text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
