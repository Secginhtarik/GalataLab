from flask import Flask, render_template, jsonify, request
import pyttsx3
import speech_recognition as sr
import threading
import json
from queue import Queue

app = Flask(__name__)
recognizer = sr.Recognizer()
recognizer.energy_threshold = 4000
stop_listening = False
listening_thread = None
message_queue = Queue()  # Konuşma ve yanıtları geçici olarak saklamak için bir kuyruk

# Sesli yanıt motoru
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)
engine_lock = threading.Lock()

def speak(text):
    def run_speech():
        with engine_lock:
            engine.say(text)
            engine.runAndWait()
    threading.Thread(target=run_speech, daemon=True).start()

def generate_response(text):
    text = text.lower()
    if "hello" in text:
        response = "Hello, how can I help you today?"
    elif "how are you" in text:
        response = "I'm doing great, thank you! How about you?"
    elif "your name" in text:
        response = "I'm an assistant, created to help you with speech recognition."
    else:
        response = "Sorry, I didn't understand that."
    speak(response)
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recognize', methods=['POST'])
def recognize():
    global stop_listening, listening_thread
    stop_listening = False
    
    def listen_thread():
        global stop_listening
        try:
            with sr.Microphone() as source:
                while not stop_listening:
                    print("Dinliyorum...")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    text = recognizer.recognize_google(audio, language="en-US", show_all=False)
                    print(f"Söylenen: {text}")
                    response = generate_response(text)
                    print(f"Yanıt: {response}")
                    # Konuşma tanındığında kuyruğa ekle
                    message_queue.put({'text': text, 'response': response})
        except sr.UnknownValueError:
            speak("Sesinizi algılayamadım, lütfen tekrar deneyin.")
            message_queue.put({'text': '', 'response': 'Sesinizi algılayamadım.'})
        except sr.RequestError:
            speak("İnternet bağlantısı sorunu, lütfen daha sonra tekrar deneyin.")
            message_queue.put({'text': '', 'response': 'İnternet bağlantısı sorunu.'})
        except Exception as e:
            print(f"Hata: {e}")
            speak("Bir hata oluştu.")
            message_queue.put({'text': '', 'response': 'Bir hata oluştu.'})
    
    listening_thread = threading.Thread(target=listen_thread, daemon=True)
    listening_thread.start()
    return jsonify({'status': 'listening'})

@app.route('/get_recognized', methods=['GET'])
def get_recognized():
    # Kuyrukta veri varsa al ve döndür, yoksa bekle
    try:
        message = message_queue.get(timeout=10)  # 10 saniye bekle, veri yoksa boş döner
        return jsonify(message)
    except:
        return jsonify({'text': '', 'response': ''})

@app.route('/stop', methods=['POST'])
def stop_listening_route():
    global stop_listening, listening_thread
    stop_listening = True
    if listening_thread and listening_thread.is_alive():
        listening_thread.join(timeout=1)
    return jsonify({'status': 'stopped'})

if __name__ == '__main__':
    app.run(debug=True)