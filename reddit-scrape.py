from RedDownloader import RedDownloader
import praw

directory = "D:/Reddit-Scrape/"
# Path
path = os.path.join(directory, subreddit_name)
isDirExist = os.path.exists(path)

if isDirExist == False:
  os.mkdir(path)
  
subreddit_name = input("Enter subreddit: ")
url = "https://www.reddit.com"

#get those parameters from reddit developer account
reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT)

hot_posts = reddit.subreddit(subreddit_name).new(limit=100)
for post in hot_posts:
  permalink = post.permalink
  title = post.title
  file = RedDownloader.Download(url + permalink, output = title , quality = 720, destination = path + "/")

