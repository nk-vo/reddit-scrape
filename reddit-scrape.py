from RedDownloader import RedDownloader
import praw
import os
import re

subreddit_name = input("Enter subreddit: ")
url = "https://www.reddit.com"

directory = DESIRED_DIRECTORY
# Path
path = os.path.join(directory, subreddit_name)

if not os.path.exists(path):
  os.mkdir(path)

#get those parameters from reddit developer account
reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT)

hot_posts = reddit.subreddit(subreddit_name).new(limit=10000)
count = 0
for post in hot_posts:
  permalink = post.permalink
  title = post.title
  title = re.sub(r'[^A-Za-z0-9 ,]+', '', title).strip()
  
  if title == "":
    title = str(count)
    count += 1
  if not os.path.exists(path + "/" + title + (".jpeg" or ".mp4")):
    file = RedDownloader.Download(url + permalink, output = title , quality = 720, destination = path + "/")
