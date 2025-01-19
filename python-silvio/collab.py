import os
from flask import Flask, jsonify, send_file
from flask_cors import CORS
from pydub import AudioSegment
import torch
import numpy as np
import google.generativeai as genai

# Set up paths for the current project and subdirectories
current_directory = os.getcwd()
print(f"Current Directory: {current_directory}")

# Change to Kokoro-82M directory
child_directory = "Kokoro-82M"
child_path = os.path.join(current_directory, child_directory)

import os

os.environ["PHONEMIZER_ESPEAK_LIBRARY"] = r"C:/Program Files/eSpeak NG/libespeak-ng.dll"
os.environ["PHONEMIZER_ESPEAK_PATH"] = r"C:/Program Files/eSpeak NG/espeak-ng.exe"

if os.path.exists(child_path) and os.path.isdir(child_path):
    os.chdir(child_path)
    print(f"Changed Directory To: {os.getcwd()}")
else:
    print(f"Directory '{child_directory}' does not exist!")

# Set up the model and load the necessary files
import sys
sys.path.append(os.getcwd())
from kokoro import generate
from models import build_model

device = 'cuda' if torch.cuda.is_available() else 'cpu'
MODEL = build_model('kokoro-v0_19.pth', device)
VOICE_NAME = [
    'af', 'af_bella', 'af_sarah', 'am_adam', 'am_michael', 'bf_emma', 'bf_isabella',
    'bm_george', 'bm_lewis', 'af_nicole', 'af_sky',
][1]  # Default voice
VOICEPACK = torch.load(f'voices/{VOICE_NAME}.pt', weights_only=True).to(device)
print(f'Loaded voice: {VOICE_NAME}')

# Initialize Flask application
app = Flask(__name__)
CORS(app)

# Audio file generation and playback function
def generate_audio_from_text(text):
    audio = []
    for chunk in text.split("."):
        print(chunk)
        if len(chunk) < 2:
            continue
        snippet, _ = generate(MODEL, chunk, VOICEPACK, lang=VOICE_NAME[0])

        if snippet.dtype == np.float32:
            snippet = (snippet * 32767).astype(np.int16)
        audio.append(snippet)

    # Combine all audio chunks into one
    def combine_audio(audio_chunks):
        if audio_chunks:
            return np.concatenate(audio_chunks)
        else:
            return np.array([], dtype=np.int16)

    # Save numpy audio data as an MP3 file
    def save_audio_as_mp3(audio_data, filename="output.mp3", sample_rate=24000):
        if audio_data.size == 0:
            print("Error: No audio data to save.")
            return

        audio_bytes = audio_data.tobytes()
        audio_segment = AudioSegment(
            data=audio_bytes,
            sample_width=2,  # Assuming 16-bit audio
            frame_rate=sample_rate,
            channels=1,  # Mono audio
        )
        audio_segment.export(filename, format="mp3")
        print(f"Audio saved to {filename}")

    # Combine and save the audio
    combined_audio = combine_audio(audio)
    save_audio_as_mp3(combined_audio, filename="../content/output.mp3")

# Route for serving the MP3 file
@app.route("/audio", methods=["GET"])
def get_audio():
    try:
        # Adjust the path to the correct directory
        # Absolute path for content folder

        mp3_file_path = os.path.join(os.getcwd(), "content", "output.mp3")
        print(f"Looking for the audio file at: {mp3_file_path}")  # Debugging line

        if not os.path.exists(mp3_file_path):
            return jsonify({"error": "File not found"}), 404

        return send_file(mp3_file_path, mimetype="audio/mpeg")

    except Exception as e:
        return jsonify({"error": str(e)}), 500




# Example route for generating text-to-speech from provided text
@app.route("/generate_audio", methods=["POST"])
def generate_audio():
    try:
        # Here you would take the input text and generate the audio
        # Example of input text (replace with actual input handling)
        text = "This is an example of generated audio from Kokoro."

        # Generate audio
        generate_audio_from_text(text)

        return jsonify({"message": "Audio generated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Start the Flask app
if __name__ == "__main__":
    os.chdir("..")  # Go one level up from Kokoro-82M
    app.run(port=5000)
