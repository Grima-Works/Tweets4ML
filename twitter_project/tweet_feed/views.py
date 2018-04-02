# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.utils.encoding import smart_str
import twitter
#from django.template import RequestContext

def get_tweets(count=10,rts=False):
	name_list=['ilyasut','trentmc0','karpathy', 'pabbeel', 'ch402', 'NandoDF']
	tweet_dict = {}

	api = twitter.Api(consumer_key='',
  consumer_secret='',
  access_token_key='',
  access_token_secret='')

	for i in name_list:
		tweet_dict[i] = api.GetUserTimeline(screen_name=i, exclude_replies=True, include_rts=rts, count=count)

	return tweet_dict, name_list

# Create your views here.
def index(request, **kwargs):
	tweet_dict, name_list = get_tweets(count=200,rts=True)
	return render(request, 'tweet_feed/home.html', {'tweets': tweet_dict, 'name_list': name_list})

def test(request, **kwargs):
	tweet_dict, name_list = get_tweets(100)
	return render(request, 'tweet_feed/test.html', {'tweets': tweet_dict, 'name_list': name_list})
