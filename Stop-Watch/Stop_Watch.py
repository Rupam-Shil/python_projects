from tkinter import*
from PIL  import  ImageTk, Image


'''
Before running this program,download or install
---pip install pillow
---install Image
'''



state=False
#----Windows---
win=Tk()
win.title("StopWatch")
win.geometry("650x550")
win.resizable(False,False)
win.config(bg="#ffc299")
win.iconbitmap(r'Alarm.ico')


#---initialize---
second=0;min=0;hour=0


#---Exist---
def exit():
    win.destroy()


def update_time():
    if (state):
        global second,min,hour

        second+=1


        #---60second=1minute

        if (second>=60):
            min+=1
            second=0

        #---60minute=1hour

        if(min>=60):
            hour+=1
            min=0

        #---Update Current Time---

        la.configure(text='%ih:%im:%is'%(hour,min,second))

    #it acts similar to time.sleep (but in milliseconds instead of seconds)

    win.after(1000,update_time)


def start():
        global state
        state=True



def stop():
            global state
            state=False



def reset():

    global second,min,hour
    second=0
    min=0
    hour=0
    la.configure(text='%ih:%im:%is'%(hour,min,second))



#---Title---

tymer=Label(win,text="StopWatch",bg="#ffc299",fg="#6fdc6f",font=("Times new roman",30,"bold"))
tymer.place(x=230,y=10)



#---Image---
img=Image.open("C:\\Users\\saira\\Desktop\\Stop_Watch\\tomato.png") #---Image.open(filename) filename of the photo
img=img.resize((500,340))
io=ImageTk.PhotoImage(img)

#----Time----
la=Label(win,text='%ih:%im:%is'%(hour,min,second),image=io,bg="#ffc299",fg="white",compound="center",font=("Arial",35,""))
la.place(y=90,x=80)


#---Button----

b1=Button(win,text="Start",width=12,height=1,font=("Arial",13,""),bg="#fff0e6",command=start)
b1.place(x=50,y=420)

b2=Button(win,text="Reset",width=12,height=1,font=("Arial",13,""),bg="#fff0e6",command=reset)
b2.place(x=450,y=421)

b3=Button(win,text="Stop",width=12,height=1,font=("Arial",13,""),bg="#fff0e6",command=stop)
b3.place(x=172,y=480)

b4=Button(win,text="Exit",width=12,height=1,font=("Arial",13,""),bg="#fff0e6",command=exit)
b4.place(x=340,y=480)

#---update time--
update_time()

win.mainloop()