from flask import Flask, request, jsonify
from flask_cors import CORS
from googletrans import Translator

app = Flask(__name__)
CORS(app)
translator = Translator()

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('text')
    src = data.get('src')
    dest = data.get('dest')
    
    try:
        translation = translator.translate(text, src=src, dest=dest)
        return jsonify({
            'translatedText': translation.text,
            'pronunciation': translation.pronunciation
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)