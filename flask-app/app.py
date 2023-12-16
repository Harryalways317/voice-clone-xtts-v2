from flask import Flask, request, Response, jsonify
import torch
import platform
from TTS.api import TTS
import uuid
import html
import io
import json
from pathlib import Path
import noisereduce as nr
import librosa
import soundfile as sf
import os
app = Flask(__name__)

# Check if running on macOS
def is_mac_os():
    return platform.system() == 'Darwin'

# Initialize TTS and device settings
device = torch.device('cpu') if is_mac_os() else torch.device('cuda:0')
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# Load the language data
with open(Path('languages.json'), encoding='utf8') as f:
    languages = json.load(f)

# Function to generate voice
def gen_voice_old(string, spk, speed, english):
    string = html.unescape(string)
    audio_buffer = io.BytesIO()
    tts.tts_to_file(
        text=string,
        speed=speed,
        file_path=audio_buffer,
        speaker_wav=[f"targets/{spk}.wav"],
        language=languages[english]
    )
    audio_buffer.seek(0)
    return audio_buffer

# Function to generate voice
def gen_voice(string, spk, speed, english):
    string = html.unescape(string)
    # Generate audio and save to a temporary file
    temp_file = f'temp-{uuid.uuid4()}.wav'
    tts.tts_to_file(
        text=string,
        speed=speed,
        file_path=temp_file,
        speaker_wav=[f"targets/{spk}.wav"],
        language=languages[english]
    )
    # Load the audio back in
    audio_data, sample_rate = sf.read(temp_file)
    # Remove the temporary file
    os.remove(temp_file)
    return audio_data, sample_rate

# Function to apply noise reduction
def reduce_noise(audio_data, sample_rate):
    # Apply noise reduction
    reduced_noise_audio = nr.reduce_noise(y=audio_data, sr=sample_rate)
    return reduced_noise_audio

# Function to update speakers
def update_speakers():
    speakers = {p.stem: str(p) for p in list(Path('targets').glob("*.wav"))}
    return list(speakers.keys())

# Text-to-Speech conversion endpoint
@app.route('/convert', methods=['POST'])
def convert_text_to_speech():
    data = request.json
    audio_data, sample_rate = gen_voice(data['text'], data['speaker'], data['speed'], data['language'])

    # Apply noise reduction
    reduced_noise_audio = nr.reduce_noise(y=audio_data, sr=sample_rate)

    # Convert numpy array back to bytes
    audio_buffer = io.BytesIO()
    sf.write(audio_buffer, reduced_noise_audio, sample_rate, format='WAV')
    audio_buffer.seek(0)

    # Stream response
    return Response(audio_buffer, mimetype="audio/wav")



def convert_text_to_speech_old():
    data = request.json
    audio_buffer = gen_voice(data['text'], data['speaker'], data['speed'], data['language'])

    # Stream response
    return Response(audio_buffer, mimetype="audio/wav")

# Update speakers endpoint
@app.route('/speakers', methods=['GET'])
def get_speakers():
    speakers = update_speakers()
    return jsonify(speakers)

# Starting the Flask app
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5002)

