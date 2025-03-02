from flask import Flask, render_template, jsonify
import pyttsx3
import speech_recognition as sr

app = Flask(__name__)
recognizer = sr.Recognizer()
recognizer.energy_threshold = 4000

# Sesli yanıt 
engine = pyttsx3.init()
engine.setProperty('rate', 150) 
engine.setProperty('volume', 1) 

# Sesli yanıt fonksiyonu
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Yanıtları analiz et ve uygun cevabı oluştur
def generate_response(text):
    text = text.lower()  # Kullanıcının söylediklerini küçük harfe dönüştür

    if "hello" in text:
        response = "Hello, how can I help you today?"
        speak(response)  
        return response
    elif "how are you" in text:
        response = "I'm doing great, thank you! How about you?"
        speak(response)  
        return response
    elif "your name" in text:
        response = "I'm an assistant, created to help you with speech recognition."
        speak(response)  
        return response
    else:
        response = "Sorry, I didn't understand that."
        speak(response)  
        return response


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recognize', methods=['POST'])
def recognize():
    try:
        with sr.Microphone() as source:
            print("Dinliyorum...")
            recognizer.adjust_for_ambient_noise(source)  # Gürültüyü filtrele
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio, language="en-US", show_all=False)
            print(f"Söylenen: {text}")

            # Dinlenen metne göre yanıt oluştur
            response = generate_response(text)
            print(f"Yanıt: {response}")

            # Sesli yanıt ver
            speak(response)
            
        return jsonify({'text': text, 'response': response})

    except sr.UnknownValueError:
        return jsonify({'error': 'Ses anlaşılamadı'})
    except sr.RequestError:
        return jsonify({'error': 'Google Web Servisleri erişilemiyor'})
    except Exception as e:
        print(f"Hata: {e}")
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
