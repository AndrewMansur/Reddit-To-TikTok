import praw
import random

# PROBABLY NOT BEST WAY TO STORE??
# Initialize the Reddit instance
reddit = praw.Reddit(client_id="GRpmJ57fuNLklmJkXiHUQg",
                     client_secret="VTIh6wY_HGnCIKsysgy8CYwgrFWFVw",
                     username="GrapefruitFront8544",
                     password="andrew1497",
                     user_agent="pythonpraw")

# Class to hold scrape results
class ScrapeResult:
    def __init__(self, url, title, selfText, username):
        self.url = url
        self.title = title
        self.selfText = selfText
        self.username = username


# Check if a string is in a line of a text file
def checkStringInFile(filePath: str, specificString: str):
    with open(filePath, 'r') as file:
        for line in file:
            if line.strip() == specificString:
                return True
    return False


# Scrape a random submission from a subreddit
def scrape(subreddit: str):
    submission = reddit.subreddit(subreddit).random()
    url = submission.url

    while checkStringInFile("UsedUrls.txt", url):
        submission = reddit.subreddit(subreddit).random()
        url = submission.url

    with open("UsedUrls.txt", "a") as usedUrls:
        usedUrls.write(submission.url + "\n")

    username = submission.author.name if submission.author else "Unknown"
    
    return ScrapeResult(url, submission.title, submission.selftext, username)


