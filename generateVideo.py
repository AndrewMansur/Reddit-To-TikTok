import random
from scraper import scrape
from PIL import Image, ImageOps, ImageDraw, ImageFont


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



def createPostImage(profilePicturePath, templatePath, maskPath, username, scrapeResult):
    mask = Image.open(maskPath).convert('L')
    im = Image.open(profilePicturePath)
    postTemplate = Image.open(templatePath).convert("RGBA")

    circle_diameter = 170
    circle_position = (71, 62)

    profilePicture = ImageOps.fit(im, (circle_diameter, circle_diameter), centering=(0.5, 0.5))
    resized_mask = mask.resize(profilePicture.size)
    profilePicture.putalpha(resized_mask)

    postTemplate.paste(profilePicture, circle_position, profilePicture)




    



    
    textColor = "black" 
    fontPath = "Kanit-Medium.ttf" 

    # Drawing text
    draw = ImageDraw.Draw(postTemplate)
    textFont = ImageFont.truetype(fontPath, 45)
    usernameFont = ImageFont.truetype(fontPath, 40)

    usernamePosition = (300, 100)
    draw.text(usernamePosition, username, fill = textColor, font = usernameFont)

    splitTextList = splitString(scrapeResult.title) 

    for i in range(0, len(splitTextList)):
        text_position = (68, 250 + 45 * i)  # Update this with the actual position
        draw.text(text_position, splitTextList[i], fill = textColor, font = textFont)

    postTemplate.show()


subRedditList = ["confession", "tifu"]
selected_subreddit = random.choice(subRedditList)

result = scrape(selected_subreddit)

createPostImage("Images/profilePicture.jpeg", "Images/PostTemplate.png", "Images/Mask.png", "Reddits.Stories", result)
