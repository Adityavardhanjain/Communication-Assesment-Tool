from flask import Flask, render_template, request
from gtts import gTTS
import os
import random
import speech_recognition as sr

app = Flask(__name__)

def calculate_accuracy(generated_text, recorded_text):
    generated_words = generated_text.lower().split()
    recorded_words = recorded_text.lower().split()
    common_words = set(generated_words) & set(recorded_words)
    accuracy_percentage = (len(common_words) / len(generated_words)) * 100
    return accuracy_percentage

def generate_speech_sample():
    greetings = ["Hello", "Hi", "Hey", "Greetings", "Salutations"]
    subjects = ["world", "everyone", "friends", "colleagues", "team", "audience"]
    verbs = ["welcomes", "greets", "acknowledges", "salutes", "extends regards to"]
    emotions = ["with joy", "warmly", "enthusiastically", "with sincerity", "with open arms"]

    speech_sample = f"{random.choice(greetings)}, {random.choice(subjects)}! " \
                    f"This is a message that {random.choice(verbs)} you {random.choice(emotions)}."
    return speech_sample

def text_to_speech(text, language='en', filename='static/output.mp3'):
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(filename)
    return filename

def recognize_speech():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Repeat the audio you just heard:")
        try:
            # Set a timeout of 10 seconds
            audio = r.listen(source, timeout=15)
            # Recognize the spoken audio
            recorded_text = r.recognize_google(audio)
            return recorded_text

        except sr.UnknownValueError:
            print("Could not understand audio")
            return None

        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

# Placeholder function for ML model prediction
def ml_model_predict(text):
    # Replace this with your actual ML model inference logic
    # For demonstration, it returns a placeholder result
    return "Placeholder Model Result: " + text.upper()

@app.route('/')
def index():
    generated_speech = generate_speech_sample()
    audio_filename = text_to_speech(generated_speech)
    return render_template('index.html', audio_filename=audio_filename)

@app.route('/speech_recognition', methods=['POST'])
def speech_recognition():
    recorded_text = request.form['generated_speech']
    
    # Replace the ml_model_predict with your actual ML model inference
    ml_result = ml_model_predict(recorded_text)

    accuracy = calculate_accuracy(generate_speech_sample(), recorded_text)

    pronunciation_result = "Pronunciation is correct!" if accuracy >= 90 else "Pronunciation is incorrect."

    return render_template('result.html', recorded_text=recorded_text, ml_result=ml_result, accuracy=accuracy, pronunciation_result=pronunciation_result)

if __name__ == '__main__':
    app.run(debug=True)
