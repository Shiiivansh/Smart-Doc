from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


def ask_ollama(prompt, model='nous-hermes2'):
    url = 'http://localhost:11434/api/generate'
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.3}
    }
    response = requests.post(url, json=data)
    return response.json()['response']


@app.route('/transform_document', methods=['POST'])
def transform_document():
    text = request.json.get("text", "")
    template = request.json.get("template", "General Document")

    prompt = (
        f"Transform this document into a professional {template} following these rules:\n"
        "1. Capitalize first letter of every sentence\n"
        "2. Use 'Smart Doc' as proper noun (capitalized)\n"
        "3. Add a single heading with the template name and the heading should be centered\n"
        "4. Fix all grammar/spelling errors\n"
        "5. Remove redundant headings\n"
        "6. Make sure proper punctuation is used throughout\n\n"
        f"Original Document:\n{text}\n\n"
        "Transformed Document:"
    )

    try:
        result = ask_ollama(prompt).strip()
        return jsonify({"transformed_text": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5001, debug=True)
