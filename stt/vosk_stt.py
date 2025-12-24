import json
from vosk import Model, KaldiRecognizer
import wave, os

def transcribe_hindi(audio_path):
    if not os.path.exists("vosk_hindi_model"):
        raise FileNotFoundError("vosk_hindi_model folder missing. Place model in project folder.")

    model = Model("vosk_hindi_model")
    wf = wave.open(audio_path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    text=""
    while True:
        data=wf.readframes(4000)
        if len(data)==0: break
        if rec.AcceptWaveform(data):
            res=json.loads(rec.Result())
            text+=res.get("text","")+" "
    final=json.loads(rec.FinalResult())
    text+=final.get("text","")
    return text.strip()
