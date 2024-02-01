import random
from scraper import scrape
from PIL import Image, ImageOps, ImageDraw, ImageFont
from speech import textToSpeech
from moviepy.editor import AudioFileClip

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

    postTemplate.show()



def generateAudio(scrape, voice: str):
    title = scrape.title
    selfText = scrape.selfText

    textToSpeech(title, voice, "Title.mp3")
    textToSpeech(selfText, voice, "SelfText.mp3")


def generateVideo():
    # Audio Files
    selfTextAudio = "SelfText.mp3"
    titleAudio = "Title.mp3"

    # Getting audio lengths
    with AudioFileClip(selfTextAudio) as audio:
        selfTextLength = audio.duration
    
    with AudioFileClip(titleAudio) as audio:
        titleLength = audio.duration
    
    videoLength = selfTextLength + titleLength + 1





    print(videoLength)















subRedditList = ["confession", "tifu"]
selected_subreddit = random.choice(subRedditList)

result = scrape(selected_subreddit)

createPostImage("Images/profilePicture.jpeg", "Images/PostTemplate.png", "Images/Mask.png", "Ressssss.Stories", result)
generateVideo()
generateAudio(result, "alloy")