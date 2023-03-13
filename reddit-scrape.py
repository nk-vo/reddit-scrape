from RedDownloader import RedDownloader
import praw
import os
import re
import datetime
import json
from dotenv import load_dotenv

load_dotenv()

subreddit_list = os.getenv("SUBREDDIT_LIST").split(",")

def clean_filename(filename, limit=259):
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


def download_posts():
  start_time = datetime.datetime.now()
  url = "https://www.reddit.com"
  post_num = 1000  # Set the number of posts to download
  media_directory = os.getenv("MEDIA_DIRECTORY")
  # Path to JSON file that stores the downloaded posts for each subreddit
  source_directory = os.getenv("SOURCE_DIRECTORY")
  posts_json_path = os.path.join(source_directory, "posts.json")

  data = {}
  if os.path.exists(posts_json_path):
    with open(posts_json_path) as f:
      data = json.load(f)
  else:
    with open(posts_json_path, "w") as f:
      json.dump(data, f, indent=2)
      
  reddit = praw.Reddit(client_id=os.getenv("CLIENT_ID"),
                        client_secret=os.getenv("CLIENT_SECRET"),
                        user_agent=os.getenv("USER_AGENT"))

  for subreddit_name in subreddit_list:
    if subreddit_name not in data:
      data[subreddit_name] = []
    hot_posts = reddit.subreddit(subreddit_name).new(limit=int(post_num))
    for post in hot_posts:
      title = post.title
      created_utc = post.created_utc
      if not any(d['title'] == title and d['created_utc'] == int(created_utc) for d in data[subreddit_name]):
        data[subreddit_name].append({"title": title, "created_utc": int(created_utc)})
        title_cleaned = clean_filename(title)
        output = f"{title_cleaned}_{int(created_utc)}"
        path = os.path.join(media_directory, subreddit_name)
        if not os.path.exists(path):
          os.mkdir(path)
        try:
          RedDownloader.Download(url + post.permalink, output=output, destination=path + "/")
        except Exception as e:
          print(f"Error while downloading media from {subreddit_name}: {e}")
          continue

  with open(posts_json_path, "w") as f:
      json.dump(data, f, indent=2)

  end_time = datetime.datetime.now()
  time_elapsed = end_time - start_time
  print("Posts downloaded:")
  for subreddit_name, post_data in data.items():
      post_count = len(post_data)
      print(f"r/{subreddit_name}: {post_count}")

  print(f"Time elapsed: {time_elapsed}")


if __name__ == "__main__":
  download_posts()
