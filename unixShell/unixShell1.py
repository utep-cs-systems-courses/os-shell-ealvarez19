#! /usr/bin/env python3

import os,sys,re

def startShell():
    os.environ['PS1'] = '$$'                            #promt variable specified by variable ps1
    print(os.environ['PS1'],end='')                     #prints promt string          
    userInput = input()                                 #waits for user input
    args = userInput.split(" ")
    if userInput == "exit":                             #exit if user enters exit
        sys.exit(1)
    rc = os.fork()
    if rc < 0:                                          #fails to make the fork call
        os.write(2, ("fork failed, returning %d\n" %rc).encode())
        sys.exit(1)
    elif rc == 0:                                          #child
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
         os.write(1, ("Parent: Child %d terminated with exit code %d\n" %
         childPidCode).encode())
         startShell()
startShell()