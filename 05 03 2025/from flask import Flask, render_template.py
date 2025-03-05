from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import speech_recognition as sr
import io
import logging

app = Flask(__name__)
CORS(app)
recognizer = sr.Recognizer()
recognizer.energy_threshold = 4000
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recognize', methods=['POST'])
def recognize():
    try:
        if 'audio' not in request.files:
            app.logger.error("Ses dosyası yüklenemedi")
            return jsonify({'error': 'Ses dosyası bulunamadı'}), 400

        audio_file = request.files['audio']
        audio_data = io.BytesIO(audio_file.read())
        
        with sr.AudioFile(audio_data) as source:
            try:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio, language="en-US")
                app.logger.info(f"Tanınan metin: {text}")
                return jsonify({'text': text})
            except sr.WaitTimeoutError:
                app.logger.error("Ses zaman aşımına uğradı")
                return jsonify({'error': 'Ses girişi algılanamadı'}), 408

    except sr.UnknownValueError:
        app.logger.error("Ses anlaşılamadı")
        return jsonify({'error': 'Ses anlaşılamadı'}), 400
    except sr.RequestError as e:
        app.logger.error(f"Google servis hatası: {e}")
        return jsonify({'error': f'Google servis hatası: {e}'}), 500
    except Exception as e:
        app.logger.error(f"Beklenmeyen hata: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)