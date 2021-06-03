#!/usr/bin/env python3
import tkinter as tk
import tweepy
import re


try:
    import config

    auth = tweepy.OAuthHandler(config.api_key, config.api_secret)
    auth.set_access_token(config.access_token, config.token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

except ImportError:

    def make_config(api_key, api_secret, access_token, token_secret):
        with open("config.py", "w") as file:
            file.write('api_key="' + api_key+'"\n')
            file.write('api_secret="'+ api_secret+'"\n')
            file.write('access_token="' + access_token+'"\n')
            file.write('token_secret="' + token_secret+'"\n')

            auth = tweepy.OAuthHandler(api_key, api_secret)
            auth.set_access_token(access_token, token_secret)
            api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
            
            if api.verify_credentials():
            	print("Valid credentials: Please rerun the software!")
            	

            else:
            	os.remove("config.py")
            	print("Fatal: Invalid credentials. Aborting ...")
            	# print("Remove the invalid coinfig file")


            sys.exit(0)


    print("Fatal: Config file not found!")
    root = tk.Tk()
    root.geometry("450x250")
    root.resizable(width=False, height=False)
    root.configure(bg='white')

    root.title("Twitter API Configuration")
    text_logo = tk.Label(root, text="Welcome to Twitter API!",
                         bg="white", fg="seashell4", font="Times 20", pady=10)
    text_logo.pack(side=tk.TOP)

    img = tk.PhotoImage(file="../image/logo.png")
    img = img.zoom(25)
    img = img.subsample(51)
    logo = tk.Label(root, image=img, borderwidth=0, highlightthickness=0)
    logo.place(x=0, y=50)

    api_key_label = tk.Label(root, text="api_key", bg="lavender")
    api_key_label.place(x=120, y=70)
    api_key_entry = tk.Entry(root, width=25, bd=2, highlightcolor="SteelBlue3")
    api_key_entry.place(x=220, y=70)

    api_secret_label = tk.Label(root, text="api_secret", bg="lavender")
    api_secret_label.place(x=120, y=100)
    api_secret_entry = tk.Entry(root, width=25, bd=2, highlightcolor="SteelBlue3")
    api_secret_entry.place(x=220, y=100)

    access_token_label = tk.Label(
        root, text="access_token", bg="lavender")
    access_token_label.place(x=120, y=130)
    access_token_entry = tk.Entry(
        root, width=25, bd=2, highlightcolor="SteelBlue3")
    access_token_entry.place(x=220, y=130)

    token_secret_label = tk.Label(root, text="token_secret", bg="lavender")
    token_secret_label.place(x=120, y=160)
    token_secret_entry = tk.Entry(
        root, width=25, bd=2, highlightcolor="SteelBlue3")
    token_secret_entry.place(x=220, y=160)

    quit = tk.Button(root, text="Quit", width=6,
                     command=root.quit, relief=tk.SUNKEN)
    quit.place(x=30, y=206)

    start = tk.Button(root, text="Login", width=6,
                      relief=tk.SUNKEN, command=lambda: make_config(
                          api_key_entry.get(), api_secret_entry.get(), access_token_entry.get(), token_secret_entry.get()))
    start.place(x=170, y=206)

    author_label = tk.Label(root, bg ="white", fg="snow4", text="Copyright (c) 2021 Wai Han", borderwidth=0, highlightthickness=0, font="Times 10")
    author_label.place(x=280, y=220)

    root.mainloop()
    sys.exit(1)
        # , api_secret, access_token, token_secret


def process_data(username, number_of_tweets):
    pattern = r"^RT @(.*):"
    print("Username: " + username)
    print("No.of tweets: " + number_of_tweets + "\n")
    user = api.get_user(username)
    timeline = api.user_timeline(username, count=number_of_tweets)
    num = 1
    tweet_data = []
    for tweet in timeline:

        try:

            print("\n\nTweet: " + str(num))
            print("______________")
            print(tweet.text)
            print(tweet.user.screen_name)
            tweet_data.append(tweet.text)

            print("______________")
            num += 1

            if re.match(pattern, tweet.text) is not None:
                print("Original Author: "+re.match(pattern, tweet.text).group(1))
                if not tweet.favorited:
                    tweet.favorite()
                    print("Like tweet")

                else:
                    print("Post already liked")

                if not tweet.retweeted:
                    tweet.retweet()
                    print("Retweet")

                else:
                    print("Post already retweet")

            else:
                print('The post is not a "retweet" post')

        except tweepy.TweepError as e:
            print(e.reason)

        except StopIteration:
            break
    print(tweet_data)

    with open("tweet_data.txt", "a") as file:
        for tweet in tweet_data:
            file.write(tweet)
            file.write("\n\n")


def main():
    window = tk.Tk()
    window.geometry("450x250")
    window.resizable(width=False, height=False)
    window.configure(bg='white')

    window.title("Tweet Bot")

    text_logo = tk.Label(window, text="Twitter Bot!",bg="white",fg="DeepSkyBlue3",font="Arial 40 italic")
    text_logo.pack(side=tk.TOP)

    img = tk.PhotoImage(file = "../image/logo.png")
    img = img.zoom(25)
    img = img.subsample(51)
    logo = tk.Label(window, image=img, borderwidth=0, highlightthickness=0)
    logo.place(x=0, y=50)

    user_label = tk.Label(window, text="Username", bg="lavender")
    user_label.place(x=120, y = 70)
    user_entry = tk.Entry(window, bd = 2, highlightcolor="SteelBlue3")
    user_entry.place(x=250, y = 70)

    tweet_num_label = tk.Label(window, text = "No. of Tweets", bg="lavender")
    tweet_num_label.place(x=120, y=120)
    tweet_entry = tk.Entry(window, bd = 2, highlightcolor="SteelBlue3")
    tweet_entry.place(x=250, y = 120)

    quit = tk.Button(window, text="Quit", width=8,
                        command=window.quit, relief=tk.SUNKEN)
    quit.place(x=30, y = 170)

    start = tk.Button(window, text="Start", width=8,
                        relief=tk.SUNKEN, command=lambda: process_data(
                            user_entry.get(), tweet_entry.get()))
    start.place(x=330, y = 170)

    author_label = tk.Label(window, bg ="white", fg="snow4", text="Copyright (c) 2021 Wai Han", borderwidth=0, highlightthickness=0, font="Times 10")
    author_label.place(x=280, y=220)

    window.mainloop()


if __name__ == "__main__":
    main()
