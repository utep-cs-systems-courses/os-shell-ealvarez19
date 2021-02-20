#Emmanuel Alvarez
#This program handles the next line of an input from the keyboard or another file

from os import read
limit = 0
index = 0

def myGetChar():                          #reads input char by char
    global limit
    global index
    if index == limit:
        index = 0
        limit = read(0,1000)              #fills array from input

        if limit == 0:                    #if there is nothing in input then EOF
            return "EOF"

    if index < len(limit) - 1:             #Avoids out of bounds
        character = chr(limit[index])
        index +=1
        return character       
    else:                                   #if index is greater than len(limit)
        return "EOF"
       
def myReadLine():
    global limit
    global index
    line = ""
    character = myGetChar()                        #c takes each character from input
    while character!='' and character!= "EOF":
        line += character                          #adds char by char to the line
        character = myGetChar()                    
    index = 0
    limit = 0
    return line
