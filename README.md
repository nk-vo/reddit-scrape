# README

This Python script downloads the media from the latest posts of the specified subreddits using the RedDownloader module and the PRAW API wrapper for Reddit. The downloaded media is stored in directories named after the subreddit, and the title of the post is used as the filename. If a post has already been downloaded, it is skipped.

The script also keeps track of the downloaded posts for each subreddit in a JSON file, so that previously downloaded media is not downloaded again.

## Requirements

* Python 3
* PRAW API wrapper for Reddit (praw module)
* RedDownloader module (RedDownloader module)
* dotenv module (python-dotenv module)

## Setup

1. Clone or download the script to a directory on your computer.
2. Install the required modules using `pip`.
3. Create a Reddit account if you don't have one already.
4. Create an application here.
5. Create a `.env` file in the same directory as the script with the following variables:
    * `CLIENT_ID`: Reddit API client ID
    * `CLIENT_SECRET`: Reddit API client secret
    * `USER_AGENT`: Reddit API user agent
    * `SUBREDDIT_LIST`: Comma-separated list of subreddits to scrape
    * `MEDIA_DIRECTORY`: Directory to save downloaded media
    * `SOURCE_DIRECTORY`: The path to the directory where the JSON file storing the downloaded posts for each subreddit will be saved.
6. Run the script using `python download_posts.py`.

## Usage

To use the script, simply run it in a Python environment. The script will scrape the latest posts from the specified subreddits, download any new media, and store the downloaded media in the specified directory.

The downloaded media is saved in directories named after the subreddit, with the title of the post used as the filename. If a post has already been downloaded, it is skipped.

The script also keeps track of the downloaded posts for each subreddit in a JSON file, so that previously downloaded media is not downloaded again.

## Note

By default, the script downloads the 1000 latest posts from each subreddit. You can change this by modifying the post_num variable in the script.

The clean_filename function removes invalid characters and trims the filename before saving the downloaded media. If you want to modify this function, you can do so in the script.

The script uses the RedDownloader package to download media from Reddit. If you want to modify how media is downloaded (e.g., to download videos in a different format), you can do so in the script.

## Contributing

* Pull requests and bug reports are welcome!
* Please see the [contributing guidelines](CONTRIBUTING.md) for more information.

## License

* This project is licensed under the MIT License.
* See the [LICENSE](LICENSE) file for more information.
