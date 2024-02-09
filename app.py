import re
import os
import speech_recognition as sr
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Set a secret key for CSRF protection
csrf = CSRFProtect(app)

class AudioForm(FlaskForm):
    audio_file = StringField('Audio File', validators=[DataRequired()])

@app.route('/', methods=['GET', 'POST'])
def transcribe_audio():
    form = AudioForm()

    if request.method == 'POST' and form.validate_on_submit():
        # Get the uploaded file
        audio_file = request.files['audio_file']

        # Define the speech recognizer
        recognizer = sr.Recognizer()

        # Use the recognizer to transcribe the audio file
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source, duration=10)
            try:
                transcription = recognizer.recognize_google(audio, language="sq-AL")
                transcription = re.sub(r'[^\w\së]', '', transcription.capitalize())

                # Add comma between words
                transcription = re.sub(r'\s+', '-', transcription)

                # Add period at the end of the transcription
                transcription = transcription.strip() + '.'

                # Extract the audio file name without the extension
                audio_filename = os.path.splitext(audio_file.filename)[0]

                # Save the transcription as a TXT file with the same name as the audio file
                save_file_path = f"{audio_filename}.txt"  # Provide the desired directory path
                with open(save_file_path, 'w', encoding='utf-8') as txt_file:
                    converted_transcription = transcription.replace("�", "ë")
                    txt_file.write(converted_transcription)

                # Render the output in the HTML template
                return render_template('output.html', transcription=transcription)

            except sr.UnknownValueError:
                error_message = "Google Speech Recognition could not understand audio"
                return render_template('output.html', error=error_message)

            except sr.RequestError as e:
                error_message = f"Could not request results from Google Speech Recognition service: {e}"
                return render_template('output.html', error=error_message)

    # Render the initial file upload form
    return render_template('index.html', form=form)

if __name__ == '__main__':
    # Run the Flask app with Gunicorn WSGI server
    app.run(host='0.0.0.0', port=5000)