from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import pyttsx3
import threading

app = Flask(__name__)

# Mikrofon için speech_recognition ayarları
recognizer = sr.Recognizer()
recognizer.energy_threshold = 4000  # Ses eşiğini artır

def generate_response(text):
    responses = {
        "hello": "Hello!",
        "how are you": "I'm fine, thank you!",
        "what's your name": "I'm a virtual assistant!",
    }
    return responses.get(text.lower(), "I don't understand")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recognize', methods=['POST'])
def recognize():
    try:
        with sr.Microphone() as source:
            print("Dinliyorum...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio, language="en-US")
            print(f"Söylenen: {text}")

            response_text = generate_response(text)

            # Her çağrıda yeni bir thread ile konuşma motorunu çalıştır
            threading.Thread(target=speak, args=(response_text,)).start()

            return jsonify({'text': text, 'response': response_text})
    except sr.UnknownValueError:
        return jsonify({'error': 'Ses anlaşılamadı'})
    except sr.RequestError:
        return jsonify({'error': 'Google Web Servisleri erişilemiyor'})
    except Exception as e:
        print(f"Hata: {e}")
        return jsonify({'error': str(e)})

def speak(text):
    # Her seferinde yeni bir engine oluşturuluyor
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Konuşma hızı
    engine.setProperty('volume', 1.0)  # Ses seviyesi
    engine.say(text)
    engine.runAndWait()

if __name__ == '__main__':
    app.run(debug=True)
#a