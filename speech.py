import boto3
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def text_to_speech(text: str, voice: str, output_path: Path) -> None:
    # Convert text to speech using AWS Polly and save as MP3
    print(f"Generating audio for: {text[:30]}...")
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    if not (access_key and secret_key):
        raise ValueError("AWS credentials not found in environment variables")

    try:
        # Initialize AWS Polly client
        polly_client = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name="us-west-2"
        ).client("polly")

        # Synthesize speech
        response = polly_client.synthesize_speech(
            VoiceId=voice,
            OutputFormat="mp3",
            Text=text,
            Engine="standard"
        )

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        # Save audio to file
        with output_path.open("wb") as file:
            file.write(response["AudioStream"].read())
    except Exception as e:
        print(f"Error generating audio: {str(e)}")
        raise