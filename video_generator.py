import math
import random
import subprocess
from pathlib import Path
import helpers
from scraper import scrape
from speech import text_to_speech
from image_generator import create_post_image

def generate_audio(scrape, voice: str) -> None:
    # Generate audio files for post title and text
    title_path = Path("Assets/Audio/Title.mp3")
    self_text_path = Path("Assets/Audio/SelfText.mp3")
    text_to_speech(scrape.title, voice, title_path)
    text_to_speech(scrape.self_text, voice, self_text_path)

def generate_video(game: str, username: str) -> None:
    # Generate a TikTok video by combining Reddit post, audio, and gameplay
    # Validate input files
    required_files = [
        Path(f"Assets/Video/{game}.mp4"),
        Path("Assets/Images/ProfilePicture.jpeg"),
        Path("Assets/Images/PostTemplate.png"),
        Path("Assets/Images/Mask.png"),
        Path("Assets/Images/Verified.png"),
        Path("Assets/Fonts/Kanit-Medium.ttf")
    ]
    for file_path in required_files:
        if not file_path.exists():
            raise FileNotFoundError(f"Required file not found: {file_path}")

    # Scrape Reddit post
    subreddits = ["confession", "tifu"]
    selected_subreddit = random.choice(subreddits)
    result = scrape(selected_subreddit)

    # Create post image
    create_post_image(
        Path("Assets/Images/ProfilePicture.jpeg"),
        Path("Assets/Images/PostTemplate.png"),
        Path("Assets/Images/Mask.png"),
        username,
        result
    )

    # Generate audio
    generate_audio(result, "Joanna")

    # Get media durations
    try:
        input_video_duration = helpers.get_media_duration(
            Path(f"Assets/Video/{game}.mp4"), "mp4"
        )
        title_duration = helpers.get_media_duration(
            Path("Assets/Audio/Title.mp3"), "mp3"
        )
        self_text_duration = helpers.get_media_duration(
            Path("Assets/Audio/SelfText.mp3"), "mp3"
        )
    except Exception as e:
        print(f"Error getting media durations: {str(e)}")
        raise

    output_video_duration = title_duration + self_text_duration
    start_time = random.randint(
        15, math.ceil(input_video_duration) - math.ceil(output_video_duration) + 1
    )

    # Generate subtitles
    helpers.generate_subtitles(
        title_duration,
        Path("Assets/Audio/SelfText.mp3"),
        Path("Assets/Subtitles/Subtitles.srt")
    )

    # Concatenate audio files
    concat_audio_command = [
        "ffmpeg",
        "-y",
        "-i", "Assets/Audio/Title.mp3",
        "-i", "Assets/Audio/SelfText.mp3",
        "-filter_complex", "concat=n=2:v=0:a=1",
        "Assets/Audio/ConcatenatedAudio.mp3"
    ]
    try:
        subprocess.run(concat_audio_command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error concatenating audio: {e.stderr}")
        raise

    print("Compiling video...")

    # Overlay post image on video
    # Note: Using libx264 due to NVIDIA driver 546.29 (NVENC requires 551.76+).
    # Revert to h264_nvenc after updating driver for faster encoding.
    overlay_command = [
        "ffmpeg",
        "-y",
        "-ss", str(start_time),
        "-i", f"Assets/Video/{game}.mp4",
        "-i", "Assets/Images/Post.png",
        "-i", "Assets/Audio/ConcatenatedAudio.mp3",
        "-filter_complex",
        f"[1:v]scale=iw*1.5:ih*1.5[scaled];[0:v][scaled]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2:enable='between(t,0,{title_duration})'[video]",
        "-map", "[video]",
        "-map", "2:a",
        "-c:v", "libx264",
        "-preset", "fast",
        "-c:a", "aac",
        "-t", str(output_video_duration),
        "Assets/Video/Temp.mp4"
    ]
    try:
        subprocess.run(overlay_command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error overlaying video: {e.stderr}")
        raise

    # Add subtitles
    subtitles_command = [
        "ffmpeg",
        "-y",
        "-i", "Assets/Video/Temp.mp4",
        "-vf", "subtitles=Assets/Subtitles/Subtitles.srt:force_style='Alignment=10,FontName=Arial,FontSize=16,PrimaryColour=&HFFFFFF,BorderStyle=1,Outline=1,Shadow=2'",
        "-c:v", "libx264",
        "-c:a", "copy",
        "Assets/Video/FinalVideo.mp4"
    ]
    try:
        subprocess.run(subtitles_command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error adding subtitles: {e.stderr}")
        raise

if __name__ == "__main__":
    generate_video("Minecraft", "reddit.Stories")