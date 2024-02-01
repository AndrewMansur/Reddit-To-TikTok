from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import os



load_dotenv()

# Access the API key
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)

#outputs mp3 of text to speech
# voice types: Alloy, Echo, Fable, Onyx, Nova, Shimmer
def textToSpeech(text: str, voice: str, filename: str):

    response = client.audio.speech.create(
    model="tts-1",
    voice = voice,
    input = text
    )

    response.stream_to_file(filename)

