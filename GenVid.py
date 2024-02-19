import ffmpeg, math, random, helpers, os, subprocess
from scraper import scrape
from PIL import Image, ImageOps, ImageDraw, ImageFont
from speech import textToSpeech


# Gets dimensions of text
def generateAudio(scrape, voice: str):
    title = scrape.title
    selfText = scrape.selfText

    textToSpeech(title, voice, "Audio/Title.mp3")
    textToSpeech(selfText, voice, "Audio/SelfText.mp3")


def createPostImage(profilePicturePath, templatePath, maskPath, username, scrape):
    print("Generating Post Image...")
    # Open files
    mask = Image.open(maskPath).convert("L")
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

    textWidth, _ = helpers.getTextDimensions(username, usernameFont)

    # Display Username
    usernamePosition = (300, 100)
    draw = ImageDraw.Draw(postTemplate)
    draw.text(usernamePosition, username, fill=textColor, font=usernameFont)

    # Display post text
    splitTextList = helpers.splitString(scrape.title)
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



def generateVideo(game: str, username: str):
    # Create scrape object
    subRedditList = ["confession", "tifu"]
    selected_subreddit = random.choice(subRedditList)
    result = scrape(selected_subreddit)

    # Create post image
    createPostImage("Images/ProfilePicture.jpeg", "Images/PostTemplate.png", "Images/Mask.png", username, result)

    #Generate audios
    generateAudio(result, "alloy")

    # Get duartion of input video
    inputVideoDuration = helpers.getMediaDuration(f"Video/{game}.mp4", "mp4")
    titleDuration = helpers.getMediaDuration("Audio/Title.mp3", "mp3")
    selfTextDuration = helpers.getMediaDuration("Audio/SelfText.mp3", "mp3")
    outputVideoDuration = titleDuration + selfTextDuration
   
    startTime = random.randint(15, math.ceil(inputVideoDuration) - math.ceil(outputVideoDuration) + 1)

    # Generate subtitles
    helpers.generateSubtitles(titleDuration)
    
    # Concatenate audio files
    concatAudioCommand = [
        "ffmpeg",
        "-y",  
        "-i", "Audio/Title.mp3",
        "-i", "Audio/SelfText.mp3",
        "-filter_complex", "concat=n=2:v=0:a=1",  # Concatenate two audio files
        "Audio/ConcatenatedAudio.mp3"
    ]
    subprocess.run(concatAudioCommand)

    print("Compiling Video...")

    # Overlay post Image
    overlayCommand = [
        "ffmpeg",
        "-y",
        "-ss", str(startTime),  # Start time for the input video
        "-i", f"Video/{game}.mp4",  # Input video file
        "-i", "Images/Post.png",    # Input image file
        "-i", "Audio/ConcatenatedAudio.mp3",  # Input concatenated audio file
        "-filter_complex",
        f"[1:v]scale=iw*1.5:ih*1.5[scaled];[0:v][scaled]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2:enable='between(t,0,{titleDuration})'[video]",
        "-map", "[video]",  # Map the video from the filter_complex
        "-map", "2:a",  # Map the concatenated audio
        "-c:v", "h264_nvenc",  # Use NVENC for video encoding
        "-preset", "fast",  # Choose a preset for speed/quality trade-off
        "-c:a", "aac",  # Specify the audio codec
        "-t", str(titleDuration + selfTextDuration + 1),  # Duration of output video
        "Video/Temp.mp4"  # Output file
    ]
    subprocess.run(overlayCommand)


    subTitlesCommand = [
        "ffmpeg",
        "-y",  # Overwrite output file if it exists
        "-i", "Video/Temp.mp4",  # Input video file
        "-vf", "subtitles=Subtitles.srt:force_style='Alignment=10,FontName=Proxima Nova Semibold.ttf,FontSize=16,PrimaryColour=&HFFFFFF,BorderStyle=1,Outline=1,Shadow=2'",  # BackColour=&H80000000 Add subtitles with custom font, size, and color
        "-c:v", "h264_nvenc",  # Re-encode video with x264 codec
        "-c:a", "copy",  # Copy the audio codec
        "Video/FinalVideo.mp4"  # Output file
    ]

    subprocess.run(subTitlesCommand)


generateVideo("Minecraft", "reddit.Stories")