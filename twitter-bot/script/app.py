#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
from twitter import Twitter
import sys
import os
import tweepy
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


def login(api_key, api_secret, access_token, token_secret):
  with open("config.py", "w") as file:
          file.write('api_key="' + api_key+'"\n')
          file.write('api_secret="'+ api_secret+'"\n')
          file.write('access_token="' + access_token+'"\n')
          file.write('token_secret="' + token_secret+'"\n')
          
          auth = tweepy.OAuthHandler(api_key, api_secret)
          auth.set_access_token(access_token, token_secret)
          api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
          try:
              if api.verify_credentials():
                logger.debug("API OK")
                sys.exit(0)
              else:
                logger.error("Bad Authentication Error")
                os.remove("config.py")
                
          except tweepy.TweepError as e:
              print(e)
              logger.error(e.reason)
              os.remove("config.py")        
              

class api_window():
  def __init__(self, master):
    self.master = master
    self.master.title("Twitter API Configuration")
    self.master.geometry("450x280")
    self.master.resizable(width=False, height=False)
    self.master.configure(bg="#252626")

    self.logo = tk.PhotoImage(file = "../image/settings.png")
    self.logo_label = tk.Label(self.master, image=self.logo, bg = "#252626")
    self.logo_label.pack(fill=tk.X, pady=(10, 10))

    self.pane1 = tk.Frame(self.master, bg="#252626")
    self.pane1.pack(fill=tk.X, side=tk.TOP, anchor=tk.NW, padx=(20, 0), pady=(0, 0))

    self.api_key_label = tk.Label(self.pane1, text = "api_key", fg = "#e8d4a0",
            bg="#252626", font = "Times 14 bold" )
    self.api_key_label.pack(side=tk.LEFT, padx=(10, 0))
    self.api_key_entry = tk.Entry(self.pane1, width=35, bd=2,
            highlightcolor="#1960bd", relief=tk.FLAT, fg="white", bg="#545454")
    self.api_key_entry.pack(side=tk.LEFT, padx=(75, 0))
    self.api_key_entry.focus_set()

    self.pane2 = tk.Frame(self.master, bg="#252626")
    self.pane2.pack(fill=tk.X, side=tk.TOP, anchor=tk.NW, padx=(20, 0), pady=(5, 0))

    self.api_s_label = tk.Label(self.pane2, text = "api_secret", fg = "#e8d4a0",
            bg="#252626", font = "Times 14 bold" )
    self.api_s_label.pack(side=tk.LEFT, padx=(10, 0))
    self.api_s_entry = tk.Entry(self.pane2, width=35, bd=2,
            highlightcolor="#1960bd", relief=tk.FLAT, fg="white", bg="#545454")
    self.api_s_entry.pack(side=tk.LEFT, padx=(58, 0))

    self.pane3 = tk.Frame(self.master, bg="#252626")
    self.pane3.pack(fill=tk.X, side=tk.TOP, anchor=tk.NW, padx=(20, 0), pady=(5, 0))

    self.access_token_label = tk.Label(self.pane3, text = "access_token", fg = "#e8d4a0",
            bg="#252626", font = "Times 14 bold" )
    self.access_token_label.pack(side=tk.LEFT, padx=(10, 0))
    self.access_token_entry = tk.Entry(self.pane3, width=35, bd=2,
            highlightcolor="#1960bd", relief=tk.FLAT, fg="white", bg="#545454")
    self.access_token_entry.pack(side=tk.LEFT, padx=(38, 0))

    self.pane4 = tk.Frame(self.master, bg="#252626")
    self.pane4.pack(fill=tk.X, side=tk.TOP, anchor=tk.NW, padx=(20, 0), pady=(5, 0))

    self.token_label = tk.Label(self.pane4, text = "token_secret", fg = "#e8d4a0",
            bg="#252626", font = "Times 14 bold" )
    self.token_label.pack(side=tk.LEFT, padx=(10, 0))
    self.token_label_entry = tk.Entry(self.pane4, width=35, bd=2,
            highlightcolor="#1960bd", relief=tk.FLAT, fg="white", bg="#545454")
    self.token_label_entry.pack(side=tk.LEFT, padx=(40, 0))


    self.exit_pane = tk.Frame(self.master, bg="#252626")
    self.exit_pane.pack(fill=tk.X, side=tk.TOP, anchor=tk.NW, padx=(20, 0), pady=(20, 0))

    self.exit_button = tk.Button(self.exit_pane, fg="white", bg="#3c71ab", text="Exit", command=self.master.destroy
      ,font="Times 11 bold")
    self.exit_button.pack(side=tk.LEFT, padx=(20, 0))

    self.login = tk.Button(self.exit_pane, fg="white", bg="#3c71ab", text="Login", font="Times 11 bold",
      command=lambda:login(self.api_key_entry.get(), 
                                 self.api_s_entry.get(), 
                                 self.access_token_entry.get(), 
                                 self.token_label_entry.get()))
    self.login.pack(side=tk.RIGHT, padx=(0, 20))   


class App():
  def __init__(self, master, logo, config):

    # Main Window
    self.master = master
    self.master.title("Twitter Bot")
    self.master.resizable(width=False, height=False)
    self.master.geometry("619x373")
    self.master.configure(bg="white")
    self.config = config

    # Images and Logos 
    self.power = tk.PhotoImage(file = "../image/start_icon.png")
    
    # Left Panel
    self.auth_frame = tk.Frame(self.master, width=250, height=400, bg="#252626")
    self.auth_frame.grid(row=0, column=0)

    # Right Panel
    self.display = tk.Frame(self.master, width=450, height=400, bg="#252626")
    self.display.grid(row=0, column=2)

    # Seprator Line
    ttk.Separator(self.master, orient=tk.VERTICAL).grid(column=1, row=0, rowspan=3, sticky='ns')

    # Text Logo
    self.text_logo = tk.Label(self.display,
                              text="Twitter Bot!",
                              bg="#252626", 
                              fg="DeepSkyBlue3",
                              font="Arial 40 italic")
    self.text_logo.grid(row=0, sticky=tk.NW, padx=10)


    # Status
    self.status_var = tk.StringVar()
    self.status_var.set("Status: Retweet Mode Ready")
    self.status = tk.Label(self.display, textvariable=self.status_var, fg="#ce8cf5",
    bg="#252626", font="Arial 12 bold", width=30, anchor=tk.NW)
    self.status.grid(row=1, sticky=tk.NW, padx=10)


    # Text Box
    self.text_box = tk.Text(self.display,
                            width=50,
                            height=10,
                            fg="white", 
                            bg="#545454", 
                            highlightcolor="#ce8cf5")
    self.text_box.grid(columnspan=4, row=2, padx=10, pady=10)


    # Radio(1)
    self.radio_var = tk.IntVar()
    self.radio_var.set(1)

    self.retweet_only = tk.Radiobutton(self.display,
                                       bg="#252626",
                                       borderwidth=0,
                                       highlightbackground="#252626", 
                                       activebackground="#8c8c8c",
                                       text="Retweet Except Quote Tweet", 
                                       fg="#ce8cf5", 
                                       variable=self.radio_var, 
                                       value=1,
                                       state=tk.NORMAL)
    self.retweet_only.grid(row=3, column=0, sticky=tk.W)


    # Radio(2)
    self.all = tk.Radiobutton(self.display,
                              bg="#252626", 
                              borderwidth=0, 
                              highlightbackground="#252626", 
                              activebackground="#8c8c8c",
                              text="Retweet Everything", 
                              fg="#ce8cf5", 
                              variable=self.radio_var, 
                              value=0, 
                              state=tk.NORMAL)
    self.all.grid(row=4, column=0, sticky=tk.W)


    # Quit Button
    self.quit_b = tk.Button(self.display,
                            width=7, 
                            bg="#ce8cf5",
                            fg="white", 
                            text="Quit",
                            command=self.master.destroy)
    self.quit_b.grid(row=5, column=0, padx=13, pady=15, sticky=tk.W)


    # Logo Picture
    self.logo = tk.Label(self.auth_frame, 
                         image=logo, 
                         borderwidth=0,
                         highlightthickness=0, 
                         bg="#252626")
    self.logo.grid(row=0, column=0, ipadx=40, ipady=10)

    self.user_frame = tk.Frame(self.auth_frame, bg="#252626")
    self.user_frame.grid(row=1, column=0)


    # Username
    tk.Label(self.user_frame,
            text="Username: ", 
            bg="#252626", 
            fg="#ce8cf5").pack(padx=10, pady=2)
    self.user_entry = tk.Entry(self.user_frame, fg="white", bg="#545454", highlightcolor="#ce8cf5")
    self.user_entry.pack()
    self.user_entry.focus_set()


    # Tweets Entry
    tk.Label(self.user_frame,
             text="Tweets No.: ",
              bg="#252626", 
              fg="#ce8cf5").pack(padx=10, pady=2)
    self.tweets_entry = tk.Entry(self.user_frame, fg="white", bg="#545454", highlightcolor="#ce8cf5")
    self.tweets_entry.pack()


    # Hashtag
    tk.Label(self.user_frame, 
             text="Filter Hashtag: ", 
             bg="#252626", 
             fg="#ce8cf5").pack(padx=10, pady=5)
    self.hashtag_entry = tk.Entry(self.user_frame, fg="white", bg="#545454", highlightcolor="#ce8cf5")
    self.hashtag_entry.pack(pady=2)


    # Mode CheckBox
    self.checkbox_value = tk.IntVar()
    self.checkbox_value.set(0)

    self.checkbox= tk.Checkbutton(self.user_frame, 
                   text="Quote Tweet Mode", 
                   variable=self.checkbox_value,
                   onvalue=1, offvalue=0, 
                   bg="#252626", 
                   fg="#ce8cf5", 
                   highlightbackground="#252626", 
                   activebackground="#8c8c8c",
                   command=self.SelectMode 
                   )
    self.checkbox.pack(pady=7)


    # Retweet Quote TextBox
    self.status = tk.Text(self.user_frame,width=20, height=3, bg="#545454", highlightcolor="#ce8cf5", fg="white")
    self.status.pack(ipady=2)

    # Start Button
    self.start_var = tk.StringVar()
    self.start_var.set('Start')
    self.start_b = tk.Button(self.display,
                            width=50, 
                            bg="#ce8cf5",
                            fg="white",
                            image=self.power,
                            compound=tk.LEFT,
                            textvariable=self.start_var,
                            command=self.StartCommand,
                            state=tk.NORMAL)

    self.start_b.grid(row=5, column=3, padx=0, pady=15)

        ###### END OF SELF ATTRIBUTES #######


  def SelectMode(self):
     if self.checkbox_value.get() == 1:
       self.retweet_only.config(state=tk.DISABLED) 
       self.all.config(state=tk.DISABLED)
       self.status_var.set("Status: Quote Tweet Mode")
     else:
       self.retweet_only.configure(state=tk.NORMAL)
       self.all.config(state=tk.NORMAL)
       self.status_var.set("Status: Retweet Mode")


  def StartCommand(self):
    twitter = Twitter(self.config, self.tweets_entry.get(), self.user_entry.get()
        , self.radio_var.get(), self.hashtag_entry.get(), self.status.get(1.0, tk.END))
    self.text_box.delete('1.0', tk.END)
    self.text_box.insert(tk.END, "Checking {num} tweets from user {name}.\n\n".
      format(num=self.tweets_entry.get().replace(' ', ''), name=self.user_entry.get()))
    self.text_box.tag_configure('left', justify='left')
    self.text_box.tag_add('left', 1.0, 'end')

    self.start_var.set("Loading")
    self.start_b.config(state='disabled', bg="#707070", fg="#D3D3D3")
    self.start_b.update()

    self.status_var.set("Status: Authenticating User")
    self.status.update()

    if twitter.checkAuth():
        self.status_var.set("Status: Quote Tweet in process")
        self.status.update()
        if self.checkbox_value.get() == 1:
            self.status_var.set("Status: Quote Tweet in process")
            self.status.update()
            twitter.like_and_quote_tweet()
            content = twitter.get_log()
        else:     
            self.status_var.set("Status: Retweet in process")
            self.status.update()
            twitter.like_and_retweet()
            content=twitter.get_log()

    self.start_var.set("Start")
    self.start_b.config(state='normal', bg="#ce8cf5", fg='white')

    if self.checkbox_value.get() == 1:
      self.status_var.set("Status: Quote Tweet Mode Ready")
    else:
      self.status_var.set("Status: Retweet Mode Ready")
    for i in range(len(content)):
      try:
        self.text_box.insert(tk.END, content[i] + "\n")
        self.text_box.tag_configure('left', justify='left')
        self.text_box.tag_add('left', 1.0, 'end')
      except:
        self.text_box.insert(tk.END, "!!! Doesn't support emoji yet, but retweeted" + "\n")
        self.text_box.tag_configure('left', justify='left')
        self.text_box.tag_add('left', 1.0, 'end')


def main():
  root = tk.Tk()
  root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='../image/tweet.png'))

  # load twitter dock logo
  logo = tk.PhotoImage(file = "../image/logo.png")
  logo = logo.zoom(25)
  logo = logo.subsample(51)

  try:
    import config
    window = App(root, logo, config)

  except ImportError:
    logger.warning("API not found. Open api window")
    window = api_window(root)

  root.mainloop() 
  
if __name__ == "__main__":
  main()
