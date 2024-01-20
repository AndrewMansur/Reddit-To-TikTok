from scraper import scrape , random

subRedditList = ["confession", "tifu"]
selected_subreddit = random.choice(subRedditList)



result = scrape(selected_subreddit)


print(f"URL: {result.url}")
print(f"Title: {result.title}")
print(f"Selftext: {result.selfText}")
