#! /usr/bin/python3

import string
alpha = string.ascii_lowercase 

def decrypt(x,y): 
    decrypted = ""
    for i in x:
        if i in alpha:
            p = alpha.find(i)
            v = (p - y) % 26
            z = alpha[v]
            decrypted += z
        else:
            decrypted += i
    print(decrypted)

def userinput():
    try:
        a = input("Enter the Encrypted Code \n>>>>").lower()
        key = 0
        while key < 27:
            decrypt(a, key)
            key += 1
    except KeyboardInterrupt:
        print("Pressed CTRL + C \nExiting...")
userinput()    