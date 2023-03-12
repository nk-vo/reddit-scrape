from RedDownloader import RedDownloader
import praw
import os
import re
import sys
import tkinter
from tkinter import ttk
from dotenv import load_dotenv
load_dotenv()

subreddit_list = os.getenv("SUBREDDIT_LIST").split(",")

def clean_filename(filename, limit=260):
    """
    Remove invalid characters, URLs, trim, and reduce filename length
    """
    # Remove any URLs from the filename
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    filename = url_pattern.sub('', filename)

    # Remove any invalid characters from the filename
    invalid_chars = re.compile(r'[\\/:*?"<>|]')
    filename = invalid_chars.sub('', filename)

    # Trim the filename
    filename = filename.strip()

    # Reduce filename length if it exceeds the limit
    if len(filename) > limit:
        filename = filename[:limit]

    return filename


for subreddit_name in subreddit_list:
    post_num = 1000  # Set the number of posts to download
    url = "https://www.reddit.com"

    directory = "E:/Reddit-Scrape/"
    # Path
    path = os.path.join(directory, subreddit_name)

    if not os.path.exists(path):
        os.mkdir(path)

    reddit = praw.Reddit(client_id=os.getenv("CLIENT_ID"),
                         client_secret=os.getenv("CLIENT_SECRET"),
                         user_agent=os.getenv("USER_AGENT"))
    try:
        hot_posts = reddit.subreddit(subreddit_name).new(limit=int(post_num))
        count = 0
        post_downloaded = 0
        for post in hot_posts:
            permalink = post.permalink
            title = post.title
            title = clean_filename(title)

            if title == "":
                while (os.path.exists(path + "/" + str(count) + ".mp4")):
                    count += 1
                title = str(count)
            if not os.path.exists(path + "/" + title + ".mp4"):
                if os.path.exists(path + "/" + title + ".jpeg"):
                    continue
                file = RedDownloader.Download(
                    url + permalink,
                    output=title,
                    quality=720,
                    destination=path + "/")
                post_downloaded += 1

            if os.path.exists(path + "/" + title + ".jpeg"):
                continue
    except Exception as e:
        print(f"Error while downloading media from {subreddit_name}: {e}")
        continue
    print("Downloaded " + str(post_downloaded) +
          " posts from r/" + subreddit_name)
