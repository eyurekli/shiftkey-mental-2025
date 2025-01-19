# #COMMAND

# # !pip install -q -U google-generativeai

# # !pip install flask

# # !pip install pyngrok
# # !pip install SpeechRecognition pydub
# # !pip install pydub
# # pip install ipython

import flask
from flask import request
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)

@app.route("/add", methods=["POST"], strict_slashes=False)
def add_articles():
    title = request.json['title']
    body = request.json['body']

    article = Articles(
        title=title,
        body=body
        )

    db.session.add(article)
    db.session.commit()

    return article_schema.jsonify(article)


import os

os.environ["PHONEMIZER_ESPEAK_LIBRARY"] = r"C:/Program Files/eSpeak NG/libespeak-ng.dll"
os.environ["PHONEMIZER_ESPEAK_PATH"] = r"C:/Program Files/eSpeak NG/espeak-ng.exe"

# # Get the current directory
current_directory = os.getcwd()
print(f"Current Directory: {current_directory}")

# # Navigate to the parent directory
# if current_directory != "C:/Users/silvi/OneDrive/Documents/Goofy Webpage":
#     os.chdir("..")
#     parent_directory = os.getcwd()
#     print(f"Parent Directory: {parent_directory}")



# # Check if the directory exists before cloning the repository
#     # Install git LFS and clone the repository if the directory doesn't exist




#     #CONSOLE COMMANDS
#     # !git lfs install
#     # !git clone https://huggingface.co/hexgrad/Kokoro-82M
#     # %cd Kokoro-82M
#     # !apt-get -qq -y install espeak-ng > /dev/null 2>&1
#     # !pip install -q phonemizer torch transformers scipy munch
#     # %cd ..
    


from io import BytesIO
from base64 import b64decode
from IPython.display import display, Javascript, HTML

import google.generativeai as genai
# Used to securely store your API key


genai.configure(api_key='AIzaSyCRBqXqcVIn4DBowSXiYYTEk6dk_X-nTsM')
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



import speech_recognition as sr
from pydub import AudioSegment

# Navigate into a child directory
child_directory = "content"  # Replace with your folder name
child_path = os.path.join(current_directory, child_directory)

# Change to the child directory
if os.path.exists(child_path) and os.path.isdir(child_path):
    os.chdir(child_path)
    print(f"Changed Directory To: {os.getcwd()}")
else:
    print(f"Directory '{child_directory}' does not exist!")

filename = 'audioTest.wav'

# Initialize the recognizer
r = sr.Recognizer()

# Open the converted WAV file
with sr.AudioFile(filename) as source:
    # Listen for the data (load audio to memory)
    audio_data = r.record(source)
    # Recognize (convert from speech to text)
    text = r.recognize_google(audio_data)

# Specify the file name
file_name = "speechTest.txt"
# Write the string to a .txt file
with open(file_name, "w") as file:
    file.write(text)



    prompt = """This message contains a brief description of an individual experiencing a mental health issue and requesting assistance.
Given the user's description, respond in a conversational and concise manners, offering support and assistance in a compassionate way. INCLUDE NO ASTERISKS OR SPECIAL CHARACTERS IN THE RESPONSE. Keep this to no more than 8 sentences.
"""


with open("speechTest.txt", "r") as file:
     sample_context = file.read()

response = chat.send_message([prompt,sample_context])



# Specify the file name
file_name = "tts.txt"

# Write the string to a .txt file
with open(file_name, "w") as file:
    file.write(response.text)




os.chdir("..")

# Get current directory
current_directory = os.getcwd()
print(f"Current Directory: {current_directory}")

# Navigate into a child directory
child_directory = "Kokoro-82M"  # Replace with your folder name
child_path = os.path.join(current_directory, child_directory)

# Change to the child directory
if os.path.exists(child_path) and os.path.isdir(child_path):
    os.chdir(child_path)
    print(f"Changed Directory To: {os.getcwd()}")
else:
    print(f"Directory '{child_directory}' does not exist!")

import sys

sys.path.append(os.getcwd())

from models import build_model
import torch
device = 'cuda' if torch.cuda.is_available() else 'cpu'
MODEL = build_model('kokoro-v0_19.pth', device)
VOICE_NAME = [
    'af', # Default voice is a 50-50 mix of Bella & Sarah
    'af_bella', 'af_sarah', 'am_adam', 'am_michael',
    'bf_emma', 'bf_isabella', 'bm_george', 'bm_lewis',
    'af_nicole', 'af_sky',
][1]
VOICEPACK = torch.load(f'voices/{VOICE_NAME}.pt', weights_only=True).to(device)
print(f'Loaded voice: {VOICE_NAME}')




with open("../content/tts.txt", "r") as file:
     text = file.read()





from kokoro import generate

# # Language is determined by the first letter of the VOICE_NAME:
# # 🇺🇸 'a' => American English => en-us
# # 🇬🇧 'b' => British English => en-gb


import numpy as np
from pydub import AudioSegment

# Simulated audio generation loop (use your actual audio generation logic)
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

# Combine all audio chunks into one
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

# Optionally, play the saved MP3 file
from IPython.display import display, Audio
display(Audio("../content/output.mp3", autoplay=True))
