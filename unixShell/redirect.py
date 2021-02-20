import os

def getOutputIndex(args):
    return args.index('>') + 1 
def getInputIndex(args):
    return args.index('<') + 1

def redirectOutput(args):
    os.close(1)                                         #Disconnect display
    os.open(args[getOutputIndex(args)], os.O_WRONLY | os.O_CREAT) #open file for output
    os.set_inheritable(1,True)                          #make it accesable
    args.remove(args[args.index('>')+1])
    args.remove('>')

def redirectInput(args):
    os.close(0)
    os.open(args[getInputIndex(args)], os.O_RDONLY)
    os.set_inheritable(0,True)
    args.remove(args[args.index('<')+1])
    args.remove('<')


