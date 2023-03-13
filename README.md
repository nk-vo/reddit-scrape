# README

This Python script downloads the media from the latest posts of the specified subreddits using the RedDownloader module and the PRAW API wrapper for Reddit. The downloaded media is stored in directories named after the subreddit, and the title of the post is used as the filename. If a post has already been downloaded, it is skipped.

The script also keeps track of the downloaded posts for each subreddit in a JSON file, so that previously downloaded media is not downloaded again.

## Requirements

Python 3
PRAW API wrapper for Reddit (praw module)
RedDownloader module (RedDownloader module)
dotenv module (python-dotenv module)

## Setup

Clone or download the script to a directory on your computer.
Install the required modules using pip.
Create a .env file in the same directory as the script with the following variables:
CLIENT_ID: Reddit API client ID
CLIENT_SECRET: Reddit API client secret
USER_AGENT: Reddit API user agent
SUBREDDIT_LIST: Comma-separated list of subreddits to scrape
MEDIA_DIRECTORY: Directory to save downloaded media
Run the script in a Python environment.

## Usage

To use the script, simply run it in a Python environment. The script will scrape the latest posts from the specified subreddits, download any new media, and store the downloaded media in the specified directory.

The downloaded media is saved in directories named after the subreddit, with the title of the post used as the filename. If a post has already been downloaded, it is skipped.

The script also keeps track of the downloaded posts for each subreddit in a JSON file, so that previously downloaded media is not downloaded again.

## Note

The Reddit API has a rate limit of 60 requests per minute. If you encounter any errors while using the script, try reducing the number of posts to download or adding a delay between requests.
