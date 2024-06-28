import json
import requests
import tempfile

import openai
import pyperclip

import numpy as np
import sounddevice as sd
import soundfile as sf

from pynput import keyboard

sample_rate = 44100
recording = False
audio_data = []

client = openai.OpenAI(
    api_key='lol'
)

def start_recording():
    global recording, audio_data
    if not recording:
        audio_data = []
    recording = True
    print('Recording started...')

def stop_recording():
    global recording
    recording = False
    print('Recording stopped. Transcribing...')
    transcribe_audio()

def record_callback(indata, frames, time, status):
    if recording:
        audio_data.extend(indata.copy())

def transcribe_audio():
    global audio_data
    #audio_np = np.array(audio_data, dtype=np.float32)
    #audio_bytes = bytes(audio_np.tobytes())
    audio_np = np.concatenate(audio_data, axis=0)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    #temp_file = 'hello.wav'
    #sf.write(temp_file, audio_np, sample_rate)
    sf.write(temp_file.name, audio_np, sample_rate)

    with open(temp_file.name, 'rb') as audio_bytes:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_bytes,
        )
    print(f'{transcript.text}')
    pyperclip.copy(transcript.text)

def on_press(key):
    if key == keyboard.Key.f6:  # Change key combination as needed
        start_recording()

def on_release(key):
    if key == keyboard.Key.f6:  # Change key combination as needed
        stop_recording()
        #return False  # Optionally stop listener

def main():
    # Set up the microphone recorder
    stream = sd.InputStream(callback=record_callback, samplerate=sample_rate, channels=1)
    stream.start()

    # Set up the keyboard listener
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == '__main__':
    main()
