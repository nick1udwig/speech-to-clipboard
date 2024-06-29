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
MIN_DURATION_SECS = 0.3

with open('./my_api_key.txt', 'r') as f:
    api_key = f.read().strip()

client = openai.OpenAI(
    api_key=api_key,
)

def check_audio_duration(filename, min_duration=MIN_DURATION_SECS):
    with sf.SoundFile(filename) as file:
        # Calculate the duration in seconds
        duration_seconds = len(file) / file.samplerate
    return duration_seconds >= min_duration

def start_recording():
    global recording, audio_data
    if not recording:
        audio_data = []
    recording = True
    print('Recording started...')

def stop_recording():
    global recording
    recording = False
    temp_file = write_audio_file(audio_data)
    if check_audio_duration(temp_file.name, min_duration=MIN_DURATION_SECS):
        print('Recording stopped. Transcribing...')
        transcribe_audio(temp_file)
    else:
        print(f'Recording stopped. False start (duration < {MIN_DURATION_SECS} second).')

def record_callback(indata, frames, time, status):
    if recording:
        audio_data.extend(indata.copy())

def write_audio_file(audio_data):
    audio_np = np.concatenate(audio_data, axis=0)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    sf.write(temp_file.name, audio_np, sample_rate)
    return temp_file

def transcribe_audio(temp_file):
    with open(temp_file.name, 'rb') as audio_bytes:
        try:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_bytes,
            )
        except Exception as e:
            print(f'got exception {e} while trying to transcribe')
            return
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
