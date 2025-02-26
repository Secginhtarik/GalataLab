from flask import Flask, render_template, request, jsonify
import speech_recognition as sr

app = Flask(__name__)
recognizer = sr.Recognizer()
recognizer.energy_threshold = 4000  # Ses eşiğini artır

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recognize', methods=['POST'])
def recognize():
    try:
        # Kullanıcının sesini kaydet
        with sr.Microphone() as source:
            print("Dinliyorum...")
            recognizer.adjust_for_ambient_noise(source)  # Gürültüyü filtrele
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio, language="en-US", show_all=False)
            print(f"Söylenen: {text}")

        return jsonify({'text': text})
    except sr.UnknownValueError:
        return jsonify({'error': 'Ses anlaşılamadı'})
    except sr.RequestError:
        return jsonify({'error': 'Google Web Servisleri erişilemiyor'})
    except Exception as e:
        print(f"Hata: {e}")
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)