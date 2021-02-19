#Emmanuel Alvarez
#This program handles the next line of an input from the keyboard or another file

from os import read
limit = 0
next = 0

def myGetChar():                          #reads input char by char
    global limit
    global next
    if next == limit:
        next = 0
        limit = read(0,1000)              #fills buffer

        if limit == 0:                    #if there is nothing in input then EOF
            return "EOF"

    if next < len(limit) - 1:             #Avoids out of bounds
        character = chr(limit[next])
        next +=1
        return character       
    else:
        return "EOF"
       
def myReadLine():
    global limit
    global next
    line = ""
    c = myGetChar()                       #c takes each character from input
    while c!='' and c!= "EOF":
        line += c                          #adds char by char to the line
        c = myGetChar()
    next = 0
    limit = 0
    return line
