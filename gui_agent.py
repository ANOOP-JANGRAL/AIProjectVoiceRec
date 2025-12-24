import tkinter as tk
from tkinter import scrolledtext
import sounddevice as sd
from scipy.io.wavfile import write
import threading
import numpy as np

from stt.vosk_stt import transcribe_hindi
from tts.gtts_tts import speak_hindi
from agent.agent_core import agent_step

recording = False
audio_data = []

# ---------------- AUDIO RECORDING ---------------- #

def record_audio():
    global recording, audio_data
    audio_data = []
    recording = True
    fs = 16000  # sample rate

    def callback(indata, frames, time, status):
        if recording:
            audio_data.append(indata.copy())
        else:
            raise sd.CallbackStop()

    try:
        with sd.InputStream(callback=callback, channels=1, samplerate=fs):
            while recording:
                sd.sleep(100)
    except:
        pass

    if audio_data:
        audio_np = np.concatenate(audio_data, axis=0)
        audio_int16 = np.int16(audio_np * 32767)
        write("record.wav", fs, audio_int16)


def start_recording():
    start_btn.config(state="disabled")
    stop_btn.config(state="normal")
    box.insert(tk.END, "\n🎤 Recording started...\n")
    threading.Thread(target=record_audio, daemon=True).start()


def stop_recording():
    global recording
    recording = False
    stop_btn.config(state="disabled")
    start_btn.config(state="normal")
    box.insert(tk.END, "⏹ Recording stopped. Processing...\n")
    process_audio()


# ---------------- AGENT PIPELINE ---------------- #

def process_audio():
    text = transcribe_hindi("record.wav")
    box.insert(tk.END, f"\n🗣 You said: {text}\n")

    response = agent_step(text)
    box.insert(tk.END, f"\n🤖 Agent: {response}\n")

    # 🔴 CRITICAL FIX → Non-blocking TTS
    threading.Thread(
        target=speak_hindi,
        args=(response,),
        daemon=True
    ).start()


# ---------------- GUI SETUP ---------------- #

root = tk.Tk()
root.title("Hindi Voice Agent")
root.geometry("700x500")

title = tk.Label(
    root,
    text="🇮🇳 Hindi Voice AI Assistant",
    font=("Arial", 18, "bold")
)
title.pack(pady=10)

start_btn = tk.Button(
    root,
    text="🎤 Start Recording",
    font=("Arial", 14),
    bg="green",
    fg="white",
    command=start_recording
)
start_btn.pack(pady=10)

stop_btn = tk.Button(
    root,
    text="⏹ Stop Recording",
    font=("Arial", 14),
    bg="red",
    fg="white",
    command=stop_recording,
    state="disabled"
)
stop_btn.pack(pady=10)

box = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    width=80,
    height=20,
    font=("Arial", 12)
)
box.pack(pady=10, fill="both", expand=True)

# ---------------- WELCOME ---------------- #

welcome_text = (
    "नमस्ते! मैं आपकी सरकारी योजनाओं की पात्रता जांचने में आपकी मदद कर सकता हूँ।\n"
    "कृपया अपना नाम बताकर शुरुआत करें।\n\n"
)
box.insert(tk.END, welcome_text)

threading.Thread(
    target=speak_hindi,
    args=("नमस्ते! मैं आपकी सरकारी योजनाओं की पात्रता जांचने में आपकी मदद कर सकता हूँ। कृपया अपना नाम बताएं।",),
    daemon=True
).start()

root.mainloop()
