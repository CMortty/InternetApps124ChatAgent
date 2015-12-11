myname = ""
def getName():
    global myname
    myname = raw_input('What is your name? ')
    return myname
    
def printMsg(msg):
    print(msg)
