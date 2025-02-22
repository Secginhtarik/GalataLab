import speech_recognition as sr
import pyttsx3

# Konuşma tanıma içinRecognizer nesnesi
recognizer = sr.Recognizer()

# Sesli okuma için pyttsx3 motoru
engine = pyttsx3.init()

# Sesli yanıtlar için bir fonksiyon
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Konuşmayı dinleyen fonksiyon
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        
    try:
        # İngilizce konuşmayı tanımaya çalışıyoruz
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-US')
        print("You said:", query)
        return query.lower()
    except Exception as e:
        print("Sorry, I could not understand your speech.")
        return None

# Ana diyalog fonksiyonu
def chat():
    speak("Hello, how can I assist you today?")
    
    while True:
        user_input = listen()
        
        if user_input:
            if 'how are you' in user_input:
                speak("I'm doing great, thank you for asking!")
            elif 'goodbye' in user_input:
                speak("Goodbye! Have a great day!")
                break
            else:
                speak("Sorry, I didn't quite get that.")
        else:
            speak("Please speak again.")

# Programı başlatma
if __name__ == "__main__":
    chat()
