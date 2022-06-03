from RedDownloader import RedDownloader
import praw

# url = "https://www.reddit.com/r/PinayTikTok/comments/v35mqg/nikki_velayo/"
subreddit_name = input("Enter subreddit: ")
url = "https://www.reddit.com"

reddit = praw.Reddit(client_id="9OfqB_EB3QrW-kQzNx7TKw",
                     client_secret="GtVZkIfefw75-AnBiu5QKS3WCaer-A",
                     user_agent="funtimeahead")

hot_posts = reddit.subreddit(subreddit_name).new(limit=100)
for post in hot_posts:
  permalink = post.permalink
  print(url + permalink)
  title = post.title
  file = RedDownloader.Download(url + permalink, output = title , quality = 720, destination = "D:/Python-Project/" + subreddit_name)

