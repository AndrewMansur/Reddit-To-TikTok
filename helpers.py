import ffmpeg, os, random
import assemblyai as aai
from datetime import timedelta


# Splits a string so that it wraps to the next line
def splitString(text: str):
    splitLength = 40
    stringToSplit = text
    words = stringToSplit.split()
    result = []
    current_string = ""

    for word in words:
        if len(current_string + word) > splitLength:
            result.append(current_string.strip())
            current_string = word
        else:
            current_string += " " + word

    if current_string:
        result.append(current_string.strip())

    return result


def getTextDimensions(text_string, font):
    ascent, descent = font.getmetrics()
    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent
    return (text_width, text_height)

def getMediaDuration(mediaPath: str, filetype: str):
    probe = ffmpeg.probe(mediaPath)
    
    if filetype == "mp4":
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        return float(video_stream['duration'])
    elif filetype == "mp3":
        audio_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
        return float(audio_stream['duration'])
    else:
        return "Invalid filetype"


def generateWords():
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe("Audio/SelfText.mp3")
    return transcript.words

def format_time(ms, titleLength):
    # Convert titleLength to a timedelta object for addition
    title_length_timedelta = timedelta(seconds=titleLength - 1)  # Adjust the offset here
    # Add the title length to the time calculated from milliseconds
    return str(timedelta(milliseconds=ms) + title_length_timedelta)[:-3].replace('.', ',')



def words_to_srt(words, titleLength):
    srt_entries = []
    title_length_seconds = titleLength + 1
    i = 0
    entry_index = 1
    while i < len(words):
        group_size = random.randint(1, 4)
        segment = words[i:i+group_size]
        if not segment:
            continue
        
        start_time = format_time(segment[0].start, title_length_seconds) 
        end_time = format_time(segment[-1].end, title_length_seconds) 
        text = ' '.join(word.text for word in segment)
        srt_entries.append(f"{entry_index}\n{start_time} --> {end_time}\n{text}\n")

        i += group_size
        entry_index += 1

    return '\n'.join(srt_entries)


def generateSubtitles(titleDuration: int):
    print("Generating Subtitles...")
    words = generateWords()
    subtitles = words_to_srt(words, titleDuration)

    with open("Subtitles.srt", "w") as file:
        file.write(subtitles)