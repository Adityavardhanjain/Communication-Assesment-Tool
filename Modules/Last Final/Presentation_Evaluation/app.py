from flask import Flask, render_template, request
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import speech_recognition as sr
import os
import language_tool_python
import textstat
from prettytable import PrettyTable
import librosa
import numpy as np

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_file = request.files['video_file']
        if video_file:
            video_path = os.path.join('uploads', 'input_video.mp4')
            audio_path = os.path.join('uploads', 'audio.wav')

            video_file.save(video_path)

            # Step 3: Convert video to audio
            video_to_audio(video_path, audio_path)
            print("Video converted to audio successfully.")

            # Step 5: Recognize speech
            recognized_text = recognize_speech(audio_path)

            # Intonation Checker
            intonation_percentage = check_intonation(audio_path)

            # Grammar Checker
            grammar_errors = grammar_check(recognized_text)

            # Readability Score
            readability_score = gf_score(recognized_text)
            readability_table = get_readability_table()

            return render_template('result.html', intonation_percentage=intonation_percentage,
                                   grammar_errors=grammar_errors, readability_score=readability_score,
                                   readability_table=readability_table)

    return render_template('index.html')

def video_to_audio(video_path, audio_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_path)
    audio_clip.close()

def recognize_speech(audio_path):
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

# ... (previous code)

def check_intonation(audio_path):
    y, sr = librosa.load(audio_path, sr=None)
    pitch_values, _ = librosa.piptrack(y=y, sr=sr)
    pitch_values_mean = pitch_values.mean(axis=0)

    threshold_low_variation = 20  # Hz
    threshold_high_variation = 40  # Hz
    min_duration_low_variation = 3  # seconds
    min_duration_high_variation = 0.2  # seconds

    low_pitch_count = 0
    high_pitch_count = 0

    in_low_variation = False
    in_high_variation = False

    for pitch_value in pitch_values_mean:
        if pitch_value < threshold_low_variation:
            if not in_low_variation:
                in_low_variation = True
                low_pitch_count += 1
                in_high_variation = False
        elif pitch_value > threshold_high_variation:
            if not in_high_variation:
                in_high_variation = True
                high_pitch_count += 1
                in_low_variation = False
        else:
            in_low_variation = False
            in_high_variation = False

    if low_pitch_count == 0:
        return 100  # Avoid division by zero
    else:
        intonation_percentage = (high_pitch_count / low_pitch_count) * 100
        return intonation_percentage

# ... (remaining code)


def grammar_check(recognized_text):
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(recognized_text)
    return matches

def gf_score(recognized_text):
    return textstat.gunning_fog(recognized_text)

def get_readability_table():
    # Create a PrettyTable object
    table = PrettyTable(["Readability Index", "Difficulty Level"])

    # Add rows to the table
    table.add_row(["6 and lower", "Very easy"])
    table.add_row(["7-9", "Easy"])
    table.add_row(["10-12", "Moderate"])
    table.add_row(["13-16", "Difficult"])
    table.add_row(["17 and higher", "Very difficult"])

    # Set the alignment of the columns
    table.align["Readability Index"] = "l"
    table.align["Difficulty Level"] = "l"

    # Get the table as a formatted string
    table_str = str(table)
    return table_str

if __name__ == "__main__":
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
