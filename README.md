# reddit Twitter Bot (UPDATED)

A Python bot that looks up new posts from a subreddit and automatically posts them on Twitter.

With an understanding of Python, and some brief understanding of [PRAW](https://praw.readthedocs.io/) and [tweepy](https://docs.tweepy.org/en/stable/client.html), you should be able to edit it with ease.

## Disclaimer

I hold no liability for what you do with this script or what happens to you by using this script. Abusing this script *can* get you banned from Twitter, so make sure to read up on proper usage of the Twitter API.

## Dependencies

You will need to install Python's [tweepy](https://github.com/tweepy/tweepy) and [PRAW](https://praw.readthedocs.org/en/) libraries first. I personally recommend using [poetry](https://python-poetry.org/docs/cli/) do manage this, but you can install them via `pip` if you please.

You will also need to create an app account on Twitter: [[instructions]](https://dev.twitter.com/apps)

1. Sign in with your Twitter account
2. Create a new app account
3. Modify the settings for that app account to allow read & write
4. Generate a new OAuth token with those permissions
5. Manually edit this script and put those tokens in the script
.
(note - by default your app will have Essential perms. With these perms, you must use the [client](https://docs.tweepy.org/en/stable/client.html) class within tweepy (TWITTER API V2 REFERENCE))

And a Reddit account:

1. Go to https://www.reddit.com/
2. Click `Sign Up` (top right on desktop) and fill out the necessary items.
3. Once logged in, you may wish to verify your email.
4. Go to the apps page https://old.reddit.com/prefs/apps/
5. Click `Create another app...` at the bottom. Fill out relevant details.
6. Your app `client_id` is located under the app name, e.g "-x1_KIHUOOJmk". The secret is below this as well.

## Usage

Once you edit the bot script to provide the necessary API keys and the subreddit you want to tweet from, you can run the bot on the command line:

    python reddit_twitter_bot.py
    
Or if you use poetry:
    `poetry run python reddit_twitter_bot.py`
 
Look into the script itself for configuration options of the bot.

## Have questions? Need help with the bot?

If you're having issues with or have questions about the bot, please [file an issue](https://github.com/rhiever/reddit-twitter-bot/issues) in this repository so one of the project managers can get back to you. Please check the existing (and closed) issues to make sure your issue hasn't already been addressed.
