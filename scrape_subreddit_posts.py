import json
import praw
import os
from dotenv import load_dotenv

load_dotenv()

def scrape_subreddit_posts():
    subreddit_list = os.getenv("SUBREDDIT_LIST").split(",")
    post_num = 1000  # Set the number of posts to download
    directory = os.getenv("SOURCE_DIRECTORY")
    path = os.path.join(directory, "posts.json")

    reddit = praw.Reddit(client_id=os.getenv("CLIENT_ID"),
                         client_secret=os.getenv("CLIENT_SECRET"),
                         user_agent=os.getenv("USER_AGENT"))

    data = {}
    if os.path.exists(path):
        with open(path) as f:
            data = json.load(f)
    else:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    for subreddit_name in subreddit_list:
        if subreddit_name not in data:
            data[subreddit_name] = []
        hot_posts = reddit.subreddit(subreddit_name).new(limit=int(post_num))
        for post in hot_posts:
            title = post.title
            created_utc = post.created_utc
            if not any(d['title'] == title for d in data[subreddit_name]):
                data[subreddit_name].append({"title": title, "created_utc": int(created_utc)})

    with open(path, "w") as f:
        json.dump(data, f, indent=2)
