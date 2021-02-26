#Emmanuel Alvarez
#Dr. Fruedenthal
#! /usr/bin/env python3
#This program mimics a shell

import os,sys,re
from myReadLine import myReadLine
from redirect import *

def pipe(args):
 leftCommand = args[:args.index('|')]                      #take left command from args
 rightCommand = args[args.index('|')+1:]                   #take right command from args

 pr,pw = os.pipe()                                         #fd for reading and fd for writing
     
 rc = os.fork()                                            #child 
 if rc < 0:
     os.write(2, ("fork failed, returning %d\n" %rc).encode())
     sys.exit(1)
 elif rc == 0:
     os.close(1)                                            #close fd 1 (display)
     os.dup(pw)                                             #dup fd for writing
     os.set_inheritable(1,True)
     
     for f in (pr,pw):                                      #close fd
         os.close(f)
         
     for dir in re.split(":", os.environ['PATH']):
         program = "%s/%s" % (dir, leftCommand[0])        
         try:
             os.execve(program, leftCommand, os.environ)
         except FileNotFoundError:
             pass
     os.write(2, ("Child:    Could not exec %s\n" % leftCommand).encode())
     sys.exit(1)     
 else:
     os.close(0)                                            #close fd 0 (keyboard)
     os.dup(pr)                                             #dup fd for reading
     os.set_inheritable(0,True)
     
     for f in (pw,pr):
         os.close(f)
         
     for dir in re.split(":", os.environ['PATH']):
         program = "%s/%s" % (dir, rightCommand[0])
         try:
             os.execve(program, rightCommand, os.environ)
         except FileNotFoundError:
             pass

     os.write(2, ("Child:    Could not exec %s\n" % rightCommand).encode())
     sys.exit(1)



while (1):
    if 'PS1' in os.environ:                           #checks if there is a pre-defined prompt str   
        os.write(1,(os.environ['PS1']).encode())
    else:                                             #if not print $ as prompt string
        os.write(1 , "$ ".encode())
        
    userInput = myReadLine()                          #waits for input
    args = userInput.split()                          #splits to know arguments with parameters
    
    if userInput == "":
        os.write(2,"No input introduced\n".encode())
    
    elif userInput == "exit":                           #exits shell
        sys.exit(1)

    elif args[0] == "cd":                             #if input begins with cd
        if len(args) == 2:                            
            try:
                os.chdir(args[1])                     #change dir to second arg
            except:
                os.write(2,"Invalid commmand\n".encode()) #if dir is not valid
        elif len(args) == 1:
            os.chdir(os.environ['HOME'])              #if input is just cd
        else:
            os.write(2,"Invalid command".encode())    #if begins with cd and it has more than 3args

    else:            
        rc = os.fork()
        
        background = True
        if "&" in args:
            args.remove("&")
            background = False
            
        if rc < 0:                                        #fails to make the fork call
            os.write(2, ("fork failed, returning %d\n" %rc).encode())
            sys.exit(1)
            
        elif rc == 0:                                     #child
            if '>' in args:
                redirectOutput(args)
            elif '<' in args:
                redirectInput(args)
            elif '|' in args:
                pipe(args)

            for dir in re.split(":", os.environ['PATH']): # try each directory in the path
                program = "%s/%s" % (dir, args[0])        #concats the directory with the command introduced by the user
                try:
                    os.execve(program, args, os.environ)  #Try to execute command
                                                          #program = dir + command
                                                          #args = user input
                                                          #os.environ = child inherance os.environ
                except FileNotFoundError:
                    pass

            os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())
            sys.exit(1)                                    # terminate with error
        else:
            os.wait()
        
