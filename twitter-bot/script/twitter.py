#!/usr/bin/env python3

import tweepy
import re
import os
import sys
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(name)s: %(message)s")

file_handler = logging.FileHandler("twitter.log")
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


class Twitter():
    def __init__(self, config, tweets_num, username, retweet_only, hashtag, status):
        self.status = status  # status for quote tweets
        self.hashtag = hashtag
        self.config = config
        self.like_counter = 0
        self.retweet_counter = 0
        self.q_tweet_counter = 0 
        self.retweet_only = retweet_only
        self.tweets_num = tweets_num.replace(' ', '')
        self.username = username.replace(' ', '')
        self.log = []
        
    def checkAuth(self):
        auth = tweepy.OAuthHandler(self.config.api_key, self.config.api_secret)
        auth.set_access_token(self.config.access_token,self.config.token_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True,
                         wait_on_rate_limit_notify=True)

        if self.api.verify_credentials():
            logger.info("Valid Credentials")
            return True
        else:
            logger.info("Invalid Credentials")
            sys.exit(1)

    def _is_retweet(self, tweet):
        pattern=r"^RT @(.*):"
        if re.match(pattern, tweet.full_text) is not None:
            return True
        else:
            return False


    def _check_hashtag(self, text):
        pattern = ".*" + self.hashtag + ".*"
        if self.hashtag == '':
            return True

        elif re.match(pattern, text.replace('\n', '').replace('\r', '')) is not None:
            return True
        
        else:
            self.log.append("? Hashtag not match")
            return False


    def _like_and_retweet(self, tweet):
        if not tweet.favorited:
            # tweet.favorite()
            self.like_counter += 1
            logger.info("like tweet")
        else:
            logger.info("already liked")

        if not tweet.retweeted:
            tweet.retweet()
            content = "* " +tweet.full_text[:48].replace('\n', ' ')
            content = content.replace('RT @', '')
            self.log.append(content)
            self.retweet_counter += 1
            logger.info("retweet")
        else:
            content = "# " +tweet.full_text[4:49].replace('\n', ' ')
            self.log.append(content)
            logger.info("retweeted post")


    def _quote_tweet(self, tweet):
        if not tweet.favorited:
            # tweet.favorite()
            self.like_counter += 1
            logger.info("like tweet")

            if tweet.is_quote_status:
                try:
                    self.url = "https://twitter.com/" + tweet.quoted_status.user.screen_name + "/status/" + tweet.quoted_status_id_str
                except:
                    self.url = "https://twitter.com/" + tweet.retweeted_status.quoted_status.user.screen_name + "/status/" + tweet.retweeted_status.quoted_status.id_str

            elif self._is_retweet(tweet):
                self.url = "https://twitter.com/" + tweet.retweeted_status.user.screen_name + "/status/" + tweet.retweeted_status.id_str

            else:
                self.url = "https://twitter.com/" + self.username + "/status/" + str(tweet.id)
            
            logger.info(self.url)
            quoted_tweet = self.status + "#WhatsHappeningInMyanmar \n" + self.url
            try:
                self.api.update_status(quoted_tweet)
                # print(tweet.quoted_status_id_str)
                content = "Q " +tweet.full_text[:48].replace('\n', ' ')
                # content = content.replace('RT @', '')
                self.log.append(content)
                self.q_tweet_counter += 1

            except tweepy.TweepError as e:
                self.log.append("! Duplicate")
                logger.warning(e.reason)
        else:
            self.log.append("! Duplicate")
            logger.warning("Duplicate")

    def like_and_retweet(self):
        try:
            self.user = self.api.get_user(self.username)
            if not re.match(r"^\d+$", self.tweets_num):
                self.log.append("Please Enter a valid number of tweets. [1-100]")
                logger.warning("Invalid number of tweets. [1-100]")
                return True
            
            self.timeline = self.api.user_timeline(self.username, count=self.tweets_num
                    ,tweet_mode="extended")
            self.sname = self.user.screen_name

            for tweet in self.timeline:
                if self.retweet_only:
                    if self._is_retweet(tweet) and self._check_hashtag(tweet.full_text):
                        self._like_and_retweet(tweet)

                else:
                    if self._check_hashtag(tweet.full_text):
                        self._like_and_retweet(tweet)

            logger.info("All good. Like {like} tweets; Retweet {retweet} tweets."
                    .format(like=self.like_counter, retweet=self.retweet_counter))

            self.log.append(">> Successfully Like {like} tweets; Retweet {retweet} tweets.\n"
                    .format(like=self.like_counter, retweet=self.retweet_counter))
        
        except tweepy.TweepError as e:
            self.log.append(e.reason)
            logger.warning(e.reason)


    def like_and_quote_tweet(self):
            try:
                # for tweet in tweepy.Cursor(api.search, q='github -filter:retweets',tweet_mode='extended').items(5):
                self.user = self.api.get_user(self.username)
                if not re.match(r"^\d+$", self.tweets_num):
                    self.log.append("Please Enter a valid number of tweets. [1-100]")
                    logger.warning("Invalid number of tweets. [1-100]")
                    return True
                
                self.timeline = self.api.user_timeline(self.username, count=self.tweets_num
                        ,tweet_mode="extended", include_rts=True)
                self.sname = self.user.screen_name

                for tweet in self.timeline:
                    if self._check_hashtag(tweet.full_text):
                        self._quote_tweet(tweet)

                logger.info("All good. Like {like} tweets; Q_Tweet {q_tweet} tweets."
                        .format(like=self.like_counter, q_tweet=self.q_tweet_counter))

                self.log.append(">> Successfully Like {like} tweets; Q_Tweet {q_tweet} tweets.\n"
                        .format(like=self.like_counter, q_tweet=self.q_tweet_counter))
            
            except tweepy.TweepError as e:
                self.log.append(e.reason)
                logger.warning(e.reason)


    def get_log(self):
    	return self.log


    def user_screen(self):
    	return self.sname
