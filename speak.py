from gtts import gTTS
import tempfile
import os

def speak(text):
    tts = gTTS(text=text, lang="en")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        filename = fp.name

    tts.save(filename)

    return filename