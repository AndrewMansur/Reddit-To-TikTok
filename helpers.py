import random
from datetime import timedelta
from pathlib import Path
import ffmpeg
import assemblyai as aai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def split_string(text: str, max_length: int = 40) -> list[str]:
    # Split text into lines with a maximum length for display
    words = text.split()
    result = []
    current_line = ""
    for word in words:
        if len(current_line + word) > max_length:
            result.append(current_line.strip())
            current_line = word
        else:
            current_line += " " + word
    if current_line:
        result.append(current_line.strip())
    return result

def get_text_dimensions(text: str, font) -> tuple[int, int]:
    # Get width and height of text using specified font
    ascent, descent = font.getmetrics()
    text_width = font.getmask(text).getbbox()[2]
    text_height = font.getmask(text).getbbox()[3] + descent
    return text_width, text_height

def get_media_duration(media_path: Path, file_type: str) -> float:
    # Get duration of a media file (mp4 or mp3)
    try:
        probe = ffmpeg.probe(str(media_path))
        if file_type == "mp4":
            stream = next((s for s in probe['streams'] if s['codec_type'] == 'video'), None)
        elif file_type == "mp3":
            stream = next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        if not stream:
            raise ValueError(f"No {file_type} stream found in {media_path}")
        return float(stream['duration'])
    except ffmpeg.Error as e:
        print(f"Error probing {media_path}: {e}")
        raise

def generate_words(audio_path: Path) -> list:
    # Transcribe audio to words using AssemblyAI
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not aai.settings.api_key:
        raise ValueError("AssemblyAI API key not found")
    try:
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(str(audio_path))
        return transcript.words
    except Exception as e:
        print(f"Error transcribing audio: {str(e)}")
        raise

def format_time(ms: int, title_length: float) -> str:
    # Format time for SRT subtitles, adjusting for title duration
    title_length_timedelta = timedelta(seconds=title_length - 1)
    return str(timedelta(milliseconds=ms) + title_length_timedelta)[:-3].replace('.', ',')

def words_to_srt(words: list, title_length: float) -> str:
    # Convert transcribed words to SRT subtitle format
    srt_entries = []
    title_length_seconds = title_length + 1
    i = 0
    entry_index = 1
    while i < len(words):
        group_size = random.randint(1, 4)
        segment = words[i:i + group_size]
        if not segment:
            continue
        start_time = format_time(segment[0].start, title_length_seconds)
        end_time = format_time(segment[-1].end, title_length_seconds)
        text = ' '.join(word.text for word in segment)
        srt_entries.append(f"{entry_index}\n{start_time} --> {end_time}\n{text}\n")
        i += group_size
        entry_index += 1
    return '\n'.join(srt_entries)

def generate_subtitles(title_duration: float, audio_path: Path, output_path: Path) -> None:
    # Generate SRT subtitles from audio file
    print("Generating subtitles...")
    try:
        words = generate_words(audio_path)
        subtitles = words_to_srt(words, title_duration)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open('w', encoding='utf-8') as file:
            file.write(subtitles)
    except Exception as e:
        print(f"Error generating subtitles: {str(e)}")
        raise