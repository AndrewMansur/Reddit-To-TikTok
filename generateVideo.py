import random, math, srt, os
from scraper import scrape
from PIL import Image, ImageOps, ImageDraw, ImageFont
from speech import textToSpeech
from moviepy.editor import TextClip, VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, CompositeAudioClip
import assemblyai as aai
from datetime import timedelta

# Splits a string so that it wraps to the next line
def splitString(text: str):
    splitLength = 40
    stringToSplit = text
    words = stringToSplit.split()
    result = []
    current_string = ''

    for word in words:
        if len(current_string + word) > splitLength:
            result.append(current_string.strip())
            current_string = word
        else:
            current_string += ' ' + word

    if current_string:
        result.append(current_string.strip())

    return result

# Gets dimensions of text
def getTextDimensions(text_string, font):
    ascent, descent = font.getmetrics()
    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent
    return (text_width, text_height)

def createPostImage(profilePicturePath, templatePath, maskPath, username, scrape):
    # Open files
    mask = Image.open(maskPath).convert('L')
    im = Image.open(profilePicturePath)
    postTemplate = Image.open(templatePath).convert("RGBA")
    verifiedImage = Image.open("Images/Verified.png").convert("RGBA")

    # Display profile Picture
    circle_diameter = 170
    circle_position = (71, 62)

    profilePicture = ImageOps.fit(im, (circle_diameter, circle_diameter), centering=(0.5, 0.5))
    resized_mask = mask.resize(profilePicture.size)
    profilePicture.putalpha(resized_mask)

    postTemplate.paste(profilePicture, circle_position, profilePicture)

    # Display username
    textColor = "black"
    fontPath = "Kanit-Medium.ttf"
    textFont = ImageFont.truetype(fontPath, 45)
    usernameFont = ImageFont.truetype(fontPath, 40)

    textWidth, _ = getTextDimensions(username, usernameFont)

    # Display Username
    usernamePosition = (300, 100)
    draw = ImageDraw.Draw(postTemplate)
    draw.text(usernamePosition, username, fill=textColor, font=usernameFont)

    # Display post text
    splitTextList = splitString(scrape.title)
    for i, line in enumerate(splitTextList):
        text_position = (68, 250 + 45 * i)
        draw.text(text_position, line, fill=textColor, font=textFont)

    # Resize verified image
    verifiedImageSize = (50, 50)
    verifiedImage = verifiedImage.resize(verifiedImageSize, Image.Resampling.LANCZOS)

    verifiedImagePosition = (usernamePosition[0] + textWidth + 10, 105)
    postTemplate.paste(verifiedImage, verifiedImagePosition, verifiedImage)

    finalizedImage = postTemplate.resize((540, 290))
    finalizedImage.save("Images/Post.png")

def generateAudio(scrape, voice: str):
    title = scrape.title
    selfText = scrape.selfText

    textToSpeech(title, voice, "Audio/Title.mp3")
    textToSpeech(selfText, voice, "Audio/SelfText.mp3")


#HIDE THE API KEY!
def generateSubtitles():
    aai.settings.api_key = os.getenv("161dc1d1eda1415d9e2a3e4210048fec")
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe("Audio/SelfText.mp3")
    return transcript.words

def format_time(ms, titleLength):
    # Convert titleLength to a timedelta object for addition
    title_length_timedelta = timedelta(seconds=titleLength)
    # Add the title length to the time calculated from milliseconds
    return str(timedelta(milliseconds=ms) + title_length_timedelta)[:-3].replace('.', ',')

def words_to_srt(words, titleLength, group_size=10):
    srt_entries = []
    # Convert titleLength to seconds for easier addition
    title_length_seconds = titleLength + 1
    for i in range(0, len(words), group_size):
        segment = words[i:i+group_size]
        if not segment:
            continue
        
        # Ensure you're adding the title length to both start and end times
        start_time = format_time(segment[0].start, title_length_seconds) 
        end_time = format_time(segment[-1].end, title_length_seconds) 
        text = ' '.join(word.text for word in segment)
        srt_entries.append(f"{i//group_size + 1}\n{start_time} --> {end_time}\n{text}\n")

    return '\n'.join(srt_entries)


# Game is just the string of the game name
def generateVideo(scrape, game: str):
    selfText = scrape.selfText
    print(selfText)

    # Audio Files
    selfTextAudioFile = "Audio/SelfText.mp3"
    titleAudioFile = "Audio/Title.mp3"

    # Getting audio lengths
    with AudioFileClip(selfTextAudioFile) as audio:
        selfTextLength = audio.duration

    with AudioFileClip(titleAudioFile) as audio:
        titleLength = audio.duration

    with VideoFileClip(f"Video/{game}.mp4") as video:
        originalVideoLength = video.duration

    videoLength = selfTextLength + titleLength + 2
    startTime = random.randint(15, math.ceil(originalVideoLength) - math.ceil(videoLength) + 1)
    endTime = startTime + videoLength

    originalVideo = VideoFileClip("Video/" + game + ".mp4")
    backgroundVideo = originalVideo.subclip(startTime, endTime)

    new_height = backgroundVideo.size[1]
    new_width = int(new_height * 9 / 16)
    backgroundVideo = backgroundVideo.crop(x_center=backgroundVideo.size[0] / 2, width=new_width)

    image_clip = ImageClip("Images/Post.png").set_start(0).set_duration(titleLength).set_pos("center", "center")
    backgroundVideo = CompositeVideoClip([backgroundVideo, image_clip])

    titleAudio = AudioFileClip("Audio/Title.mp3")
    selfTextAudio = AudioFileClip("Audio/SelfText.mp3")
    finalAudio = CompositeAudioClip([titleAudio, selfTextAudio.set_start(titleLength + 1)])
    backgroundVideo = backgroundVideo.set_audio(finalAudio).set_start(0.1)

    srt_content = words_to_srt(generateSubtitles(), titleLength)

    with open("Subtitles.srt", "w") as file:
        file.write(srt_content)

    subtitles = []
    with open('Subtitles.srt', 'r') as f:
        subtitle_generator = srt.parse(f.read())
        for subtitle in subtitle_generator:
            start_time = subtitle.start.total_seconds()
            end_time = subtitle.end.total_seconds()
            text = subtitle.content
            subtitles.append((start_time, end_time, text))

    text_clips = []
    for subtitle in subtitles:
        start_time, end_time, text = subtitle
        duration = end_time - start_time
        fontsize = max(90 - int(len(text) / 5), 10) / 3
        text_clip = TextClip(text, fontsize=fontsize, color='white', align='center').set_duration(duration)
        text_clip = text_clip.set_position('center')
        text_clip = text_clip.set_start(start_time).set_end(end_time)
        text_clips.append(text_clip)

    backgroundVideo = CompositeVideoClip([backgroundVideo] + text_clips)
    backgroundVideo.write_videofile("Video/BackgroundVideo.mp4", codec="libx264", audio_codec="aac")



subRedditList = ["confession", "tifu"]
selected_subreddit = random.choice(subRedditList)

result = scrape(selected_subreddit)
# createPostImage("Images/profilePicture.jpeg", "Images/PostTemplate.png", "Images/Mask.png", "Ressssss.Stories", result)
# generateAudio(result, "alloy")
generateVideo(result, "minecraft")
generateSubtitles()
