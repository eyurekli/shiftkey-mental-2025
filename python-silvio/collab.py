import os
from flask import Flask, jsonify, send_file, request
from flask_cors import CORS
from pydub import AudioSegment
import torch
import numpy as np
import google.generativeai as genai
import speech_recognition as sr
from pydub import AudioSegment

from io import BytesIO
from base64 import b64decode
from IPython.display import display, Javascript, HTML


import google.generativeai as genai
# Used to securely store your API key

from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GENAI_API_KEY')
genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    'gemini-1.5-flash',
    generation_config=genai.GenerationConfig(
        temperature=0.7,
    ))
chat = model.start_chat(history=[])

import locale
def getpreferredencoding(do_setlocale = True):
    return "UTF-8"
locale.getpreferredencoding = getpreferredencoding


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

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return "No file part", 400
    audio_file = request.files['audio']
    
    if audio_file.filename == '':
        return "No selected file", 400
    
    # Save the file to the server
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
    audio_file.save(file_path)

    # After saving the audio file, call the gen_ai function
    gen_ai()
    os.chdir("..")

    
    
    return "File uploaded successfully", 200

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


def gen_ai():
    r = sr.Recognizer()

    from pydub import AudioSegment
    def convert_to_pcm_wav(input_file, output_file):
        audio = AudioSegment.from_file(input_file)
        audio = audio.set_channels(1).set_sample_width(2).set_frame_rate(16000)  # Standard settings
        audio.export(output_file, format="wav")

    # Original file path
    file_path = 'uploads/recordedAudio.wav'
    
    # Convert to PCM if necessary
    converted_file_path = 'uploads/converted_recordedAudio.wav'
    convert_to_pcm_wav(file_path, converted_file_path)

    # Check if the converted file exists
    if not os.path.exists(converted_file_path):
        print(f"Error: {converted_file_path} does not exist.")
        return

    # Perform speech recognition
    with sr.AudioFile(converted_file_path) as source:
        audio_data = r.record(source)
        try:
            text = r.recognize_google(audio_data)
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand the audio.")
            return
        except sr.RequestError:
            print("Sorry, the service is down.")
            return

    # Save the recognized text to 'speech.txt'
    text_file = "speechTest.txt"
    with open(text_file, "w") as file:
        file.write(text)

    prompt = """This message contains a brief description of an individual experiencing a mental health issue and requesting assistance.
    Given the user's description, respond in a conversational and concise manner, offering support and assistance in a compassionate way. INCLUDE NO ASTERISKS OR SPECIAL CHARACTERS IN THE RESPONSE. Keep this to no more than 4 sentences.
    """

    with open(text_file, "r") as file:
        sample_context = file.read()

    # Sending the text to the chat for response
    response = chat.send_message([prompt, sample_context])

    # Write the response to 'tts.txt'
    file_tts = "tts.txt"
    with open(file_tts, "w") as file:
        file.write(response.text)

    # Get the current directory to navigate
    current_directory = os.getcwd()
    print(f"Current Directory: {current_directory}")

    child_directory = "Kokoro-82M"  # Change this to your correct folder name
    child_path = os.path.join(current_directory, child_directory)

    # Ensure the directory exists before moving
    if os.path.exists(child_path) and os.path.isdir(child_path):
        os.chdir(child_path)
        print(f"Changed Directory To: {os.getcwd()}")
    else:
        print(f"Directory '{child_directory}' does not exist!")

    sys.path.append(os.getcwd())

    from models import build_model
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    MODEL = build_model('kokoro-v0_19.pth', device)
    VOICE_NAME = 'af_bella'  # Default voice, you can choose another

    VOICEPACK = torch.load(f'voices/{VOICE_NAME}.pt', weights_only=True).to(device)
    print(f'Loaded voice: {VOICE_NAME}')

    with open("../tts.txt", "r") as file:
        text = file.read()

    from kokoro import generate

    # Simulated audio generation loop
    audio = []
    for chunk in text.split("."):
        print(chunk)
        if len(chunk) < 2:
            continue
        snippet, _ = generate(MODEL, chunk, VOICEPACK, lang=VOICE_NAME[0])

        # Handle `numpy.ndarray` snippet
        if snippet.dtype == np.float32:
            snippet = (snippet * 32767).astype(np.int16)
        audio.append(snippet)

    # Combine all audio chunks into one numpy array
    def combine_audio(audio_chunks):
        if audio_chunks:
            return np.concatenate(audio_chunks)
        else:
            return np.array([], dtype=np.int16)

    # Save numpy audio data as an MP3
    def save_audio_as_mp3(audio_data, filename="output.mp3", sample_rate=24000):
        if audio_data.size == 0:
            print("Error: No audio data to save.")
            return

        # Convert numpy array to bytes
        audio_bytes = audio_data.tobytes()

        # Create an AudioSegment from raw PCM data
        audio_segment = AudioSegment(
            data=audio_bytes,
            sample_width=2,  # Assuming 16-bit audio
            frame_rate=sample_rate,
            channels=1,  # Assuming mono audio
        )
        # Export the AudioSegment as an MP3 file
        audio_segment.export(filename, format="mp3")
        print(f"Audio saved to {filename}")

    # Combine and save the audio
    combined_audio = combine_audio(audio)
    save_audio_as_mp3(combined_audio, filename="../content/output.mp3")

    # Optionally, play the saved MP3 file (requires IPython)
    try:
        from IPython.display import display, Audio
        display(Audio("../content/output.mp3", autoplay=True))
    except ImportError:
        print("IPython display not available, audio won't play automatically.")
    

# Start the Flask app
if __name__ == "__main__":
    os.chdir("..")  # Go one level up from Kokoro-82M
    app.run(port=5000)
