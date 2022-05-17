# -*- coding: utf-8 -*-

'''
Copyright 2015 Randal S. Olson

This file is part of the reddit Twitter Bot library.

The reddit Twitter Bot library is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

The reddit Twitter Bot library is distributed in the hope that it will be
useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
License for more details. You should have received a copy of the GNU General
Public License along with the reddit Twitter Bot library.
If not, see http://www.gnu.org/licenses/.
'''

import praw
import tweepy
import os
import sys
import time
import logging

# create the log file in the same directory as .py script
logger = logging.getLogger("tweepy")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="tweepy.log")
logger.addHandler(handler)

# path of text file that'll document posts that've already been tweeted
# create the file manually, can name it whatever you want
# place in same file as .py file
PATH = os.path.join(sys.path[0], "posted_cache.txt")
# Place the name of the file to store the IDs of posts that have been posted
POSTED_CACHE = 'posted_cache.txt'

# Place the string you want to add at the end of your tweets (can be empty)
# e.g a hashtag
TWEET_SUFFIX = ''

# Place the maximum length for a tweet
TWEET_MAX_LEN = 280

# Place the time you want to wait between each tweets (in seconds)
DELAY_BETWEEN_TWEETS = 30

# Place the lengths of t.co links (cf https://dev.twitter.com/overview/t.co)
T_CO_LINKS_LEN = 24


def setup_connection_reddit(subreddit):
    ''' Creates a connection to the reddit API. '''
    print('[bot] Setting up connection with reddit')
    # read-only reddit auth
    reddit_api = praw.Reddit(
                        user_agent='reddit Twitter tool monitoring ',
                        client_id=CLIENT_ID_GOES_HERE,
                        client_secret=CLIENT_SECRET_GOES_HERE)
    return reddit_api.subreddit(subreddit)


def tweet_creator(subreddit_info):
    ''' Looks up posts from reddit and shortens the URLs to them. '''
    post_dict = {}
    post_ids = []

    print('[bot] Getting posts from reddit')

    # "limit" tells the API the maximum number of posts to look up

    for submission in subreddit_info.new(limit=10):
        if not already_tweeted(submission.id):
            # This stores a link to the reddit post itself
            # If you want to link to what the post is linking to instead, use
            # "submission.url"   instead of "submission.permalink"
            # if you read through PRAW documentation, you should also find ways to filter out posts you don't want
            # e.g posts by specific authors
            # or whitelists posts  that match specific queries, etc
            
            # creates dict like {'submission_title': {}}
            post_dict[f'"{submission.title}"'] = {}
            
            post = post_dict[f'"{submission.title}"']
            # {'submission_title': {'link': 'the_url_of_the_post_here'}}
            post['link'] = f"https://reddit.com{submission.permalink}"

            # Store the url the post points to (if any)

            post_ids.append(submission.id)
        else:
            print('[bot] Already tweeted: {}'.format(str(submission)))

    return post_dict, post_ids


def already_tweeted(post_id):
    ''' Checks if the reddit Twitter bot has already tweeted a post. '''
    found = False
    with open(POSTED_CACHE, 'r') as in_file:
        for line in in_file:
            if post_id in line:
                found = True
                break
    return found


def strip_title(title, num_characters):
    ''' Shortens the title of the post to the 280 character limit. '''

    # How much you strip from the title depends on how much extra text
    # (URLs, hashtags, etc.) that you add to the tweet
    # Note: it is annoying but some short urls like "data.gov" will be
    # replaced by longer URLs by twitter. Long term solution could be to
    # use urllib.parse to detect those.
    if len(title) <= num_characters:
        return title
    else:
        return title[:num_characters - 1] + '…'


def tweeter(post_dict, post_ids):
    ''' Tweets all of the selected reddit posts. '''
    # twitter auth
    # strongly recommend storing these keys in a .env file or some such
    api = tweepy.Client(bearer_token=BEARER_TOKEN_HERE,
                        consumer_key=CONSUMER_KEY_HERE,
                        consumer_secret=CONSUMER_SECRET_HERE,
                        access_token=ACCESS_TOKEN_HERE,
                        access_token_secret=ACCESS_TOKEN_SECRET_HERE,
                        wait_on_rate_limit=True)

    for post, post_id in zip(post_dict, post_ids):

        # calculate the length of the tweet and strip the post title when necessary
        extra_text_len = 1 + T_CO_LINKS_LEN + len(TWEET_SUFFIX)
        
        # post_text is the actual contents of the tweet
        # here it posts the title of the reddit post (Stripped if needed), then the url on a new line, then any suffix' you added
        
        post_text = f"{strip_title(post, TWEET_MAX_LEN - extra_text_len)}\n{post_dict[post]['link']}\n{TWEET_SUFFIX}"

        print('[bot] Posting this link on Twitter')
        print(post_text)
        # tweeting
        api.create_tweet(text=post_text)
        log_tweet(post_id)
        # delaying to avoid hitting a rate limit
        time.sleep(DELAY_BETWEEN_TWEETS)

# appends reddit post ID to text file
def log_tweet(post_id):
    # opens file in append mode
    with open(PATH, 'a') as posted_cache:
        # writes the post id to text file then adds a new line
        posted_cache.write(str(post_id) + '\n')


def main():
    ''' Runs through the bot posting routine once. '''

    # run script continously 
    while True:
        def reddit_to_twitter():
            subreddit = setup_connection_reddit('ENTER_SUBREDDIT_NAME_HERE')
            post_dict, post_ids = tweet_creator(subreddit)
            tweeter(post_dict, post_ids)
        reddit_to_twitter()
        print("waiting 3600 seconds (1 hour)....")
        time.sleep(3600)


if __name__ == '__main__':
    main()
