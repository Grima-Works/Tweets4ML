from __future__ import absolute_import
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment

import re
import os


def lens(lists):
	return len(lists)

def twitter_date(value):
    import datetime
    split_date = value.split()
    del split_date[0], split_date[-2]
    value = ' '.join(split_date)  # Fri Nov 07 17:57:59 +0000 2014 is the format
    return datetime.datetime.strptime(value, '%b %d %H:%M:%S %Y')

def urlize_tweet_text(tweet):
    """ Turn #hashtag and @username in status text to Twitter hyperlinks,
        similar to the ``urlize()`` function in Django.
    """
    try:
        from urllib import quote
    except ImportError:
        from urllib.parse import quote
    hashtag_url = '<a href="https://twitter.com/search?q=%%23%s" target="_blank">#%s</a>'
    user_url = '<a href="https://twitter.com/%s" target="_blank">@%s</a>'
    text = tweet.text
    for hash in tweet.hashtags:
        text = text.replace('#%s' % hash.text, hashtag_url % (quote(hash.text.encode("utf-8")), hash.text))
    for mention in tweet.user_mentions:
        text = text.replace('@%s' % mention.screen_name, user_url % (quote(mention.screen_name), mention.screen_name))
    return text

def expand_tweet_urls(tweet):
    """ Replace shortened URLs with long URLs in the twitter status
        Should be used before urlize_tweet
    """
    for url in tweet.urls:
        tweet.text = tweet.text.replace(
            url.url, '<a href="{}" target="_blank">{}</a>'.format(url.expanded_url, url.url)
        )
    return tweet

def environment(**options):
	env = Environment(**options)
	env.globals.update({'static': staticfiles_storage.url,'url': reverse,})
	env.globals['lens'] = lens
	env.globals['twitter_date'] = twitter_date
	env.globals['urlize_tweet_text'] = urlize_tweet_text
	env.globals['expand_tweet_urls'] = expand_tweet_urls
	return env