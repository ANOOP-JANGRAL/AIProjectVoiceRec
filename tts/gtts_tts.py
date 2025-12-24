from gtts import gTTS
from playsound import playsound
import os
import uuid
import time

def speak_hindi(text):
    try:
        filename = f"tts_{uuid.uuid4().hex}.mp3"

        tts = gTTS(text=text, lang='hi')
        tts.save(filename)

        # playsound is blocking → waits till sound finishes
        playsound(filename)

        time.sleep(0.2)  # allow Windows to release file handle
        os.remove(filename)

    except Exception as e:
        print("TTS Error:", e)
