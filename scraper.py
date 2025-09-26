import random
import time
from pathlib import Path
import praw
import prawcore
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Reddit client with credentials from .env
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

class ScrapeResult:
    # Class to store scraped Reddit post data
    def __init__(self, url: str, title: str, self_text: str, username: str):
        self.url = url
        self.title = title
        self.self_text = self_text
        self.username = username

def check_string_in_file(file_path: Path, search_string: str) -> bool:
    # Check if a string exists in a file; create file if it doesn't exist
    try:
        with file_path.open('r', encoding='utf-8') as file:
            return any(line.strip() == search_string for line in file)
    except FileNotFoundError:
        file_path.touch()
        return False

def scrape(subreddit: str) -> ScrapeResult:
    # Scrape a random post from a subreddit, ensuring unique URLs
    print(f"Scraping r/{subreddit}")
    used_urls_file = Path("UsedUrls.txt")
    try:
        # Try fetching a random post
        submission = reddit.subreddit(subreddit).random()
        print(f"Fetched random post: {submission.title}")
    except prawcore.exceptions.BadRequest:
        # Fallback to hot posts if random is not supported
        print(f"Random post not supported for r/{subreddit}, fetching from hot posts...")
        posts = list(reddit.subreddit(subreddit).hot(limit=10))
        if not posts:
            raise ValueError(f"No posts found in r/{subreddit}")
        submission = random.choice(posts)
        print(f"Fetched hot post: {submission.title}")
    except prawcore.exceptions.TooManyRequests:
        # Handle Reddit API rate limit
        print("Rate limit hit, waiting 60 seconds...")
        time.sleep(60)
        return scrape(subreddit)
    except Exception as e:
        print(f"Error scraping r/{subreddit}: {str(e)}")
        raise

    url = submission.url
    # Ensure URL hasn't been used before
    while check_string_in_file(used_urls_file, url):
        print(f"URL {url} already used, fetching another post...")
        try:
            submission = reddit.subreddit(subreddit).random()
        except prawcore.exceptions.BadRequest:
            posts = list(reddit.subreddit(subreddit).hot(limit=10))
            if not posts:
                raise ValueError(f"No more posts available in r/{subreddit}")
            submission = random.choice(posts)
        url = submission.url

    # Save URL to file
    with used_urls_file.open('a', encoding='utf-8') as file:
        file.write(f"{url}\n")

    username = submission.author.name if submission.author else "Unknown"
    return ScrapeResult(url, submission.title, submission.selftext, username)