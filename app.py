from flask import Flask, render_template, request, redirect
from transformers import pipeline
import speech_recognition as sr

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    transcript = ""
    summary_text = ""
    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(file)
            with audioFile as source:
                data = recognizer.record(source)
            transcript = recognizer.recognize_google(data, key=None)
            summarization = pipeline("summarization")
            original = transcript
            summary_text = summarization(original)[0]['summary_text']
    return render_template('index.html', transcript=transcript, summary_text = summary_text)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)