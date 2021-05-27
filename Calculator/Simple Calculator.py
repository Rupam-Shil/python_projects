from tkinter import*



win=Tk()
win.geometry("315x418")
win.resizable(False,False)
win.title("Calculator")
op=""

def button_click(number):

    global op
    op=op+str(number)
    e.delete(0,END)
    e.insert(0,op)

def clear():
    global op
    op=""
    e.delete(0,END)

def button_equal():
    global op
    result=str(eval(op))
    e.delete(0,END)
    e.insert(0,result)
    op=result


#----Entry----
s=StringVar()
e=Entry(win,textvariable=s,bd=15,relief=RIDGE,font=("Arial",15,"bold"),bg="#5F9EA0",justify='right')
e.place(width=315,height=60,y=10)


frame=Frame(win,height=350,width=332,bg="#5F9EA0",bd=5,relief=RAISED)
frame.place(y=70)

#----Numbers------
n1=Button(frame,text="0",bd=5,relief=RAISED,height=2,width=5,command=lambda:button_click("0"),font=("Arial",14,"bold"),bg="#CD5C5C",activebackground="#e7b1b1")
n1.grid(row=0,column=0)

n2=Button(frame,text="+",bd=5,relief=RAISED,height=2,width=5,command=lambda:button_click("+"),font=("Arial",14,"bold"),bg="#CD5C5C",activebackground="#e7b1b1")
n2.grid(row=0,column=1)

n3=Button(frame,text="%",bd=5,relief=RAISED,height=2,width=5,command=lambda:button_click("%"),font=("Arial",14,"bold"),bg="#CD5C5C",activebackground="#e7b1b1")
n3.grid(row=0,column=2)

n4=Button(frame,text="=",bd=5,relief=RAISED,height=2,width=5,command=button_equal,font=("Arial",14,"bold"),bg="#CD5C5C",activebackground="#e7b1b1")
n4.grid(row=0,column=3)



n5=Button(frame,text="7",bd=5,relief=RAISED,height=2,width=5,command=lambda:button_click(7),font=("Arial",14,"bold"),bg="#5F9EA0",activebackground="#9fc4c6")
n5.grid(row=1,column=0)

n6=Button(frame,text="8",bd=5,relief=RAISED,height=2,width=5,command=lambda:button_click(8),font=("Arial",14,"bold"),bg="#5F9EA0",activebackground="#9fc4c6")
n6.grid(row=1,column=1)

n7=Button(frame,text="9",bd=5,relief=RAISED,height=2,width=5,command=lambda:button_click(9),font=("Arial",14,"bold"),bg="#5F9EA0",activebackground="#9fc4c6")
n7.grid(row=1,column=2)

n8=Button(frame,text="X",bd=5,relief=RAISED,height=2,width=5,command=lambda:button_click("*"),font=("Arial",14,"bold"),bg="#CD5C5C",activebackground="#e7b1b1")
n8.grid(row=1,column=3)

n9=Button(frame,text="4",bd=5,relief=RAISED,height=2,width=5,command=lambda:button_click(4),font=("Arial",14,"bold"),bg="#5F9EA0",activebackground="#9fc4c6")
n9.grid(row=2,column=0)

n10=Button(frame,text="5",bd=5,relief=RAISED,height=2,width=5,command=lambda:button_click(5),font=("Arial",14,"bold"),bg="#5F9EA0",activebackground="#9fc4c6")
n10.grid(row=2,column=1)

n11=Button(frame,text="6",bd=5,relief=RAISED,height=2,width=5,command=lambda:button_click(6),font=("Arial",14,"bold"),bg="#5F9EA0",activebackground="#9fc4c6")
n11.grid(row=2,column=2)

n12=Button(frame,text="-",bd=5,relief=RAISED,height=2,width=5,command=lambda:button_click("-"),font=("Arial",14,"bold"),bg="#CD5C5C",activebackground="#e7b1b1")
n12.grid(row=2,column=3)


n13=Button(frame,text="1",bd=5,relief=RAISED,height=2,width=5,command=lambda:button_click(1),font=("Arial",14,"bold"),bg="#5F9EA0",activebackground="#9fc4c6")
n13.grid(row=3,column=0)

n14=Button(frame,text="2",bd=5,relief=RAISED,height=2,width=5,command=lambda:button_click(2),font=("Arial",14,"bold"),bg="#5F9EA0",activebackground="#9fc4c6")
n14.grid(row=3,column=1)

n15=Button(frame,text="3",bd=5,relief=RAISED,height=2,width=5,command=lambda:button_click(3),font=("Arial",14,"bold"),bg="#5F9EA0",activebackground="#9fc4c6")
n15.grid(row=3,column=2)

n16=Button(frame,text="/",bd=5,relief=RAISED,height=2,width=5,command=lambda:button_click("/"),font=("Arial",14,"bold"),bg="#CD5C5C",activebackground="#e7b1b1")
n16.grid(row=3,column=3)

n17=Button(frame,text="Clear",bd=5,relief=RAISED,height=2,width=24,command=clear,font=("Arial",14,"bold"),bg="#CD5C5C",activebackground="#e7b1b1")
n17.grid(row=4,columnspan=4)







win.mainloop()
