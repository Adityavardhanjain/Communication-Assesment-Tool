from flask import Flask, render_template, request, redirect, url_for
import random
import speech_recognition as sr
import Levenshtein
from tabulate import tabulate

app = Flask(__name__)

def generate_paragraph():
    sentences = [
        "The sun was shining brightly in the clear blue sky.",
        "A gentle breeze rustled the leaves of the tall trees.",
        "Children were playing in the park, laughing and enjoying their time.",
        "The smell of fresh flowers filled the air, creating a pleasant atmosphere.",
        "People strolled along the peaceful path, taking in the beauty of nature.",
        "A small cafe nearby offered delicious pastries and aromatic coffee.",
        "Birds chirped happily, adding to the symphony of nature's sounds.",
        "As the day progressed, the sky painted itself with warm hues of orange and pink.",
        "It was a serene evening, perfect for reflection and relaxation.",
    ]
    selected_sentences = random.sample(sentences, 2)
    paragraph = ' '.join(selected_sentences)
    return paragraph

def recognize_speech_from_file(audio_file):
    recognizer = sr.Recognizer()
    recognized_texts = []  # Store recognized texts in a list

    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)

    try:
        user_text = recognizer.recognize_google(audio)
        recognized_texts.append(user_text)  # Append recognized text to the list
        return user_text
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def evaluate_pronunciation(generated_text, user_text):
    distance = Levenshtein.distance(generated_text, user_text)
    max_length = max(len(generated_text), len(user_text))
    similarity_ratio = 1 - (distance / max_length)
    return similarity_ratio

def calculate_single_fluency_score(recognized_text, target_text):
    distance = Levenshtein.distance(recognized_text, target_text)
    max_length = max(len(recognized_text), len(target_text))
    fluency_score = 1 - (distance / max_length)
    return fluency_score

@app.route('/')
def index():
    generated_paragraph = generate_paragraph()
    return render_template('index.html', paragraph=generated_paragraph)

@app.route('/result', methods=['POST'])
def result():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    audio_file = request.files['file']

    if audio_file.filename == '':
        return redirect(url_for('index'))

    audio_file.save('uploaded_audio.wav')  # Save the uploaded audio file

    generated_paragraph = generate_paragraph()
    user_response = recognize_speech_from_file('uploaded_audio.wav')

    if user_response:
        similarity_ratio = evaluate_pronunciation(generated_paragraph, user_response)

        single_fluency_score = calculate_single_fluency_score(user_response, generated_paragraph)

        table = [
            ["Fluency Score", f"{single_fluency_score:.2%}"],
            ["Fluency Interpretation", 
                "Excellent fluency" if 0.90 <= single_fluency_score <= 1.00
                else "Good fluency" if 0.80 <= single_fluency_score < 0.90
                else "Moderate fluency" if 0.70 <= single_fluency_score < 0.80
                else "Fair fluency" if 0.60 <= single_fluency_score < 0.70
                else "Poor fluency" if 0.50 <= single_fluency_score < 0.60
                else "Very poor fluency, potential understanding issues"
            ]
        ]

        return render_template('result.html', paragraph=generated_paragraph, user_response=user_response, similarity_ratio=similarity_ratio, table=table)

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
