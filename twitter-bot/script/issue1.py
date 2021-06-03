#!/usr/bin/env python3
import tweepy
import sys
import re
import config

def main():
    try:
        # setup twitter API
        auth = tweepy.OAuthHandler(config.api_key, config.api_secret)
        auth.set_access_token(config.access_token, config.token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        admin = api.me()
        print("\nWelcome to Twitter Bot CML!\n---------------------------\n")

        query = read_file('query.txt')
        for i in range(len(query)):
                
            pattern = r"https:\/\/twitter\.com\/(.+)\/status\/(\d*)"
            result = re.findall(pattern, query[i])

            user_id = result[0][0]
            tweet_id = result[0][1]
            print("Tweet author: {user_id}".format(user_id=user_id))
            api = tweepy.API(auth)

            tweet = api.get_status(tweet_id)

            if not tweet.favorited:
                tweet.favorite()
                print("-> favorite tweet")

            else:
                print("-> tweet already favorited")

            if not tweet.retweeted:
                tweet.retweet()
                print("-> retweet tweet")

            else:
                print("-> tweet already retweeted")

            # print(admin.screen_name)
            relationships =  api.lookup_friendships(screen_names=[user_id])

            for relationship in relationships:
                if not relationship.is_following:
                    api.create_friendship(user_id)
                    print("-> follow the tweet user")
                    print("\n")
                else:
                    print("-> already followed the tweet user")
            
            api.update_status(status="a comment", in_reply_to_status_id=tweet_id, auto_populate_reply_metadata=True) 
            print("-> reply to the author's tweet")

        print("Done! Existing...")

    except KeyboardInterrupt:
        print("\nAbort")
        sys.exit(0)
    
    except tweepy.error as e:
        print("\nError: {e}".format(e=e))

def read_file(filename):
    dict_ = {}
    id_ = 0
    pattern = r"^https:\/\/twitter\.com\/.+\/status\/\d*"
    with open(filename) as file:
        for line in file:
            if re.match(pattern, line):
               (key, val) = id_, line
               dict_[key] = val
               id_ += 1
        return dict_

if __name__ == '__main__':
    main()
