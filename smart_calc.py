from tkinter import *

#MATH
def add(a,b):
    return a + b

def sub(a,b):
    return a - b

def mul(a, b):
    try:
        return a * b
    except ZeroDivisionError:
        return "Can't divide with zero"

def div(a, b):
    return a/b

def mod(a, b):
    return a % b

def lcm(a, b):
    L = a if a>b else b
    while L <=a*b:
        if L %a == 0 and L % b == 0:
            return L
        
        L+=1

def hcf(a, b):
    H = a if a<b else b
    while H >=1:
        if a % H == 0 and b % H==0:
            return H

        H -=1

#CAlculate
def extract_from_text(text):
    l = []
    for t in text.split(' '):
        try:
            l.append(float(t))
        except ValueError:
            pass
    return l

def calculate():
    text = textin.get()
    for word in text.split(' '):
        if word.upper() in operations.keys():
            try:
                l = extract_from_text(text)
                r = operations[word.upper()](l[0],l[1])
                lst.delete(0,END)
                lst.insert(END,"The answer is {}".format(r))
            except:
                lst.delete(0,END)
                lst.insert(END,"SOMETHING WENT WRONG!\nPlease Enter Again")
            finally:
                break

        elif word.upper() not in operations.keys():
            lst.delete(0,END)
            lst.insert(END,"OOPS!Seems like a new function that I didn't learned yet")


#OPERATIONS
operations = {"ADD":add, "ADDITION":add,"SUM":add,"PLUS": add, "SUB":sub,"DIFFERENCE": sub, "MINUS":sub,"SUBTRACT":sub,"LCM":lcm,"HCF":hcf,"PRODUCT":mul,"MULTIPLY":mul,"MUL":mul,"INTO":mul,"MULTIPLICATION":mul,"DIVISION":div,"DIVIDE":div,"DIV":div,"MOD":mod,"REMAINDER":mod,"MODULUS":mod}




#FRONTEND
win = Tk()
win.geometry('500x300')
win.title("MLBACKBENCHERS")
win.configure(bg = "yellow")

l1 = Label(win, text="Mlbackbencher Smart Calc.", width =25,padx = 3)
l1.place(x=150, y = 10)

l2 = Label(win, text="I am MLbot", width =20,padx = 3)
l2.place(x=170, y = 40)

l3 = Label(win, text="How can I help you?", width =25,padx = 3)
l3.place(x=150, y = 100)

textin = StringVar()
e1 = Entry(win, width= 30, textvariable = textin)
e1.place(x= 130,y=130)

b1 = Button(win, text="Just This", command = calculate)
b1.place(x=210, y = 160)

lst = Listbox(win, width = 30,height = 3)
lst.place(x = 130, y= 200)

win.mainloop()
