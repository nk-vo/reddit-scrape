import json
import os
import re
import time

import praw
from dotenv import load_dotenv
from RedDownloader import RedDownloader
from tabulate import tabulate

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
  url = "https://www.reddit.com"
  post_num = 10000  # Set the number of posts to download
  media_directory = os.getenv("MEDIA_DIRECTORY")
  # Path to JSON file that stores the downloaded posts for each subreddit
  source_directory = os.getenv("SOURCE_DIRECTORY")
  posts_json_path = os.path.join(source_directory, "posts.json")

  print("Loading posts from JSON...")
  data = {}
  if os.path.exists(posts_json_path):
    with open(posts_json_path) as f:
      data = json.load(f)
  else:
    with open(posts_json_path, "w") as f:
      json.dump(data, f, indent=2)
  
  print("Authenticating...")
  reddit = praw.Reddit(client_id=os.getenv("CLIENT_ID"),
                        client_secret=os.getenv("CLIENT_SECRET"),
                        user_agent=os.getenv("USER_AGENT"))

  print("Downloading posts...")
  subreddit_downloaded = {subreddit_name: {"count": 0, "download_time": 0} for subreddit_name in subreddit_list}
  for subreddit_name in subreddit_list:
    if subreddit_name not in data:
      data[subreddit_name] = []
    try:
        hot_posts = reddit.subreddit(subreddit_name).new(limit=int(post_num))
    except praw.exceptions.NotFound as e:
        print(f"Subreddit r/{subreddit_name} does not exist. Skipping...")
        continue
    
    download_start_time = time.time()
    
    print("Checking if posts have been downloaded from r/" + subreddit_name)
    
    # Create the media_directory if it does not exist
    path = os.path.join(media_directory, subreddit_name)
    if not os.path.exists(path):
        os.makedirs(path)
            
    for post in hot_posts:
      title = post.title
      created_utc = post.created_utc
      
      if not any(d['title'] == title and d['created_utc'] == int(created_utc) for d in data[subreddit_name]):
        data[subreddit_name].append({"title": title, "created_utc": int(created_utc)})
        title_cleaned = clean_filename(title)
        output = f"{title_cleaned}_{int(created_utc)}"
        path = os.path.join(media_directory, subreddit_name)
        print("Downloading from r/" + subreddit_name + ": " + title)
        if not os.path.exists(path):
          os.mkdir(path)
        try:
          RedDownloader.Download(url + post.permalink, output=output, destination=path + "/")
          subreddit_downloaded[subreddit_name]["count"] += 1
        except Exception as e:
          print(f"Error while downloading media from {subreddit_name}: {e}") 
          continue
        
      print("Saving posts to JSON...")
      with open(posts_json_path, "w") as f:
        try:
            json.dump(data, f, indent=2)
            print("Data successfully written to JSON.")
        except Exception as e:
            print("Error while saving data to JSON:", e)
        
    if subreddit_downloaded[subreddit_name]["count"] == 0:
      print("No new posts found from r/" + subreddit_name)
        
    download_end_time = time.time()
    subreddit_downloaded[subreddit_name]["download_time"] = download_end_time - download_start_time
  
    
  
  
  print("Done at " + time.strftime("%H:%M:%S"))
  
  total_count = sum(stats['count'] for stats in subreddit_downloaded.values())
  total_time = sum(stats['download_time'] for stats in subreddit_downloaded.values())
  
  print("Posts downloaded:")
  table_data = [["Subreddit", "Posts Downloaded", "Download Time (seconds)"]]
  for subreddit_name, stats in subreddit_downloaded.items():
      table_data.append([f"r/{subreddit_name}", f"{stats['count']}", f"{round(stats['download_time'] % 60, 2)}"])
      
  table_data.append(["Total", total_count, round(total_time, 2)])
  
  print(tabulate(table_data, headers="firstrow", tablefmt="rounded_grid"))

if __name__ == "__main__":
  download_posts()
