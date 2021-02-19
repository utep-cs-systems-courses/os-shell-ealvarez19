#Emmanuel Alvarez
#Dr. Fruedenthal
#! /usr/bin/env python3

import os,sys,re
from myReadLine import myReadLine

while (1):
    if 'PS1' in os.environ:                           #checks if there is a prompt    
        os.write(1,(os.environ['PS1']).encode())
    else:                                             #if not print $ as prompt variable
        os.write(1 , "$ ".encode())
        
    userInput = myReadLine()                          #waits for input
    args = userInput.split()                          #splits to know arguments with parameters
    
    if userInput == "exit":                           #exits shell
        sys.exit(1)
    rc = os.fork()
    if rc < 0:                                        #fails to make the fork call
        os.write(2, ("fork failed, returning %d\n" %rc).encode())
        sys.exit(1)
    elif rc == 0:                                     #child
        for dir in re.split(":", os.environ['PATH']): # try each directory in the path
            program = "%s/%s" % (dir, args[0])        #concats the directory with the command intro                                                       duced by the user
            try:
                os.execve(program, args, os.environ)  #Tries to execute command
                                                      #program = dir + command
                                                      #args = user input
                                                      #os.environ = child inherance os.environ
            except FileNotFoundError:
                pass

        os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())
        sys.exit(1)                                    # terminate with error
    else:
        childPidCode = os.wait()
        
