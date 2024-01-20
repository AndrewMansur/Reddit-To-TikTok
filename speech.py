from pathlib import Path
from openai import OpenAI

client = OpenAI(api_key = "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")




#outputs mp3 of text to speech
# voice types: Alloy, Echo, Fable, Onyx, Nova, Shimmer
def textToSpeech(text: str, voice: str):
    speech_file_path = "speech.mp3"

    response = client.audio.speech.create(
    model="tts-1",
    voice = voice,
    input = text
    )

    response.stream_to_file(speech_file_path)


textToSpeech("hello there, my name is andrew", "alloy")