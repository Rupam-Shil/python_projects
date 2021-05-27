from tkinter import*
from tkinter import colorchooser
from PIL import ImageTk,Image
import speech_recognition as sp
from time import ctime
import webbrowser
import playsound
import os
import random
from gtts import gTTS
import time
import requests
import bs4
from tkinter import messagebox



#---Main Windows---
win=Tk()
win.geometry('400x590+400+15')
win.title("Pikachu VoiceBot")
win.resizable(False,False)
win.iconbitmap(r'chabot.ico')
win.config(bg="#ececec")

'''
Before running this program,download or install:

pip install pillow
pip install SpeechRecognition
pip install pipwin
pipwin install pyaudio
pip install gTTS
pip install requests
pip install bs4
pip install playsound

'''


'''
This program requires internet connection.
'''


#---Question---
tar1=['who made you', 'who created you']
tar2=['I was created by Pikachu.', 'Pikachu a cartoon']
question=['what is your name', 'who are you']
greetings = ['hey there', 'hello', 'hi', 'hai', 'hey']
how=['how are you', 'how are you doing']
tme=['what time is it now','time','tell me about time','current time','what is the time']
srch=['search','search in Google']
loc=['find location','location','open Google Map']
wikip=['Wikipedia','open Wikipidea','search on Wikipedia']
wther = ['tell me the weather', 'weather', 'what about the weather','the weather']
cov=['covid-19','covid','covid statistics','covid status']
tymr=['set time','set a time','timer','open timer']
to_do=['add item','add an item','add list']
ex = ['exit', 'close', 'close the program']




#--Enter Voice-Bot
def chat_enter():

    #---To recognize input from the microphone,use a recognizer class
    r = sp.Recognizer()

    #---Speech to Text
    def record_audio(ask=False):

        #---Set microphone to accept sound & PyAudio is required
        with sp.Microphone() as source:

            if ask:

                pikachu_speak(ask)


            #---record the source and save it into audio
            audio = r.record(source,duration=3)
            text = ''

            try:
                #---Audio into text
                text = r.recognize_google(audio)

            except sp.UnknownValueError:

                pikachu_speak("Sorry I did not get that")


            except sp.RequestError:

                pikachu_speak("Sorry, my speech service is down")
        #---Return The text file
        return text

    #---Text to Speech
    def pikachu_speak(audio_string):

        #---gTTS (Google Text-to-Speech)
        #---Convert the string into voice
        adio=gTTS(text=audio_string,lang='en')
        #---Returns a random integer number & randint() method
        ran=random.randint(1,10000000)
        #---Audio file name
        audio_file='audio-'+str(ran)+'.mp3'
        #---The voice save in the audio_file
        adio.save(audio_file)
        #---Play the audio file
        playsound.playsound(audio_file)
        #---Remove the audio file
        os.remove(audio_file)


    def respond(voice_or_text_data):

        print(voice_or_text_data)

        if voice_or_text_data in tar1:

            r_answer=random.choice(tar2)
            l1.config(text=r_answer)
            pikachu_speak(r_answer)

        elif  voice_or_text_data in question :

            l1.config(text="My name is pikachu.\nI am a bot.I work for you")
            pikachu_speak("My name is pikachu. I am a bot. I work for you")

        elif voice_or_text_data in greetings:

            r_choice=random.choice(greetings)
            pikachu_speak(r_choice)
            l1.config(text=r_choice)

        elif voice_or_text_data in how:

            pikachu_speak("I am fine.Nice to talk with you")
            l1.config(text="I am fine.\nNice to talk with you")

        elif voice_or_text_data in tme:

            pikachu_speak("Current Local Time:")
            pikachu_speak(ctime())
            l1.config(text="Current Local Time:\n" + ctime())


        elif voice_or_text_data in srch:

            search = record_audio("what do you want to search for?")
            url = 'https://google.com/search?q=' + search
            #---The webbrowser module open() method will open default web browser with a given url
            webbrowser.get().open(url)
            pikachu_speak("here is search" + search)
            l1.config(text="Here is search:\n" + search)


        elif voice_or_text_data in loc:

            location = record_audio("Say the name of the location?")
            url = 'https://google.nl/maps/place/' + location + '/&amp;'
            webbrowser.get().open(url)
            pikachu_speak("The location map: "+location)
            l1.config(text="The location map:\n"+location)

        elif voice_or_text_data in wikip:

            wiki=record_audio("what do you want to search in wikipedia?")
            url = 'https://en.wikipedia.org/wiki/=' + wiki
            webbrowser.get().open(url)
            l1.config(text="Here is wikipedia:\n" + wiki)
            pikachu_speak("Here is wikipedia " + wiki)



        elif  voice_or_text_data in wther:

            location=record_audio("Say the name of the city:")
            link = "https://api.openweathermap.org/data/2.5/weather?q=" + location + "&appid=c4c80c6387c03dde649323ba4e878114"
            #--- get() method sends a GET request to the specified url.
            api_link = requests.get(link)
            api_data = api_link.json()



            if api_data['cod']=='404':

                pikachu_speak("Incorrect location name.Please check the location")
                l1.config(text="Incorrect location name.\nPlease check the location.")
            else:

                #---Store data
                #---Kelvin to celsius
                city = ((api_data['main']['temp']) - 273.15)
                weather = api_data['weather'][0]['description']
                humadity = api_data['main']['humidity']
                wind_speed = api_data['wind']['speed']

                temp=float("{:.2f}".format(city))

                l1.config(text="Location Name: "+location+"\nCurrent temperature is: "+str(temp)+" degree Celsius\nWeather forecast : " + weather+"\nHumidity : " +str( humadity)+" %\nWind speed : " + str(wind_speed) + "km/h",font=('calibri',12,''))

                pikachu_speak("Current temperature is: "+str(temp)+" degree Celsius")
                pikachu_speak("Weather forecast: " + weather)
                pikachu_speak("Humidity: " +str( humadity)+" percentage")
                pikachu_speak("Wind speed: " + str(wind_speed) + 'kilometre per hour')

        elif voice_or_text_data in cov:

            country=record_audio("Which country?")
            url = "https://worldometers.info/coronavirus/country/"+country+"/"
            html_data = requests.get(url)
            web_scrap = bs4.BeautifulSoup(html_data.text,'html.parser')
            all_info = ""

            try:
                info = web_scrap.find("div",class_="content-inner").findAll("div",id="maincounter-wrap")

                for block in info:
                    h1 = block.find("h1",class_=None).get_text()
                    span = block.find("span",class_=None).get_text()
                    all_info = all_info + h1 + " " + span + "\n"
                pikachu_speak("Country name: "+country+"\n"+all_info)
                l1.config(text="Country name: "+country+"\n"+all_info)

            except:

                pikachu_speak("Country name is not found.")
                l1.config(text="Country name is not found.")

        elif  voice_or_text_data in tymr:

            pikachu_speak("Here is Time counter. Set a time")
            l1.config(text="Here is Time counter. Set a time")

            #---Time Counter
            win1 = Toplevel(win)
            win1.title("Time Counter")
            win1.geometry("340x220+430+200")
            win1.resizable(False,False)
            win1.config(bg="#DAA520")

            def tim():
                try:
                    total_sec = int(hour.get())*3600+int(minute.get())*60+int(second.get())
                except:
                    messagebox.showerror("Error","Input the correct value")

                while total_sec >= 0:
                    hours = 0
                    # mins=total_sec/60; secs=total_sec%60
                    mins,secs = divmod(total_sec,60)

                    if mins > 60:
                        # hours=total_sec/60 ;mins=total_sec%60
                        hours,mins = divmod(total_sec,60)

                    hour.set("{0:2d}".format(hours))
                    minute.set("{0:2d}".format(mins))
                    second.set("{0:2d}".format(secs))

                    win1.update()
                    time.sleep(1)

                    if (total_sec == 0):
                        win2 = Toplevel(win)
                        win2.title("Time Counter")
                        win2.geometry("340x150+430+200")
                        win2.resizable(False,False)
                        win2.config(bg="#DAA520")

                        def win_destroy():
                            win2.destroy()
                            win1.destroy()

                        la1 = Label(win2,text="Time's up",font=('calibri',30,'bold'),fg="#fe1a0e",bg="#DAA520")
                        la1.place(x=90,y=8)

                        but = Button(win2,text="OK",height=1,width=8,font=('veranda',10,''),command=win_destroy,
                                     bg="#F5DEB3")
                        but.place(x=130,y=90)

                        win2.mainloop()

                    total_sec = total_sec - 1

            hour = StringVar()
            minute = StringVar()
            second = StringVar()

            hour.set("00")
            minute.set("00")
            second.set("00")

            h1 = Entry(win1,width=3,font=('Arial',30,''),textvariable=hour)
            h1.place(x=50,y=30)

            m1 = Entry(win1,width=3,font=('Arial',30,''),textvariable=minute)
            m1.place(x=140,y=30)

            s1 = Entry(win1,width=3,font=('Arial',30,''),textvariable=second)
            s1.place(x=230,y=30)

            buto = Button(win1,text="Set Time",height=1,width=8,font=('verandra',10,''),bg="#008080",bd=5,fg="white",
                          command=tim)
            buto.place(x=130,y=130)

            win1.mainloop()

        elif voice_or_text_data in to_do:

            li=record_audio("What do you want to add in list?")
            pikachu_speak("Added. Here is List")
            l1.config(text="Added. Here is List")

            win1 = Toplevel(win)
            win1.title("To-Do-List")
            win1.geometry("340x220+430+200")
            win1.resizable(False,False)

            def delete():
                selected_item = work.get(ACTIVE)
                work.delete(ACTIVE)

                if os.path.exists("To-Do-List.txt"):
                    os.remove("To-Do-List.txt")

                fil = 'To-Do-List.txt'
                fi = open(fil,'a')
                cnt = 0

                for i in list1:
                    if i == selected_item and cnt == 0:
                        cnt = 1
                    else:
                        fi.write(i)

                fi.close()

            selected_item = ""
            list1 = []

            scroll = Scrollbar(win1)
            scroll.place(x=323,y=0,height=218)

            work = Listbox(win1,yscrollcommand=scroll.set,bg="#DAA520")
            work.place(x=0,y=0,height=220,width=320)

            scroll.config(command=work.yview)

            de = Button(work,text="Delete",bg="#F5DEB3",command=delete)
            de.place(x=140,y=190)

            #--Add item in list & file
            file = 'To-Do-List.txt'
            file1 = open(file,'a')
            file1.write(li+ "\n")
            file1.close()

            f = open(file,"r")
            for i in f:
                work.insert(END,i)
                list1.append(i)

            f.close()

            win1.mainloop()

        elif voice_or_text_data in ex:

            pikachu_speak("Good Bye")
            win.destroy()

        else:

            pikachu_speak("I am a pikachu chatbot")
            l1.config(text="I am a pikachu chatbot.")


    def ri():

        #---Take input from microphone
        voice_data = record_audio()
        #---Respond to the voice
        respond(voice_data)



    global cl
    global var
    color = "";bg_clr1="";mode = "";fg_clr1="";bg_clr2="";fg_clr2="";ac1=""
    select_value = var.get()

    if select_value == 1:
        color = "#262626";mode = "#808080";bg_clr1="#262626";fg_clr1="#C0C0C0";bg_clr2="#696969";fg_clr2="white";ac1="#d1d0c6"
    if select_value == 2:
        color = "#ececec";mode = "#C0C0C0";bg_clr1="#2E8B57";fg_clr1="#F8F8FF";bg_clr2="#625f3e";fg_clr2="white";ac1="#A3A18E"

    cnt = 0
    clp = ""
    try:
        for i in cl:
            cnt = cnt + 1
            if cnt == 2:
                clp = i
    except:
        print(" ")

    if clp != None and clp != "":
        color = clp

    frmi=Frame(bg=color)
    frmi.place(x=0,y=0,height=590,width=400)

    frm1=Frame(frmi,bg=color)
    frm1.place(x=0,y=0,height=500,width=400)

    frm2=Frame(frmi,bg=mode)
    frm2.place(x=0,y=500,height=90,width=400)

    if select_value==1:

        im=Image.open("setting.png")
        n=im.resize((48,48))
        img=ImageTk.PhotoImage(n)
        bu=Button(frm2,command=dark,relief=FLAT,image=img)
        bu.image=img
        bu.place(x=360,y=28,height=30,width=30)

        im2 = Image.open("gramophone-record.png")
        n2 = im2.resize((60,60))
        img2 = ImageTk.PhotoImage(n2)
        bu2 = Button(frm2,relief=RAISED,image=img2,command=ri,activebackground="#da3e3e",bg="#D3D3D3")
        bu2.image = img2
        bu2.place(x=70,y=20,height=50,width=250)

    elif select_value==2:

        im=Image.open("green-settings.png")
        n=im.resize((40,40))
        img=ImageTk.PhotoImage(n)
        bu = Button(frm2,relief=FLAT,command=light,image=img)
        bu.image=img
        bu.place(x=360,y=28,height=30,width=30)

        im2 = Image.open("record.png")
        n2 = im2.resize((55,55))
        img2 = ImageTk.PhotoImage(n2)
        bu2 = Button(frm2,relief=RAISED,image=img2,command=ri,activebackground="#F5DEB3",bg="#DAA520")
        bu2.image = img2
        bu2.place(x=70,y=20,height=50,width=250)

    i=Image.open("ot.png")
    po=i.resize((300,300))
    image = ImageTk.PhotoImage(po)
    p = Label(frm1,image=image,bg=color)
    p.image = image
    p.place(x=50,y=10)

    l1 = Label(frm1,text="Result",bg="#FA8072",font=('calibri',15,''))
    l1.place(x=50,y=340,height=130,width=300)


#---Color Palette
def color():
    global cl
    cl = colorchooser.askcolor()


#---Change into Light Mode
def light():

    fr1=Frame(win,bg="#ececec")
    fr1.place(x=0,y=0,width=400,height=590)

    #---Image Add
    image = ImageTk.PhotoImage(Image.open("chatbot-1.png"))
    p = Label(fr1,image=image)
    p.image=image
    p.place(x=-215,y=0)

    #---Welcome to pikachu chatbot
    la1 = Label(fr1,text="Welcome to Pikachu",font=('veranda',25,''),bg="#ececec")
    la1.place(x=50,y=310)

    la2 = Label(fr1,text="VoiceBot",font=('veranda',25,''),bg="#ececec")
    la2.place(x=130,y=360)

    #---Theme & Chat background
    la3 = Label(fr1,text="Theme",font=('calibri',11,''),bg="#ececec")
    la3.place(x=50,y=450)

    global var
    var = IntVar()
    var.set("2")
    r1 = Radiobutton(fr1,text="Dark",variable=var,value=1,bg="#ececec",command=dark)
    r1.place(x=190,y=450)
    r2 = Radiobutton(fr1,text="Light",variable=var,value=2,bg="#ececec",command=light)
    r2.place(x=290,y=450)


    la4 = Label(fr1,text="Background",font=('calibri',11,''),bg="#ececec")
    la4.place(x=50,y=490)
    but1 = Button(fr1,text="Pick Color",width=20,font=('calibri',10,''),bg="#878f84",fg="white",command=color)
    but1.place(x=190,y=490)

    #---Enter to the chat
    but2 = Button(fr1,text="Enter",width=10,font=('calibri',11,''),bg="#2E8B57",fg="white",command=chat_enter)
    but2.place(x=160,y=540)


#---Change into Dark Mode
def dark():
    
    fr1 = Frame(win,bg="#262626")
    fr1.place(x=0,y=0,width=400,height=590)

    #---Image Add
    image = ImageTk.PhotoImage(Image.open("chatbot-2.jpg"))
    p = Label(fr1,image=image)
    p.image = image
    p.place(x=-215,y=0)

    #---Welcome to pikachu chatbot
    la1 = Label(fr1,text="Welcome to Pikachu",font=('veranda',25,''),bg="#262626",fg="#F5F5F5")
    la1.place(x=50,y=310)

    la2 = Label(fr1,text="VoiceBot",font=('veranda',25,''),bg="#262626",fg="#F5F5F5")
    la2.place(x=130,y=360)

    #---Theme & Chat background
    la3 = Label(fr1,text="Theme",font=('calibri',11,''),bg="#262626",fg="#F5F5F5")
    la3.place(x=50,y=450)

    global var
    var = IntVar()
    var.set("1")
    r1 = Radiobutton(fr1,text="Dark",variable=var,value=1,bg="#262626",fg="#F5F5F5",command=dark)
    r1.place(x=190,y=450)
    r2 = Radiobutton(fr1,text="Light",variable=var,value=2,bg="#262626",fg="#F5F5F5",command=light)
    r2.place(x=290,y=450)

    la4 = Label(fr1,text="Background",font=('calibri',11,''),bg="#262626",fg="#F5F5F5")
    la4.place(x=50,y=490)
    but1 = Button(fr1,text="Pick Color",width=20,font=('calibri',10,''),bg="#878f84",fg="white",command=color)
    but1.place(x=190,y=490)

    #---Enter to the chat
    but2 = Button(fr1,text="Enter",width=10,font=('calibri',11,''),bg="#2E8B57",fg="white",command=chat_enter)
    but2.place(x=160,y=540)


light()
win.mainloop()
