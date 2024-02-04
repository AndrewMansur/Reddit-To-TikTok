import random
import math
import datetime
import srt
from scraper import scrape
from PIL import Image, ImageOps, ImageDraw, ImageFont
from speech import textToSpeech
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io.VideoFileClip import VideoFileClip
import pysrt

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

    # Add the last string if it's not empty
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

    #Display profile Picture
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

    # Use get_text_dimensions to calculate text width
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

    # Dynamic position for the verified image
    verifiedImagePosition = (usernamePosition[0] + textWidth + 10, 105)  # 10 is additional spacing
    postTemplate.paste(verifiedImage, verifiedImagePosition, verifiedImage)

    finalizedImage = postTemplate.resize((540,290))

    finalizedImage.save("Images/Post.png")



def generateAudio(scrape, voice: str):
    title = scrape.title
    selfText = scrape.selfText

    textToSpeech(title, voice, "Audio/Title.mp3")
    textToSpeech(selfText, voice, "Audio/SelfText.mp3")



def splitString(text):
    # Placeholder function to split text into manageable lines
    # This should be replaced with your actual implementation
    return text.split('. ')

def estimate_duration(text):
    # Estimate duration based on text length
    words_per_minute = 150  # Average speech rate
    words = len(text.split())
    minutes = words / words_per_minute
    return minutes * 60  # Return duration in seconds

def format_time(seconds):
    # Convert seconds to SRT time format
    return str(datetime.timedelta(seconds=seconds)).split(".")[0].replace(":", ",").replace("0 days,", "").strip()

def generateSubtitles(scrape):
    title = scrape.title  # Adjusted for dict access
    selfText = scrape.selfText # Adjusted for dict access

    # Split the text into lines
    splitTitle = splitString(title)
    splitSelfText = splitString(selfText)

    startTime = 0
    with open("Subtitles.srt", "w") as subtitles:
        # Then process selfText
        for i, line in enumerate(splitSelfText, start=1):
            duration = estimate_duration(line)
            endTime = startTime + duration
            subtitles.write(f"{i + len(splitTitle)}\n{format_time(startTime)} --> {format_time(endTime)}\n{line}\n\n")
            startTime += duration  # Update start time for the next line

    return "Subtitles.srt"



def make_textclip(txt):
    return TextClip(txt, font='Arial', fontsize=24, color='white', bg_color='black')

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
    endTime = startTime + videoLength  # make it + videoLength after testing and random video time


    # Crop the video to the proper dimensions
    originalVideo = VideoFileClip("Video/" + game + ".mp4")
    backgroundVideo = originalVideo.subclip(startTime, endTime)

    new_height = backgroundVideo.size[1]
    new_width = int(new_height * 9 / 16)

    backgroundVideo = backgroundVideo.crop(x_center=backgroundVideo.size[0]/2, width=new_width)
    

     # Paste post photo
    image_clip = ImageClip("Images/Post.png").set_start(0).set_duration(titleLength).set_pos("center", "center")
    backgroundVideo = CompositeVideoClip([backgroundVideo, image_clip])


    # Play audio
    titleAudio = AudioFileClip("Audio/Title.mp3")
    selfTextAudio = AudioFileClip("Audio/SelfText.mp3")
    finalAudio = CompositeAudioClip([titleAudio, selfTextAudio.set_start(titleLength + 1)])
    

    backgroundVideo = backgroundVideo.set_audio(finalAudio).set_start(0.1)

    backgroundVideo.write_videofile("Video/BackgroundVideo.mp4", codec="libx264", audio_codec="aac")
    


subRedditList = ["confession", "tifu"]
selected_subreddit = random.choice(subRedditList)

result = scrape(selected_subreddit)

createPostImage("Images/profilePicture.jpeg", "Images/PostTemplate.png", "Images/Mask.png", "Ressssss.Stories", result)
generateAudio(result, "alloy")
generateSubtitles(result)
generateVideo(result, "minecraft")
