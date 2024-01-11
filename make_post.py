import praw
import tweepy
from cfg_parse import parse_auth


def make_twitter_post(post_content):
    twitter_keys = parse_auth("TWITTER")
    auth = tweepy.OAuthHandler(twitter_keys["CONSUMER_KEY"], twitter_keys["CONSUMER_SECRET_KEY"])
    auth.set_access_token(twitter_keys["ACCESS_TOKEN"], twitter_keys["ACCESS_TOKEN_SECRET"])

    twt_api = tweepy.API(auth)
    twt_api.update_status(post_content)


def make_reddit_post(subreddit, post_title, post_content):
    reddit_keys = parse_auth("REDDIT")
    rdt_api = praw.Reddit(client_id=reddit_keys['CLIENT_ID'],
                          client_secret=reddit_keys['CLIENT_SECRET'],
                          user_agent=reddit_keys['USER_AGENT'],
                          redirect_uri=reddit_keys['REDIRECT_URI'],
                          refresh_token=reddit_keys['REFRESH_TOKEN'])

    rdt_sub = rdt_api.subreddit(subreddit)
    rdt_sub.submit(title=post_title, selftext=post_content)
